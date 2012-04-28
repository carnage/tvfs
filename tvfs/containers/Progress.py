'''
Created on 23 Jul 2011

@author: Carnage
'''
import xml.dom.minidom as xml

class SeasonFinished(Exception):
    pass

class Progress:
    def __init__(self,series,currentSeason,currentEpisode):
        self.currentSeason = int(currentSeason)
        self.currentEpisode = int(currentEpisode)
        self.series = series

    def toXml(self):
        doc = xml.Document()
        progress = doc.createElement('progress')

        ce = doc.createElement('currentepisode')
        ce.appendChild(doc.createTextNode(str(self.currentEpisode)))
        cs = doc.createElement('currentseason')
        cs.appendChild(doc.createTextNode(str(self.currentSeason)))
        progress.appendChild(cs)
        progress.appendChild(ce)      
        
        return progress  

    @classmethod
    def fromXml(self, xml, series):
        season = xml.getElementsByTagName('currentseason')[0].childNodes[0].data.strip()
        episode = xml.getElementsByTagName('currentepisode')[0].childNodes[0].data.strip()
        return Progress(series,season,episode)
        
    def getNext(self):
        def getSeason():     
            try:
                season = sorted(self.series.seasonInfo.values()).pop(self.currentSeason)
            except IndexError:
                season = sorted(self.series.seasonInfo.values()).pop(0)
                self.currentSeason = 0
                
            return season
        
        def getEpisode(season):
            try:
                episode = sorted(season.episodeInfo.values()).pop(self.currentEpisode)
            except IndexError:
                self.currentEpisode = 0
                raise SeasonFinished()
            return episode
            
        try:
            episode = getEpisode(getSeason())
        except SeasonFinished:
            self.currentSeason += 1
            episode = getEpisode(getSeason())

        self.currentEpisode += 1  
        return episode
