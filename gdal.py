from osgeo import gdal, osr

# Open the input image
input_file = 'mslp_0001.png'
input_ds = gdal.Open(input_file)

# Get the projection information for the input image
input_proj = input_ds.GetProjection()
input_srs = osr.SpatialReference()
input_srs.ImportFromEPSG(4326)

# Define the output projection
output_srs = osr.SpatialReference()
output_srs.ImportFromEPSG(3411)

# Create a transformer to convert coordinates
transform = osr.CoordinateTransformation(input_srs, output_srs)

# Get the image dimensions
cols = input_ds.RasterXSize
rows = input_ds.RasterYSize

# Perform the reprojection
output_file = 'image_polar.png'
output_ds = gdal.Warp('', input_ds, format='PNG', dstSRS=output_srs)

# Save the output image
output_ds = None


