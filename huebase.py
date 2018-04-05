import requests
import json
import yaml
import time

"""
    hue.config -- Configuration --

    For configuration use a file called hue.config
    This is a yaml file

    Content:
---
bridgeurl: xxx.xxx.xxx.xxx
userid: abc123
...
"""

class HueBridge:

    baseUrl = None

    def __init__(self):
        with open("hue.config", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        url = cfg['bridgeurl']
        userId = cfg['userid']
        self.baseUrl = 'http://' + url + '/api/' + userId + '/'

    def Get(self, cmd):
        resp = requests.get(self.baseUrl + cmd)
        return resp.json()

    def Put(self, cmd, body):
        resp = requests.put(self.baseUrl + cmd, data=json.dumps(body))
        return resp

class Light:

    # Fixed properties
    id = None
    props = None
    state = None

    prevState = None

    # helper
    bridge = None
    
    def __init__(self, bridge, id):
        self.bridge = bridge
        self.id = id

        self.GetAllAttributes()

    def GetAllAttributes(self):
        if self.bridge is not None and self.id is not None:
            self.props = self.bridge.Get('lights/' + self.id)
            self.state = self.props['state']
            self.prevState = self.state
        
    def GetState(self):
        if self.bridge is not None:
            self.state = self.bridge.Get('lights/' + self.id)['state']
            self.prevState = self.state

        return self.state

    def SetHue(self, hue, sat):
        body = {}
        if hue is not None and hue >= 0 and hue <= 65535:
            body['hue'] = hue
        if sat is not None and sat >= 0 and sat < 255:
            body['sat'] = sat

        if len(body) > 0 and self.bridge is not None:
            self.bridge.Put('lights/{0}/state'.format(self.id), body)
            self.GetState()

    def SetStateProp(self, prop, value):
        body = {}
        if self.bridge is not None:
            body[prop] = value
            self.bridge.Put('lights/{0}/state'.format(self.id), body)
            self.GetState()
            
    def SetAttribute(self, name, value):
        body = {}
        if self.bridge is not None:
            body[name] = value
            self.bridge.Put('lights/{0}'.format(self.id), body)
            self.GetState()
            

# Start of main
