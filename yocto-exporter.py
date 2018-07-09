from prometheus_client import start_http_server, Gauge
from yoctopuce.yocto_api import *
from time import sleep
from signal import pause

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error :" + errmsg.value)

s = YSensor.FirstSensor()
while s is not None:
    (Gauge(s.get_functionId(), 'Current {} reading'.format(s.get_functionId()), ['unit', 'hardwareId'])
        .labels(s.get_unit(), s.get_hardwareId())
        .set_function(s.get_currentValue))
    s = s.nextSensor()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    pause()
