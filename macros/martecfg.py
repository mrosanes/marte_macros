from sardana.macroserver.macro import Macro, Type
from sardana.macroserver.msexception import UnknownEnv
from martecfglib import MarteConfig

inputsignal_cfg = [["InputSignal", Type.String, "Time", "Signal name"],
                   ["DataSource", Type.String, "Timer", "Data Source"],
                   ["Type", Type.String, "uint32", "Type"]]

outputsignal_cfg = [["OutputSignal", Type.String, "Time", "Signal name"],
                    ["DataSource", Type.String, "DDB1", "Data Source"],
                    ["Type", Type.String, "uint32", "Type"]]

gam_cfg = [["GAMName", Type.String, "GAMTimer", "GAM name"],
           ["Class", Type.String, "IOGAM", "GAM Class"],
           ["InputSignals", inputsignal_cfg, "in", "Input Signal"],
           ["OutputSignals", outputsignal_cfg, "out", "Output Signal"]]

function_cfg = [["Class", Type.String, "ReferenceContainer", "Functions Class"],
                ["GAMs", gam_cfg, "None", "GAM Configurations"],
                {'min': 1, 'max': 1}]


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
          ['data', Type.String, "dat", 'Data'],
          ['states', Type.String, "state", 'States'],
          ['scheduler', scheduler_cfg, None, 'Scheduler']],
         None, 'List of apps'
         ]
    ]


