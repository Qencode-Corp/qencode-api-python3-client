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

params = qencode.custom_params()

FORMAT = qencode.format()
STREAM = qencode.stream()
DESTINATION = qencode.destination()
VIDEO_CODEC = qencode.x264_video_codec()

# set your S3 access credentials here
# for more storage types see Destination object description: https://docs.qencode.com/#010_050
DESTINATION.url = "s3://s3.eu-east-1.amazonaws.com/qencode-test"
DESTINATION.key = "AKIAIKASDJ7SD12345"
DESTINATION.secret = "h2TGNXeQA9OT+DtZ3RGr+94HEhptS6oYsm12345"

VIDEO_CODEC.vprofile = "baseline"
VIDEO_CODEC.level = 31
VIDEO_CODEC.coder = 0
VIDEO_CODEC.flags2 = "-bpyramid+fastpskip-dct8x8"
VIDEO_CODEC.partitions = "+parti8x8+parti4x4+partp8x8+partb8x8"
VIDEO_CODEC.directpred = 2

# stream object is specified for HLS or DASH outputs only.
# for MP4 or WEBM output set properties below in format object directly
STREAM.profile = "baseline"
STREAM.size = "1920x1080"
STREAM.audio_bitrate = 128
STREAM.video_codec_parameters = VIDEO_CODEC

FORMAT.stream = [STREAM]
FORMAT.output = "advanced_hls"
FORMAT.destination = DESTINATION

params.source = 'https://qa.qencode.com/static/1.mp4'
params.format = [FORMAT]


def start_encode():

  """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: client object
  """

  client = qencode.client(API_KEY)
  if client.error:
    print('Error', client.message, sep=":", end="\n")
    raise SystemExit

  """
    Create task
    :return: task object
  """

  task = client.create_task()
  task.custom_start(params)
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
