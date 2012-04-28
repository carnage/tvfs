'''
Created on 23 Jul 2011

@author: Carnage
'''
import sys
from tvfs.ui.cli import cli

#directory = 'F:\\media'
#mpc = "C:\\Program Files\\MPC HomeCinema (x64)\\mpc-hc64.exe"

#x = ui()          
#try:            
#    if sys.argv[1] == '/playnext':
#        x.playNext(sys.argv[2])
#    if sys.argv[1] == '/build':
#        x.build(sys.argv[2])
#        
#except IndexError:
#    pass
argv = ['','','']
argv[0] = ''
argv[1] = '/playnext'
argv[2] = 'F:\\media\\Simpsons'

x = cli()
x.run(argv)

#x.saveXml()
#x.playNext('F:\\media\\24\\')
#print x.seriesInfo['24'].toXML().toprettyxml()
#x.toXML()