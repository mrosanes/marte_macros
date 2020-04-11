from martecfglib import MarteConfig

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
                            
        [
            [
                "ReferenceContainer",
                "DDB1",
                "GAMDataSource",
                "LoggerDataSource",
                "TimingDataSource",
                [
                    [
                        "Timer",
                        "LinuxTimer",
                        "Default",
                        [
                            [
                                "Counter",
                                "uint32",
                            ],
                            [
                                "Time",
                                "uint32",
                            ],
                        ],
                    ],
                ],
            ],
        ],
        

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
                                        ["GAMTimer", "GAMTimer2", "GAMTimer3"],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],

            ],
        ],
               
        # scheduler
        [
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

