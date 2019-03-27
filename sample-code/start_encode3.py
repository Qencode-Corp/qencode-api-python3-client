#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import json



API_KEY = '5a5db6fa5b4c5'
TRANSCODING_PROFILEID = '5a5db6fa5b8ac'
VIDO_URL = 'https://qa.qencode.com/static/1.mp4'


def my_callback(e):
  try:
    print_status(e)
  except BaseException as e:
    print(str(e), end="\n")


def my_callback2(e):
  try:
    print_status(e)
  except BaseException as e:
    print(str(e), end="\n")

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

def start_encode():
  """
    Create encoder object
    :param api_key: string
    :param api_url: string. not required
    :return: encode object
  """
  client = qencode.client(API_KEY, api_url='https://api-qa.qencode.com/')
  if client.error:
   print('Error', client.message, sep=":", end="\n")
   raise SystemExit

  """
    Create task
    :param access_token: string. access_token from encoder object
    :param connect: string. connect object from encoder object
    :return: task object
  """
  task = client.create_task()
  task.start(TRANSCODING_PROFILEID, VIDO_URL)
  if task.error:
    print('Error', task.message, sep=":", end="\n")
    raise SystemExit

  task.progress_changed(my_callback)
  task.task_completed(my_callback2)




if __name__ == '__main__':
   start_encode()