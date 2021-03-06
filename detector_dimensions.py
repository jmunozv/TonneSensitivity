# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units



#####################################################################
### Dictionary with relevant dimensions of all detectors considered
detector_dimensions = {

    'next_2x2': {
        'ACTIVE_diam'         :  2. * units.m,
        'ACTIVE_length'       :  2. * units.m,
        'FIELD_CAGE_thickness':  1. * units.cm,
        'ICS_thickness'       : 12. * units.cm,
        'HOLLOWS_width'       : 20. * units.cm,
        'VESSEL_thickness'    :  2. * units.cm
    },

    'next_3x3': {
        'ACTIVE_diam'         :  3. * units.m,
        'ACTIVE_length'       :  3. * units.m,
        'FIELD_CAGE_thickness':  1. * units.cm,
        'ICS_thickness'       : 12. * units.cm,
        'HOLLOWS_width'       : 20. * units.cm,
        'VESSEL_thickness'    :  2. * units.cm
    },

    'next_hd': {
        'ACTIVE_diam'         :  2.6 * units.m,
        'ACTIVE_length'       :  2.6 * units.m,
        'FIELD_CAGE_thickness':  1.  * units.cm,
        'ICS_thickness'       : 12.  * units.cm,
        'HOLLOWS_width'       : 20.  * units.cm,
        'VESSEL_thickness'    :  2.  * units.cm
    }
}

# Dimensions "hard-wired" in the code
CATHODE_THICKNESS = 0.25 * units.mm
ANODE_THICKNESS   = 1.5  * units.cm
READOUT_GAP       = 5.0  * units.mm
WATER_THICKNESS   = 3.0  * units.m
TANK_THICKNESS    = 1.0  * units.cm
MUON_EXTRA_RAD    = 50.0 * units.cm


#####################################################################
### Material densities
Xe_density          =   89. * units.kg / units.m3  # 15 bar & 300 kelvin
HDPE_density        =  970. * units.kg / units.m3
Teflon_density      = 2200. * units.kg / units.m3
Copper_density      = 8960. * units.kg / units.m3
SSteel316Ti_density = 7990. * units.kg / units.m3


