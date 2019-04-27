## qencode-api-python3-client

####Installation

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

##Usage

````
import qencode

client = qencode.client(API_KEY)
client.create()

task = client.create_task()
task.start(TRANSCODING_PROFILEID, VIDO_URL)

````

####Documentation

Documentation is available at <https://docs.qencode.com>