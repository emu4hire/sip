#sip (Shell In Python), for Operating Systems (CS444)
import os
from socket import gethostname
from getpass import getuser

print "\nWelcome to sip (Shell In Python)! \n"

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

  #Parse command line into commands

  #Echo out the parsed commands

  #If the command is exit, exit
  

  
