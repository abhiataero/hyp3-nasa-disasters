set ppath="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" 
set mdcspath=C:\Users\hjkristenson\PycharmProjects\hyp3-nasa-disasters\image_server\nasa_disasters
set gdbwks=C:\Users\ASF\Documents\COVID19\Disasters\Esri\MosaicDatasets\missouri_disasters_mosaics.gdb

REM ---------- Using ACS File -------------------------

%ppath% %mdcspath%\scripts\MDCS.py -i:%mdcspath%\Parameter\Config\disasters_mosaics_rgb.xml -m:%gdbwks%\rgb -s:C:\Users\ASF\Documents\COVID19\Disasters\FloodAreas\NASA_Disasters_AWS.acs\Missouri_UTM\ -p:C:\Users\ASF\Documents\COVID19\Disasters\Esri\MosaicDatasets\PixelCache\$cachelocation -p:USE_PIXEL_CACHE$pixelcache -c:CM+AF+AR+BF+BB+SP+CC+CV
REM %ppath% %mdcspath%\scripts\MDCS.py -i:%mdcspath%\Parameter\Config\disasters_mosaics_comp.xml -m:%gdbwks%\sar_comp -s:%gdbwks%\sar_s1 -p:CompositeVV_VH_32.art.xml$art -c:CM+AR+UpdateTagField+UpdateNameField+BB+SP+CC+SE

