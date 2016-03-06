import sys,os


import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..', '..','db','plugins'))
sys.path.append('../../db')

from plugins import *

from importlib import import_module 


class load(object):
    def __init__(self):
        self.plugins = []
        self.myplugins = []
        self.config = ['myplugin1','myplugin2']
 
        print sys.path[0]
        print os.path.realpath(os.path.dirname(sys.path[0]))
        self.mypath = os.path.realpath(os.path.dirname(sys.path[0]))
      
    def dynamicLoadModules(self):
        print sys
        print sys.modules['plugins']
        #
#        sys.modules['plugins'] = self.plugins = type(sys)('just_init')
#        print sys.modules['plugins']
#        self.plugins.__path__ = []
#        for path in self.config:
#            mypath = os.path.join(self.mypath,'plugins',path)
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
    
