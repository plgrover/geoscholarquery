#! /usr/bin/env python
"""
This module is used to perform a geo-located google scholar query and return
results and associated coordinates.
"""
#
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import scholar
import osgeo.gdal as gdal
import osgeo.osr as osr
import osgeo.ogr as ogr
import csv
from google import google




def __queryForName(x, y, path, queryfield):
    retval = []
    # Fine 
    shapdata = ogr.Open(path, 1)
    layer = shapdata.GetLayer()     
    wktPoint = "POINT ({0} {1})".format(x,y)
    point  = ogr.CreateGeometryFromWkt(wktPoint)
    retval = []
    for feature in layer:
        geom = feature.GetGeometryRef()
        pnt = geom.Centroid()
        if point.Within(feature.GetGeometryRef()):
            val = feature.GetField(queryfield)
            namegeo = {}
            namegeo['name']=val
            namegeo['pnt'] = pnt
            retval.append(namegeo)
    return retval
    
       
def getkeywords(filename):
    keywords = []
    keywordfile = filename
    with open(keywordfile) as f:
        lines = f.readlines()
        for line in lines:
            keywords.append(line.rstrip('\n'))
    return keywords


def getgeocodenames(x,y):
    #read csv
    retval = []
    layerlistfile = r'layers.txt'
    layerlist = []
    # Read layer list
    with open(layerlistfile) as f:
        lines = f.readlines()
        for line in lines:
            layerlist.append(line.rstrip('\n').split(','))  
    # Query the data  
    for layer in layerlist:
        results = __queryForName(x, y, layer[0],  layer[1])
        for namegeo in results:
            retval.append(namegeo)
        
    return retval

# https://github.com/abenassi/Google-Search-API
def queryGoogle(geonames,keywords,num_page=10):
    search_terms = ' '.join(keywords)
    search_results = google.search("This is my query", num_page)#google.search(search_terms, num_page)
    print('ok')
    return search_results

def queryGoogleScholar(andkeywords,orkeywords,pnt, filename, header):
    query = scholar.SearchScholarQuery()
    query.set_words(' '.join(andkeywords))
    query.set_words_some(' '.join(orkeywords))
    query.set_num_page_results(10)
    
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    querier.send_query(query)    
    scholar.csv(querier, header=header, sep='|', filename=filename,geo=pnt)

def getGoogleScholarArticles(x,y, csvoutput):
    geonames = getgeocodenames(x,y) 
    placenames = []
    pnt = None
    header = True
    for geoname in geonames:
        pnt = geoname['pnt']    
        orkeywordnames = getkeywords('orkeywords.txt')
        andkeywordnames = getkeywords('andkeywords.txt')
        andkeywordnames.append(geoname['name'])
        print('Querying: {0}'.format(geoname['name']))
        print('AND: {0}'.format(' '.join(andkeywordnames)))
        print('OR: {0}'.format(' '.join(orkeywordnames)))
        print('Pnt: {0}  {1}'.format(pnt.GetX(), pnt.GetY()))
        queryGoogleScholar(andkeywordnames, orkeywordnames, pnt, csvoutput, header)
        header = False
    
def getMiningPressReleases(x,y,csvoutput):
    geonames = getgeocodenames(x,y)   
    
    placenames = []
    for geoname in geonames:
        placenames.append(geoname['name'])
    
    andkeywordnames = getkeywords('pressreleasekeywords.txt')
    search_results = queryGoogle(placenames,andkeywordnames,10)
    
    with open(csvoutput,'w') as f:
        for result in search_results:
            print(result)
            f.write('{0},{1},{2}'.format(result.name,result.link,result.description))
    

def main():
    x = -134.2901
    y =  58.579185
    getGoogleScholarArticles(x,y,'Papers.txt')
    #getMiningPressReleases(x,y,'miningrelease.txt')
    
    
if __name__ == "__main__":
    sys.exit(main())

