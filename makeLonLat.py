# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal,gdalconst
import numpy as np
from pyproj import Transformer

def Pixel2world(geotransform, line, column):
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    x = column*pixelWidth + originX - pixelWidth/2
    y = line*pixelHeight + originY - pixelHeight/2
    return(x,y)



transformer1 = Transformer.from_crs(4326,32645,always_xy=True)
p1 = transformer1.transform(121,31)
print(p1)









aim=r'E:\0NDSI填补数据\3_pre-processed\geo\dem_ccy500_tp.tif'
ds = gdal.Open(aim)
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount
geotrans=ds.GetGeoTransform()

# coordarray=np.zeros((rows,cols))
colX,rowY=np.meshgrid(np.arange(1,cols+1),np.arange(1,rows+1))

coordx,coordy=Pixel2world(geotrans, rowY, colX)

#输出经纬度数据
# driver = gdal.GetDriverByName("GTiff")
# outdata=driver.Create(r"E:\0NDSI填补数据\3_pre-processed\geo\coordx_32645.tif",
#                         cols,rows,
#                         1,gdalconst.GDT_Float32)
# outdata.SetGeoTransform(geotrans)
# outdata.SetProjection(ds.GetProjection())
# outband=outdata.GetRasterBand(1)  
# outband.WriteArray(coordx)
# # outband=outdata.GetRasterBand(2)  
# # outband.WriteArray(coordy)
# outdata.FlushCache()
# outdata = None

# outdata=driver.Create(r"E:\0NDSI填补数据\3_pre-processed\geo\coordy_32645.tif",
#                         cols,rows,
#                         1,gdalconst.GDT_Float32)
# outdata.SetGeoTransform(geotrans)
# outdata.SetProjection(ds.GetProjection())
# outband=outdata.GetRasterBand(1)  
# outband.WriteArray(coordy)
# # outband=outdata.GetRasterBand(2)  
# # outband.WriteArray(coordy)
# outdata.FlushCache()
# outdata = None

print(f"rows:{rows}")
print(f"cols:{cols}")
print(f"bands:{bands}")
print(geotrans)
