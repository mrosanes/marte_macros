# platform (can be used to deduce if the system uses py2 or py3)
import platform

import collections
import json


# APPLICATION CFG
APPNAME = 0
CLASSNAME = 1
FUNCTIONS = 2
DATA = 3
STATES = 4
SCHEDULER = 5


# FUNCTIONS/GAMS CFG
FUNCTION_CLASS = 0
FUNCTION_GAMS = 1

GAM_NAME = 0
GAM_CLASS = 1
GAM_INPUTSIGNALS = 2
GAM_OUTPUTSIGNALS = 3

SIGNAL_NAME = 0
SIGNAL_DATASOURCE = 1
SIGNAL_TYPE = 2


# STATES CFG
STATESCFG_CLASS = 0
STATESCFG_STATES = 1

STATE_NAME = 0
STATE_CLASS = 1
STATE_THREADS = 2

THREADSCFG_CLASS = 0
THREADSCFG_THREADS = 1

THREAD_NAME = 0
THREAD_CLASS = 1
THREAD_CPUs = 2
THREAD_GAMS_CFG = 3

THREAD_GAMS = 0

# SCHEDULER(S) CFG
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
        for signal in signals_cfg:
            signal_name = signal[SIGNAL_NAME]
            signal_dict = collections.OrderedDict()
            signal_dict["DataSource"] = signal[SIGNAL_DATASOURCE]
            signal_dict["Type"] = signal[SIGNAL_TYPE]
            
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

    def create_threads_config(self, threads_dict, threads_cfg):
        for thread_cfg in threads_cfg:
            thread_name = thread_cfg[THREAD_NAME]
            thread_dict = collections.OrderedDict()
            thread_dict["Class"] = thread_cfg[THREAD_CLASS]
            thread_dict["CPUs"] = thread_cfg[THREAD_CPUs]
            GAMs_on_thread_cfg = thread_cfg[THREAD_GAMS_CFG]
            GAMs_on_thread_list = []
            for GAM in GAMs_on_thread_cfg:
                GAMs_on_thread_list.append(GAM[0])
            thread_dict["Functions"] = GAMs_on_thread_list
            threads_dict[thread_name] = thread_dict        
    
    def create_states_config(self, states_dict, states_cfg):
        for state_cfg in states_cfg:
            state_name = state_cfg[STATE_NAME]
            state_dict = collections.OrderedDict()
            state_dict["Class"] = state_cfg[STATE_CLASS]

            threads_dict = collections.OrderedDict()
            threads_cfg = state_cfg[STATE_THREADS]
            
            threads_dict["Class"] = threads_cfg[0][THREADSCFG_CLASS]
            threads_cfg = threads_cfg[0][THREADSCFG_THREADS]
            self.create_threads_config(threads_dict, threads_cfg)
            state_dict["Threads"] = threads_dict
            
            states_dict[state_name] = state_dict

    def generate_app_config(self, app):
        app_name = app[APPNAME]
        self.data[app_name] = collections.OrderedDict()
        self.data[app_name]["Class"] = app[CLASSNAME]
        
        # FUNCTIONS
        functions_dict = collections.OrderedDict()
        functions_dict["Class"] = app[FUNCTIONS][0][FUNCTION_CLASS]  
        gams_cfg = app[FUNCTIONS][0][FUNCTION_GAMS]
        self.create_gams_config(functions_dict, gams_cfg)
        self.data[app_name]["Functions"] = functions_dict
        
        # DATA
        self.data[app_name]["Data"] = app[DATA]
        
        # STATES
        states_dict = collections.OrderedDict()
        states_dict["Class"] = app[STATES][0][STATESCFG_CLASS]
        states_cfg = app[STATES][0][STATESCFG_STATES]
        self.create_states_config(states_dict, states_cfg)
        self.data[app_name]["States"] = states_dict
        
        # SCHEDULER
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
        [  # functions (One note but yet it is required to be a repeat node)
            [
                "ReferenceContainer",
                [
                    [
                        "GAMTimer",
                        "IOGAM1",
                        [
                            [
                                "Time",
                                "Timer",
                                "uint32",
                            ],
                            [
                                "Count",
                                "Counter",
                                "uint32",
                            ],
                        ],
                        [
                            [
                                "outtime",
                                "outTimer",
                                "float",
                            ],
                            [
                                "outcount",
                                "outCounter",
                                "float",
                            ],
                        ],                        
                    ],
                ],

            ],
        ],
                            
        "data", 
        

        [  # States (One note but yet it is required to be a repeat node)
            [
                "ReferenceContainer",
                [
                    [
                        "State1",    
                        "RealTimeState",
                        [
                            [
                                "ReferenceContainer",
                                [
                                    [
                                        "Thread1",
                                        "RealTimeThread",
                                        "0x1",
                                        [
                                            ["GAMTimer"],
                                            ["GAMTimer2"],
                                            ["GAMTimer3"],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],

            ],
        ],
               

        [# scheduler
            [
                "GAMScheduler",
                "Timings",
            ],
        ],
    ]
    ]
            
    FILE_NAME = './martecfg.txt'
    martecfg_obj = MarteConfig(FILE_NAME, apps)
    martecfg_obj.generate_file()


