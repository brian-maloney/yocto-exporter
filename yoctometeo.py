from prometheus_client import start_http_server, Gauge
from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_humidity import *
from time import sleep
from signal import pause

UNIT = 'F'

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error :" + errmsg.value)

t = YTemperature.FirstTemperature()
if t is None : sys.exit("No temperature sensor found");

h = YHumidity.FirstHumidity()
if h is None : sys.exit ("No humidity sensor found");

if t.get_unit() != UNIT:
    t.set_unit(UNIT)
    sleep(1)

temp_gauge = Gauge('temperature', 'Temperature in {}'.format(UNIT))
temp_gauge.set_function(t.get_currentValue)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    pause()
