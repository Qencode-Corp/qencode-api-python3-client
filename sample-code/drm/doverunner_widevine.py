#!/usr/bin/env python3
"""
End-to-end DoveRunner Widevine DRM encoding with Qencode.

Steps:
  1. Request CPIX encryption keys from DoveRunner KMS (Widevine)
  2. Launch a Qencode transcoding job with cenc_drm encryption
  3. Poll until the job completes

Prerequisites:
  pip install qencode3

Usage:
  python doverunner_qencode_widevine.py \
    --qencode-api-key YOUR_QENCODE_API_KEY \
    --kms-token YOUR_DOVERUNNER_KMS_TOKEN \
    --content-id my-content-01 \
    --source https://nyc3.s3.qencode.com/qencode/bbb_30s.mp4
"""

import argparse
import base64
import json
import sys
import time
import uuid
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error

import qencode3
from qencode3 import QencodeClientException, QencodeTaskException


# ---------------------------------------------------------------------------
# DoveRunner CPIX
# ---------------------------------------------------------------------------

WIDEVINE_SYSTEM_ID = "edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"
DOVERUNNER_KMS_URL = "https://drm-kms.doverunner.com/v2/cpix/doverunner/getKey/{token}"
DOVERUNNER_LICENSE_URL = "https://drm-license.doverunner.com/ri/licenseManager.do"

CPIX_REQUEST_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<cpix:CPIX id="{content_id}"
    xmlns:cpix="urn:dashif:org:cpix"
    xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc"
    xmlns:speke="urn:aws:amazon:com:speke">
  <cpix:ContentKeyList>
    <cpix:ContentKey kid="{kid}"></cpix:ContentKey>
  </cpix:ContentKeyList>
  <cpix:DRMSystemList>
    <cpix:DRMSystem kid="{kid}" systemId="{widevine_system_id}" />
  </cpix:DRMSystemList>
</cpix:CPIX>"""


def request_cpix_keys(kms_token, content_id, kid):
    """Send CPIX request to DoveRunner KMS and parse the response."""

    url = DOVERUNNER_KMS_URL.format(token=kms_token)
    body = CPIX_REQUEST_TEMPLATE.format(
        content_id=content_id,
        kid=kid,
        widevine_system_id=WIDEVINE_SYSTEM_ID,
    )

    req = urllib.request.Request(
        url,
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        response_xml = resp.read().decode("utf-8")

    ns = {
        "cpix": "urn:dashif:org:cpix",
        "pskc": "urn:ietf:params:xml:ns:keyprov:pskc",
    }
    root = ET.fromstring(response_xml)

    content_key = root.find(".//cpix:ContentKey", ns)
    key_id_hex = content_key.attrib["kid"].replace("-", "")

    plain_value = root.find(".//pskc:PlainValue", ns).text
    key_hex = base64.b64decode(plain_value).hex()

    iv_hex = None
    explicit_iv = content_key.attrib.get("explicitIV")
    if explicit_iv:
        iv_hex = base64.b64decode(explicit_iv).hex()

    pssh_b64 = None
    for drm_system in root.findall(".//cpix:DRMSystem", ns):
        if drm_system.attrib.get("systemId") == WIDEVINE_SYSTEM_ID:
            pssh_el = drm_system.find("cpix:PSSH", ns)
            if pssh_el is not None:
                pssh_b64 = pssh_el.text.strip()
            break

    return {
        "key_id": key_id_hex,
        "key": key_hex,
        "iv": iv_hex,
        "pssh": pssh_b64,
    }


# ---------------------------------------------------------------------------
# Qencode job
# ---------------------------------------------------------------------------

def build_query(source, cenc_drm):
    """Build the Qencode custom query JSON."""

    query = {
        "query": {
            "source": source,
            "format": [
                {
                    "output": "advanced_dash",
                    "stream": [
                        {
                            "video_codec": "libx264",
                            "audio_codec": "aac",
                            "width": 1280,
                            "height": 720,
                            "bitrate": 3000,
                            "audio_bitrate": 128,
                        }
                    ],
                    "cenc_drm": cenc_drm,
                }
            ],
        }
    }
    return json.dumps(query)


def run_encode(api_key, query_json):
    """Create a Qencode task, start encoding, and poll until complete."""

    client = qencode3.client(api_key)
    if client.error:
        raise QencodeClientException(client.message)
    print(f"Qencode client created. Expires: {client.expire}")

    task = client.create_task()
    if task.error:
        raise QencodeTaskException(task.message)

    task.custom_start(query_json)
    if task.error:
        raise QencodeTaskException(task.message)

    print(f"Encoding started. Task token: {task.task_token}")

    while True:
        status = task.status()
        print(json.dumps(status, indent=2, sort_keys=True))
        if status.get("error") or status.get("status") == "completed":
            break
        time.sleep(5)

    return status


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="DoveRunner Widevine DRM encoding with Qencode"
    )
    parser.add_argument("--qencode-api-key", required=True, help="Qencode project API key")
    parser.add_argument("--kms-token", required=True, help="DoveRunner KMS encryption token")
    parser.add_argument("--content-id", required=True, help="Content identifier for DoveRunner")
    parser.add_argument("--kid", default=None, help="Key ID in UUID format (auto-generated if omitted)")
    parser.add_argument("--source", required=True, help="URL of the source video")
    args = parser.parse_args()

    kid = args.kid or str(uuid.uuid4())

    # Step 1: Get CPIX keys from DoveRunner
    print("=" * 60)
    print("Step 1: Requesting CPIX keys from DoveRunner KMS...")
    print(f"  Content ID: {args.content_id}")
    print(f"  KID (UUID): {kid}")

    try:
        keys = request_cpix_keys(args.kms_token, args.content_id, kid)
    except urllib.error.HTTPError as e:
        print(f"CPIX request failed: HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        sys.exit(1)

    cenc_drm = {
        "key_id": keys["key_id"],
        "key": keys["key"],
        "pssh": keys["pssh"],
        "la_url": DOVERUNNER_LICENSE_URL,
    }
    if keys["iv"]:
        cenc_drm["iv"] = keys["iv"]

    print("\ncenc_drm values:")
    print(json.dumps(cenc_drm, indent=2))

    # Step 2: Launch Qencode job
    print("\n" + "=" * 60)
    print("Step 2: Starting Qencode encoding job...")

    query_json = build_query(
        source=args.source,
        cenc_drm=cenc_drm,
    )

    print("\nQuery JSON:")
    print(json.dumps(json.loads(query_json), indent=2))

    print("\n" + "=" * 60)
    print("Step 3: Polling task status...\n")

    status = run_encode(args.qencode_api_key, query_json)

    if status.get("error"):
        print(f"\nEncoding failed: {status.get('error_description', 'unknown error')}")
        sys.exit(1)
    else:
        print("\nEncoding completed successfully.")


if __name__ == "__main__":
    main()
