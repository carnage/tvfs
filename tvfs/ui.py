'''
Created on 23 Jul 2011

@author: Carnage
'''

import os
from .builder import builder

from .containers.Series import Series
from .containers.Season import Season
from .containers.Episode import Episode
from .containers.Progress import Progress
from .players.mpc import mpc

import xml.dom.minidom as xml 

class ui:
    seriesInfo = {}
    
    def build(self,directory):
        b = builder(directory)
        self.seriesInfo = b.build()
        self.saveXml()
        
            
    def playnext(self,dir):
        test1 = os.path.split(dir)[0]
        test2 = os.path.split(test1)[0]
        if test1 == self.directory:
            #selected a series
            series = os.path.split(dir)[1]
            self.seriesInfo[series].playnext()
        elif test2 == self.directory:
            #selected a season
            series = os.path.split(test1)[1]
            self.seriesInfo[series].playnext(os.path.split(dir)[1])
                
        self.save()
        n = raw_input('press key:')
        if n == 'c':
            self.playnext(dir)

    def setnext(self,dir):
        test1 = os.path.split(dir)[0]
        test2 = os.path.split(test1)[0]
        if test1 == self.directory:
            #selected a series
            series = os.path.split(dir)[1]
            self.seriesInfo[series].setnext()
        elif test2 == self.directory:
            #selected a season
            series = os.path.split(test1)[1]
            self.seriesInfo[series].setnext(os.path.split(dir)[1])

        self.save()
    
    def refresh(self,dir):
        test1 = os.path.split(dir)[0]
        test2 = os.path.split(test1)[0]
        if test1 == self.directory:
            #selected a series
            pass
        elif test2 == self.directory:
            #selected a season
            series = os.path.split(test1)[1]
            self.buildSeason(self.seriesInfo[series].seasonInfo[os.path.split(dir)[1]])

        self.save()  

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
        def loadSeriesFromXml(series):
            def loadSeasonsFromXml(seasons,series):
                def loadSeasonFromXml(season):
                    def loadEpisodesFromXml(episodes,season):
                        def loadEpisodeFromXml(episode):
                            name = episode.getElementsByTagName('name')[0].childNodes[0].data.strip()
                            path = episode.getElementsByTagName('path')[0].childNodes[0].data.strip()
                            numeric = episode.getAttribute('numeric')
                            format = episode.getElementsByTagName('name')[0].getAttribute('format')
                            
                            e = Episode(path,name,numeric,format,season)   
                            return e
                        es = {}
                        
                        for x in episodes.getElementsByTagName('episode'):
                            e = loadEpisodeFromXml(x)
                            es[e.name] = e
                        
                        return es                                                 

                    episodes = season.getElementsByTagName('episodes')[0]
                    season.removeChild(episodes)
                    name = season.getElementsByTagName('name')[0].childNodes[0].data.strip()
                    path = season.getElementsByTagName('path')[0].childNodes[0].data.strip()
                    numeric = season.getAttribute('numeric')
                    
                    s = Season(path,name,numeric,series)                    
                    s.episodeInfo = loadEpisodesFromXml(episodes,s)
                    
                    return s
                
                ss = {}
                
                for x in seasons.getElementsByTagName('season'):
                    s = loadSeasonFromXml(x)
                    ss[s.name] = s
                
                return ss            
            
            seasons = series.getElementsByTagName('seasons')[0]
            series.removeChild(seasons)
            name = series.getElementsByTagName('name')[0].childNodes[0].data.strip()
            path = series.getElementsByTagName('path')[0].childNodes[0].data.strip()
            
            s = Series(path,name)
            s.seasonInfo = loadSeasonsFromXml(seasons,s)
            
            return s
        
        xmlfile = self.findXml(directory,'SeriesInfo.xml')
        if xmlfile == None:
            return None#for now, need to build eventually
        x = xml.parse(xmlfile)
        series = loadSeriesFromXml(x.getElementsByTagName('series')[0]) 
        self.seriesInfo[series.name] = series 
        return series    

    def loadProgressXml(self,directory,series):
        xmlfile = self.findXml(directory,'Progress.xml')
        if xmlfile == None:
            return Progress(series,0,0)
        
        x = xml.parse(xmlfile)
        season = x.getElementsByTagName('currentseason')[0].childNodes[0].data.strip()
        episode = x.getElementsByTagName('currentepisode')[0].childNodes[0].data.strip()
        
        return Progress(series,season,episode)
    
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
        
    def playNext(self,directory):
        series = self.loadXml(directory)
        progress = self.loadProgressXml(directory, series)
        
        print series.name
        def playLoop():
            
            episode = progress.getNext()
            print episode.name
            
            player = mpc()
            player.play(episode)
            
            self.saveProgressXml(progress)
            n = raw_input('press key:')
            if n == 'c':
                playLoop()   
                
        playLoop()     