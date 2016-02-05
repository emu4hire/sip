import os, signal, errno, sys
from sip import run
from parser import parse
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

#Clear history
def rmhistory(state, cm):
  state.clearhistory()
  print "History cleared!"

def clear(state, cm):
  sys.stderr.write("\x1b[2J\x1b[H")

#Repeat an item from history                                                                                          
def repeat(state,cmd):
      num = int(cmd.name[1:])
      if((len(state.hist)-1) <num):                                                            
        print "No such command in history"                                                
      else:                                                                               
        if num < 0:                                                                       
          ref = (len(state.hist)-1) + num
          line = state.hist[ref]
        else:                                                                             
          ref = num
          line = state.hist[ref]
        
        state.updatehistory(line)
        command = parse(line)
        run(state, command)
                                                                                          
#list current jobs                                                                        
def jobs(state, cmd):                                                                           
  state.updatejobs()                                                                      
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
  print "\n "
  print "                         SHELL IN PYTHON"
  print "-------------------------------------------------------------------------"
  print "   cd         -- Changes directory"
  print "   pwd        -- Print current working directory to std out"
  print "   history    -- Print current history"
  print "   !n         -- repate command n from history"
  print "   rmhistory  -- Clear history"
  print "   jobs       -- List currently background jobs"
  print "   kill       -- Kill the process with the PID given, or the position n on the list if the input is %n"
  print "   clear      -- Clear terminal"
  print "   exit       -- Exit the shell, assuming that no background processes are currently running"
                                                                                          
#Exit                                                                                     
def exit(state, cmd):                                                                          
  state.updatejobs()
  if len(state.jobs) > 0:                                                                    
    print "There are jobs running in the background. Please kill them!"                   
  else:                                                                                   
    print "Thanks having a sip."                                                          
    sys.exit()            
