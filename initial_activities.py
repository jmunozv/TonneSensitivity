# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units


###############################################################################
### Dictionary with radiogenic activities from the relevant detector components
radiogenic_activity = {

    ##### REFERENCE values corresponding to current activity limits / measurements.
    'reference': {
        'Copper': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=960)
            'Bi214': 1.26e-3 * units.mBq / units.kg,
            'Tl208': 4.35e-4 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            # Limits from ActivityAssumptions - V8 internal document.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # Current Kapton boards extrapolating from act/unit -> act/m2 (assuming units of 11x11 cm2).
            'Bi214': 5.785    * units.mBq / units.m2,
            'Tl208': 8.595e-1 * units.mBq / units.m2
        },
        
        'Teflon': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=959)
            'Bi214': 2.27e-2 * units.mBq / units.kg,
            'Tl208': 8.23e-3 * units.mBq / units.kg
        },
        
#        'SSteel316Ti': {
#            # Limits from ActivityAssumptions - V8 internal document.
#            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
#            # From Nironit provider
#            'Bi214': 4.60e-1 * units.mBq / units.kg,
#            'Tl208': 4.31e-2 * units.mBq / units.kg
#        }
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
            'Bi214': 5.785e-1 * units.mBq / units.m2,
            'Tl208': 8.595e-2 * units.mBq / units.m2
        },
        
        'Teflon': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=959)
            'Bi214': 2.27e-2 * units.mBq / units.kg,
            'Tl208': 8.23e-3 * units.mBq / units.kg
        },
        
#        'SSteel316Ti': {
#            # Limits from ActivityAssumptions - V8 internal document.
#            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
#            # From Nironit provider
#            'Bi214': 4.60e-1 * units.mBq / units.kg,
#            'Tl208': 4.31e-2 * units.mBq / units.kg
#        }
    },

    
    ##### OPTIMISTIC values corresponding to the best scenario by the time Next-Tonne is build.
    ##### Copper electroformed measured by Majorana (radiopurity.org)
    ##### Teflon (measurements from PNNL)
    ##### DiceBoards activity = Current DBs / 20.
    'optimistic': {
        'Copper': {
            # Electroformed copper limits from Majorana (radiopurity.org)
            'Bi214': 9.92e-5 * units.mBq / units.kg,
            'Tl208': 4.27e-5 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            # Limits from ActivityAssumptions - V8 internal document / 20.
            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
            # Current Kapton boards extrapolating from act/unit -> act/m2 (assuming units of 10x10 cm2).
            'Bi214': 2.893e-1 * units.mBq / units.m2,
            'Tl208': 4.298e-2 * units.mBq / units.m2
        },
        
        'Teflon': {
            # Measurements from PNNL (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=959)
            'Bi214': 2.27e-2 * units.mBq / units.kg,
            'Tl208': 8.23e-3 * units.mBq / units.kg
        },
        
#        'SSteel316Ti': {
#            # Limits from ActivityAssumptions - V8 internal document.
#            # (https://next.ific.uv.es/cgi-bin/DocDB/private/ShowDocument?docid=182)
#            # From Nironit provider
#            'Bi214': 4.60e-1 * units.mBq / units.kg,
#            'Tl208': 4.31e-2 * units.mBq / units.kg
#        }
    }
}




###############################################################################
### Dictionary with radon activities
### Any detector Rn activity = NEW Rn activity, as it comes from the gas system
### Take into account that this is an absolute value.
### (https://arxiv.org/pdf/1804.00471.pdf)

radon_activity = {
    ### OPTIMISTIC
    # Rn coming from the gas system
    'optimistic':  3.11 * units.mBq,
    
    ### PESIMISTIC
    # Rn coming from materials (facing to the ACTIVE volume) degassing
    'pessimistic': 2.91 * units.mBq / units.m2
}



###############################################################################
### Dictionary with the muon flux for the different hosting labs

muon_flux = {
    ### Canfranc
    'LSC'    : 4.810e-7 / units.cm2 / units.second,
    
    ### Gran Sasso (Borexino measurement)
    'LNGS'   : 3.432e-8 / units.cm2 / units.second,

    ### SNO lab (From SNO measurements)
    'SNOLAB' : 3.31e-10 / units.cm2 / units.second
}

muon_flux_error = {
    ### Canfranc
    'LSC'    : 0.1e-7   / units.cm2 / units.second,
    
    ### Gran Sasso (Borexino measurement)
    'LNGS'   : 0.003e-8 / units.cm2 / units.second,

    ### SNO lab (From SNO measurements)
    'SNOLAB' : 0.1e-10  / units.cm2 / units.second
}



#####################################################################
def get_radiogenic_activities(radiogenic_bkgnd_level: str) -> Dict[str, float]:
    '''
    it returns the radiogenic material activities
    corresponding to the background level passed.
    '''
    return radiogenic_activity[radiogenic_bkgnd_level]



#####################################################################
def get_radon_activity(radon_bkgnd_level: str) -> float:
    '''
    it returns the radon activity corresponding to the level passed.
    '''
    return radon_activity[radon_bkgnd_level]



#####################################################################
def get_muon_flux(hosting_lab: str) -> float:
    '''
    it returns the muon flux corresponding to the hosting lab.
    '''
    return muon_flux[hosting_lab]



#####################################################################
def get_muon_flux_error(hosting_lab: str) -> float:
    '''
    it returns the muon flux error corresponding to the hosting lab.
    '''
    return muon_flux_error[hosting_lab]



#####################################################################
def print_initial_activities(radiogenic_bkgnd_level: str,
                             radon_bkgnd_level     : str,
                             hosting_lab           : str
                            ) -> None:
    '''
    It print the material activities corresponding to the corresponding levels:
    radiogenic activities : f(radiogenic_bkgnd_level)
    radon activity        : f(radon_bkgnd_level) 
    muons activity        : f(hosting_lab)
    '''
    
    ## Radiogenic activities
    radiogenic_activities = get_radiogenic_activities(radiogenic_bkgnd_level)

    print(f"*** '{radiogenic_bkgnd_level}' RADIOGENIC ACTIVITIES ***")
    for material in radiogenic_activities.keys():
        print(f"\n* {material}:")
        for isotope in radiogenic_activities[material].keys():
            if (material == 'DiceBoard'):
                print("    {}: {:8.3e} mBq/m**2".format(isotope,
                                                        radiogenic_activities[material][isotope] \
                                                        / units.mBq * units.m2))
            else:
                print("    {}: {:8.3e} mBq/kg".format(isotope,
                                                      radiogenic_activities[material][isotope] \
                                                      / units.mBq * units.kg))


    ## Radon activities
    radon_activity = get_radon_activity(radon_bkgnd_level)

    print(f"\n\n*** '{radon_bkgnd_level}' RADON ACTIVITY ***")
    if (radon_bkgnd_level == 'optimistic'):    
        print(f"\n* Radon activity: {radon_activity/units.mBq:8.3e} mBq")
    else:
        print(f"\n* Radon activity: {radon_activity/units.mBq*units.m2:8.3e} mBq/m**2")

        
    ## Muon flux
    muon_flux = get_muon_flux(hosting_lab)
    
    print(f"\n\n*** '{hosting_lab}' MUON FLUX ***")
    print(f"\n* Muon flux: {muon_flux * units.cm2 * units.second:8.3e} cm**-2 sec**-1")

