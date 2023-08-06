import os
import numpy as np


dict_vars = {'lst': ['Land surface temperature', r'$^\circ$C', 'MODIS LST', ''],
             'GDD': ['Growing degree days', r'$^\circ$C', 'Growing Degree days: computed from NOAA CPC temperature', ''],
             'cGDD': ['Cumulative growing degree days', r'$^\circ$C', 'Growing Degree days: computed from NOAA CPC temperature', ''],
             'ndvi': ['NDVI', '', 'NDVI: UMD GLAM system', 'NDVI'],
             'gcvi': ['GCVI', '', 'GCVI: UMD GLAM system', ''],
             'yearly_ndvi': ['NDVI', '', 'NDVI: UMD GLAM system', ''],
             'yearly_gcvi': ['GCVI', '', 'GCVI: UMD GLAM system', ''],
             'cNDVI': [r'$\Sigma\ NDVI$', '', ''],
             'aucNDVI': ['AUC NDVI', '', ''],
             'lai': ['Leaf area index', r'$m^2/m^2$', '', ''],
             'fpar': ['Fraction of PAR', '%', '', ''],
             'et_daily': ['Evap. anomaly', '%', '', ''],
             'esi_12wk': ['Evaporative Stress Index', '', ''],
             'esi_4wk': ['Evaporative Stress Index', '', '', 'Índice de Evapotranspiración'],
             'chirps': ['Precipitation', 'mm', 'Precipitation: CHIRPS', ''],
             'daily_precip': ['Precipitation', 'mm', 'Precipitation: CHIRPS', ''],
             'cumulative_precip': ['Precipitation', 'mm', 'Precipitation: CHIRPS', ''],
             'ncep2_min': ['Temperature (min)', r'$^\circ$C', 'Temperature: NCEP2', ''],
             'ncep2_mean': ['Temperature (mean)', r'$^\circ$C', 'Temperature: NCEP2', ''],
             'ncep2_max': ['Temperature (max)', r'$^\circ$C', 'Temperature: NCEP2', ''],
             'ncep2_precip': ['Precipitation (NCEP)', 'mm', 'Precipitation: NCEP2', ''],
             'cpc_tmin': ['Min. Temperature', r'$^\circ$C', 'Temperature: NOAA CPC', 'Temperatura Mínima'],
             'cpc_tmax': ['Max. Temperature', r'$^\circ$C', 'Temperature: NOAA CPC', 'Temperatura Máxima'],
             'cpc_precip': ['Precipitation', 'mm', 'Precipitation: NOAA CPC', ''],
             'soil_moisture_as1': ['Soil moisture (surface)', 'mm', '', 'Humedad Superficial'],
             'soil_moisture_as2': ['Soil moisture (sub-surface)', 'mm', '', '']}


def get_crop_name(crop):
    if crop == 'ww':
        return 'Winter Wheat'
    elif crop == 'sw':
        return 'Spring Wheat'
    elif crop == 'mz':
        return 'Maize'
    elif crop == 'sb':
        return 'Soybean'
    else:
        raise ValueError(f'Crop {crop} not recognized')


def sliding_mean(data_array, window=5):
    """
    This function takes an array of numbers and smoothes them out.
    Smoothing is useful for making plots a little easier to read.
    Args:
        data_array:
        window:

    Returns:

    """
    # Return without change if window size is zero
    if window == 0:
        return data_array

    data_array = np.array(data_array)
    new_list = []
    for i in range(len(data_array)):
        indices = range(max(i - window + 1, 0),
                        min(i + window + 1, len(data_array)))
        avg = 0
        for j in indices:
            avg += data_array[j]
        avg /= float(len(indices))
        new_list.append(avg)

    return np.array(new_list)