#####################################################################
def get_dimensions(det_name: str) -> Dict[str, float]:
    '''
    Based on the relevant dimensions of any detector,
    it computes all the dimensions needed and returns them as a dictionary
    '''
    dimensions = detector_dimensions[det_name]

    ### Adding 'ACTIVE' derived dimensions
    dimensions['ACTIVE_surface'] = (dimensions['ACTIVE_diam']/2)**2 * math.pi * 2 + \
                                   math.pi * dimensions['ACTIVE_diam'] * dimensions['ACTIVE_length']

    dimensions['ACTIVE_volume'] = (dimensions['ACTIVE_diam']/2)**2 * \
                                  math.pi * dimensions['ACTIVE_length']

    dimensions['ACTIVE_mass']   = dimensions['ACTIVE_volume'] * Xe_density


    ### Adding 'READOUT PLANES' derived dimensions
    dimensions['READOUT_PLANE_surface'] = (dimensions['ACTIVE_diam']/2)**2 * math.pi


    ### Adding 'CATHODE' derived dimensions
    dimensions['CATHODE_volume'] = dimensions['READOUT_PLANE_surface'] * CATHODE_THICKNESS
    dimensions['CATHODE_mass']   = dimensions['CATHODE_volume'] * SSteel316Ti_density


    ### Adding 'FIELD CAGE' derived dimensions
    dimensions['FIELD_CAGE_innerRad'] = dimensions['ACTIVE_diam']/2.
    dimensions['FIELD_CAGE_outerRad'] = dimensions['FIELD_CAGE_innerRad'] + \
                                        dimensions['FIELD_CAGE_thickness']
    dimensions['FIELD_CAGE_length']   = dimensions['ACTIVE_length']

    dimensions['FIELD_CAGE_volume']   = (dimensions['FIELD_CAGE_outerRad']**2 - \
                                         dimensions['FIELD_CAGE_innerRad']**2) * \
                                        dimensions['FIELD_CAGE_length'] * math.pi

    dimensions['FIELD_CAGE_mass']     = dimensions['FIELD_CAGE_volume'] * Teflon_density


    ### Adding 'ICS' derived dimensions
    dimensions['ICS_innerRad']    = dimensions['FIELD_CAGE_outerRad']
    dimensions['ICS_outerRad']    = dimensions['ICS_innerRad'] + \
                                    dimensions['ICS_thickness']

    dimensions['ICS_innerLength'] = dimensions['ACTIVE_length'] + \
                                    2 * ANODE_THICKNESS + 2 * READOUT_GAP
    dimensions['ICS_outerLength'] = dimensions['ICS_innerLength'] + \
                                    dimensions['ICS_thickness'] * 2.

    dimensions['ICS_innerEndcapSurf'] = dimensions['ICS_innerRad']**2 * math.pi
    dimensions['ICS_outerEndcapSurf'] = dimensions['ICS_outerRad']**2 * math.pi

    dimensions['ICS_volume']          = ((dimensions['ICS_outerRad']**2 * \
                                         dimensions['ICS_outerLength']) -
                                         (dimensions['ICS_innerRad']**2 * \
                                         dimensions['ICS_innerLength'])) * math.pi

    dimensions['ICS_mass']            = dimensions['ICS_volume'] * Copper_density


    ### Adding 'VESSEL' derived dimensions
    dimensions['VESSEL_innerRad']    = dimensions['ICS_outerRad']
    dimensions['VESSEL_outerRad']    = dimensions['VESSEL_innerRad'] + \
                                       dimensions['VESSEL_thickness']

    dimensions['VESSEL_innerLength'] = dimensions['ICS_outerLength'] + \
                                       dimensions['HOLLOWS_width'] * 2.
    dimensions['VESSEL_outerLength'] = dimensions['VESSEL_innerLength'] + \
                                       dimensions['VESSEL_thickness'] * 2.
    
    dimensions['VESSEL_volume']      = ((dimensions['VESSEL_outerRad']**2 * \
                                        dimensions['VESSEL_outerLength']) -
                                        (dimensions['VESSEL_innerRad']**2 * \
                                        dimensions['VESSEL_innerLength'])) * math.pi

    dimensions['VESSEL_mass']        = dimensions['VESSEL_volume'] * SSteel316Ti_density


    ### Adding 'TANK' derived dimensions
    detector_diam = dimensions['ACTIVE_diam'] + 2 * dimensions['FIELD_CAGE_thickness'] + \
                    2 * dimensions['ICS_thickness'] + 2 * dimensions['VESSEL_thickness']

    detector_length = dimensions['ACTIVE_length'] + 2 * ANODE_THICKNESS + 2 * READOUT_GAP + \
                      2 * dimensions['ICS_thickness'] + 2 * dimensions['HOLLOWS_width'] + \
                      2 * dimensions['VESSEL_thickness']
    
    dimensions['TANK_outerDiam']  = max(detector_length, detector_diam) + \
                                    2. * WATER_THICKNESS + 2. * TANK_THICKNESS
    dimensions['TANK_topSurface'] = (dimensions['TANK_outerDiam']/2)**2 * math.pi
    dimensions['MUON_surface']   = (dimensions['TANK_outerDiam'] + 2 * MUON_EXTRA_RAD)**2

    return dimensions



