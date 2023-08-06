"""Sunsynk Logger API Interface."""

import json
import aiohttp


from .sensor import Sensor,Sensors

from async_timeout import timeout
from voluptuous import Optional

from datetime import datetime

from .const import API_TIMEOUT, APIHEADERS, BASEURL
from .const import WATT, KWATT_HOUR, AMPEREHOUR
from .const import VOLT, AMPERE, HERTZ
from .const import DEGREE_CELSIUS, PERCENT

from .const import (
    _LOGGER
)


class SunSynkLoggerAPI:
    def __init__(self) -> None:
        self._username = None
        self._password = None
        self.accesstoken = None
        self.expiresin = None
        self.tokencreatetime = None 
        self._isAuthenticated = False
        self._timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
        #self.inverters: list[Inverter] = []
        self.plants: list[Objects] = []
        self.inverters: list[Objects] = []
        self.inputData: list[Objects] = []
        self.outputData: list[Objects] = []
        self.loadData: list[Objects] = []
        self.gridData: list[Objects] = []
        self.batteryData: list[Objects] = []
        self.settingsData: list[Objects] = []
        self.sensorData: list[Objects] = []

    async def Bearer(self) -> str:
        await self.__isTokenValid() 
        if self._isAuthenticated is True:
            return "Bearer " + self.accesstoken
        else:
            return ""

    async def __isTokenValid(self) -> bool:
        """Check if API needs re-authentication."""
        if self.accesstoken is not None:
            if (self.expiresin is not None) and (self.tokencreatetime is not None):
                timediff = datetime.utcnow() - self.tokencreatetime
                if timediff.total_seconds() < self.expiresin:
                    #_LOGGER.debug("Authentication token remains valid.")
                    return True
                else:
                    self._isAuthenticated = False
                    _LOGGER.error("Authentication token expired, redo login.")
                    await self.Login(self._username, self._password)
                    return self._isAuthenticated
        return False

    async def Login(self, username, password) -> bool:
        """Login to API"""

        self._username = username
        self._password = password

        _LOGGER.debug("SunSynk Logger API Login")

        if not self._isAuthenticated or await self.__isTokenValid() is False:

            resource = f"{BASEURL}/oauth/token"

            async with aiohttp.ClientSession(timeout=self._timeout) as sess:
                try:
                    _LOGGER.debug("Trying authentication with username: %s", self._username)
                    response = await sess.post(
                        resource,
                        json={
                            "username": self._username,
                            "password": self._password,
                            "grant_type": "password",
                            "client_id": "csp-web"
                        },
                        headers=APIHEADERS
                    )

                    if response is not None:
                        if response.status == 200:
                            json_response = await response.json()
                            if "success" in json_response and json_response["success"] != True:
                                self._isAuthenticated=False
                            else:
                                if "access_token" in json_response["data"]:
                                    self.accesstoken = json_response["data"]["access_token"]
                                if "expires_in" in json_response["data"]:
                                    self.expiresin = json_response["data"]["expires_in"]
                                self.tokencreatetime = datetime.now()
                                self.username = username
                                self.password = password
                                self._isAuthenticated = True
                            _LOGGER.debug(json_response["msg"])
                            return True
                        else:
                            self._isAuthenticated=False
                            _LOGGER.error("API Error:" + response.status)
                            return False
                except (aiohttp.ClientConnectionError) as e:
                    _LOGGER.error(e)

                except (aiohttp.client_exceptions.ClientConnectorError) as e:
                    _LOGGER.error(e)

    async def __post(self, path, json) -> Optional(dict):
        """Post Data from SunSynk Logger API"""

        if self._isAuthenticated and await self.__isTokenValid() is True:
            resource = f"{BASEURL}/{path}"
            _LOGGER.debug("Sending %s", resource)
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                try:
                    session.headers.update(APIHEADERS)
                    _bearer = await self.Bearer()
                    session.headers.update({'Authorization': f'{_bearer}'})
                    response = await session.post(
                        resource,
                        json=json
                    )
                    if response is not None:
                        if response.status == 200:
                            json_response = await response.json()

                            if "success" in json_response and json_response["success"] == True:
                                if json_response["data"] is not None:
                                    return json_response["data"]
                                else:
                                    _LOGGER.debug("Response contained no data.")
                                    _LOGGER.error(json_response["msg"])
                                    return None
                except Exception as e:
                    _LOGGER.error(e)

    async def __get(self, path) -> Optional(dict):
        """Get Data from SunSynk Logger API"""

        if self._isAuthenticated and await self.__isTokenValid() is True:
            resource = f"{BASEURL}/{path}"
            _LOGGER.debug("Retrieving %s", resource)
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                try:
                    session.headers.update(APIHEADERS)
                    _bearer = await self.Bearer()
                    session.headers.update({'Authorization': f'{_bearer}'})
                    response = await session.get(
                        resource
                    )
                    if response is not None:
                        if response.status == 200:
                            json_response = await response.json()

                            if "success" in json_response and json_response["success"] == True:
                                if json_response["data"] is not None:
                                    return json_response["data"]
                                else:
                                    _LOGGER.debug("Response contained no data.")
                                    _LOGGER.error(json_response["msg"])
                                    return None
                except Exception as e:
                    _LOGGER.error(e)

    async def __getInverters(self) -> bool:
        """Get Inverter List"""
        _LOGGER.debug("Retrieving Inverter List")
        inv = await self.__get(path=const.SS_INVERTER_LIST_API)
        _LOGGER.debug(inv["infos"])
        for i in inv["infos"]:
            _LOGGER.debug("Adding Inverter %s",i["sn"])
            self.inverters.append(inverter_from_dict(i))

    async def __getInverterList(self) -> bool:
        """Get Inverter List"""
        _LOGGER.debug("Retrieving Inverter List")
        inv = await self.__get(path=const.SS_INVERTER_LIST_API)
        _LOGGER.debug(inv["infos"])
        return inv["infos"]

    async def __getInverterListByPlant(self, plantId) -> bool:
        """Get Inverter List"""
        _LOGGER.debug("Retrieving Inverter List")
        inv = await self.__get(path="api/v1/inverters?page=1&limit=10&total=0&status=-1&sn=&plantId="+str(plantId)+"&type=-2&softVer=&hmiVer=&agentCompanyId=-1&gsn=")
        _LOGGER.debug(inv["infos"])
        return inv["infos"]

    async def getInverterList(self) -> Optional(dict):
        """Get Inverter List"""
        _LOGGER.debug("Retrieving Inverter List")
        return await self.__getInverterList()

    async def getInverterListByPlant(self, plantId) -> Optional(dict):
        """Get Inverter List"""
        _LOGGER.debug("Retrieving Inverter List")
        return await self.__getInverterListByPlant(plantId)

    async def readInverterInput(self, sn) -> Optional(dict):
        """Get Inverter Input"""
        _LOGGER.debug("Retrieving Input Data for Serial : %s", sn)
        input = await self.__get(path="api/v1/inverter/" + sn + "/realtime/input")
        _LOGGER.debug(input)
        return input

    async def readInverterOutput(self, sn) -> Optional(dict):
        """Get Inverter Output"""
        _LOGGER.debug("Retrieving Output Data for Serial : %s", sn)
        output = await self.__get(path="api/v1/inverter/" + sn + "/realtime/output")
        _LOGGER.debug(output)
        return output

    async def readInverterGrid(self, sn) -> Optional(dict):
        """Get Inverter Grid"""
        _LOGGER.debug("Retrieving Grid Data for Serial : %s", sn)
        grid = await self.__get(path="api/v1/inverter/grid/" + sn + "/realtime?sn=" + sn)
        _LOGGER.debug(grid)
        return grid

    async def readInverterLoad(self, sn) -> Optional(dict):
        """Get Inverter Load"""
        _LOGGER.debug("Retrieving Load Data for Serial : %s", sn)
        load = await self.__get(path="api/v1/inverter/load/" + sn + "/realtime?sn=" + sn)
        _LOGGER.debug(load)
        return load

    async def readInverterBattery(self, sn) -> Optional(dict):
        """Get Inverter Battery"""
        _LOGGER.debug("Retrieving Battery Data for Serial : %s", sn)
        batt = await self.__get(path="api/v1/inverter/battery/" + sn + "/realtime?sn=" + sn + "&lan")
        _LOGGER.debug(batt)
        return batt

    async def readInverterSettings(self,sn: str) -> Optional(dict):
        """ Get Inverter Current Settings Data"""
        _LOGGER.debug("Reading Inverter Settings Data.... %s", sn)
        settings = await self.__get(path="api/v1/common/setting/" + sn + "/read")
        inverter_index = self.getInverterIndex(sn)
        if self.settingsData:   
            self.settingsData[inverter_index] = settings
        else:
            self.settingsData.append(settings)
        _LOGGER.debug(settings)
        return settings  

    async def readInverterCustom(self, sn: str, params) -> Optional(dict):
        """Get Inverter Custom"""
        _LOGGER.debug("Retrieving Custom Data for Serial : %s", sn)
        today = datetime.today()
        d = today.strftime("%Y-%m-%d")
        custom =  await self.__get(path="api/v1/inverter/" + sn + "/day?sn=" + sn + "&date="+ d+ "&edate="+ d+ "&lan=en&params="+params)
        _LOGGER.debug(custom)
        return custom

    def __getInverterSensors(self, inverter) -> Sensors:
        sensors: Sensors = []
        sensors.append( Sensor (  key = inverter["sn"]  +"_status", name = "Inverter Status", value = inverter["status"] ) )
        sensors.append( Sensor (  key = inverter["sn"]  +"_pac", name = "Inverter Energy", unit =WATT , value = inverter["pac"]) )
        sensors.append( Sensor (  key = inverter["sn"]  +"_etoday", name = "Inverter Energy Today", unit = KWATT_HOUR,  value = inverter["etoday"]) )
        #sensors.append( Sensor (  key = inverter["sn"]  +"_emonth", name = "Inverter Energy Month", unit = KWATT_HOUR,  value = inverter["emonth"]) )
        sensors.append( Sensor (  key = inverter["sn"]  +"_etotal", name = "Inverter Energy Total", unit = KWATT_HOUR, value = inverter["etotal"]) )
        #sensors.append( Sensor (  key = inverter["sn"]  +"_runstatus", name = "Inverter Run Status", unit = KWATT_HOUR, value = inverter["runStatus"]) )
        return sensors

    async def __getInverterCustomSensors(self,inverter) -> Sensors:
        sensors: Sensors = []
        params="21,29,79,23,88,20"
        custData = await self.readInverterCustom(inverter["sn"] ,params)
        for p in custData["infos"]:
            sensors.append( Sensor (  key = inverter["sn"]  +"_custom_" + p["label"], name = "Inverter Data " + p["label"], unit = WATT, value = p["records"][-1]["value"]) )
        return sensors

    def __getInverterInputSensors(self,inverter) -> Sensors:
        sensors: Sensors = []
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pac", name = "Input P-ac", unit =WATT , value = inverter["pac"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_eToday", name = "Input eToday", unit =KWATT_HOUR , value = inverter["etoday"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_eTotal", name = "Input eTotal", unit =KWATT_HOUR , value = inverter["etotal"]) )

        inverter_index = self.getInverterIndex(inverter["sn"])
        inData = self.inputData[inverter_index]
        _LOGGER.debug(inData)

        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv1_power", name = "P-pv-L1", unit =WATT , value = inData["pvIV"][0]["ppv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv1_current", name = "I-pv-L1", unit = AMPERE , value = inData["pvIV"][0]["ipv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv1_voltage", name = "V-pv-L1", unit =VOLT , value = inData["pvIV"][0]["vpv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv1_todayPV", name = "P-pv-L1-Today", unit =KWATT_HOUR , value = inData["pvIV"][0]["todayPv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv2_power", name = "P-pv-L2", unit =WATT , value = inData["pvIV"][1]["ppv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv2_current", name = "I-pv-L2", unit =AMPERE , value = inData["pvIV"][1]["ipv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv2_voltage", name = "V-pv-L2", unit =VOLT , value = inData["pvIV"][1]["vpv"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_input_pv2_todayPV", name = "P-pv-L2-Today", unit =KWATT_HOUR , value = inData["pvIV"][1]["todayPv"]) )


        return sensors

    def __getInverterOutputSensors(self,inverter) -> Sensors:
        sensors: Sensors = []

        inverter_index = self.getInverterIndex(inverter["sn"])
        outData = self.outputData[inverter_index]
        _LOGGER.debug (outData)

        sensors.append( Sensor (  key = inverter["sn"] +"_output_power", name = "Output Power", unit = WATT , value = outData["pac"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_output_current", name = "Output Current", unit =AMPERE , value = outData["vip"][0]["current"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_output_voltage", name = "Output Voltage", unit =VOLT , value = outData["vip"][0]["volt"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_output_frequency", name = "Output Frequency", unit = HERTZ , value = outData["fac"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_output_pInv", name = "Output pInv", unit = WATT , value = outData["pInv"]) )

        return sensors

    def __getInverterGridSensors(self,inverter) -> Sensors:
        sensors: Sensors = []
        inverter_index = self.getInverterIndex(inverter["sn"])
        gridData = self.gridData[inverter_index]
        _LOGGER.debug(gridData)

        sensors.append( Sensor (  key = inverter["sn"] +"_grid_power_ext_ct", name = "P-Ext-CT", unit =WATT , value = gridData["pac"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_power", name = "Grid Power", unit =WATT , value = gridData["vip"][0]["power"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_current", name = "Grid Current", unit =AMPERE , value = gridData["vip"][0]["current"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_voltage", name = "Grid Voltage", unit =VOLT , value = gridData["vip"][0]["volt"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_frequency", name = "Grid Frequency", unit = HERTZ , value = gridData["fac"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_powerfactor", name = "Grid Power Factor" , value = gridData["pf"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_status", name = "Grid Status" , value = gridData["status"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_in_today", name = "Grid Supply Today", unit =KWATT_HOUR , value = gridData["etodayFrom"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_in_total", name = "Grid Supply Total", unit =KWATT_HOUR , value = gridData["etotalFrom"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_out_today", name = "Grid Export Today", unit =KWATT_HOUR , value = gridData["etodayTo"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_grid_out_total", name = "Grid Export Total", unit =KWATT_HOUR , value = gridData["etotalTo"]) )
        return sensors

    def __getInverterLoadSensors(self,inverter) -> Sensors:
        sensors: Sensors = []

        inverter_index = self.getInverterIndex(inverter["sn"])
        loadData = self.loadData[inverter_index]
        _LOGGER.debug (loadData)
        
        sensors.append( Sensor (  key = inverter["sn"] +"_load_totalUsed", name = "Load Total Used", unit =KWATT_HOUR , value = loadData["totalUsed"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_dailyUsed", name = "Load Used Daily", unit =KWATT_HOUR , value = loadData["dailyUsed"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_totalPower", name = "Load Total Power", unit =WATT , value = loadData["totalPower"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_smartload", name = "Smartload Status", value = loadData["smartLoadStatus"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_fac", name = "Load Frequency", unit =HERTZ , value = loadData["loadFac"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_upsPower", name = "UPS Total Power", unit =WATT , value = loadData["upsPowerTotal"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_voltage", name = "V-L1", unit =VOLT , value = loadData["vip"][0]["volt"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_current", name = "I-L1", unit =AMPERE , value = loadData["vip"][0]["current"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_load_power", name = "P-L1", unit =WATT , value = loadData["vip"][0]["power"]) )

        return sensors

    def __getInverterBatterySensors(self,inverter) -> Sensors:
        sensors: Sensors = []
        inverter_index = self.getInverterIndex(inverter["sn"])
        battData = self.batteryData[inverter_index]
        _LOGGER.debug (battData)

        sensors.append( Sensor (  key = inverter["sn"] +"_battery_status", name = "Battery Status", value = battData["status"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_current", name = "Battery Current", unit =AMPERE , value = battData["current"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_voltage", name = "Battery Voltage", unit =VOLT , value = battData["voltage"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_power", name = "Battery Power", unit =WATT , value = battData["power"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_temp", name = "Battery Temperature", unit =DEGREE_CELSIUS , value = battData["temp"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_etodayChg", name = "Battery Charge Today", unit =KWATT_HOUR , value = battData["etodayChg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_etodayDischg", name = "Battery Discharge Today", unit =KWATT_HOUR , value = battData["etodayDischg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_emonthChg", name = "Battery Charge Month", unit =KWATT_HOUR , value = battData["emonthChg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_emonthDischg", name = "Battery Discharge Month", unit =KWATT_HOUR , value = battData["emonthDischg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_eyearChg", name = "Battery Charge Year", unit =KWATT_HOUR , value = battData["eyearChg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_eyearDischg", name = "Battery Discharge Year", unit =KWATT_HOUR , value = battData["eyearDischg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_etotalChg", name = "Battery Charge Total", unit =KWATT_HOUR , value = battData["etotalChg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_etotalDischg", name = "Battery Discharge Total", unit =KWATT_HOUR , value = battData["etotalDischg"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_soc", name = "Battery State of Charge", unit =PERCENT , value = battData["soc"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_capacity", name = "Battery Capacity", unit =AMPEREHOUR , value = battData["capacity"]) )
        sensors.append( Sensor (  key = inverter["sn"] +"_battery_correctCap", name = "Battery Corrected Capacity", unit =AMPEREHOUR , value = battData["correctCap"]) )
        return sensors

    async def getSensorsForInverter(self,serial) -> Optional(Sensors):
        """Get Sensor Objects by Inverter Serial"""
        sen: Sensors = Sensors()
        _LOGGER.info("Retrieving Sensors for Inverter : %s", serial)
        inverter_index=self.getInverterIndex(serial)
        inv = self.inverters[inverter_index]
        sen.add( self.__getInverterSensors(inv))
        sen.add( await self.__getInverterCustomSensors(inv))
        sen.add( self.__getInverterInputSensors(inv))
        sen.add( self.__getInverterOutputSensors(inv))
        sen.add( self.__getInverterGridSensors(inv))
        sen.add( self.__getInverterLoadSensors(inv))
        sen.add( self.__getInverterBatterySensors(inv))
        self.sensorData = sen
        return sen

    async def getSensors(self,sn) -> Optional(Sensors):
        """Get Sensor Objects Data"""
        return await self.getSensorsForInverter(sn)

    async def readSettings(self,sn: str) -> bool:
        """ Get Inverter Current Settings Data"""
        return await self.readInverterSettings(sn)

    async def read(self) -> bool:
        return await self.readAll()

    async def readAll(self) -> bool:
        """ Update All Data"""
        _LOGGER.info("Reading Plant Data....")
        
        for plant in await self.getPlantList():
            plant_index = next((i for i, p in enumerate(self.plants) if p["id"] == plant["id"]), -1)
            if plant_index == -1:
                _LOGGER.info("Adding Plant : %s %s %s" , plant["id"], ":", plant["name"])
                self.plants.append(plant)
            else:
                _LOGGER.info("Updating Plant : %s %s %s" , plant["id"], ":", plant["name"])
                self.plants[plant_index] = plant


        #print(self.plants)

        _LOGGER.info("Reading Inverter Data....")
        for inv in await self.getInverterList():
            inv_index = self.getInverterIndex(inv["sn"])
            if inv_index == -1:
                _LOGGER.info("Adding Inverter : %s %s %s" , inv["sn"], ":", inv["alias"])
                self.inverters.append(inv)
            else:
                _LOGGER.info("Updating Inverter : %s %s %s" , inv["sn"], ":", inv["alias"])
                self.inverters[inv_index] = inv                

        #print(self.inverters)

        for inv in self.inverters:
            if not self.inputData:
                _LOGGER.info("Retrieving Data for Inverter : %s" , inv["sn"])
                self.inputData.append (await self.readInverterInput(inv["sn"]) )
            else:    
                self.inputData[inv_index] = (await self.readInverterInput(inv["sn"]) )
            if not self.outputData:
                self.outputData.append ( await self.readInverterOutput(inv["sn"]) )
            else: 
                self.outputData[inv_index] = ( await self.readInverterOutput(inv["sn"]) )
            if not self.settingsData:
                self.settingsData.append( await self.readInverterSettings(inv["sn"]) )
            else: 
                self.settingsData[inv_index] = ( await self.readInverterSettings(inv["sn"]) )
            if not self.loadData:
                self.loadData.append ( await self.readInverterLoad(inv["sn"]) )
            else: 
                self.loadData[inv_index] = ( await self.readInverterLoad(inv["sn"]) )
            if not self.gridData:
                self.gridData.append ( await self.readInverterGrid(inv["sn"]) )
            else: 
                self.gridData[inv_index] = ( await self.readInverterGrid(inv["sn"]) )
            if not self.batteryData:
                self.batteryData.append ( await self.readInverterBattery(inv["sn"]) )
            else: 
                self.batteryData[inv_index] = ( await self.readInverterBattery(inv["sn"]) )               

        _LOGGER.info("Reading Inverter Data Completed.")    
        return True

    async def __getPlantList(self) -> Optional(dict):
        plants = await self.__get(path=const.SS_PLANT_LIST_API)
        return plants["infos"]
        
    async def getPlantList(self) -> Optional(dict):
        """Get Plant List"""
        _LOGGER.debug("Retrieving Plant List")
        return await self.__getPlantList()

    def getInverterIndex(self, sn: str) -> int:
        """Return Inverter Index by SN"""
        index = next((i for i, inv in enumerate(self.inverters) if inv["sn"] == sn), -1)
        return index