from huebase import HueBridge
from huebase import Light

bridge = HueBridge()
light = Light(bridge, '3')
print ("The light {0} is ".format(light.props['name']) + ('On' if light.state['on'] else 'Off'))
print ("The light {0} has hue {1} sat {2} and bri {3}".format(light.id, light.state['hue'], light.state['sat'], light.state['bri']))

""" for iCnt in range(0, 60000, 1000):
    light.SetHue(iCnt, None)
    lastState = light.GetState()
    print ("The light " + light.name + " has hue {:d}".format(light.state['hue']))
    time.sleep(2)
 """

light.SetStateProp('bri', 15)
light.SetStateProp('hue', 300)
print ("The light {0} has hue {1} sat {2} and bri {3}".format(light.id, light.state['hue'], light.state['sat'], light.state['bri']))