#####################################################################
def print_dimensions(det_name: str) -> None:
    '''
    It prints to screen all detector dimensions.
    '''
    dimensions = get_dimensions(det_name)

    print(f"*** DETECTOR '{det_name}' DIMENSIONS ***")
    
    print("\n* ACTIVE")
    print('  ACTIVE Diameter = {} cm'        .format(dimensions['ACTIVE_diam']/units.cm))
    print('  ACTIVE Length   = {} cm'        .format(dimensions['ACTIVE_length']/units.cm))
    print('  ACTIVE Surface  = {:8.3e} cm**2'.format(dimensions['ACTIVE_surface']/units.cm2))
    print('  ACTIVE Volume   = {:8.3e} cm**3'.format(dimensions['ACTIVE_volume']/units.cm3))
    print('  ACTIVE mass     = {:8.3e} kg'   .format(dimensions['ACTIVE_mass']/units.kg))
    
    print("\n* READOUT_PLANE")
    print('  READOUT_PLANE Surface (each one) = {:8.3e} cm**2'.format(dimensions['READOUT_PLANE_surface']/units.cm2))

    print("\n* CATHODE")
    print('  CATHODE Volume = {:8.3e} cm**3'.format(dimensions['CATHODE_volume']/units.cm3))
    print('  CATHODE Mass   = {:8.3e} kg'   .format(dimensions['CATHODE_mass']/units.kg))

    print("\n* FIELD_CAGE")
    print('  FIELD_CAGE Thickness = {} cm'        .format(dimensions['FIELD_CAGE_thickness']/units.cm))
    print('  FIELD_CAGE Inner Rad = {:8.3e} cm'   .format(dimensions['FIELD_CAGE_innerRad']/units.cm))
    print('  FIELD_CAGE Outer Rad = {:8.3e} cm'   .format(dimensions['FIELD_CAGE_outerRad']/units.cm))
    print('  FIELD_CAGE Length    = {:8.3e} cm'   .format(dimensions['FIELD_CAGE_length']/units.cm))
    print('  FIELD_CAGE Volume    = {:8.3e} cm**3'.format(dimensions['FIELD_CAGE_volume']/units.cm3))
    print('  FIELD_CAGE Mass      = {:8.3e} kg'   .format(dimensions['FIELD_CAGE_mass']/units.kg))

    print("\n* INNER_SHIELDING")
    print('  ICS Thickness         = {} cm'        .format(dimensions['ICS_thickness']/units.cm))
    print('  ICS Inner Rad         = {:8.3e} cm'   .format(dimensions['ICS_innerRad']/units.cm))
    print('  ICS Outer Rad         = {:8.3e} cm'   .format(dimensions['ICS_outerRad']/units.cm))
    print('  ICS Inner Length      = {:8.3e} cm'   .format(dimensions['ICS_innerLength']/units.cm))
    print('  ICS Outer Length      = {:8.3e} cm'   .format(dimensions['ICS_outerLength']/units.cm))
    print('  ICS Inner EndCap Surf = {:8.3e} cm**2'.format(dimensions['ICS_innerEndcapSurf']/units.cm2))
    print('  ICS Outer EndCap Surf = {:8.3e} cm**2'.format(dimensions['ICS_outerEndcapSurf']/units.cm2))
    print('  ICS Volume            = {:8.3e} cm**3'.format(dimensions['ICS_volume']/units.cm3))
    print('  ICS Mass              = {:8.3e} kg'   .format(dimensions['ICS_mass']/units.kg))

#    print("\n* HOLLOWS")
#    print('  HOLLOWS Width = {} cm'.format(dimensions['HOLLOWS_width']/units.cm))

    print("\n* VESSEL")
    print('  VESSEL Thickness    = {} cm'        .format(dimensions['VESSEL_thickness']/units.cm))
    print('  VESSEL Inner Rad    = {:8.3e} cm'   .format(dimensions['VESSEL_innerRad']/units.cm))
    print('  VESSEL Outer Rad    = {:8.3e} cm'   .format(dimensions['VESSEL_outerRad']/units.cm))
    print('  VESSEL Inner Length = {:8.3e} cm'   .format(dimensions['VESSEL_innerLength']/units.cm))
    print('  VESSEL Outer Length = {:8.3e} cm'   .format(dimensions['VESSEL_outerLength']/units.cm))
    print('  VESSEL Volume       = {:8.3e} cm**3'.format(dimensions['VESSEL_volume']/units.cm3))
    print('  VESSEL Mass         = {:8.3e} kg'   .format(dimensions['VESSEL_mass']/units.kg))

    print("\n* TANK")
    print('  TANK Outer Diam     = {:8.3e} cm'   .format(dimensions['TANK_outerDiam']/units.cm))
    print('  TANK Top Surface    = {:8.3e} cm**2'.format(dimensions['TANK_topSurface']/units.cm2))
    print('  MUON Surface        = {:8.3e} cm**2'.format(dimensions['MUON_surface']/units.cm2))

    
