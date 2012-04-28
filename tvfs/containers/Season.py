import os
import xml.dom.minidom as xml
from .Episode import Episode
    
class Season:
    def __init__(self,path,name,numeric,series=None):
        self.path = os.path.join(path,name)
        self.parentpath = path
        self.name = name    
        self.numeric = int(numeric)
        self.episodeInfo = {}
        self.currentepisode = 0

    def __cmp__(self,other):
        return cmp(self.numeric,other.numeric)

    def toXML(self):
        doc = xml.Document()
        season = doc.createElement('season')
        season.setAttribute('numeric',str(self.numeric))
        path = doc.createElement('path')
        path.appendChild(doc.createTextNode(self.parentpath))
        name = doc.createElement('name')
        name.appendChild(doc.createTextNode(self.name))
        season.appendChild(path)
        season.appendChild(name)
        episodes = doc.createElement('episodes')
        
        for x in sorted(self.episodeInfo.values()):
            episodes.appendChild(x.toXML())
        
        season.appendChild(episodes)
        
        return season

    @classmethod
    def fromXml(self, xml):
        episodes = xml.getElementsByTagName('episodes')[0]
        es = {}
        for x in episodes.getElementsByTagName('episode'):
            e = Episode.fromXml(x)
            es[e.name] = e

        xml.removeChild(episodes)
        name = xml.getElementsByTagName('name')[0].childNodes[0].data.strip()
        path = xml.getElementsByTagName('path')[0].childNodes[0].data.strip()
        numeric = xml.getAttribute('numeric')
        
        s = Season(path,name,numeric)                    
        s.episodeInfo = es
        
        return s        
        
    def namecheck(self):
        if self.name != 'Season ' + self.numeric:
            print self.name + ' failed'
            print 'Rename: ' + self.path + ' to: ' + os.path.join(self.parentpath,'Season ' + self.numeric)
            
    def write(self,h):
        h.write('\t'+self.name+'\n')
        for x in self.episodeInfo:
            self.episodeInfo[x].write(h)           

        
    def setnext(self,season=None):
        i = 1
        for x in sorted(self.episodeInfo.values()):
            print i,
            print ')',
            print x.name
            i+=1
            
        self.currentepisode = int(raw_input('Select number:')) -1    