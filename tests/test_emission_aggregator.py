import pytest
import numpy as np
from src.emission_aggregator import EmissionAggregator

@pytest.fixture
def ef_data_farmer():
    return {'EF_CT_P': np.array([0.01721731]), 'EF_CT_PE': np.array([0.0100768]), 'EF_Topo': np.array([0.01721731]), 'EF': np.array([0.01098705])}

@pytest.fixture
def ef_data_scientific():
    return {
        'P': {'EF_CT_P': np.array([0.01721731, 0.03008165, 0.05255789]), 
              'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
              'EF_Topo': np.array([0.01721731, 0.03008165, 0.05255789]), 
              'EF': np.array([0.01098705, 0.01919629, 0.03353927])}, 
        'PE': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
               'EF_CT_PE': np.array([0.0100768 , 0.01760592, 0.03076062]), 
               'EF_Topo': np.array([0.01721731, 0.01726282, 0.01880323]), 
               'EF': np.array([0.01098705, 0.01101609, 0.01199909])}, 
        'FR_Topo': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
                    'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
                    'EF_Topo': np.array([0.01721731, 0.01721731, 0.01721731]), 
                    'EF': np.array([0.01098705, 0.01098705, 0.01098705])}, 
        'soil_texture': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
                         'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
                         'EF_Topo': np.array([0.01721731, 0.01721731, 0.01721731]), 
                         'EF': np.array([0.01098705, 0.0132293 , 0.01547155])}, 
        'RF_AM': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
                  'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
                  'EF_Topo': np.array([0.01721731, 0.01721731, 0.01721731]), 
                  'EF': np.array([0.01098705, 0.01098705, 0.01098705])}, 
        'RF_CS': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
                  'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
                  'EF_Topo': np.array([0.01721731, 0.01721731, 0.01721731]), 
                  'EF': np.array([0.01098705, 0.01098705, 0.01098705])}, 
        'RF_NS': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
                  'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
                  'EF_Topo': np.array([0.01721731, 0.01721731, 0.01721731]), 
                  'EF': np.array([0.01098705, 0.01098705, 0.01098705])}, 
        'RF_Till': {'EF_CT_P': np.array([0.01721731, 0.01721731, 0.01721731]), 
                    'EF_CT_PE': np.array([0.0100768, 0.0100768, 0.0100768]), 
                    'EF_Topo': np.array([0.01721731, 0.01721731, 0.01721731]), 
                    'EF': np.array([0.01098705, 0.01098705, 0.01098705])}}


@pytest.fixture
def n_data_farmer():
    return {'C_p': np.array([3268.0]), 
            'above_ground_carbon_input': np.array([5228.8]), 
            'below_ground_carbon_input': np.array([1307.1999999999998]), 
            'above_ground_residue_n': np.array([14.161333333333335]), 
            'below_ground_residue_n': np.array([2.5417777777777775]), 
            'n_crop_residue': np.array([1670.3111111111114])}

