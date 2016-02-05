# Parser for sip
# Author:Michael Fulton
# Licensed Under the MIT License (full details in LICENSE)
from cmdinfo import CmdInfo

# Parses a line with space seperated commands, and create a command info object to represent it.
def parse(line):
  tokens = line.split()
  args = list()
  instream = None
  outstream = None
  background = False
  skip = False

  for index, item in enumerate(tokens[1:]):
    #IF skip is set, this means that the next token has already been handled, and can be skipped.
    if skip:
      continue
    #Recognize if input redirect is called for, and open the file object.
    elif item == '<':
      infile = tokens[index+2]
      try:
        instream = open(infile, 'r')
      except IOError as e:
        print "No such file exists.  Standard in will be used"
        instream = None
      skip = True

    #Recognize if output redirect is called for, and open the file object.
    elif item == '>':
      outfile = tokens[index+2]
      try:
        outstream = open(outfile, 'w')
      except IOError as e:
        outstream = None
      skip = True

    #REcognize if the process is to be backgrounded
    elif item == '&':
      background = True

    #If this argument is nothing else, append it to the argument list.  This includes the first 
    # toekn, which is also added to the object as the name of the command.
    else:
      args.append(item)

  return CmdInfo(tokens[0], args, instream, outstream, background)

#Return the command type which was passed, (if None is returned, it is an external command)
def commandtype(cmd):
  if cmd.lower() == 'cd':
    return 'builtin'
  elif cmd.lower() == 'pwd':
    return 'builtin'
  elif cmd.lower() == 'history':
    return 'builtin'
  elif cmd.lower() == 'rmhistory':
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
