import geopandas as gpd
import json
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import earthpy.plot as ep
from skimage import io, segmentation, exposure
from rasterio.plot import reshape_as_image, reshape_as_raster


def NDVIMap(parameter, *args, **kwargs):

    title = kwargs.get('title', "NDVI")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")

    try:

        # Open the file:
        raster = rasterio.open(parameter['data'])

        red = raster.read(parameter['red'])
        nir = raster.read(parameter['nir'])
        np.seterr(divide='ignore', invalid='ignore')
        c_map = kwargs.get('cmap', 'viridis')
        minn = kwargs.get('min', -1)
        maxx = kwargs.get('max', 1)

        # Calculate ndvi
        ndvi = (nir.astype(float)-red.astype(float)) / \
            (nir.astype(float)+red.astype(float))

        fig, ax = plt.subplots(figsize=(12, 12))
        im = ax.imshow(ndvi.squeeze(), cmap=c_map, vmin=minn, vmax=maxx)
        ep.colorbar(im)
        ax.set(title=title)
        ax.set(xlabel=xlabel + '\n'+'\n' + '© Vallaris Maps')
        ax.set(ylabel=ylabel)

        return plt.show()

    except Exception as e:
        return 'error display :' + str(e)


def ExtractSAR(test, *args, **kwargs):

    title = kwargs.get('title', "Building footprint")
    # ylabel = kwargs.get('ylabel', "Row #")
    # xlabel = kwargs.get('xlabel', "Column #")
    try:
        # Load the SAR image
        dataset = rasterio.open(test)
        image = dataset.read()

        with rasterio.open(test) as src:
            img = src.read()[:,:,:]
        # Change image dimensions by reshape into long 2d array in format (nrows*ncol, nband)
        image = reshape_as_image(img)

        # Apply multi-looking to reduce speckle noise
        image = exposure.rescale_intensity(image, out_range=(0, 1))
        image = exposure.adjust_gamma(image, gamma=0.5)
        image = exposure.adjust_log(image, gain=0.6)
        image = exposure.adjust_sigmoid(image, cutoff=0.5, gain=5)

        images = image[:,:,0] #HH band

        images_test =images
        images_test[images_test <= 0.076520674] = 0
        images_test[images_test > 0.076520674] = 1

        profile = {
            'driver': 'GTiff',
            'dtype': 'int8',
            'nodata': None,
            'width': images_test.shape[1],
            'height': images_test.shape[0],
            'count': 1,
            'crs': dataset.crs,
            'transform': dataset.transform
        }

        # write the arrays to a two-band TIFF file
        with rasterio.open('Labeled.tif', 'w', **profile) as dst:
            dst.write(images_test, 1)

    except Exception as e:
        return 'error:' + str(e)