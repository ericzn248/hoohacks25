import xarray as xr

ds = xr.open_dataset('final_data\matched_currents_and_winds000.nc')

lats = ds.latitude.values
lons = ds.longitude.values
uo = ds['uo_interp'].values
vo = ds['vo_interp'].values

for i in range(len(lats)):
    for j in range(len(lons)):
        lat = lats[i]
        lon = lons[j]
        uo_val = uo[i, j]
        vo_val = vo[i, j]
        print(f"Lat: {lat:.2f}, Lon: {lon:.2f} → uo: {uo_val:.3f}, vo: {vo_val:.3f}")