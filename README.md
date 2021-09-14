# From GEE to NPY
#### A GEE python-api script for downloading parcel-level Sentinel-1 and Sentinel-2 time series

### Setup

Install earthengine-api using
```
pip install earthengine-api
```

Follow instructions [here](https://developers.google.com/earth-engine/guides/python_install) to authenticate


### Example
Download Sentinel-2 time series from January - December 2020

Requirements
* geojson file containing parcel geometry with label column e.g. 'CODE_GROUP'
```python
import ee

# initialize 
ee.Authenticate()
ee.Initialize()

# get data
prepare_dataset.py --

```

### Acknowledgements
* Multi-temporal despeckling from [WeiyingZhao](https://github.com/WeiyingZhao/Multitemporal-Sentinel-1-images-denoising-and-downloading-via-GEE)
* Parcel data preprocessing from [VSainteuf](https://github.com/VSainteuf/pytorch-psetae/tree/master/preprocessing)
* Sample parcels obtained from [IGN Registre parcellaire graphique (RPG)](https://www.data.gouv.fr/fr/datasets/registre-parcellaire-graphique-rpg-contours-des-parcelles-et-ilots-culturaux-et-leur-groupe-de-cultures-majoritaire/) 
