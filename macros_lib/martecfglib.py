# platform (can be used to deduce if the system uses py2 or py3)
import platform

import collections
import json


APPNAME = 0
CLASSNAME = 1
FUNCTIONS = 2
DATA = 3
STATES = 4
SCHEDULER = 5

FUNCTION_CLASS = 0
FUNCTION_GAMS = 1

GAM_NAME = 0
GAM_CLASS = 1
GAM_INPUTSIGNALS = 2
GAM_OUTPUTSIGNALS = 3

SIGNAL_NAME = 0
SIGNAL_DATASOURCE = 1
SIGNAL_TYPE = 2

SCHEDULER_CLASS = 0
SCHEDULER_DS = 1  # Scheduler DataSource


class MarteConfig():

    def __init__(self, filename="/root/marte_cfg_fname.txt", apps=None):
        self.filename = filename
        self.destination = "empty"
        self.apps = apps
        self.data = collections.OrderedDict()
        self.python_version = platform.python_version()[0]

    def create_signals_config(self, signals_dict, signals_cfg):
        for Signal in signals_cfg:
            signal_name = Signal[SIGNAL_NAME]
            signal_dict = collections.OrderedDict()
            signal_dict["DataSource"] = Signal[SIGNAL_DATASOURCE]
            signal_dict["Type"] = Signal[SIGNAL_TYPE]
            
            signals_dict[signal_name] = signal_dict
            
    def create_gams_config(self, functions_dict, gams_cfg):
        for gam_cfg in gams_cfg:
            gam_name = gam_cfg[GAM_NAME]
            gam_dict = collections.OrderedDict()
            gam_dict["Class"] = gam_cfg[GAM_CLASS]

            inputsignals_dict = collections.OrderedDict()
            inputsignals_cfg = gam_cfg[GAM_INPUTSIGNALS]
            self.create_signals_config(inputsignals_dict, inputsignals_cfg)
            gam_dict["InputSignals"] = inputsignals_dict
            
            outputsignals_dict = collections.OrderedDict()
            outputsignals_cfg = gam_cfg[GAM_OUTPUTSIGNALS]
            self.create_signals_config(outputsignals_dict, outputsignals_cfg)
            gam_dict["OutputSignals"] = outputsignals_dict
            
            functions_dict[gam_name] = gam_dict
    
    def generate_app_config(self, app):
        app_name = app[APPNAME]
        self.data[app_name] = collections.OrderedDict()
        self.data[app_name]["Class"] = app[CLASSNAME]
                
        functions_dict = collections.OrderedDict()
        functions_dict["Class"] = app[FUNCTIONS][0][FUNCTION_CLASS]    
        self.create_gams_config(functions_dict, 
                                app[FUNCTIONS][0][FUNCTION_GAMS])
        
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


if __name__ == '__main__':
    
    apps = [
    [
        'AppTest',  # App Name
        'RealTimeApplication',  # Class
        [  # functions (only one but it is a repeat node)
            [
                "ReferenceContainer",
                [
                    [
                    "IOGAM1",
                    "InputSignal1",
                    "OutputSignal1",
                    ],
                ],
            ],
        ],
        "data",  # flat field position x
        "states",  # flat field position y
        [# scheduler
            [
                "GAMScheduler",
                "Timings",
            ],
        ],  # flat field exposure time
    ]
    ]
            
    FILE_NAME = './martecfg.txt'
    martecfg_obj = MarteConfig(FILE_NAME, apps)
    martecfg_obj.generate_file()


