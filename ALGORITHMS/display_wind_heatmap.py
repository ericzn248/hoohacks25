import os
import requests
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# -------- CONFIGURATION -------- #
# Specify date and run hour
date_str = "20250329"   # YYYYMMDD format
run_hour = "00"         # "00", "06", "12", or "18"
forecast_hour = "000"   # Forecast lead time in hours

# Construct URL
base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
file_name = f"gfs.t{run_hour}z.pgrb2.0p25.f{forecast_hour}"
full_url = f"{base_url}/gfs.{date_str}/{run_hour}/atmos/{file_name}"

# Destination path
output_dir = "gfs_data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, file_name)

# -------- DOWNLOAD FILE -------- #
def download_file(url, path):
    if os.path.exists(path):
        print(f"[✓] File already exists: {path}")
        return
    print(f"[*] Downloading {url} ...")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[✓] Download complete: {path}")
    else:
        raise Exception(f"Failed to download file (status {r.status_code})")

download_file(full_url, output_path)

# -------- READ WIND DATA -------- #
print("[*] Reading wind data...")
ds = xr.open_dataset(output_path, engine='cfgrib',
                     filter_by_keys={'typeOfLevel': 'heightAboveGround', 'level': 10}, decode_timedelta=False)

print(ds)
# Extract wind components
u10 = ds['u10']
v10 = ds['v10']

# Compute wind speed magnitude
wind_speed = np.sqrt(u10**2 + v10**2)

# -------- PLOT -------- #
print("[*] Plotting wind speed...")
plt.figure(figsize=(10, 6))
#wind_speed.isel(time=0).plot(cmap='viridis')
print(wind_speed.shape)
wind_speed.squeeze().plot(cmap='viridis')
plt.title("10-meter Wind Speed (m/s)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()
