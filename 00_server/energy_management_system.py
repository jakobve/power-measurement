import logging
from datetime import datetime
from battery import Battery
from energy_source import EnergySource
from battery_state import BatteryState
from power_measurement import PowerMeasurement
from jtop import jtop
import time

class EnergyManagementSystem:

    def __init__(self):
        self.battery = Battery("battery_01")
        self.energy_source = EnergySource("energy_source_01")

        # Set up logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s >>> %(message)s',
                            handlers=[logging.StreamHandler()])
        self.logger = logging.getLogger(__name__)
        self.logger.info("Energy management system created")


    # Get energy consumption from device in mA
    # Mock: 7.5W at 5V -> (7.5W / 5V) = 1.5A = 1500mA
    # Returns data in mA
    def get_device_energy_consumption_ma(self):
       # Return mock data
       # return 1500
       jetson = jtop()
       jetson.start
       stat = int(jetson.power['tot']['curr'])
       jetson.close()
       return stat
            
    # Get energy consumption from device in milli Watt
    def get_device_energy_consumption_mw(self):
       # Return mock data
       #return 7500
       jetson = jtop()
       jetson.start
       stat = int(jetson.power['tot']['power'])
       jetson.close()
       return stat

    # Returns 
    def get_battery_state(self):
        return self.battery.get_battery_state()
    
    # Returns battery capacity in %
    def get_battery_capacity_rel(self):
        return self.battery.get_capacity_rel()
    
    # Returns the energy consumption of the battery

    
    # Returns energy supply in milli Watt
    def get_energy_supply(self):
        return self.energy_source.get_energy_supply() * 1000
    
    # Converts current energy supply from milli watt to milli ampere
    def convert_energy_supply(self, mw):
        # Watt / Volt
        # Volatage = 5V
        ma = (mw / 5)
        return ma
    
    def get_powermeasurement(self):
        # energy_supply = self.get_energy_supply()
        # energy_supply_conv = self.convert_energy_supply(energy_supply)

        return PowerMeasurement(
            # Format: 
            timestamp = str(datetime.now()),
            # In mW
            device_energy_consumption_mw = self.get_device_energy_consumption_mw(),
            # In mA
            device_energy_consumption_ma = self.get_device_energy_consumption_ma(), 
            # In mW
            energy_supply = self.get_energy_supply(),
            # In %
            battery_capacity_rel = self.get_battery_capacity_rel()
            )
    
    #async def management_task(self):
    def manage(self):

        while True:
            # Enqueue the power measurement
            #await self.queue.put(await self.get_powermeasurement())

            #mW
            device_energy_consumption_mw = self.get_device_energy_consumption_mw()
            self.logger.info("Energy consumption mW: {}".format(device_energy_consumption_mw))

            # mA
            device_energy_consumption_ma = self.get_device_energy_consumption_ma()
            self.logger.info("Energy consumption mA: {}".format(device_energy_consumption_ma))

            # mW
            energy_supply = self.get_energy_supply()
            self.logger.info("Energy supply: {}".format(energy_supply))

            # mA
            energy_supply_conv = self.convert_energy_supply(energy_supply)
            self.logger.info("Energy supply conv: {}".format(energy_supply_conv))

            delta = energy_supply_conv - device_energy_consumption_ma
            self.logger.info("Delta: {}".format(delta))

            if delta < 0:
                if not self.battery.battery_state is BatteryState.EMPTY:
                    self.battery.discharge
                    self.logger.info("Discharging battery")
                else:
                    self.logger.info("Battery EMPTY. Stopping monitoring...")
                    break
            elif delta > 0:
                if not self.battery.battery_state is BatteryState.FULL:
                    self.battery.charge(delta)
                    self.logger.info("Charging battery")
                else:
                    self.logger.info("Battery FULL")
        
            time.sleep(1)