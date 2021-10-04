import os
from dbfread import DBF
import pandas as pd
import numpy as np
import pysal as ps
import rasterio

def SDR_BugFix(FilePath_BaU, FilePath_NBS, Region):
    """
    FilePath_BaU: SDR model output directory for BaU scenario
    FilePath_NBS: SDR model output directory for NBS scenario
    Region: Analysis region suffix
    """

    # Open SDR - BaU
    SDR_BaU_Tif = rasterio.open(os.path.join(FilePath_BaU,'sed_export_' + Region + '.tif'))
    SDR_BaU     = SDR_BaU_Tif.read(1)
    SDR_BaU_Tif.close()

    # Open SDR - NBS
    SDR_NBS_Tif = rasterio.open(os.path.join(FilePath_NBS,'sed_export_' + Region + '.tif'))
    NoValue     = SDR_NBS_Tif.nodata
    SDR_NBS     = SDR_NBS_Tif.read(1)
    Param       = {'height': SDR_NBS_Tif.shape[0],
                   'width': SDR_NBS_Tif.shape[1],
                   'crs': SDR_NBS_Tif.crs,
                   'transform': SDR_NBS_Tif.transform}
    SDR_NBS_Tif.close()

    # Correct
    Posi = SDR_BaU < SDR_NBS
    SDR_NBS[Posi] = SDR_BaU[Posi]

    # Save Results
    with rasterio.open(
        os.path.join(FilePath_NBS,'sed_export_' + Region + '.tif'),'w',
        driver='GTiff',
        height= Param['height'],
        width=Param['width'],
        count=1,
        dtype=SDR_NBS.dtype,
        crs=Param['crs'],
        transform=Param['transform'],
        nodata=NoValue
    ) as dst:
        dst.write(SDR_NBS, 1)

    # ------------------------------------------------------------------------------------------------------------------
    # Zonal Statistics
    # ------------------------------------------------------------------------------------------------------------------
    New_Export = np.sum(SDR_NBS[SDR_NBS != NoValue])

    # ------------------------------------------------------------------------------------------------------------------
    # Change DBF
    # ------------------------------------------------------------------------------------------------------------------
    # Open DBF
    FileName_DBF    = 'watershed_results_sdr_' + Region + '.dbf'
    Table_DBF       = DBF(os.path.join(FilePath_NBS,FileName_DBF))
    Table_PD        = pd.DataFrame(iter(Table_DBF))

    # Change sed_export Data - DBF
    Table_PD['sed_export'] = New_Export

    # adaptation of the function `df2dbf` to write your resulting dbf file
    type2spec = {int: ('N', 20, 0),
                 np.int64: ('N', 20, 0),
                 float: ('N', 36, 15),
                 np.float64: ('N', 36, 15),
                 np.float32: ('N', 36, 15),
                 str: ('C', 14, 0)}

    types = [type(Table_PD[i].iloc[0]) for i in Table_PD.columns]
    specs = [type2spec[t] for t in types]

    # Save Dbf
    db = ps.open(os.path.join(FilePath_NBS,FileName_DBF), 'w')
    db.header = list(Table_PD.columns)
    db.field_spec = specs
    for i, row in Table_PD.T.iteritems():
        db.write(row)
    db.close()