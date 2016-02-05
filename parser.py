# Parser for sip
# Author:Michael Fulton
# Licensed Under the MIT License (full details in LICENSE)
from cmdinfo import CmdInfo

def parse(line):
  tokens = line.split()
  args = list()
  instream = None
  outstream = None
  background = False
  skip = False

  for index, item in enumerate(tokens[1:]):
    if skip:
      continue
    elif item == '<':
      infile = tokens[index+1]
      try:
        instream = open(infile, 'r')
      except IOError as e:
        instream = None
      skip = True
    elif item == '>':
      outfile = tokens[index+1]
      try:
        outstream = open(outfile, 'r')
      except IOError as e:
        outstream = None
      skip = True
    elif item == '&':
      background = True
    else:
      args.append(item)

  return CmdInfo(tokens[0], args, instream, outstream, background)

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
