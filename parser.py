# Parser for sip
# Author:Michael Fulton
# Licensed Under the MIT License (full details in LICENSE)
from cmdinfo import CmdInfo

def parse(line):
  tokens = line.split()
  args = list()
  instream = ""
  outstream = ""
  background = False
  skip = False

  for index, item in enumerate(tokens[1:]):
    if skip:
      continue
    elif item == '<':
      ins = tokens[index+1]
      skip = True
    elif item == '>':
      outs = tokens[index+1]
      skip = True
    elif item == '&':
      background = True
    else:
      args.append(item)

  return CmdInfo(tokens[0], args, background)

def commandtype(cmd):
  if cmd.lower() == 'cd':
    return 'builtin'
  elif cmd.lower() == 'pwd':
    return 'builtin'
  elif cmd.lower() == 'history':
    return 'builtin'
  elif cmd.lower() == 'clear':
    return 'builtin'
  elif cmd.lower() == "jobs":
    return 'builtin'
  elif cmd.lower() == 'kill':
    return 'builtin'
  elif cmd.lower() == 'help':
    return 'builtin'
  elif cmd.lower() == 'exit':
    return 'builtin'
  elif cmd.lower()[0] == '!':
    return 'historyrepeat'
  else:
    return None
