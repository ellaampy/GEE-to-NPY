import ee
import os
import numpy as np
import geojson, json
from tqdm import tqdm
from shapely.geometry import Polygon
import time
from datetime import datetime
from utils import *


ee.Authenticate()
ee.Initialize()


def prepare_dataset(rpg_file, label_names, id_field, output_dir, col_id, start_date, end_date, num_per_month, cloud_cover, addNDVI, orbit, speckle_filter, kernel_size):
    np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)
    start = datetime.now()

    # prepare output directory
    prepare_output(output_dir)

    # get parcel geometries & labels
    polygons, lab_rpg = parse_rpg(rpg_file, label_names=label_names, id_field = ID_field)

    # dict of global metadata to store parcel dates/labels
    dates = {k:[] for k in list(polygons.keys())}
    labels = dict([(l, {}) for l in lab_rpg.keys()])

    # counter for ignored parcels
    ignored = 0

    # iterate parcels
    for parcel_id, geometry in tqdm(polygons.items()):
        
        # get collection
        geometry = ee.Geometry.Polygon(geometry)
        collection = get_collection(geometry, col_id, start_date, end_date, num_per_month, cloud_cover, addNDVI, orbit, speckle_filter, kernel_size)

        # global normalize using 2nd & 98th percentile
        collection = collection.map(normalize)

        # check for incomplete and overlapping footprints
        collection = collection.map(lambda img: img.set('temporal', ee.Image(img).reduceRegion(reducer = ee.Reducer.toList(), geometry= geometry, scale=10).values()))

        # iterate collection and return array of TxCxN. length of time series X number of channels X number of pixels in parcel
        try:
            # query pre-selected collection & make numpy array            
            np_all_dates = np.array(collection.aggregate_array('temporal').getInfo())
            assert np_all_dates.shape[-1] > 0 
            
        except:
            print('Error in parcel --------------------> {}'.format(parcel_id))
            with open(os.path.join(output_dir, 'META', 'ignored_parcels.json'), 'a+') as file:
                file.write(json.dumps(int(parcel_id))+'\n')
            ignored += 1
            
        else:
            # create date metadata
            date_series = collection.aggregate_array('doa').getInfo()
            dates[str(parcel_id)] = date_series

            # save lABELS
            for l in labels.keys():
                labels[l][parcel_id] = int(lab_rpg[l][parcel_id])
            
            # save .npy 
            np.save(os.path.join(output_dir, 'DATA', str(parcel_id)), np_all_dates)


        # save global metadata (parcel dates and labels)
        with open(os.path.join(output_dir, 'META', 'labels.json'), 'w') as file:
            file.write(json.dumps(labels, indent=4))

        with open(os.path.join(output_dir, 'META', 'dates.json'), 'w') as file:
            file.write(json.dumps(dates, indent=4))


    # get processing time
    end = datetime.now()
    print('total ignored pixels', ignored)
    print(f"\n processing time -> {end - start}")

    
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    
    args = parse_args()
    prepare_dataset(args.rpg_file, args.label_names, args.id_field, args.output_dir, args.col_id, args.start_date, args.end_date, args.num_per_month, args.cloud_cover, args.addNDVI, args.orbit, args.speckle_filter, args.kernel_size)


