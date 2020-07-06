## Installation

**install sdk libraries from github**

```sh
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python3-client
cd qencode-api-python3-client
pip install -r requirements.txt
python setup.py install
```

**Usage**

```python
import qencode3

client = qencode3.client(API_KEY)
client.create()

task = client.create_task()
task.start(TRANSCODING_PROFILEID, VIDEO_URL)

```

**Documentation**

Documentation is available at <https://docs.qencode.com>
