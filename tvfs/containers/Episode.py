import os
import xml.dom.minidom as xml

class Episode:
    def __init__(self,path,name,numeric,format,season=None):
        self.season = season
        self.path = os.path.join(path,name)
        self.parentpath = path
        self.name = name    
        self.numeric = int(numeric)
        self.format = format

    def __cmp__(self,other):
        return cmp(self.numeric,other.numeric)
    
    def toXML(self):
        doc = xml.Document()
        episode = doc.createElement('episode')
        episode.setAttribute('numeric',str(self.numeric))
        path = doc.createElement('path')
        path.appendChild(doc.createTextNode(self.parentpath))
        name = doc.createElement('name')
        name.appendChild(doc.createTextNode(self.name))
        name.setAttribute('format',str(self.format))
        episode.appendChild(path)
        episode.appendChild(name)
        
        return episode
    
    @classmethod
    def fromXml(self, xml):
        name = xml.getElementsByTagName('name')[0].childNodes[0].data.strip()
        path = xml.getElementsByTagName('path')[0].childNodes[0].data.strip()
        numeric = xml.getAttribute('numeric')
        format = xml.getElementsByTagName('name')[0].getAttribute('format')
        
        e = Episode(path,name,numeric,format)   
        return e        
    
    #depricated    
    def namecheck(self):
        if self.name.split(' ')[0] != self.season.numeric + 'x' + self.numeric:
            print self.name + ' failed'
            print 'Rename: ' + self.path + ' to: ' + os.path.join(self.parentpath,self.season.numeric + 'x' + self.numeric + ' ' + self.name)
    #depricated 
    def write(self,h):
        h.write('\t\t' + self.name + '\n')   

