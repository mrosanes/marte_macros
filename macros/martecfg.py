from sardana.macroserver.macro import Macro, Type
from sardana.macroserver.msexception import UnknownEnv
from collectlib.martecfglib import MarteConfig


gam_cfg = [["Class", Type.String, "IOGAM", "GAM Class"],
           ["InputSignal", Type.String, None, "Input Signal"],
           ["OutputSignal", Type.String, None, "Output Signal"]]

function_cfg = [["Class", Type.String, "ReferenceContainer", "Functions Class"],
                ["GAM", gam_cfg, "None", "GAM Configurations"],
                {'min': 1, 'max': 1}]


#gam_cfg = [["Class", Type.String, "GAMScheduler", "Class"],
#           ["InputSignal", Type.String, "Timings", "Input Signal"],
        #["OutputSignal", Type.String, "Timings", "Output Signal"]]

scheduler_cfg = [
    ['Class', Type.String, "GAMScheduler", 'Scheduler Class'],
    ['DataSource', Type.String, "Timings", 'Scheduler DataSource'],
    {'min': 1, 'max': 1}]

class marteconfig(Macro):

    def run(self, filename, apps):
        martecfg_obj = MarteConfig(filename, apps)
        martecfg_obj.generate_file()

    param_def = [
        ['filename', Type.Filename, "/root/hihi.txt", 'Output file'],
        ['apps', 
         [['application', Type.String, "AppTest", 'Application name'],
          ['class', Type.String, "RealTimeApplication", 'Class name'],
          ['functions', function_cfg, None, 'Functions'],
          ['data', Type.String, None, 'Data'],
          ['states', Type.String, None, 'States'],
          ['scheduler', scheduler_cfg, None, 'Scheduler']],
         None, 'List of apps'
         ]
    ]


