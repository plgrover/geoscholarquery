import os
import osgeo.gdal as gdal
import osgeo.osr as osr
import osgeo.ogr as ogr




def main(path):
    shapdata = ogr.Open(path, 1)
    layer = shapdata.GetLayer() 
    for feature in layer:
        if hasgold(feature) == True:
            feature.SetField('Gold',1)   
        else:
            feature.SetField('Gold',0)   
        layer.SetFeature(feature)         

        
def hasgold(feature):
    retval = False
    commod1 = feature.GetField("commod1")
    commod2 = feature.GetField("commod2")
    commod3 = feature.GetField("commod3")
    if(commod1 != None):
        comms = commod1.split(',')
        for comm in comms:
            if(comm=='Gold'):
                retval = True
    if(commod2 != None):
        comms = commod2.split(',')
        for comm in comms:
            if(comm=='Gold'):
                retval = True
    if(commod3 != None):
        comms = commod3.split(',')
        for comm in comms:
            if(comm=='Gold'):
                retval = True

    return retval

def appendGeology


if __name__ == '__main__':
    path = r'C:\Users\pgrover\Documents\Projects\Hackathon\data\Mineral Resources Data System\mrds-f02110.shp'
    
    geopath r'C:\Users\pgrover\Documents\Projects\Hackathon\data\export\WGS84\Geology\AKStategeolpoly_generalized.shp'
    
    main(path)
    