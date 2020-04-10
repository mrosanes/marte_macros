# platform: py2 or py3
import platform

import collections
import json


FILE_NAME = 'martecfg.txt'

APPNAME = 0
CLASSNAME = 1
FUNCTIONS = 2
DATA = 3
STATES = 4
SCHEDULER = 5

FUNCTION_CLASS = 0
FUNCTION_GAMS = 1

GAM_CLASS = 0
GAM_INPUTSIGNALS = 1
GAM_OUTPUTSIGNALS = 2

SCHEDULER_CLASS = 0
SCHEDULER_DS = 1  # Scheduler DataSource

"""
apps = [
    [   'classname1'
        'function1',  
        'data1', 
        'states1',  
        'scheduler1',  
    ],
]
"""

class MarteConfig():

    def __init__(self, filename="/root/marte_cfg_fname.txt", apps=None):
        self.filename = filename
        self.destination = "empty"
        self.apps = apps
        self.data = collections.OrderedDict()
        self.python_version = platform.python_version()[0]
        
    def generate_app_config(self, app):
        app_name = app[APPNAME]
        self.data[app_name] = collections.OrderedDict()
        functions_dict = collections.OrderedDict()
        functions_dict.update({"Class": app[FUNCTIONS][0][FUNCTION_CLASS]})     
        self.data[app_name].update({"Class": app[CLASSNAME]})

        for GAM in app[FUNCTIONS][0][FUNCTION_GAMS]:
            pass
        
        self.data[app_name]["Functions"] = functions_dict
        self.data[app_name]["Data"] = app[DATA]
        self.data[app_name]["States"] = app[STATES]
        
        schedulers_dict = collections.OrderedDict()
        schedulers_dict["Class"] = app[SCHEDULER][0][SCHEDULER_CLASS]
        schedulers_dict["TimingDataSource"] = app[SCHEDULER][0][SCHEDULER_DS]
        self.data[app_name]["Scheduler"] = schedulers_dict
        
        json.dump(self.data, self.destination, indent=4, sort_keys=False)

    def generate_marte_cfg(self):
        for app in self.apps:
            self.generate_app_config(app)

    def generate_file(self):
        destination = open(self.filename, 'w')
        with destination as self.destination:
            self.generate_marte_cfg()


#if __name__ == '__main__':
#    martecfg_obj = MarteConfig(FILE_NAME, apps)
#    martecfg_obj.generate_file()


