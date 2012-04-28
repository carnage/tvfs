'''
Created on 28 Apr 2012

@author: Carnage
'''

import os
from .containers.Series import Series
from .containers.Progress import Progress

import xml.dom.minidom as xml 

class tvfs:
    def findXml(self,directory,filename):
        if directory[-1] == '\\' or os.path.isfile(directory):
            #Cleanup path if it ends in a \\ or is a file.
            directory = os.path.split(directory)[0]
        
        parentdir = os.path.split(directory)[0]
        #file could be in current dir or parentdir
        locations = [os.path.join(directory,filename),os.path.join(parentdir,filename)]
        for x in locations:
            if os.path.isfile(x):
                return x            

        return None
    
    def loadXml(self,directory):
        xmlfile = self.findXml(directory,'SeriesInfo.xml')
        if xmlfile == None:
            return None#for now, need to build eventually
        
        x = xml.parse(xmlfile)
        series = Series.fromXml(x.getElementsByTagName('series')[0]) 
        self.seriesInfo[series.name] = series 
        return series    

    def loadProgressXml(self, series):
        xmlfile = self.findXml(series.path,'Progress.xml')
        if xmlfile == None:
            return Progress(series,0,0)
        
        x = xml.parse(xmlfile)

        return Progress.fromXml(x, series)
    
    def saveXml(self):
        for x in self.seriesInfo:
            series = self.seriesInfo[x]
            f = open(os.path.join(series.path,'SeriesInfo.xml'),'w+')
            f.write(series.toXML().toprettyxml())
            f.close()         

    def saveProgressXml(self,progress):
        f = open(os.path.join(progress.series.path,'Progress.xml'),'w+')
        f.write(progress.toXml().toprettyxml())
        f.close()    