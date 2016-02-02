from os.path import isfile
from os import makedirs, environ, remove

class ShellState:
  home = environ['HOME']
  histfile = home + '/.sip/siphistory'
  maxhist = 100
  
  def __init__(self):
    self.hist = list()
    self.jobs = list()
    self.currentprocess = -1
    self.hist = self.loadhistory()

  def loadhistory(self):
    hist = list()
    if isfile(self.histfile):
      with open(self.histfile, 'r') as f:
        for line in f:
          line = line.rstrip('\n')
          hist.append(line)
    else:
      makedirs((self.home+ '/.sip'))
      f= open(self.histfile, 'w')
      f.close()
    return hist
    
  def __del__(self):
    with open(self.histfile, 'w') as f:
      for entry in self.hist:
        f.write(entry +'\n')

  def updatehistory(self, entry):
    if len(self.hist) < self.maxhist:
      self.hist.append(entry) 
    else:
      self.hist.pop(0)
      self.hist.append(enry)

  def clearhistory(self):
    remove(self.histfile)
    (open(self.histfile, 'w')).close()
    self.hist = self.loadhistory()

  def updateprocess(self, pid):
    state.currentprocess = pid
