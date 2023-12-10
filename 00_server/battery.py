from battery_state import BatteryState
import logging

class Battery:

    # Constants
    # Maximum battery capacity in mAs (3500 mAh * 3600s)
    # -> Measurements are in mAs
    MAX_ABS_CAPACITY = 3500 * 3600

    # Minimum charge capacity in mAh
    MIN_ABS_CAPACITY = MAX_ABS_CAPACITY * 0.2

    MAX_CHARGE_AMOUNT = 2000

    def __init__(self, name, current_abs_capacity = MAX_ABS_CAPACITY):
        self.name = name
        self.current_abs_capacity = current_abs_capacity
        self.battery_state = BatteryState.FULL
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s >>> %(message)s',
                        handlers=[logging.StreamHandler()])
        self.logger = logging.getLogger(__name__)
        self.logger.info("Battery {} created".format(self.name))
        
    # Retuns the Enum state of a battery
    def get_battery_state(self):
        self.logger.info("BATTERY STATE: {}".format(self.battery_state))
        return self.battery_state

    # Returns the relative current battery capacity as float
    def get_capacity_rel(self):
        self.logger.info("BATTERY CAPACITY REL: {}".format((self.current_abs_capacity / self.MAX_ABS_CAPACITY)))
        return self.current_abs_capacity / self.MAX_ABS_CAPACITY
    
    def get_capacity_abs(self):
        self.logger.info("BATTERY CAPACITY REL: {}".format(self.current_abs_capacity))
        return self.current_abs_capacity

    # Charges the actual absolute battery capacity by an absolute amount
    def charge(self, amount):
        if 0 <= amount <= self.MAX_CHARGE_AMOUNT:
            if 0 <= amount < (self.MAX_ABS_CAPACITY - self.current_abs_capacity):
                self.current_abs_capacity += amount
                self.battery_state = BatteryState.NORMAL
            else:
                self.current_abs_capacity = self.MAX_ABS_CAPACITY
                self.battery_state = BatteryState.FULL
        elif amount > self.MAX_CHARGE_AMOUNT:
            if (self.current_abs_capacity + self.MAX_CHARGE_AMOUNT) < self.MAX_ABS_CAPACITY:
                self.current_abs_capacity += self.MAX_CHARGE_AMOUNT
                self.battery_state = BatteryState.NORMAL
            else:
                self.current_abs_capacity = self.MAX_ABS_CAPACITY
                self.battery_state = BatteryState.FULL



    def discharge(self, amount):
        if 0 <= amount <= self.current_abs_capacity - self.MIN_ABS_CAPACITY:
            self.current_abs_capacity -= amount
            self.battery_state = BatteryState.NORMAL
        else:
            self.current_abs_capacity = self.MIN_ABS_CAPACITY
            self.battery_state = BatteryState.EMPTY


    