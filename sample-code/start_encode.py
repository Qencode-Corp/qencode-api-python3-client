#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import qencode3
import time
import json
from qencode3 import QencodeClientException, QencodeTaskException

# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'

# replace with your Transcoding Profile ID (can be found in your Project settings on Qencode portal)
TRANSCODING_PROFILEID = 'your-qencode-profile-id'

# replace with a link to your input video
VIDEO_URL = 'https://qencode.com/static/1.mp4'
# or stitch
# STITCH = ['https://qencode.com/static/1.mp4', 'https://qencode.com/static/2.mp4']


def start_encode():
    """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: task object
  """

    client = qencode3.client(API_KEY)
    if client.error:
        raise QencodeClientException(client.message)

    print('The client created. Expire date: {0}'.format(client.expire))

    task = client.create_task()
    task.start_time = 0.0
    task.duration = 10.0

    if task.error:
        raise QencodeTaskException(task.message)

    task.start(TRANSCODING_PROFILEID, VIDEO_URL)
    # or stitch
    # task.start(TRANSCODING_PROFILEID, STITCH)

    if task.error:
        raise QencodeTaskException(task.message)

    print('Start encode. Task: {0}'.format(task.task_token))

    line = "-" * 80
    while True:
        print(line)
        status = task.status()
        # print status
        print(json.dumps(status, indent=2, sort_keys=True))
        if status['error'] or status['status'] == 'completed':
            break
        time.sleep(5)


if __name__ == '__main__':
    start_encode()
