'''
Created on 28 Apr 2012

@author: Carnage
'''
import sys
from ..tvfs import tvfs
from ..builder import builder
from ..players.mpc import mpc

class cli:
    def __init__(self):
        self.tvfs = tvfs()
    
    def run(self):
        try:            
            if sys.argv[1] == '/playnext':
                self.playNext(sys.argv[2])
            if sys.argv[1] == '/build':
                self.build(sys.argv[2])
                
        except IndexError:
            pass        
        
    def playNext(self, path):
        series = self.tvfs.loadXml(path)
        progress = self.tvfs.loadProgressXml(path, series)
        
        print series.name
        def playLoop():
            
            episode = progress.getNext()
            print episode.name
            
            player = mpc()
            player.play(episode)
            
            self.tvfs.saveProgressXml(progress)
            n = raw_input('press key:')
            if n == 'c':
                playLoop()   
                
        playLoop()  
    
    def build(self, path):
        b = builder(path)
        self.tvfs.seriesInfo = b.build()
        self.tvfs.saveXml()