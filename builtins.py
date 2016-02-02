import os
###########################################                                               
# BUILT IN FUNCTIONS                                                                      
###########################################                                               
                                                                                          
#Change directory                                                                            
def cd(state, cmd):
  if len(cmd.args) == 0:                                                                      
    os.chdir(os.environ['HOME'])                                                          
  elif cmd.args[0] == '~':                                                                    
    os.chdir(os.environ['HOME'])                                                          
  else:                                                                                   
    os.chdir(str(cmd.args[0]))                                                                
                                                                                          
#Print current working directory                                                             
def pwd(state, cmd):                                                                            
  print os.getcwd()                                                                       
                                                                                          
#Print history                                                                               
def history(state, cmd):                                                                        
  for index, item in enumerate(state.hist):                                                     
    print ("%d      %s" %(index, item))                                                   

def clear(state, cm):
  state.clearhistory()
  print "History cleared!"
                                                                                          
def repeat(state,cmd):
      num = cmd[1:]
      if((len(state.hist)-1) <num):                                                            
        print "No such command in history"                                                
      else:                                                                               
        if num < 0:                                                                       
          ref = (len(state.hist)-1) + num                                                       
        else:                                                                             
          ref = num                                                                       
                                                                                          
#list current jobs                                                                        
def jobs(state, cmd):                                                                           
                                                                                          
    #Update backgroun job list                                                            
    for job in state.jobs:                                                                   
      try:                                                                                
        os.kill(job[0], 0)                                                                
      except OSError as e:                                                                
        if e.errno == errno.ESRCH:                                                        
          state.jobs.remove(job)                                                             
        continue                                                                          
                                                                                          
    print "#    PID     COMMAND"                                                          
    for index, item in enumerate(state.jobs):                                                
      print ("%d    %s    %s" %(index, item[0], item[1]))                                 
                                                                                          
#Kill numbered process                                                                       
def kill(state, cmd):                                                                           
  try:                                                                                    
    if cmd.args[0] == '%':                                                                    
      os.kill(state.jobs(cmd.args[1:])[0], signal.SIGKILL)                                       
    else:                                                                                 
      os.kill(int(cmd.args[0]), signal.SIGKILL)                                               
                                                                                          
  except OSError as e:                                                                    
      print e.strerror                                                                    
                                                                                          
#Print help                                                                                  
def help(state, cmd):                                                                           
  return None                                                                             
                                                                                          
#Exit                                                                                     
def exit(state, cmd):                                                                           
  if len(state.jobs) > 0:                                                                    
    print "There are jobs running in the background. Please kill them!"                   
  else:                                                                                   
    print "Thanks having a sip."                                                          
    sys.exit()            
