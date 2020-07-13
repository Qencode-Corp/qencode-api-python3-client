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
import qencode

client = qencode.client(API_KEY)
client.create()

task = client.create_task()
task.start(TRANSCODING_PROFILEID, VIDO_URL)

#getting video metadata:
metadata = client.get_metadata(VIDEO_URL)

````

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