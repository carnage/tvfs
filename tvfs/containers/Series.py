import os
import xml.dom.minidom as xml
from .Season import Season

class Series:
    def __init__(self,path,name):
        self.path = os.path.join(path,name)
        self.parentpath = path
        self.name = name
        self.seasonInfo = {}
        self.seasons = 0
        self.currentseason = 0
        
    def write(self,h):
        h.write(self.name+'\n')
        for x in self.seasonInfo:
            self.seasonInfo[x].write(h)

    def toXML(self):
        doc = xml.Document()
        series = doc.createElement('series')
        path = doc.createElement('path')
        path.appendChild(doc.createTextNode(self.parentpath))
        name = doc.createElement('name')
        name.appendChild(doc.createTextNode(self.name))
        series.appendChild(path)
        series.appendChild(name)
        seasons = doc.createElement('seasons')
        
        for x in sorted(self.seasonInfo.values()):
            seasons.appendChild(x.toXML())
        
        series.appendChild(seasons)
        
        return series

    @classmethod
    def fromXml(self, xml):
        seasons = xml.getElementsByTagName('seasons')[0]
        ss = {}
        
        for x in seasons.getElementsByTagName('season'):
            s = Season.fromXml(x)
            ss[s.name] = s      
              
        xml.removeChild(seasons)
        name = xml.getElementsByTagName('name')[0].childNodes[0].data.strip()
        path = xml.getElementsByTagName('path')[0].childNodes[0].data.strip()
        
        s = Series(path,name)
        s.seasonInfo = ss     
        
        return s   

            
    def setnext(self,season=None):
        i = 1
        for x in sorted(self.seasonInfo.values()):
            print i,
            print ')',
            print x.name
            i+=1
            
        self.currentseason = int(raw_input('Select number:')) -1
        try:
            season = sorted(self.seasonInfo.values()).pop(self.currentseason)
        except IndexError:
            season = sorted(self.seasonInfo.values()).pop(0)
            self.currentseason = 0 

        season.setnext()