class PowerMeasurement:
    """
    Structure that contains the data representing a power consumption
    measurement of a specific device.

    - timestamp: timestamp of the measurement, given in microseconds.
        -> This timestamp is NOT based on UNIX epoch time, but on the elapsed time 
            since start-up of the ESP32 power measurement node.  
    - (energy_consumption: total power consumption at the time of measurement, given in mAs.)
    - current: the electrical current at the time of measurement, given in mA.
    - energy_supply: Electrical current at the time of measurement, given in W
    - battery_state: Relative state of the battery in %
    """
    def __init__(self, timestamp, device_energy_consumption_mw, device_energy_consumption_ma, energy_supply, battery_capacity_rel):
        self.timestamp = timestamp
        self.device_energy_consumption_mw = device_energy_consumption_mw
        self.device_energy_consumption_ma = device_energy_consumption_ma
        self.energy_supply = energy_supply
        self.battery_capacity_rel = battery_capacity_rel