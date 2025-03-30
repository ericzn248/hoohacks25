import xarray as xr

ds = xr.open_dataset('final_data\matched_currents_and_winds000.nc')

import numpy as np
import matplotlib.pyplot as plt

import xarray as xr
import numpy as np

# Step 1: Build mask where BOTH uo_interp AND u10 are not NaN
valid_mask = (~np.isnan(ds['uo_interp'])) & (~np.isnan(ds['u10']))

# Step 2: Apply mask to variables
uo_clean = ds['uo_interp'].where(valid_mask)
vo_clean = ds['vo_interp'].where(valid_mask)
u10_clean = ds['u10'].where(valid_mask)
v10_clean = ds['v10'].where(valid_mask)

# Optional: Calculate current speed
current_speed = np.sqrt(uo_clean**2 + vo_clean**2)

# Step 3: Create a cleaned dataset
cleaned_ds = xr.Dataset({
    'u10': u10_clean,
    'v10': v10_clean,
    'uo_interp': uo_clean,
    'vo_interp': vo_clean,
    'current_speed': current_speed
})

# Step 4: Drop all lat/lon rows/columns that are fully NaN
cleaned_ds = cleaned_ds.dropna(dim='latitude', how='all')
cleaned_ds = cleaned_ds.dropna(dim='longitude', how='all')
uo_clean = cleaned_ds['uo_interp']
print(uo_clean.shape)

# Step 5: Save the cleaned dataset
cleaned_ds.to_netcdf("final_data/cleaned_matched_currents_and_winds.nc")
print(" Cleaned dataset saved!")
