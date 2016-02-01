#!/usr/bin/python
#sip (Shell In Python), for Operating Systems (CS444)
import os, sys, signal, errno
from socket import gethostname
from getpass import getuser
import parser
import builtins

#########################################
# MAIN SHELL
########################################

def sip():
  print("\n           Welcome to sip (Shell In Python)!\n")

  hostname = gethostname()
  username = getuser()
  homedir = os.environ['HOME']

  while True:
    #Prepare prompt
    cwd = os.getcwd()
    cwd = cwd.replace(homedir, '~', 1) #Collapse home directory to ~
    prompt = "%s@%s:%s$ " %(username, hostname, cwd)

    #Get command line and print prompt
    line = raw_input(prompt)

    #Put commands into history
    if len(hist) < 100:
      hist.append(line)
    else:
      hist.pop(0)
      hist.appendi(line)

    #Parse command line into commands
    cmd, args, instream, outstream, background = parser.parse(line)

    #Check if the command is a builtin
    if parser.isbuiltin(cmd):
      getattr(sys.modules[__name__], cmd)(args)

    #Check if command is a history call.
    elif cmd[0] == '!':
      repeat(int(cmd[1:]))

    #If command is external,
    else:
      try:
        childPid = os.fork() #Create new process.

        if childPid == 0: 
          os.execvp(cmd, ([cmd]+args)) #If child, execute

        else:
          if background: #If the process is background, don't wait, and append to the list.
            signal.signal(signal.SIGCHLD, reaper)
            joblist.append((childPid, cmd))

          else: #If the process is no background, wait for it.
            ecode = os.waitpid(childPid, 0)

      except OSError as e:
        print e.strerror

def reaper(sig, stack):
  os.waitpid(-1, os.WNOHANG)

###########################################
# BUILT IN FUNCTIONS
###########################################

#Change directory                                                                            
def cd(args):                                                                             
  if len(args) == 0:                                                                      
    os.chdir(os.environ['HOME'])                                                          
  elif args[0] == '~':                                                                    
    os.chdir(os.environ['HOME'])                                                          
  else:                                                                                   
    os.chdir(str(args[0]))                                                                
                                                                                          
#Print current working directory                                                             
def pwd(args):                                                                            
  print os.getcwd()                                                                       
                                                                                          
#Print history                                                                               
def history(args):                                                                        
  for index, item in enumerate(hist):                                                     
    print ("%d      %s" %(index, item))                                                   
                                                                                          
def repeat(num):                                                                          
      if((len(hist)-1) < num):                                                            
        print "No such command in history"                                                
      else:                                                                               
        if num < 0:                                                                       
          ref = (len(hist)-1) + num                                                       
        else:                                                                             
          ref = num                                                                       

#list current jobs
def jobs(args):

    #Update backgroun job list
    for job in joblist:
      try:
        os.kill(job[0], 0)
      except OSError as e:
        if e.errno == errno.ESRCH:
          joblist.remove(job)
        continue

    print "#    PID     COMMAND"
    for index, item in enumerate(joblist):
      print ("%d    %s    %s" %(index, item[0], item[1]))
                                                                                        
#Kill numbered process                                                                       
def kill(args):
  try:
    if args[0] == '%':
      os.kill(joblist(args[1:])[0], signal.SIGKILL)
    else:                                                                           
      os.kill(int(args[0]), signal.SIGKILL)
    
  except OSError as e:
      print e.strerror
                                                                                          
#Print help                                                                                  
def help(args):                                                                           
  return None                                                                             
                                                                                          
#Exit                                                                                     
def exit(args):
  if len(joblist) > 0:
    print "There are jobs running in the background. Please kill them!"
  else:
    print "Thanks having a sip."
    sys.exit()                                                                             

#########################################
#Hook for executing shell.
#########################################
if __name__ == "__main__":
  hist = list()
  joblist = list()
  sip()
