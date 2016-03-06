import sys,os

sys.path.append('../modules')
sys.path.append(os.path.join(os.path.dirname(__file__),'..','modules','plugins'))

#module
from plugins import *

from importlib import import_module 

class load(object):

    def __init__(self):
        self.config = ['myplugin1','myplugin2']
 
        self.mypath = os.path.realpath(os.path.dirname(sys.path[0]))
#        self.ppath = os.path.abspath(os.path.join(self.mypath,'../')) up one level
        print self.mypath
      
    def dynamicLoadModules(self):
        #TODO dynamic load module
        #sys.modules['plugins'] = self.plugins = type(sys)('just_init')
        #self.plugins.__path__ = []
        #for path in self.config:
#            mypath = os.path.join(self.mypath,path)
#            mypath = os.path.join(sys.path[0],'plugins',path)
#            print mypath
#            self.plugins.__path__.append(mypath)

        ##dynamic load modules
        self.modules = []
        self.modules = [ import_module(module) for module in self.config]
        for module in self.modules: 
            reload(module)
        for module in self.modules:
            module.init()

def main():
    p = load() 
    p.dynamicLoadModules()

if __name__ == "__main__":
    main()
    
