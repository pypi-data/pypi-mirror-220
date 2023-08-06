import iimcsim.tools as fg
import numpy as np
from iimcsim.shape_ext import shape_generator

class eda:

    def __init__(self):
        pass

    def shapes_extraction(self, calib_data_path='../src/data/calib_ch0.npy',
                        high_rate_path = '../src/data/shaula_00000-003_ch0.npy',
                        data_save_path='../src/data/',
                        bins = 21400
                        ):
        # required files
        # calib.npy and shaula_00000-003_ch0.npy
        select_files = shape_generator(calib_data_path, high_rate_path,data_save_path)
        generate_shapes = select_files.generator(bin_num=bins)
        shapes, save_path = select_files.scalar(generate_shapes)
        # generated file
        # shaula_00000-003_ch0_shapes.npy
        return shapes

    def pulse_sh_plat(self, shapes_path = '../src/data/shaula_00000-003_ch0_shapes.npy',
                    pulse_info_path = '../src/data/',
                    plat_size_sel = 1,
                    plot_save_path = '../plots/',
                    lst=[3,4,5]):
        uniq_shape = np.load(shapes_path)
        # Generate data of extracted pulse, individually; pulse height, pulse width, skewness, kurtosis in dataframe format
        df = fg.pulse_data(uniq_shape)
        df.to_csv('calib_pulse_data.csv')
        fg.skew_kurt(df, plat_size_sel, plot_save_path)
        platauless_uniq_shapes, uniq_shapes = fg.filter_shapes_based_on_plat_size(df, uniq_shape, platau_removal=True, lst=lst, save_path=pulse_info_path)
        return platauless_uniq_shapes, uniq_shapes


#shapes = shapes_extraction(r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data\calib_ch0.npy",
#                           r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data\shaula_00000-003_ch0.npy",
#                           r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data")

#pulse_sh_plat(r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data\shaula_00000-003_ch0_shapes.npy",
#              r"C:\Users\jigar\Downloads\photon_position_reconstruction-main\photon_position_reconstruction-main\src\data",
#              plot_save_path = './')