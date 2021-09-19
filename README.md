# From GEE to NPY
#### A GEE python-api script for downloading parcel-level Sentinel-1 / Sentinel-2 time series as NumPy
Returns array of size ```T x C x N ```
* T --> number of acquisitions
* C --> number of channels/bands
* N --> number of pixels within parcel


### Setup

Install earthengine-api using
```
pip install earthengine-api
```

Follow instructions [here](https://developers.google.com/earth-engine/guides/python_install) to authenticate

### General processing workflow
* filter collection by aoi, date, cloud-cover (for Sentinel-2), bands (10 S2 bands @10-20m, 2 S1 bands VV-VH)
* alternatively filter by footprint ID (eg granule ID for S2 or orbit number for S1)
* optionally pre-compute NDVI and add to bands
* apply speckle filter (S1 only). Options --> ['mean', 'median', 'temporal']
* co-register (align S1 with S2 pixels)
* normalize (min-max @ 2nd and 98th percentile)
* overlap analysis --> discard no data, repeating observations from overlapping scenes, incomplete image coverage
* save time series array as .npy per parcel
* save dates of acquisition + parcel label in separate files

### Example

Requirements
* packages : earthengine-api + shapely + tqdm  
* input parcel : geojson file containing parcel geometry with crop label column e.g. 'CODE_GROUP' and crop ID column e.g. 'ID_PARCEL'


```python

# Sentinel-1 
get_data.py --rpg_file sample_farm.geojson, --label_names ['CODE_GROUP'] --id_field ID_PARCEL --output_dir C:/downloads/s1_data --col_id COPERNICUS/S1_GRD --start_date 2021-01-01 --end_date 2021-01-31 --speckle_filter mean --footprint_id [154]

# Sentinel-2
get_data.py --rpg_file sample_farm.geojson, --label_names ['CODE_GROUP'] --id_field ID_PARCEL --output_dir C:/downloads/s2_data --col_id COPERNICUS/S2_SR  --footprint_id ["30UVU"] --start_date 2021-01-01 --end_date 2021-01-31 
```

### Notes
Footprint argument is set to None by default. However to avoid using partly covered scenes when one can have full Sentinel-1/2 scenes, 
pre-run *Example_findFootprint.ipynb*

<img src="img/sample_footprint.jpg" alt="sample S1/S2 footprints" width="500">


### Contributor
* [Dr. Charlotte Pelletier](https://sites.google.com/site/charpelletier)

### Credits
* Multi-temporal despeckling from [WeiyingZhao](https://github.com/WeiyingZhao/Multitemporal-Sentinel-1-images-denoising-and-downloading-via-GEE)
* Parcel data preprocessing from [VSainteuf](https://github.com/VSainteuf/pytorch-psetae/tree/master/preprocessing)
* Sample parcels obtained from [IGN Registre parcellaire graphique (RPG)](https://www.data.gouv.fr/fr/datasets/registre-parcellaire-graphique-rpg-contours-des-parcelles-et-ilots-culturaux-et-leur-groupe-de-cultures-majoritaire/) 
