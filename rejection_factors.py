# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units



#####################################################################
def get_rejection_factors(det_name: str) -> pd.DataFrame:
    '''
    It returns a DataFrame with all the existing rejection factors
    for the setector passed.
    '''

    ifile_name = f"rejection_factors.{det_name}.csv"

    factors_df = pd.read_csv(ifile_name,
                             index_col=['source', 'energyRes', 'spatialDef'],
                             comment='#')
    return factors_df
