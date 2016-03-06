import sys,os

#sys.path.append(os.path.join(os.path.dirname(__file__), '..','plugin'))
sys.path.append('plugins')

import plugins
from importlib import import_module 


class load(object):
    def __init__(self):
        self.plugins = []
        self.myplugins = []
        self.config = ['myplugin1','myplugin2']
      
    def dynamicLoadModules(self):
        print sys.path
        sys.modules['plugins'] = self.plugins = type(sys)('plugins')
        self.plugins.__path__ = []
        for path in self.config:
            mypath = os.path.join(sys.path[0],'plugins',path)
            print mypath
            self.plugins.__path__.append(mypath)
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
    
