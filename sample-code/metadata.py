#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
#import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode3
from qencode3 import QencodeClientException

#replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = ''
VIDEO_URL = 'https://nyc3.s3.qencode.com/qencode/bbb_30s.mp4'

client = qencode3.client(API_KEY)
if client.error:
    raise QencodeClientException(client.message)

print('The client created. Expire date: {0}'.format(client.expire))

metadata = client.get_metadata(VIDEO_URL)

try:
  metadata = metadata.decode("utf-8")
except Exception as e:
    pass

print(metadata)



