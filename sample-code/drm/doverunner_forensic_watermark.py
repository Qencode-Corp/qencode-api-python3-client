#!/usr/bin/env python3
"""
DoveRunner forensic watermarking with Qencode.

Launches a Qencode transcoding job that produces two A/B watermarked
HLS variants using DoveRunner forensic watermarking.

Prerequisites:
  pip install qencode3

Usage:
  python doverunner_forensic_watermark.py \
    --qencode-api-key YOUR_QENCODE_API_KEY \
    --wm-key YOUR_DOVERUNNER_WM_KEY \
    --access-key YOUR_DOVERUNNER_ACCESS_KEY \
    --source https://nyc3.s3.qencode.com/qencode/bbb_30s.mp4
"""

import argparse
import json
import sys
import time

import qencode3
from qencode3 import QencodeClientException, QencodeTaskException


def build_query(source, wm_key, access_key):
    """Build the Qencode custom query JSON with forensic watermarking."""

    query = {
        "query": {
            "source": source,
            "encoder_version": 2,
            "format": [
                {
                    "output": "advanced_hls",
                    "forensic_watermark": {
                        "doverunner_wm_key": wm_key,
                        "doverunner_access_key": access_key,
                    },
                    "stream": [
                        {
                            "size": "1920x1080",
                            "bitrate": "5000",
                        },
                        {
                            "size": "1280x720",
                            "bitrate": "2500",
                        },
                    ],
                }
            ],
        }
    }
    return json.dumps(query)


def run_encode(api_key, query_json, api_url=None):
    """Create a Qencode task, start encoding, and poll until complete."""

    client = qencode3.client(api_key, api_url=api_url)
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
        percent = status.get("percent", 0)
        task_status = status.get("status", "unknown")
        print(f"  [{task_status}] {percent}%")
        if status.get("error") or task_status == "completed":
            print(json.dumps(status, indent=2, sort_keys=True))
            break
        time.sleep(5)

    return status


def main():
    parser = argparse.ArgumentParser(
        description="DoveRunner forensic watermarking with Qencode"
    )
    parser.add_argument("--qencode-api-key", required=True, help="Qencode project API key")
    parser.add_argument("--wm-key", required=True, help="DoveRunner watermark key (base64)")
    parser.add_argument("--access-key", required=True, help="DoveRunner access key")
    parser.add_argument("--source", required=True, help="URL of the source video")
    parser.add_argument("--api-url", default=None, help="Qencode API URL override")
    args = parser.parse_args()

    print("=" * 60)
    print("Building Qencode job with forensic watermarking...")
    print(f"  Source: {args.source}")

    query_json = build_query(
        source=args.source,
        wm_key=args.wm_key,
        access_key=args.access_key,
    )

    # Print query with credentials masked
    query_display = json.loads(query_json)
    fmt = query_display["query"]["format"][0]
    fmt["forensic_watermark"]["doverunner_wm_key"] = "***"
    fmt["forensic_watermark"]["doverunner_access_key"] = "***"
    print("\nQuery JSON:")
    print(json.dumps(query_display, indent=2))

    print("\n" + "=" * 60)
    print("Starting encoding...\n")

    status = run_encode(args.qencode_api_key, query_json, api_url=args.api_url)

    if status.get("error"):
        print(f"\nEncoding failed: {status.get('error_description', 'unknown error')}")
        sys.exit(1)
    else:
        print("\nEncoding completed successfully.")
        # Show wm_symbol from each video output's meta
        print("\nOutputs:")
        for video in status.get("videos", []):
            meta = video.get("meta", {})
            wm_symbol = meta.get("wm_symbol", "N/A")
            url = video.get("url", "N/A")
            tag = video.get("tag", "")
            print(f"  [{tag}] wm_symbol={wm_symbol}  url={url}")


if __name__ == "__main__":
    main()
