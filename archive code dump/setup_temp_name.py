'''
Structure of gui task creator:
    - Task
        - name
        - Channels
            - ai
            - ci?
        - timing
            - sample clk timing
                - rate
                - finite vs continuous aquisition
                - samples per channel
            - change detection timing
        - triggering
            - analog edge start
            - analog window start
            - digital edge start
        
        - save structure and location

- needs to create a sample log file maybe .json?
- use python dictionary to log config
'''
task_config = {'name': None, 'channels': None, 'timing' : None}