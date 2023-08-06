import numpy as np
import pandas as pd
import pickle
import sys
sys.path.append("..")
import iimcsim.data_gen as data_gen
import iimcsim.tools as fg

# Required files: MC.py, monte_carlo.py and pulse shape file in 
# .npy format(here plateauless_uniq_pulses.npy)

class data_gen_run:

    def __init__(self) -> None:
        pass


    def generate_data(self, train_exe = 50,
                    name = 'plateauless_uniq_pulses_345.npy',
                    samp_size = 256,
                    max_num_photon = 60,
                    folder_name = 'sh06x2'):
        data_gen.generator(samp_size, max_num_photon, name, train_exe, folder_name)
#generate_data()