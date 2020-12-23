## qencode-api-python3-client


**install sdk libraries from github**

````
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python3-client
cd qencode-api-python3-client
pip install -r requirements.txt
python setup.py install
````
**install from pip**

````
sudo pip install qencode3
````

**Usage**

````
import qencode3

API_KEY = 'your-api-qencode-key'

QUERY = """
{"query": {
  "source": "https://nyc3.s3.qencode.com/qencode/samples/1080-sample.mov",
  "format": [
    {
      "output": "mp4",
      "size": "320x240",
      "video_codec": "libx264"
    }
  ]
  }
}
"""

client = qencode3.client(API_KEY)
client.create()

task = client.create_task()
task.custom_start(QUERY)
````

````
#getting status

status = task.status()
or
status = task.extend_status()
````

````
#getting video metadata

metadata = client.get_metadata(VIDEO_URL)
````

**DRM** <sub><sup>*[details](https://docs.qencode.com/api-reference/transcoding/#start_encode2___query__attributes--format__attributes--fps_drm__attributes)*</sup></sub>


````
from qencode3 import fps_drm, cenc_drm

# getting Fairplay DRM encryption parameters
encryption_parameters, payload = cenc_drm(DRM_USERNAME, DRW_PASSWORD)

# getting Widevine and Playready DRM encryption parameters
encryption_parameters, payload = fps_drm(DRM_USERNAME, DRW_PASSWORD)

````


**AWS Signed URL**

````
source_url = generate_aws_signed_url(region, bucket, object_key, access_key, secret_key, expiration)

````

**Documentation**

Documentation is available at <https://docs.qencode.com>

**Documentation**

Documentation is available at <https://docs.qencode.com>

**Description**

Here you will find examples of Qencode solutions using the latest version of python. Some popular examples include launching [video encoding](https://cloud.qencode.com/) jobs through the API, basic testing functionality, and code developed to exhibit a wide range of features that we offer. Please send over any ideas you have to help us improve our solution and continue to provide you with the easiest transcoding solutions on the market.

Key features of encoding your videos:

Output Formats
 * HLS 
 * MPEG-DASH 
 * MP4 
 * MXF 
 * WebM

Codecs
 * H.264 (AVC1) 
 * H.265 (HEVC) 
 * VP9 
 * VP8 
 * AV1 
 * MPEG-2

Input Formats
 * MP4 
 * AVI 
 * MOV 
 * MKV 
 * HLS 
 * MPEG‑2 (TS & PS) 
 * MXF 
 * ASF 
 * ProRes 
 * XDCAM 
 * DNx 
 * FLV 
 * ...and many more
 
  ## Copyright
  Copyright 2021 Qencode, Inc.