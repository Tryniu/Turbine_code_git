# -*- coding: utf-8 -*-

################################NOTES_TO_MYSELF#############################################
#
#
#
#
#
#
#############################################################################


import time
import threading
import sys
import imp

from __init__ import *

import Threads_Manager
import File_reader
import Turbine
import Database_manage

class Start():

    def __init__( self ):
       pass

    def Get_devices_to_launch( self ):

        INPUT_file_path     = "DevicesMaps\input_devices_map.txt"
        OUTPUT_file_path    = "DevicesMaps\output_devices_map.txt"

        INPUT_devices_data = { 'T': {}, 'P': {}, 'F': {}, 'RPM': {}, 'EXH': {} }          # stores data read
        INPUT_devices_instances = {'T': [], 'P': [], 'F': [], 'RPM': [], 'EXH': []}        # stores clases instancies
        INPUT_classes_map = {'T' :Turbine.Thermocouple, 'F': Turbine.Flowmeter, 'RPM': Turbine.Rev_counter, 'P': Turbine.Manometer, 'EXH': Turbine.Exhaust_sensor }       # hashes classes adreses against their shortcuts

        OUTPUT_devices_data = { 'GAS_VALVE': {}, 'THROTTLE': {}, 'SPARK': {} , 'FAN': {} , 'WASTEGATE': {} , 'OIL_PUMP': {} }              # stores data read
        OUTPUT_devices_instances ={ 'GAS_VALVE': [], 'THROTTLE': [], 'SPARK': [] , 'FAN': [] , 'WASTEGATE': [] , 'OIL_PUMP': []}           # stores clases instances
        OUTPUT_classes_map = {'GAS_VALVE' : Turbine.Gas_valve, 'THROTTLE': Turbine.Throttle, 'SPARK':Turbine.Ignition , 'WASTEGATE': Turbine.Wastegate , 'OIL_PUMP': Turbine.Oil_pump  }                # hashes classes adreses against their shortcuts

        Devices_creator =   File_reader.Devices_creator(INPUT_file_path, OUTPUT_file_path)

        INPUT_devices_instances  = Devices_creator.prepare_devices_to_launch(Devices_creator.input_file, INPUT_devices_data, INPUT_devices_instances, INPUT_classes_map)
        OUTPUT_devices_instances = Devices_creator.prepare_devices_to_launch(Devices_creator.output_file, OUTPUT_devices_data, OUTPUT_devices_instances, OUTPUT_classes_map)

        Turbine.d.set_labjack()
        return INPUT_devices_instances + OUTPUT_devices_instances

    def Start_threads( self, devices_instances, recorder, exporter ):

        launcher    = Threads_Manager.Measure_and_control()
        commander   = Threads_Manager.Command()

        measure_control_thread  =   threading.Thread(target = launcher.launch, args=(operating_devices, recorder, ) )
        command_thread          =   threading.Thread(target = commander.simple_command, args=(exporter, )) # LAter on we can add start commands
       
        measure_control_thread.start()      
        command_thread.start()


starter = Start()
operating_devices = starter.Get_devices_to_launch()
recorder = Database_manage.Record() 
exporter = Database_manage.Export( ["Turbine", "History"], operating_devices )   # sending history start_dir_list

starter.Start_threads( operating_devices, recorder, exporter )





