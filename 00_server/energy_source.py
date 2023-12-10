from datetime import datetime
import logging
#import pandas as pd

class EnergySource:
    '''
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
'''
from datetime import datetime
import logging
import csv

class EnergySource:

    def __init__(self, name):
        self.energy_table = self.read_energy_table("./de_avg_125w.csv")
        self.name = name
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s >>> %(message)s',
                        handlers=[logging.StreamHandler()])
        self.logger = logging.getLogger(__name__)
        self.logger.info("Energy source {} created".format(self.name))

    def read_energy_table(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            return list(reader)

    def get_energy_supply(self):
        time = datetime.now().strftime('%H:%M:%S')
        self.logger.info("Get energy for time {}".format(time))

        # Find the corresponding value in the list of dictionaries
        for row in self.energy_table:
            if row['time'] == time:
                value = float(row['avg'])
                break
        else:
            # Handle the case when the time is not found
            value = 0.0
            self.logger.warning("Energy data not available for time {}".format(time))

        self.logger.info("Energy production for time {} is {}".format(time, value))
        return value

if __name__ == '__main__':
    e = EnergySource('test')
    value = e.get_energy_supply()
    print(value)

