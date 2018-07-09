from prometheus_client import start_http_server, Gauge
from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_humidity import *
from time import sleep
from signal import pause

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error :" + errmsg.value)

s = YSensor.FirstSensor()
while s is not None:
    (Gauge(s.get_functionId(), 'Current reading', ['unit', 'hardwareId'])
        .labels(s.get_unit(), s.get_hardwareId())
        .set_function(s.get_currentValue))
    s = s.nextSensor()

#t = YTemperature.FirstTemperature()
#while t is not None:
#    (Gauge('temperature', 'Current temperature', ['unit', 'hardwareId'])
#        .labels(t.get_unit(), t.get_hardwareId())
#        .set_function(t.get_currentValue))
#    t = t.nextTemperature()

#h = YHumidity.FirstHumidity()
#while h is not None:
#    (Gauge('humidity', 'Current humidity', ['unit', 'hardwareId'])
#        .labels(t.get_unit(), h.get_hardwareId())
#        .set_function(t.get_currentValue))
#    h = h.nextTemperature()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    pause()
