import os
import requests
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIGURATION ---------------- #
# Define the date and forecast hour of interest
date_str = "20250328"  # Format: YYYYMMDD
forecast_hour = "000"  # Forecast hour (e.g., "000" for analysis time)

# Construct the file name and URL
file_name = f"rtofs_glo_2ds_forecast_3hrly_prog{forecast_hour}.nc"
base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod"
file_url = f"{base_url}/rtofs.{date_str}/rtofs_glo_2ds_f{forecast_hour}_prog.nc"
print(file_url)
#file_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20250328/rtofs_glo_2ds_f000_prog.nc"

# Define the local directory and file path
output_dir = "rtofs_data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, file_name)

# ---------------- DOWNLOAD FILE ---------------- #
def download_file(url, path):
    headers = {'User-Agent': 'Mozilla/5.0'}
    if os.path.exists(path):
        print(f"[✓] File already exists: {path}")
        return
    print(f"[*] Downloading {url} ...")
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"[✓] Download complete: {path}")
    else:
        raise Exception(f"Failed to download file (status {response.status_code})")

# Download the NetCDF file
download_file(file_url, output_path)

# ---------------- READ AND PLOT DATA ---------------- #
print("[*] Reading ocean current data...")
ds = xr.open_dataset(output_path)
print(ds)
# Extract the eastward (uo) and northward (vo) surface current components
uo = ds['u_velocity']  # Eastward velocity at the first time step
vo = ds['v_velocity']  # Northward velocity at the first time step
print(ds['u_velocity'].attrs['units'])
# Compute the current speed magnitude
current_speed = np.sqrt(uo**2 + vo**2)

# Plot the surface current speed
print("[*] Plotting surface current magnitude...")
plt.figure(figsize=(12, 6))
current_speed = current_speed.squeeze()
current_speed.plot(cmap='viridis')
print(current_speed.shape)

plt.title(f"Surface Ocean Current Speed (m/s) on {date_str} Forecast Hour {forecast_hour}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()
