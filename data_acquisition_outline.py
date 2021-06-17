

def take_data(iterations, samp_rate, filename):
  
  # initialize task and configurations
  task_init()
  
  # measure ramp time
  time = meas_ramp_time()
  
  # create data array
  data = create_array(iterations, samp_rate, time)
  
  # loop for iterations
  
# function code mostly here
  
  # write data to file
  write_file(filename, data)
  
  pass

def task_init():
  pass

def meas_ramp_time():
  pass

def create_array(iterations, samp_rate, time):
  pass

def write_file(filename, data):
  pass
