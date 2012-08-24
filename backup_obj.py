import os.path
import datetime

class BackupObject(object):

  def __init__(self, id, **args):
    #Set values that must be there
    self._Name = ""
    self._Description = ""
    self._Location = ""
    self._Backup = lambda: return true
    self._LastBackup =  datetime.datetime.now
    self._Group = "default"
    self._Id = id
    #initialize all values passed to the obj
    for key in args:
      exec('self._' + key + '=' + args[key])

  @property
  def Name(self):
    return self._Name

  @Name.setter
  def Name(self, newName):
    self.Name = _newName

  @property
  def Description(self):
    return self._Description

  @Description.setter
  def Description(self, newDescription):
    self.Description = _newDescription

  @property
  def Location(self):
    return self._Location

  @Location.setter
  def Location(self, newLocation):
    self._Location = newLocation

  @property
  def Backup(self):
    return _Backup()

  @Backup.setter
  def Backup(self, newBackupFunc):
    self._Backup = newBackupFunc

  @property
  def LastBackup(self):
    return self._LastBackup

  @LastBackup.setter
  def LastBackup(self, newBackupTime):
    self._LastBackup = newBackupTime

  @property
  def Group(self):
    return self._Group

  @Group.setter
  def Group(self, newGroup):
    self._Group = newGroup

  @property
  def ID(self):
    return self._Id
