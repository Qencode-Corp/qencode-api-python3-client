
def client(api_key, api_url=None, version=None, **kwargs):
    from . client import Client
    return Client(api_key, api_url=api_url, version=version, **kwargs)

def custom_params():
  from . custom_params import CustomTranscodingParams
  return CustomTranscodingParams()

def format():
  from . custom_params import Format
  return Format()

def destination():
  from . custom_params import Destination
  return Destination()

def stream():
  from . custom_params import Stream
  return Stream()

def x264_video_codec():
  from . custom_params import Libx264_VideoCodecParameters
  return Libx264_VideoCodecParameters()

def x265_video_codec():
  from . custom_params import Libx265_VideoCodecParameters
  return Libx265_VideoCodecParameters()

from . exeptions import QencodeClientException, QencodeTaskException

from . tools import generate_aws_signed_url, fps_drm, cenc_drm



__version__ = "1.0.1"
__status__ = "Production/Stable"
__author__ = "Qencode"



