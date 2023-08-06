import logging
import sys

BASEURL = "https://pv.inteless.com"

API_TIMEOUT = 10

LOG_LEVEL = logging.INFO

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(LOG_LEVEL)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
handler.setFormatter(formatter)
_LOGGER.addHandler(handler)

DEGREE_CELSIUS = "°C"
WATT = "W"
KWATT = "kW"
WATT_HOUR = "Wh"
KWATT_HOUR = "kWh"
AMPERE = "A"
AMPEREHOUR = "Ah"
VOLT = "V"
PERCENT = "%"
HERTZ = "Hz"
PER_KILOWATTHOUR = "{}/kWh"

APIHEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
    "Origin" : "https://sunsynk.net",
    "Referrer" : "https://sunsynk.net"
}

SS_PLANT_LIST_API = "api/v1/plants?page=1&limit=10&name=&status="
SS_INVERTER_LIST_API = "api/v1/inverters?page=1&limit=10&total=0&status=-1&sn=&plantId=&type=-2&softVer=&hmiVer=&agentCompanyId=-1&gsn="