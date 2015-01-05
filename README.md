# polyv-python-sdk

## Demo Code

``
from polyvSDK import *

p = PolyvSDK(readtoken=READTOKEN, writetoken=WRITETOKEN, privatekey=PRIVATEKEY, sign=True)
p.uploadfile('title1', 'desc1', 'tag1', '1', '/path/demo.mp4')
``
