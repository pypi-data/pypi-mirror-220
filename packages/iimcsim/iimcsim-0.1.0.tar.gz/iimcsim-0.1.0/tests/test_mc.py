import iimcsim.data_gen_run as dg
from iimcsim.eda import eda

dg.data_gen_run().generate_data(train_exe = 50,
                    name = r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data\plateauless_uniq_pulses_2345.npy",
                    samp_size = 256,
                    max_num_photon = 60,
                    folder_name = 'sh06x2')

q = eda()
q.shapes_extraction(calib_data_path=r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data\calib_ch0.npy",
                      high_rate_path = r'C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data\shaula_00000-003_ch0.npy',
                      data_save_path='C:\\Users\\jigar\\Downloads\\photon_position_reconstruction-main\\photon_position_reconstruction-main\\src\\data\\',
                      bins = 21400)