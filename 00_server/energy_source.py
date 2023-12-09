from datetime import datetime
import logging
import pandas as pd

class EnergySource:

    def __init__(self, name):
        self.energy_table = pd.read_csv("./de_avg_125w.csv", sep=";")
        self.name = name
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s >>> %(message)s',
                        handlers=[logging.StreamHandler()])
        self.logger = logging.getLogger(__name__)
        self.logger.info("Energy source {} created".format(self.name))

    # Get time and date, look it up in the table and return energy production value
    def get_energy_supply(self):
        # Get the time in the format %H:%M:%S
        time = datetime.now().strftime('%H:%M:%S')

        self.logger.info("Get energy for time {}".format(time))

        # Find the corresponding value in the DataFrame
        value = float(self.energy_table[self.energy_table['time'] == time]['avg'].values[0])

        self.logger.info("Energy production for time {} is {}".format(time, value))

        # Return in Watts NOT in Kilo Watts
        return value

if __name__ == '__main__':
    e = EnergySource('test')
    value = e.get_energy_supply()
    print(value)