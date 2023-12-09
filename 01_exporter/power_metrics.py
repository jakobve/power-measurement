import logging

#from powermeasurement import PowerMeasurement
from power_measurement import PowerMeasurement
from prometheus_client import Counter, Gauge

logger = logging.getLogger(__name__)


class CounterWrapper:
    """ Wrapper for a prometheus counter in order to keep track of its value. """
    def __init__(self, prom_counter: Counter):
        self.counter = prom_counter
        self.counter_value = 0

    def set_value(self, new_value: float):
        self.counter_value = new_value

    def get_value(self):
        return self.counter_value

#METRIC_NAME_TOTAL_CONSUMPTION = "powerexporter_power_consumption_ampere_seconds_total"
#METRIC_DESC_TOTAL_CONSUMPTION = "The total power consumption given in ampere-seconds."

METRIC_NAME_CURRENT_USE_W = "powerexporter_current_watt_consumption"
METRIC_DESC_CURRENT_USE_W = "The consumption of electric current given in watt."

METRIC_NAME_CURRENT_USE_MW = "powerexporter_current_milli_watt_consumption"
METRIC_DESC_CURRENT_USE_MW = "The consumption of electric current given in milli watt."

METRIC_NAME_CURRENT_USE_A = "powerexporter_current_ampere_consumption"
METRIC_DESC_CURRENT_USE_A = "The consumption of electric current given in ampere."

METRIC_NAME_CURRENT_USE_MA = "powerexporter_current_milli_ampere_consumption"
METRIC_DESC_CURRENT_USE_MA = "The consumption of electric current given in milli ampere."

METRIC_NAME_CURRENT_PROD = "powerexporter_current_ampere_production"
METRIC_DESC_CURRENT_PROD = "The production of electric current given in ampere."

METRIC_NAME_CURRENT_PROD_MA = "powerexporter_current_milli_ampere_production"
METRIC_DESC_CURRENT_PROD_MA = "The production of electric current given in milli ampere."

METRIC_NAME_BATTERY_REL = "powerexporter_battery_rel"
METRIC_DESC_BATTERY_REL = "The state of the battery in %"

#ENERGY_CONSUMPTION_COUNTER = CounterWrapper(
#    Counter(METRIC_NAME_TOTAL_CONSUMPTION, METRIC_DESC_TOTAL_CONSUMPTION)
#)

ENERGY_CONSUMPTION_W = Gauge(METRIC_NAME_CURRENT_USE_W, METRIC_DESC_CURRENT_USE_W)
ENERGY_CONSUMPTION_MW = Gauge(METRIC_NAME_CURRENT_USE_MW, METRIC_DESC_CURRENT_USE_MW)

ENERGY_CONSUMPTION_A = Gauge(METRIC_NAME_CURRENT_USE_A, METRIC_DESC_CURRENT_USE_A)
ENERGY_CONSUMPTION_MA = Gauge(METRIC_NAME_CURRENT_USE_MA, METRIC_DESC_CURRENT_USE_MA)

ENERGY_SUPPLY = Gauge(METRIC_NAME_CURRENT_PROD, METRIC_DESC_CURRENT_PROD)
ENERGY_SUPPLY_MA = Gauge(METRIC_NAME_CURRENT_PROD_MA, METRIC_DESC_CURRENT_PROD_MA)

BATTERY_STATE_REL = Gauge(METRIC_NAME_BATTERY_REL, METRIC_DESC_BATTERY_REL)

def update_metrics(new_data: PowerMeasurement) -> None:
    """ Updates the power-related metrics based on the new data. """
    #increment_counter_to(ENERGY_CONSUMPTION_COUNTER, new_data.energy_consumption / 1000)  # mAs -> A
    ENERGY_CONSUMPTION_W.set(new_data.device_energy_consumption_mw)
    ENERGY_CONSUMPTION_MW.set(new_data.device_energy_consumption_mw / 1000) # mW -> W

    ENERGY_CONSUMPTION_MA.set(new_data.device_energy_consumption_ma)  # mA
    ENERGY_CONSUMPTION_A.set(new_data.device_energy_consumption_ma / 1000)  # mA -> A

    ENERGY_SUPPLY.set(new_data.energy_supply) # W
    ENERGY_SUPPLY_MA.set(new_data.energy_supply) # mA

    BATTERY_STATE_REL.set(new_data.battery_capacity_rel) # %
    
    logger.info("POWER METRICS - update_metrics done")

def increment_counter_to(counter_wrapper: CounterWrapper, new_value: float) -> None:
    """
    Increments a prometheus counter up to the given `new_value`

    This is a workaround because the counter API does not support incrementing a counter up to a fixed value, but only
    increment by a certain value. This is a problem as we are only receiving the most recent value of the total power
    consumption and not its difference compared to the previous measurement.

    :param counter_wrapper: the prometheus counter to increment.
    :param new_value: the desired new value of the counter.
    """
    if new_value < 0 or new_value < counter_wrapper.get_value():
        logger.error("Illegal operation - Cannot increment counter to a negative or lower value!")
        return

    difference: float = new_value - counter_wrapper.get_value()
    counter_wrapper.counter.inc(difference)
    counter_wrapper.set_value(new_value)
