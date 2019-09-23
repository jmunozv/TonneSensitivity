# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units


#####################################################################
### Dictionary with activities from the relevant detector components
material_activity = {

    ##### REFERENCE values corresponding to current activity limits / measurements
    'reference': {
        'Copper': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=960)
            'Bi214': 1.26e-3 * units.mBq / units.kg,
            'Tl208': 4.35e-4 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # Current Kapton boards extrapolating from act/unit -> act/m2 (assuming units of 10x10 cm2).
            'Bi214': 7.00 * units.mBq / units.m2,
            'Tl208': 1.04 * units.mBq / units.m2
        },
        
        'HDPE': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # From Simona provider
            'Bi214': 6.20e-2 * units.mBq / units.kg,
            'Tl208': 7.55e-3 * units.mBq / units.kg
        },
        
        'Teflon': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=959)
            'Bi214': 2.27e-2 * units.mBq / units.kg,
            'Tl208': 8.23e-3 * units.mBq / units.kg
        },
        
        'SSteel316Ti': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # From Nironit provider
            'Bi214': 4.60e-1 * units.mBq / units.kg,
            'Tl208': 4.31e-2 * units.mBq / units.kg
        }
    },

    
    ##### PROBABLE values corresponding to those expected by the time Next-Tonne is build.
    ##### Copper and Teflon (measurements from PNNL)
    ##### DiceBoards activity = Current DBs / 10.
    'probable': {
        'Copper': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=960)
            'Bi214': 1.26e-3 * units.mBq / units.kg,
            'Tl208': 4.35e-4 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            # Limits from ActivityAssumptions - V8 internal document / 10.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # Current Kapton boards extrapolating from act/unit -> act/m2 (assuming units of 10x10 cm2).
            'Bi214': 7.00e-1 * units.mBq / units.m2,
            'Tl208': 1.04e-1 * units.mBq / units.m2
        },
        
        'HDPE': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # From Simona provider
            'Bi214': 6.20e-2 * units.mBq / units.kg,
            'Tl208': 7.55e-3 * units.mBq / units.kg
        },
        
        'Teflon': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=959)
            'Bi214': 2.27e-2 * units.mBq / units.kg,
            'Tl208': 8.23e-3 * units.mBq / units.kg
        },
        
        'SSteel316Ti': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # From Nironit provider
            'Bi214': 4.60e-1 * units.mBq / units.kg,
            'Tl208': 4.31e-2 * units.mBq / units.kg
        }
    },

    
    ##### OPTIMISTIC values corresponding to the best scenario by the time Next-Tonne is build.
    ##### Copper and teflon from Current detection limits for candidate DarkSide-20K materials
    ##### (arXiv:1707.08145v1 Table 14)
    ##### DiceBoards activity = Current DBs / 20.
    'optimistic': {
        'Copper': {
            # Limits from DarkSide-20K candidate materials (arXiv:1707.08145v1 Table 14)
            'Bi214': 1.31e-4 * units.mBq / units.kg,
            'Tl208': 1.22e-5 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            # Limits from ActivityAssumptions - V8 internal document / 20.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # Current Kapton boards extrapolating from act/unit -> act/m2 (assuming units of 10x10 cm2).
            'Bi214': 3.50e-1 * units.mBq / units.m2,
            'Tl208': 5.20e-2 * units.mBq / units.m2
        },
        
        'HDPE': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # From Simona provider
            'Bi214': 6.20e-2 * units.mBq / units.kg,
            'Tl208': 7.55e-3 * units.mBq / units.kg
        },
        
        'Teflon': {
            # Limits from DarkSide-20K candidate materials (arXiv:1707.08145v1 Table 14)
            'Bi214': 1.00e-3 * units.mBq / units.kg,
            'Tl208': 3.59e-4 * units.mBq / units.kg
        },
        
        'SSteel316Ti': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # From Nironit provider
            'Bi214': 4.60e-1 * units.mBq / units.kg,
            'Tl208': 4.31e-2 * units.mBq / units.kg
        }
    }
}



#####################################################################
def get_activities(bkgnd_level: str) -> Dict[str, float]:
    '''
    it returns the material activities corresponding to the
    background level passed.
    '''
    return material_activity[bkgnd_level]



#####################################################################
def print_activities(bkgnd_level: str) -> None:
    '''
    it returns the material activities corresponding to the
    background level passed.
    '''
    activities = get_activities(bkgnd_level)

    print(f"*** '{bkgnd_level}' MATERIAL ACTIVITIES ***")

    for material in activities.keys():
        print(f"\n* {material}:")

        for isotope in activities[material].keys():
            if (material == 'DiceBoard'):
                print("    {}: {:.4} mBq/m**2".format(isotope,
                                                      activities[material][isotope] \
                                                      / units.mBq * units.m2))
            else:
                print("    {}: {:.4} mBq/kg".format(isotope,
                                                    activities[material][isotope] \
                                                    / units.mBq * units.kg))