@pytest.fixture
def n_data_scientific():
    return {
        'area':{'C_p': np.array([3268.0]), 
                'above_ground_carbon_input': np.array([5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335]), 
                'below_ground_residue_n': np.array([2.5417777777777775]), 
                'n_crop_residue': np.array([1670.3111111111114])}, 
        'yield': {'C_p': np.array([3268.0]), 
                  'above_ground_carbon_input': np.array([5228.8]), 
                  'below_ground_carbon_input': np.array([1307.1999999999998]), 
                  'above_ground_residue_n': np.array([14.161333333333335]), 
                  'below_ground_residue_n': np.array([2.5417777777777775]), 
                  'n_crop_residue': np.array([1670.3111111111114])}, 
        'group': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                  'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                  'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]),
                  'above_ground_residue_n': np.array([14.161333333333335, 14.161333333333335, 6.5360000000000005]), 
                  'below_ground_residue_n': np.array([2.5417777777777775, 1.6703111111111109, 2.5417777777777775]), 
                  'n_crop_residue': np.array([1670.3111111111114, 1583.1644444444446, 907.7777777777777])}, 
        'S_p': {'C_p': np.array([3268.0, 3182.0, 3096.0]), 
                'above_ground_carbon_input': np.array([5228.8, 4932.099999999999, 4644.0]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1272.8, 1238.3999999999999]), 
                'above_ground_residue_n': np.array([14.161333333333335, 13.435111111111109, 12.727999999999998]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.4748888888888887, 2.408]), 
                'n_crop_residue': np.array([1670.3111111111114, 1590.9999999999995, 1513.5999999999997])}, 
        'S_s': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5392.200000000001, 5555.6]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335, 14.706, 15.250666666666667]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.5417777777777775, 2.5417777777777775]), 
                'n_crop_residue': np.array([1670.3111111111114, 1724.7777777777778, 1779.2444444444445])}, 
        'S_r': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1388.9, 1470.6]), 
                'above_ground_residue_n': np.array([14.161333333333335, 14.161333333333335, 14.161333333333335]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.7233333333333336, 2.904888888888889]), 
                'n_crop_residue': np.array([1670.3111111111114, 1688.4666666666667, 1706.6222222222223])}, 
        'carbon_concentration': {'C_p': np.array([3268.0, 4085.0, 4902.0]), 
                                 'above_ground_carbon_input': np.array([5228.8, 6536.0, 7843.2]), 
                                 'below_ground_carbon_input': np.array([1307.1999999999998, 1634.0, 1960.7999999999997]), 
                                 'above_ground_residue_n': np.array([14.161333333333335, 17.701666666666668, 21.241999999999997]), 
                                 'below_ground_residue_n': np.array([2.5417777777777775, 3.1772222222222224, 3.8126666666666664]), 
                                 'n_crop_residue': np.array([1670.3111111111114, 2087.888888888889, 2505.4666666666662])}, 
        'moisture': {'C_p': np.array([3268.0, 3230.0, 3192.0]), 
                     'above_ground_carbon_input': np.array([5228.8, 5168.0, 5107.2]), 
                     'below_ground_carbon_input': np.array([1307.1999999999998, 1292.0, 1276.8]), 
                     'above_ground_residue_n': np.array([14.161333333333335, 13.996666666666666, 13.831999999999999]), 
                     'below_ground_residue_n': np.array([2.5417777777777775, 2.5122222222222224, 2.4826666666666664]), 
                     'n_crop_residue': np.array([1670.3111111111114, 1650.8888888888891, 1631.4666666666665])}, 
        'R_p': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 4085.0, 3703.7333333333336]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 653.5999999999999, 435.73333333333335]), 
                'above_ground_residue_n': np.array([14.161333333333335, 10.348666666666666, 9.07777777777778]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 1.2708888888888887, 0.8472592592592594]), 
                'n_crop_residue': np.array([1670.3111111111114, 1161.9555555555555, 992.5037037037038])}, 
        'R_s': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 6372.599999999999, 7516.4]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335, 17.973999999999997, 21.78666666666667]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.5417777777777775, 2.5417777777777775]), 
                'n_crop_residue': np.array([1670.3111111111114, 2051.5777777777776, 2432.844444444445])}, 
        'R_r': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 2287.6, 3267.999999999999]), 
                'above_ground_residue_n': np.array([14.161333333333335, 14.161333333333335, 14.161333333333335]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 4.720444444444444, 6.89911111111111]), 
                'n_crop_residue': np.array([1670.3111111111114, 1888.1777777777777, 2106.0444444444447])}, 
        'R_e': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1634.0, 1960.8]), 
                'above_ground_residue_n': np.array([14.161333333333335, 14.161333333333335, 14.161333333333335]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.9048888888888884, 3.268]), 
                'n_crop_residue': np.array([1670.3111111111114, 1706.6222222222223, 1742.9333333333336])}, 
        'N_p': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335, 20.697333333333333, 27.233333333333334]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.5417777777777775, 2.5417777777777775]), 
                'n_crop_residue': np.array([1670.3111111111114, 2323.911111111111, 2977.5111111111114])}, 
        'N_s': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335, 19.24488888888889, 24.328444444444447]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.5417777777777775, 2.5417777777777775]), 
                'n_crop_residue': np.array([1670.3111111111114, 2178.666666666667, 2687.0222222222224])}, 
        'N_r': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335, 14.161333333333335, 14.161333333333335]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 3.6311111111111107, 4.720444444444444]), 
                'n_crop_residue': np.array([1670.3111111111114, 1779.2444444444445, 1888.1777777777777])}, 
        'N_e': {'C_p': np.array([3268.0, 3268.0, 3268.0]), 
                'above_ground_carbon_input': np.array([5228.8, 5228.8, 5228.8]), 
                'below_ground_carbon_input': np.array([1307.1999999999998, 1307.1999999999998, 1307.1999999999998]), 
                'above_ground_residue_n': np.array([14.161333333333335, 14.161333333333335, 14.161333333333335]), 
                'below_ground_residue_n': np.array([2.5417777777777775, 2.723333333333333, 2.9048888888888884]), 
                'n_crop_residue': np.array([1670.3111111111114, 1688.4666666666667, 1706.6222222222223])}
        }

def test_farmer_mode_output(ef_data_farmer, n_data_farmer):
    aggregator = EmissionAggregator(ef_data_farmer, n_data_farmer)
    output = aggregator.get_result()
    assert isinstance(output, dict)
    assert 'n_crop_direct' in output
    assert len(output['n_crop_direct']) == 1

def test_scientific_mode_output_structure(ef_data_scientific, n_data_scientific):
    aggregator = EmissionAggregator(ef_data_scientific, n_data_scientific, operation_mode='scientific')
    output = aggregator.get_result()
    assert isinstance(output, dict)
    assert 'P' in output
    assert len(output['P']['n_crop_direct']) == 3

def test_data_transformation(ef_data_farmer, n_data_farmer):
    aggregator = EmissionAggregator(ef_data_farmer, n_data_farmer)
    modified_ef = aggregator.prepare_ef_input_for_ec('EF_CT_P', 0.02)
    modified_n = aggregator.prepare_n_input_for_ec('C_p', 3300)
    assert modified_ef['EF'] == 0.02
    assert modified_n['n_crop_residue'] == 3300
