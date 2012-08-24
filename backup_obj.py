import os.path
import datetime

## @package BackupObject
#  This contains the definition for a backup object
#
#  @author Barrett Hostetter-Lewis
#  @date  8/23/2012

## The BackupObject class
#  This class holds all the information for a backup object
#
#  The class uses properties to track the data of the item to
#  to be backed up. Mostley a container class.
class BackupObject(object):

  ## @var __properties
  #  legal properties
  __properties = ['Name',
                  'Description',
                  'Location',
                  'Backup',
                  'LastBackup',
                  'Group',
                  'Id']

  ## Constructor
  #  @pre  There should be a valid unique id.
  #  @post The object is instantiated with the values
  #        provided.
  #  @param self The current object being constructed
  #  @param id The unquie identifier for the object
  #  @param **args arbitrary number of params with a key
  #         Name, Description, Location, Backup, Group, Id are allowed
  #  @brief Constructs the objects allowing for custom initialization
  def __init__(self, id, **args):
    #Set values that must be there
    self._Name = ""
    self._Description = ""
    self._Location = ""
    self._Backup = lambda obj: true
    self._LastBackup =  datetime.datetime.now
    self._Group = "default"
    self._Id = id
    #initialize all values passed to the obj
    for key in args:
      if key in __properties:#limit to properties that are valid
        exec('self._' + key + '=' + args[key])

  ## Name
  #  @brief Name property, allows you to get the Name variable
  #  @retval string The name of the backup item
  @property
  def Name(self):
    return self._Name

  ## Name
  #  @brief Name property, allows setting the Name variable
  @Name.setter
  def Name(self, newName):
    self.Name = _newName

  ## Description
  #  @brief Description property, allows getting the Description variable
  #  @retval string The description of the object
  @property
  def Description(self):
    return self._Description


  ## Description
  #  @brief Description property, allows setting the Description variable
  @Description.setter
  def Description(self, newDescription):
    self.Description = _newDescription

  ## Location
  #  @brief Location property, allows getting the Location variable
  #  @retval string The path to the files location
  @property
  def Location(self):
    return self._Location

  ## Location
  #  @brief Location property, allows setting the Location variable
  @Location.setter
  def Location(self, newLocation):
    self._Location = newLocation

  ## Backup
  #  @brief Backup property, allows evaluation of the Backup property
  #         This will return true or false, true if the item wants to
  #         be backed up.
  #  @retval bool True if the the item wants to be backed up, false otherwise
  @property
  def Backup(self):
    return _Backup(self)

  
  ## Backup
  #  @brief Backup property, allows setting the Backup property.
  #  This should be a function
  @Backup.setter
  def Backup(self, newBackupFunc):
    self._Backup = newBackupFunc

  ## LastBackup
  #  @brief LastBackup property, allows for getting the LastBackup date
  #  @retval datetime The datetime of the last backup
  @property
  def LastBackup(self):
    return self._LastBackup

  @LastBackup.setter
  def LastBackup(self, newBackupTime):
    self._LastBackup = newBackupTime

  ## Group
  #  @brief Group property, allows for getting the group
  #  @retval string The group name
  @property
  def Group(self):
    return self._Group


  ## Group
  #  @brief Group property, allows for setting the group
  @Group.setter
  def Group(self, newGroup):
    self._Group = newGroup

  ## ID
  #  @brief ID property, allows for getting the item ID
  #  @retval int The ID of the object, not mutable
  @property
  def ID(self):
    return self._Id
