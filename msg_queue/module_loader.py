import sys,os

sys.path.append('../modules')
sys.path.append(os.path.join(os.path.dirname(__file__),'..','modules','auth'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..','modules','lobby'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..','modules','game'))

#module
from plugins import *
from auth import *
from lobby import * 
from game import * 

from importlib import import_module 

class module_load(object):

    def __init__(self,module_list):
        self._default_module = ['auth','lobby']
        self.config = module_list
 
        self.modules = []
        self.mypath = os.path.realpath(os.path.dirname(sys.path[0]))
#        self.ppath = os.path.abspath(os.path.join(self.mypath,'../')) up one level
#        print self.mypath
      
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
        self.modules = [ import_module(module) for module in self.config]
        for module in self.modules: 
            reload(module)
        #for module in self.modules:
        #    module.init()

    def execute_work(self,json_msg):

        module_idx = 0 
        if json_msg['module'] in self._default_module:
           module_idx = self._default_module.index(json_msg['module'])
        print module_idx
        print self.modules[module_idx]
        result = self.modules[module_idx].handle(json_msg)
        return result
        #msg['cmd'] = "login"
         

def main():
    p = load() 
    p.dynamicLoadModules()

if __name__ == "__main__":
    main()
    
