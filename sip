#!/usr/bin/python
#sip (Shell In Python), for Operating Systems (CS444)
import os, sys, signal, errno
from socket import gethostname
from getpass import getuser
import parser
import builtins
from shellstate import ShellState
from cmdinfo import CmdInfo

#########################################
# MAIN SHELL
########################################

def sip():
  print("\n           Welcome to sip (Shell In Python)!\n")
  #initialize state
  state = ShellState()
 
  #initiialize hostname, username, and home variables
  hostname = gethostname()
  username = getuser()
  homedir = os.environ['HOME']

  try:
    while True:
      #Prepare prompt
      cwd = os.getcwd()
      cwd = cwd.replace(homedir, '~', 1) #Collapse home directory to ~
      prompt = "%s@%s:%s$ " %(username, hostname, cwd)

      #Get command line and print prompt
      line = raw_input(prompt)
  
      #Update history
      state.updatehistory(line)

      #Parse command line into commands
      cmd = parser.parse(line)

      #execute command
      run(state, cmd)

  except KeyboardInterrupt as e:
    print '\n'
    exit()

def run(state, cmd):
  #Check if the command is a builtin                                                  
  if parser.commandtype(cmd.name) == 'builtin':                                       
    (getattr(builtins, cmd.name)(state, cmd))                                         
                                                                                          
  #Check if command is a history call.                                                
  elif parser.commandtype(cmd.name) == 'historyrepeat':                               
    builtins.repeat(state, cmd)                                                       
                                                                                          
  #If command is external,                                                            
  else:                                                                               
    try:
      childPid = os.fork() #Create new process.                                                                          
      if childPid == 0:                                                               
        updateio(cmd.instream, cmd.outstream)
        os.execvp(cmd.name, ([cmd.name]+cmd.args)) #If child, execute                    
                                                                                             
      else:                                                                              
        if cmd.background: #If the process is background, don't wait, and append to the list.
          signal.signal(signal.SIGCHLD, reaper)                                          
          state.addjob(childPid, cmd.name) 
                                                                                          
        else: #If the process is no background, wait for it.                          
          ecode = os.waitpid(childPid, 0)

#      updateio(sys.__stdin__, sys.__stdout__)
                                                                                          
    except OSError as e:                                                              
      print e.strerror

def updateio(instream, outstream):
  if instream != None:
    os.dup2(instream.fileno(), 0)
  if outstream != None:
    os.dup2( outstream.fileno(), 1)

def reaper(sig, stack):
  os.waitpid(-1, os.WNOHANG)

#########################################
#Hook for executing shell.
#########################################
if __name__ == "__main__": 
  sip()

else:
  print "This module cannot be imported"
