# Class containing the current state of the shell, for instance history, jobs, etc.
import errno
from os.path import isfile
from os import makedirs, environ, remove, kill

class ShellState:
  home = environ['HOME']
  histfile = home + '/.sip/siphistory'
  maxhist = 100
 
#Initialize with empty lists, and attempt to load history from file. 
  def __init__(self):
    self.hist = list()
    self.jobs = list()
    self.hist = self.loadhistory()

# Cleans up the shell state while saving history to file.
  def __del__(self):
    with open(self.histfile, 'w') as f:
      for entry in self.hist:
        f.write(entry +'\n')


#Load history from a file in HOME
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
    
# Update the history with a new entry
  def updatehistory(self, entry):
    if len(self.hist) < self.maxhist:
      self.hist.append(entry) 
    else:
      self.hist.pop(0)
      self.hist.append(enry)

##Clear history and overwrite file.
  def clearhistory(self):
    remove(self.histfile)
    (open(self.histfile, 'w')).close()
    self.hist = self.loadhistory()

#Add job to background list
  def addjob(self, pid, name):
    self.jobs.append((pid, name))
  
#Update jobs to keep the list of background jobs acurate
  def updatejobs(self):
    for job in self.jobs:                                                                     
      try:                                                                                  
        kill(job[0], 0)                                                                  
      except OSError as e:                                                                
        if e.errno == errno.ESRCH:                                                        
          self.jobs.remove(job)                                                          
          continue   
