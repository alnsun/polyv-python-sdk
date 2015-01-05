#!/usr/bin/env python
# -*- coding: utf-8 -*-
import StringIO
from hashlib import sha1

import pycurl
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

class PolyvSDK(object):

    def __init__(self, **kwargs):
        if kwargs.has_key('readtoken'):
            self._readtoken = kwargs['readtoken']
        if kwargs.has_key('writetoken'):
            self._writetoken = kwargs['writetoken']
        if kwargs.has_key('privatekey'):
            self._privatekey = kwargs['privatekey']
        if kwargs.has_key('sign'):
            self._sign = bool(kwargs['sign'])

    def uploadfile(self, title, desc, tag, cataid, filename):
        JSONRPC = '{"title":"%(title)s","tag":"%(tag)s","desc":"%(desc)s"}' % {'title':title, 'tag':tag, 'desc':desc}

        if (self._sign):
            hash = sha1(
                'cataid=%(cataid)s&JSONRPC=%(JSONRPC)s&writetoken=%(writetoken)s' % {
                    'cataid':cataid, 'JSONRPC':JSONRPC, 'writetoken': self._writetoken + self._privatekey
                }
            ).hexdigest()

        ch = pycurl.Curl()
        timeout = 360
        ch.setopt(pycurl.CONNECTTIMEOUT, timeout)
        ch.setopt(pycurl.URL, 'http://v.polyv.net/uc/services/rest?method=uploadfile')
        post_data = [
            ("JSONRPC", JSONRPC),
            ('cataid', cataid),
            ('writetoken', self._writetoken),
            ('sign', hash),
            ('format', 'json'),
            ('Filedata', (pycurl.FORM_FILE, filename))
        ]
        ch.setopt(pycurl.HTTPPOST, post_data)
        b = StringIO.StringIO()
        ch.setopt(pycurl.WRITEFUNCTION, b.write)

        try:
            ch.perform()
            print 'data=%s' % b.getvalue()
        except Exception, e:
            print 'Connection error: %s' % str(e)
            ch.close()
