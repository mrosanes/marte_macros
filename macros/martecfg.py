from sardana.macroserver.macro import Macro, Type
from sardana.macroserver.msexception import UnknownEnv
from martecfglib import MarteConfig


DefaultGAM = "GAMTimer" # GAMTimer will be used by used Default GAM


# Functions/GAMs configuration
inputsignal_cfg = [["InputSignal", Type.String, "Time", "Signal Name"],
                   ["DataSource", Type.String, "Timer", "Data Source"],
                   ["Type", Type.String, "uint32", "Type"]]

outputsignal_cfg = [["OutputSignal", Type.String, "Time", "Signal Name"],
                    ["DataSource", Type.String, "DDB1", "Data Source"],
                    ["Type", Type.String, "uint32", "Type"]]

gam_cfg = [["GAM", Type.String, DefaultGAM, "GAM Name"],
           ["Class", Type.String, "IOGAM", "GAM Class"],
           ["InputSignals", inputsignal_cfg, None, "Input Signal"],
           ["OutputSignals", outputsignal_cfg, None, "Output Signal"]]

functions_cfg = [
    ["Class", Type.String, "ReferenceContainer", "Functions Class"],
    ["GAMs", gam_cfg, "None", "GAMs Configurations"],
    {'min': 1, 'max': 1}]


# Data Configuration
signal_cfg = [["Signal", Type.String, "Time", "Signal Name"],
              ["Type", Type.String, "uint32", "Type"]]

timer_cfg = [["TimerName", Type.String, "Timer", "Data Timer Name"],
             ["Class", Type.String, "LinuxTimer", "Data Timer Class"],
             ["SleepNature", Type.String, "Default", 
              "Sleep Nature (usually Default)"],
             ["Signals", signal_cfg, None, "Timer Signals configuration"],
             {'min': 1, 'max': 1}]


data_cfg = [
    ["Class", Type.String, "ReferenceContainer", "Data Config Class"],
    ["DefaultDataSource", Type.String, "DDB1", "Default Data Source"],
    ["DDB1", Type.String, "GAMDataSource", "Data Source"],
    ["LoggerDataSource", Type.String, "LoggerDataSource", "Logger"],
    ["Timings", Type.String, "TimingDataSource", "Timing"],
    ["Timer", timer_cfg, None, "Data Timer Configuration"],
    {'min': 1, 'max': 1}]


# States Configuration: Threads Configuration
gams_list = [["GAM", Type.String, DefaultGAM, "GAM Name"],]

thread_cfg = [["ThreadName", Type.String, "Thread1", "Thread Name"],
              ["Class", Type.String, "RealTimeThread", "Thread Class"],
              ["CPUs", Type.String, "0x1", "State Name"],
              ["Functions", gams_list, None, "Functions Names Dict"],
              {'min': 1}]

threads_cfg = [["Class", Type.String, "ReferenceContainer", "Threads Class"],
               ["Threads", thread_cfg, None, "Threads Configuration"],
               {'min': 1, 'max': 1}]

state_cfg = [["StateName", Type.String, "State1", "State Name"],
             ["Class", Type.String, "RealTimeState", "State Class"],
             ["Threads", threads_cfg, "None", "Threads Configurations"],
             {'min': 1}]

states_cfg = [
    ["Class", Type.String, "ReferenceContainer", "States Config Class"],
    ["States", state_cfg, None, "States Configurations"],
    {'min': 1, 'max': 1}]


# Scheduler Configuration
scheduler_cfg = [
    ['Class', Type.String, "GAMScheduler", 'Scheduler Class'],
    ['DataSource', Type.String, "Timings", 'Scheduler DataSource'],
    {'min': 1, 'max': 1}]


class marteconfig(Macro):

    def run(self, filename, apps):
        martecfg_obj = MarteConfig(filename, apps)
        martecfg_obj.generate_file()

    param_def = [
        ['filename', Type.Filename, "/MARTe_config_filename.txt", 'Output file'],
        ['apps', 
         [['AppName', Type.String, "AppTest", 'Application name'],
          ['Class', Type.String, "RealTimeApplication", 'Class name'],
          ['Functions', functions_cfg, None, 'Functions Configuration'],
          #['Data', Type.String, None, 'Data Configuration'],
          ['Data', data_cfg, None, 'Data Configuration'],
          ['States', states_cfg, None, 'States Configuration'],
          ['Scheduler', scheduler_cfg, None, 'Scheduler Configuration']],
         None, 'List of apps'
         ]
    ]

