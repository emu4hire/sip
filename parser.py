# Parser for sip
# Author:Michael Fulton
# Licensed Under the MIT License (full details in LICENSE)

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

  return tokens[0], args, instream, outstream, background

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
