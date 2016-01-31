# Parser for sip
# Author:Michael Fulton
# Licensed Under the MIT License (full details in LICENSE)

def parse(line):
  return line.split()

def isbuiltin(cmd):
  if cmd.lower() == 'cd':
    return True
  elif cmd.lower() == 'pwd':
    return True
  elif cmd.lower() == 'history':
    return True
  elif cmd.lower() == 'kill':
    return True
  elif cmd.lower() == 'help':
    return True
  elif cmd.lower() == 'exit':
    return True
  else:
    return False
