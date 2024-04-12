# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:44:48 2023

@author: user
"""

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



transformer1 = Transformer.from_crs(32645,4326,always_xy=True)









aim=r'E:\0NDSI\cankaoshange\ck_tpbf10km1.tif'
ds = gdal.Open(aim,gdalconst.GA_ReadOnly)
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount
geotrans=ds.GetGeoTransform()

# coordarray=np.zeros((rows,cols))
colX,rowY=np.meshgrid(np.arange(1,cols+1),np.arange(1,rows+1))

coordx,coordy=Pixel2world(geotrans, rowY, colX)
coordx_WGS84=np.zeros((rows,cols))
coordy_WGS84=np.zeros((rows,cols))
for r in range(rows):
    for c in range(cols):
        cx=coordx[r,c]
        cy=coordy[r,c]
        p1 = transformer1.transform(cx,cy)
        coordx_WGS84[r,c]=p1[0]
        coordy_WGS84[r,c]=p1[1]

#输出经纬度数据
driver = gdal.GetDriverByName("GTiff")
outdata=driver.Create(r"E:\0NDSI\dem_coord\coordx_WGS84.tif",
                        cols,rows,
                        1,gdalconst.GDT_Float32)
outdata.SetGeoTransform(geotrans)
outdata.SetProjection(ds.GetProjection())
outband=outdata.GetRasterBand(1)  
outband.WriteArray(coordx_WGS84)
# outband=outdata.GetRasterBand(2)  
# outband.WriteArray(coordy)
outdata.FlushCache()
outdata = None

outdata=driver.Create(r"E:\0NDSI\dem_coord\coordy_WGS84.tif",
                        cols,rows,
                        1,gdalconst.GDT_Float32)
outdata.SetGeoTransform(geotrans)
outdata.SetProjection(ds.GetProjection())
outband=outdata.GetRasterBand(1)  
outband.WriteArray(coordy_WGS84)
# outband=outdata.GetRasterBand(2)  
# outband.WriteArray(coordy)
outdata.FlushCache()
outdata = None

print(f"rows:{rows}")
print(f"cols:{cols}")
print(f"bands:{bands}")
print(geotrans)
