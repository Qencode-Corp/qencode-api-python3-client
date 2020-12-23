## Installation

**install sdk libraries from github**

````
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
pip install -r requirements.txt
python setup.py install
````

**Usage**

````
import qencode

params = """
{"query": {
  "source": "https://qencode.com/static/1.mp4",
  "format": [
    {
      "output": "mp4",
      "size": "320x240",
      "video_codec": "libx264"
    }
  ]
  }
}

client = qencode.client(API_KEY)
client.create()

task = client.create_task()
task.custom_start(params)


````


**Documentation**

Documentation is available at <https://docs.qencode.com>