#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time
import json

#replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = '5a5db6fa5b123'

#replace with your Transcoding Profile ID (can be found in your Project settings on Qencode portal)
TRANSCODING_PROFILEID = '5a5db6fa5b123'

#replace with a link to your input video
VIDEO_URL = 'https://qa.qencode.com/static/1.mp4'


def start_encode():
  """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version:  string. not required. default 'v1'
    :return: client object
  """

  client = qencode.client(API_KEY, api_url='https://api-qa.qencode.com/')
  if client.error:
   print('Error', client.message, sep=":", end="\n")
   raise SystemExit

  """
    Create task
    :return: task object
  """
  task = client.create_task()
  task.start_time = 0.0
  task.duration = 10.0
  task.start(TRANSCODING_PROFILEID, VIDEO_URL)
  if task.error:
    print('Error', task.message, sep=":", end="\n")
    raise SystemExit

  while True:
    status = task.status()
    try:
      print_status(status)
    except BaseException as e:
      print(str(e), end="\n")
    if status['error']:
      break
    if status['status'] == 'completed':
      break
    time.sleep(10)


def print_status(status):
  if not status['error'] and status['status'] != 'error':
    print("Status: {0} {1}%".format(status.get('status'), status.get('percent')), end="\n")
  elif status['error'] or status['status'] == 'error':
    print("Error: %s\n" % (status.get('error_description')), end="\n")
  if status['status'] == 'completed':
    for video in status['videos']:
      meta = json.loads(video['meta'])
      print('Resolution',  meta.get('resolution'), sep=":")
      print('Url', video.get('url'), sep=":", end="\n")



if __name__ == '__main__':
  start_encode()