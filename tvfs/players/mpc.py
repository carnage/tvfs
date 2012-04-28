'''
Created on 23 Jul 2011

@author: Carnage
'''

import subprocess

from .playerAbstract import playerAbstract

class mpc(playerAbstract):
    def play(self,episode):
        subprocess.Popen(["C:\\Program Files\\MPC HomeCinema (x64)\\mpc-hc64.exe",episode.path,'/play','/close','/fullscreen'] )        