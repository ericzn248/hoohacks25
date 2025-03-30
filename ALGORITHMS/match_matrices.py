import xarray as xr
import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

forecast_hour = "000"
run_hour = "00"
file_name_gfs = f"gfs.t{run_hour}z.pgrb2.0p25.f{forecast_hour}"
file_name_rtofs = f"rtofs_glo_2ds_forecast_3hrly_prog{forecast_hour}.nc"


# Load wind (GFS) dataset
gfs = xr.open_dataset(f"gfs_data\{file_name_gfs}", engine="cfgrib", filter_by_keys={'typeOfLevel': 'heightAboveGround', 'level': 10}, decode_timedelta=False)
u10 = gfs['u10']
v10 = gfs['v10']
lat_wind = u10.latitude.values
print("wint lat values", lat_wind.size)
lon_wind = u10.longitude.values
print("wind lon values", lon_wind.size)

# Load current (RTOFS) dataset
rtofs = xr.open_dataset(f"rtofs_data\{file_name_rtofs}")
uo = rtofs['u_velocity']
vo = rtofs['v_velocity']
lat_curr = rtofs['Latitude'].values
print("current lat values", lat_curr.size)
lon_curr = rtofs['Longitude'].values
print("current Lon values", lon_curr.size)
print("loaded in values")
# Create meshgrids of GFS and RTOFS
lon_wind_grid, lat_wind_grid = np.meshgrid(lon_wind, lat_wind)   # (721, 1440)
lon_curr_grid, lat_curr_grid = lon_curr, lat_curr   # (3298, 4500)
print("created meshgrids")

# Flatten current grid and create KDTree for fast lookup
curr_points = np.column_stack([lat_curr_grid.ravel(), lon_curr_grid.ravel()])
tree = cKDTree(curr_points)
print("created tree")

# Flatten wind grid and query nearest neighbors
wind_points = np.column_stack([lat_wind_grid.ravel(), lon_wind_grid.ravel()])
_, indices = tree.query(wind_points)

# Map currents to wind grid
uo_interp = uo.values.ravel()[indices].reshape(721, 1440)
vo_interp = vo.values.ravel()[indices].reshape(721, 1440)



uo_da = xr.DataArray(
    data=uo_interp,
    coords={"latitude": lat_wind, "longitude": lon_wind},
    dims=["latitude", "longitude"],
    name="uo_interp"
)

vo_da = xr.DataArray(
    data=vo_interp,
    coords={"latitude": lat_wind, "longitude": lon_wind},
    dims=["latitude", "longitude"],
    name="vo_interp"
)
current_speed = np.sqrt(uo_da**2 + vo_da**2)


# Plot the surface current speed
print("[*] Plotting surface current magnitude...")
plt.figure(figsize=(12, 6))
current_speed = current_speed.squeeze()
current_speed.plot(cmap='viridis')
print(current_speed.shape) 

plt.title(f"Surface Ocean Current Speed (m/s) on 3/28/25 Forecast Hour {forecast_hour}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()
