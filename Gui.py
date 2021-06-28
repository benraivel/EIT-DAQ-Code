'''
creates a GUI window for eit experiment managment and data collection

notes: 
    - google drive data upload option using pydrive
    - gif probably easiest way to create scope feed
    - option to open experimental data viewer window with ploting functions for already collected data
    - need to pass in counter reader to control updates
'''
import tkinter as tk
from tkinter import ttk

class AppWindow(ttk.Frame):
   
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        
    def create_frames(self):
        '''
        creates four frames for the main sections of the GUI
        '''
        # create four frames for the main sections of the GUI
        self.scope_windows = ttk.Frame(self.parent)
        self.measurment_display_window = ttk.Frame(self.parent)
        self.options_window = ttk.Frame(self.parent)
        self.dialog_window = ttk.Frame(self.parent)
        
        # create paned windows for sidebar and scope channels
        self.scope_panes = ttk.PanedWindow(self.scope_windows)
        self.sidebar_panes = ttk.PanedWindow(self.parent)
        
        # add sidebar frames to paned window
        self.sidebar_panes.add(self.options_window)
        self.sidebar_panes.add(self.dialog_window)
        
        # arrange everything
        self.scope_windows.grid(column = 0, row = 0)
        self.measurment_display_window.grid(column = 0, row = 1)
        self.sidebar_panes.grid(column = 1, row = 0, rowspan = 2)
        
        
    def create_options_window(self):
        ''' 
        creates the various menu widgets in the options widow:
            - Analog Channel Manager
            - sample rate slider
                - limit determined by # of channels               
            - or spinbox and unit selector?
            - scope toggle for each signal
                - toggle to use one window?
                - offsets like oscilliscope
            - scale control for scope
            
            - data save options 
                - add notes (popup?)
                    - prompt to create README
                    - skippable but discouraged (cancel option)
                    
            - display scopes as notebook tabs?
        '''
        self.display_mode_label = ttk.Label(self.options_window, text = 'Display Signals in:')
        self.display_mode_select = ttk.Combobox(self.options_window, state = "readonly")
        
        
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    #he he