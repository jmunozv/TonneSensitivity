# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units

# Specific TONNE stuff
from detector_dimensions import get_dimensions

from initial_activities import get_radiogenic_activities
from initial_activities import get_radon_activity
from initial_activities import get_muon_flux
from initial_activities import get_muon_flux_error

from muons.xe137_normalization import xe137_normalization
    

#####################################################################
def get_radiogenic_background_level(det_name               : str,
                                    radiogenic_bkgnd_level : str
                                   )                      -> pd.DataFrame:
    '''
    It returns the detector background levels for every component and isotope
    as a dictionary.
    In principle, only 'READOUT_PLANES', 'CATHODE', 'FIELD_CAGE' and 'INNER_SHIELDING' are considered.
    '''

    det_dim = get_dimensions(det_name)
    
    radiogenic_act = get_radiogenic_activities(radiogenic_bkgnd_level)

    det_background = {
    
        'READOUT_PLANE': {
            'Tl208': det_dim['READOUT_PLANE_surface'] * 2 * radiogenic_act['DiceBoard']['Tl208'],
            'Bi214': det_dim['READOUT_PLANE_surface'] * 2 * radiogenic_act['DiceBoard']['Bi214']
        },
    
#        'CATHODE': {
#            'Tl208': det_dim['CATHODE_mass'] * radiogenic_act['SSteel316Ti']['Tl208'],
#            'Bi214': det_dim['CATHODE_mass'] * radiogenic_act['SSteel316Ti']['Bi214']
#        },

        'FIELD_CAGE': {
            'Tl208': det_dim['FIELD_CAGE_mass'] * radiogenic_act['Teflon']['Tl208'],
            'Bi214': det_dim['FIELD_CAGE_mass'] * radiogenic_act['Teflon']['Bi214']
        },
        
        'INNER_SHIELDING': {
            'Tl208': det_dim['ICS_mass'] * radiogenic_act['Copper']['Tl208'],
            'Bi214': det_dim['ICS_mass'] * radiogenic_act['Copper']['Bi214']
        }
    }

    det_background_df = pd.DataFrame(det_background).T
    det_background_df /= units.Bq
    det_background_df.index.names = ['source']

    return det_background_df



#####################################################################
def get_radon_background_level(det_name          : str,
                               radon_bkgnd_level : str
                              )                 -> float:
    '''
    It returns the detector background level expected from the radon contamination
    In principle, only 'READOUT_PLANES', 'CATHODE', 'FIELD_CAGE' and 'INNER_SHIELDING' are considered.
    '''

    radon_act = get_radon_activity(radon_bkgnd_level)

    # If 'optimistic' radon activity comes as an absolute background level
    if (radon_bkgnd_level == 'optimistic'):
        radon_background = radon_act
    
    # Any other case, radon activity comes as an activity per surface unit
    else:
        det_dim = get_dimensions(det_name)
        tot_surface = det_dim['READOUT_PLANE_surface'] * 2 + \
                      math.pi * det_dim['ACTIVE_diam'] * det_dim['ACTIVE_length']
        radon_background = tot_surface * radon_act

    return radon_background



#####################################################################
def get_muon_background_level(det_name    : str,
                              hosting_lab : str
                             )           -> float:

    det_dim = get_dimensions(det_name)
    muon_surface = det_dim['MUON_surface']
    
    
    muon_flux       = get_muon_flux(hosting_lab)
    muon_flux_error = get_muon_flux_error(hosting_lab)

    generate_muon_config_file(det_name, hosting_lab, muon_flux, muon_flux_error, muon_surface)
    
    Xe137_background = xe137_normalization(['dummy', 'muons.conf'], suppress_df = True)
    
    return Xe137_background



#####################################################################
def generate_muon_config_file(det_name        : str,
                              hosting_lab     : str,
                              muon_flux       : float,
                              muon_flux_error : float,
                              muon_surface    : float
                             )               -> None:

    heading_text = f"### Muons config file for {det_name} in {hosting_lab} ###"

    # The flux & Xe137_activation & output file names
    # Num simulated muons
    if (hosting_lab == 'LSC'):
        flux_file_name = './muons/lngs_100Mmuons.h5'
        acti_file_name = './muons/Xe137Count_sim87799000muons.h5'
        out_file_name  = './muons/lsc_xe137_test.h5'
        num_muons      = 87799000
    elif (hosting_lab == 'LNGS'):
        flux_file_name = './muons/lngs_100Mmuons.h5'
        acti_file_name = './muons/Xe137Count_sim87799000muons.h5'
        out_file_name  = './muons/lngs_xe137_test.h5'
        num_muons      = 87799000
    elif (hosting_lab == 'SNOLAB'):
        flux_file_name = './muons/snolab_100Mmuons.h5'
        acti_file_name = './muons/Xe137Count_sim87799000muons.h5'
        out_file_name  = './muons/snolab_xe137_test.h5'
        num_muons      = 87799000

    # Bins set
    bins_set = "1, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000"
    
    # File content
    file_text = f'''{heading_text}
flux_file = "{flux_file_name}"
acti_file = "{acti_file_name}"
file_out  = "{out_file_name}"

n_simulated_muons = {num_muons}

bin_edges = {bins_set}

lab_flux     = {muon_flux * units.cm2 * units.second}
lab_flux_err = {muon_flux_error * units.cm2 * units.second}

gen_area     = {muon_surface / units.cm2}
    '''
    
    print(file_text)

    # Writing 'muons.conf' file
    muons_conf_file = open('muons.conf', 'w')
    muons_conf_file.write(file_text)
    muons_conf_file.close()

    