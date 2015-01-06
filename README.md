# polyv-python-sdk

## Demo Code

```python
from polyvSDK import *

polyvSDK = PolyvSDK(readtoken=READTOKEN, writetoken=WRITETOKEN, privatekey=PRIVATEKEY, sign=True)

#upload a local video file
polyvSDK.uploadfile('title1', 'desc1', 'tag1', '1', '/path/demo.mp4')
```

```
#get video info by vid
result = polyvSDK.getById('5e9e0e9c30f551262f6b52c53548d310_5')
print result['swf_link']
```

```
#load newest video list
result = polyvSDK.getNewList(1, 10, '') 
for video in result:
    print video['swf_link']
```
