#!/usr/bin/env python
# -*- coding: utf-8 -*-
import StringIO
from hashlib import sha1
from xml.etree import ElementTree

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
        except Exception, e:
            print 'Connection error: %s' % str(e)
            ch.close()

    def _processXmlResponse(self, url, xml=''):

        ch = pycurl.Curl()
        timeout = 10
        ch.setopt(ch.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.URL, url)
        ch.setopt(ch.CONNECTTIMEOUT, timeout)
        if not xml:
            ch.setopt(ch.HEADER, 0)
            ch.setopt(ch.CUSTOMREQUEST, 'POST')
            ch.setopt(ch.POST, 1)
            ch.setopt(ch.POSTFIELDS, xml)
            ch.setopt(ch.HTTPHEADER, [
                'Content-type: application/xml',
                'Content-length: %s' % len(xml)
            ])
        b = StringIO.StringIO()
        ch.setopt(pycurl.WRITEFUNCTION, b.write)

        try:
            ch.perform()
        except Exception, e:
            print 'error: %s' % str(e)
            ch.close()

        if b.getvalue():
            return ElementTree.XML(b.getvalue())
        else:
            return False

    def _processJsonResponse(self, url, json_data=''):

        ch = pycurl.Curl()
        timeout = 10
        ch.setopt(ch.SSL_VERIFYPEER, False)
        ch.setopt(pycurl.URL, url)
        ch.setopt(ch.CONNECTTIMEOUT, timeout)
        if not json_data:
            ch.setopt(ch.HEADER, 0)
            ch.setopt(ch.CUSTOMREQUEST, 'POST')
            ch.setopt(ch.POST, 1)
            ch.setopt(ch.POSTFIELDS, json_data)
            ch.setopt(ch.HTTPHEADER, [
                'Content-type: application/json',
                'Content-length: %s' % len(json_data)
            ])
        b = StringIO.StringIO()
        ch.setopt(pycurl.WRITEFUNCTION, b.write)

        try:
            ch.perform()
        except Exception, e:
            print 'error: %s' % str(e)
            ch.close()

        if b.getvalue():
            return b.getvalue()
        else:
            return False

    def getById(self, vid):

        if (self._sign):
            hash = sha1('readtoken=%(readtoken)s&vid=%(vid)s%(privatekey)s' % {
                    'readtoken': self._readtoken,
                    'vid': vid,
                    'privatekey': self._privatekey
                }
            ).hexdigest()

        url = 'http://v.polyv.net/uc/services/rest?readtoken=%(readtoken)s&method=getById&vid=%(vid)s&format=xml&sign=%(sign)s'
        url = url % {'readtoken': self._readtoken,
            'vid': vid,
            'sign': hash
        }
        xml = self._processXmlResponse(url, '')

        if xml is not None:
            if xml.find('./error').text == '0':
                return self.makeVideo(xml.find('./data').find('./video'))
            else:
                return {
                    'returncode': xml.find('./error').text
                }
        else:
            return None

    def makeVideo(self, video):
        return {
            'vid': video.find('./vid').text,
            'hlsIndex': video.find('./hlsIndex').text,
            'swf_link': video.find('./swf_link').text,
            'ptime': video.find('./ptime').text,
            'status': video.find('./status').text,
            'df': video.find('./df').text,
            'first_image': video.find('./first_image').text,
            'title': video.find('./title').text,
            'desc': video.find('./context').text,
            'duration': video.find('./duration').text,
            'flv1': video.find('./flv1').text,
            #'flv2': video.find('./flv2').text,
            #'flv3': video.find('./flv3').text,
            'mp4_1': video.find('./mp4_1').text,
            #'mp4_2': video.find('./mp4_2').text,
            #'mp4_3': video.find('./mp4_3').text,
            #'hls_1': video.find('./hls_1').text,
            #'hls_2': video.find('./hls_2').text,
            #'hls_3': video.find('./hls_3').text,
            'seed': video.find('./seed').text,
        }

