import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import xarray as xr
import glob
import sys
import math


def get_data_from_dat_file(file_path, height_levels = 1540):
    df_topex = pd.read_csv(file_path, header=None)

    # Import Time
    times = df_topex.iloc[2::7].reset_index(drop=True).rename(columns  = {0: "Times"})
    # Last Value is "close file" so this needs too be dropped.
    times.drop(times.tail(1).index,inplace=True)
    try:
        times['Times'] = times['Times'].apply(lambda x: datetime.strptime(x[1:], "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        print(f"{file_path} doesn't work")
        sys.exit()
    times = times.T
    
    valueHex_df = df_topex.iloc[7::7].reset_index(drop=True)
    value_list = []
    for testHex in valueHex_df[0]:
        height_list = np.zeros(height_levels)
        good_value = None
        for i in range(0,height_levels-1):
            #h = testHex[5*(i-1)+1:(5*(i-1)+6)]
            h = testHex[i*5:i*5+5]
            w = int(h,16)
            if good_value is None:
                good_value = w

            if w > 10000+good_value:
                w = 0 #None  #1000 + math.log(w)
            else:
                good_value = w

            if w > 0:
                w = math.log(w)

            height_list[i] = w
        
        value_list.append(height_list)
    value_df = pd.DataFrame(value_list).T
    
    
    da = xr.DataArray(data=value_df)#, dims=["z_id", "time"], coords=[value_df.index,times.values])
    da = xr.DataArray(
        data = value_df,
        coords={
            "z_id": ("z_id", np.arange(0, 1540,1)),
            "time": ("time", times.values[0,:]),
        },
        dims=["z_id","time"],
    )

    return da

def get_data_from_folder(folder_path, height_levels = 1540):
    data_files = sorted(glob.glob(f"{folder_path}/*.DAT"))
    xr_dat_list = []

    for file_name in data_files:
        xr_dat_list.append(get_data_from_dat_file(
                                file_name, 
                                height_levels))

    complete_dat = xr.concat(xr_dat_list, dim='time')
    return complete_dat