#sip (Shell In Python), for Operating Systems (CS444)
import os
import parser
import sys
from socket import gethostname
from getpass import getuser

def sip():
  print("\n           Welcome to sip (Shell In Python)!\n")

  hostname = gethostname()
  username = getuser()
  homedir = os.environ['HOME']

  while True:
    #Prepare prompt
    cwd = os.getcwd()
    cwd = cwd.replace(homedir, '~', 1) #Collapse home directory to ~
    prompt = "  %s@%s:%s$ " %(username, hostname, cwd)

    #Get command line and print prompt
    line = raw_input(prompt)

    #Put commands into history
    if len(hist) < 100:
      hist.append(line)
    else:
      hist.pop(0)
      hist.append(line)

    #Parse command line into commands
    cmd, args, instream, outstream, background = parser.parse(line)

    #Check if the command is a builtin
    if parser.isbuiltin(cmd):
      getattr(sys.modules[__name__], cmd)(args)
    else:
      childPid = os.fork()
      if childPid == 0:
        os.execvp(cmd, ([cmd]+args))
      else:
        if background:
          continue
        else:
          os.waitpid(childPid, 0)

    #If the command is exit, exit

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

#Kill numbered process
def kill(args):
  return None

#Print help
def help(args):
  return None

#Exit
def exit(args):
  sys.exit()
  return None

#Hook for executing shell.
if __name__ == "__main__":
  hist = list()
  sip()
