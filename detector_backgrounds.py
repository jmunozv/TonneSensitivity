# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units

# Specific TONNE stuff
from detector_dimensions import get_dimensions
from material_activities import get_activities



#####################################################################
def get_background_level(det_name: str,
                         bkgnd_level: str) -> pd.DataFrame:
    '''
    It returns the detector background levels for every component and isotope
    as a dictionary.
    In principle, only 'READOUT_PLANES', 'CATHODE', 'FIELD_CAGE' and 'INNER_SHIELDING' are considered.
    '''

    det_dim = get_dimensions(det_name)
    mat_act = get_activities(bkgnd_level)

    det_background = {
    
        'READOUT_PLANE': {
            'Tl208': det_dim['READOUT_PLANE_surface'] * 2 * mat_act['DiceBoard']['Tl208'],
            'Bi214': det_dim['READOUT_PLANE_surface'] * 2 * mat_act['DiceBoard']['Bi214']
        },
    
        'CATHODE': {
            'Tl208': det_dim['CATHODE_mass'] * mat_act['SSteel316Ti']['Tl208'],
            'Bi214': det_dim['CATHODE_mass'] * mat_act['SSteel316Ti']['Bi214']
        },

        'FIELD_CAGE': {
            'Tl208': det_dim['FIELD_CAGE_mass'] * mat_act['Teflon']['Tl208'],
            'Bi214': det_dim['FIELD_CAGE_mass'] * mat_act['Teflon']['Bi214']
        },
        
        'INNER_SHIELDING': {
            'Tl208': det_dim['ICS_mass'] * mat_act['Copper']['Tl208'],
            'Bi214': det_dim['ICS_mass'] * mat_act['Copper']['Bi214']
        }
    }

    det_background_df = pd.DataFrame(det_background).T
    det_background_df /= units.Bq
    det_background_df.index.names = ['source']

    return det_background_df
