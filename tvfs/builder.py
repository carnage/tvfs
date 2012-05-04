'''
Created on 23 Jul 2011

@author: Carnage
'''
import re,os
from .containers.Series import Series
from .containers.Season import Season
from .containers.Episode import Episode

class builder:
    seriesInfo = {}
    seriesMatch = re.compile('(series|season|s)([\s]?)([\d]+)',re.I)
    episodeFormats = [re.compile(x,re.I) for x in ['(?:S[\d]+)?E(?:pisode(?: )?)?([\d]+)','(?:[\d]+)x([\d]+)','[\d]-([\d][\d])','[\d]([\d][\d])','^([\d][\d])']]
    def __init__(self,directory):
        self.directory = directory
    
    def buildSeries(self,series):
        for season in os.listdir(series.path):
            match = self.seriesMatch.search(season)
            if os.path.isdir(os.path.join(series.path,season)) and match:
                series.seasons+=1
                series.seasonInfo[season] = Season(series.path,season,match.group(3),series)
                self.buildSeason(series.seasonInfo[season])

    def buildSeason(self,season):
        #season.namecheck()
        for episode in os.listdir(season.path):
            if not os.path.isdir(os.path.join(season.path,episode)):
                name = os.path.splitext(episode)[0]
                ext = os.path.splitext(episode)[1]
                ext = ext.lower()
                try: 
                    ['.avi','.mkv','.mpg','.ogm','.wmv','.divx'].index(ext)
                    found = False
                    format = 0
                    for x in self.episodeFormats:
                        match = x.search(name)
                        if match:
                            epinfo = match.group(1)
                            found = True
                            break
                        format += 1
                    if found:
                        season.episodeInfo[episode] = Episode(season.path,episode,epinfo,format,season)
                    else:
                        print 'Unable to parse: ' + os.path.join(season.path,name)
                    
                except ValueError:
                    try: 
                        ['.srt','.db','.txt','.nfo','.ini','.mds','.jpg','.md5','.sfv','.incomplete'].index(ext)
                    except ValueError:
                        if ext == '.iso':
                            print 'ISO extention is not supported; encode into something else: ' + episode
                        else:
                            print 'unknown extention: ' + episode
    def build(self):
        #two options; could be on a series dir or in a dir containing many series.
        parentPath,series = os.path.split(self.directory)
        for d in os.listdir(self.directory):  
            if os.path.isdir(os.path.join(self.directory,d)) and self.seriesMatch.search(d):
                self.seriesInfo[series] = Series(parentPath,series)
                self.buildSeries(self.seriesInfo[series])    
                return self.seriesInfo  
        
        for series in os.listdir(self.directory):
            #detect if this is a series
            for d in os.listdir(os.path.join(self.directory,series)):  
                if os.path.isdir(os.path.join(self.directory,series,d)) and self.seriesMatch.search(d):
                    self.seriesInfo[series] = Series(self.directory,series)
                    self.buildSeries(self.seriesInfo[series])    
                    break
                        
        return self.seriesInfo 
                