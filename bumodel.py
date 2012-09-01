import xml.etree.ElementTree as xml  #holds our database object
from os import path                  #for checking if the xml file exists
import sys                           #allows us to abort if there is an issue
from backup_obj import BackupObject

## @package bumodel
#  This contains the definitions for our model object.
#
#  This package holds the classes used for maintaining our data structure and
#  local database.
#  @author Barrett Hostetter-Lewis
#  @date   5/7/2012
                   
## The data model.
#  This class maintains interactions between the program and the database.
#
#  It takes the xml database we create and builds our element tree.
#  Once we have that we can run queries on it and allow for varied settings on all
#  back up items in the database.
#  It handles reading and writing to and from our database file.
#  This will be used by our two main driver programs.
#  The first is that allows user interactions with the database file, and the second
#  is the one that is run to actually complete the backup process.
#  Since it will be the common api it will save a lot of the work of duplicate programming
class Model:

  ## @var _XmlTree 
  #  The xml element tree
  _XmlTree = None


  ## The constructor.
  #  @pre  None
  #  @post Ensures the the file PyBakUP.xml exists - and if it doesn't creates it
  #        and saves it.
  #  @param self The current instance pointer
  #  @todo Decide whether or not to save on a bad parse (my assumption is that we have a bad xml file and i'm not sure how to recover from that yet)
  def __init__(self):
    print('running init')
    if not path.exists('PyBakUP.xml'): #if the file doens't exist lets make it and set defaults
      self._InitElementTree()  
      self.Save()
    else:
      try: #we need to attempt a parse. If there is an issue with the parse we recreate the file
        self._XmlTree = xml.parse('PyBakUP.xml')#parse our tree
      except:
        self._InitElementTree()
        self.Save() #This is up in the air

  ## Save the document.
  #  @pre  We should have a valid xmltree to be saved
  #  @post The current version of the db is saved.
  #        This function will attempt to write the element tree to the file, however
  #        if there is some form of corruption it will catch it and exit the program.
  #  @param self The current instance pointer
  #
  #  @brief This function allows us to save the tree to an xml database.
  #  It essentially overwrites the whole file because the tree in memory
  #  is the most recent version. If an exception is raised, then the program will abort
  #  after closing the file.
  def Save(self):
    file = open('PyBakUP.xml', 'wb')

    try:
      self._XmlTree.write(file, xml_declaration=True, encoding='utf-8', method='xml')
    except:
      print("unable to save - xml tree is corrupt")
    finally:
      file.close()

  ## Add a new backup item to our database.
  #  @pre  We must give either a file or folder.
  #  @post The new backup item is created and added to the element tree
  #  @param self The current instance pointer
  #  @param source A file or folder on the disk to be inserted into the backup list
  #  @param itemType Should be either file or folder
  #  @param title The name that will be displayed to the user
  #  @param description (Optional)An optional description of the backup item. Defaults to an empty string
  #  @retval bool True if element was inserted false otherwise
  #
  #  @brief A folder or file is added to our back up list.
  #  This includes adding the source, name, and type to the back up item
  #  It doesn't actually perform the insert until it is confirmed that the new entry
  #  isn't a duplicate.
  def AddBackUpItem(self, source, itemType, title, description=''):
    backupItems = self._GetAllBackupItems()

    #here we check to ensure the type was set
    #we also ensure that the source isn't already backed up
    if (itemType != 'folder' and itemType != 'file') or any(item.get('src', '') == source for item in backupItems):
      return False #we had a bad entry

    #if we reached here, the src wasn't already being backed up
    #so we add it to the list

    #create the item itself
    newItem = xml.Element('bi')
    newItem.set('type', itemType)
    newItem.set('src', source)
    #create the frequency element
    newItemFrequency = xml.Element('frequency')
    newItemFrequency.set('condition','Default')
    newItemFrequency.set('last', 'never')
    newItem.append(newItemFrequency)
    #create the title
    newTitle = xml.Element('title')
    newTitle.text = title
    newItem.append(newTitle)

    #create the description if set
    if description :
      newItemDescription = xml.Element('description')
      newItemDescription.text = description
      newItem.append(newItemDescription)

    #finally, add the newly built backup item to our element tree
    bl.append(newItem)
    return True
  

  ## Get a detailed list of elements in the database.
  #  @pre  The tree must not be corrupt
  #  @post None
  #  @param self The current instance pointer
  #  @retval 
  #
  #  @brief This function is used to get detailed information about the items in the backup
  #         list. It gives the program a way to take all the attributes associated with
  #         a given node and apply it to however is necessary. The dictionary is indexed
  #         by the items title.
  def GetBackupData(self):
    backupItems = self._GetAllBackupItems()

    for backupItem in backupItems:
      item = Model.ConvertElementToBackupObj(backupItem)
      yield item

  ## Remove a backup item from the database.
  #  @pre  The xml structure must be intact
  #  @post The internal xml tree is modified such that
  #        the backup item sent is no longer in the tree
  #  @param self The current instance pointer
  #  @param source The source that is being removed from the database
  #
  #  @brief This function gives a way of deleting an item from out
  #         xml database. It only deletes backup items.
  def RemoveBackUpItem(self, source):
    backupItems = self._GetAllBackupItems()
    
    for backupItem in backupItems:
      if backupItem.get('src') == source:
        bl.remove(backupItem)
        break

  ## Modify an attribute of a backup item
  #  @pre  The xml structure must be intact, the new attributeValue
  #        should be a valid value.
  #  @post The item of the given source will have its selected attribute changed
  #  @param self The current instance pointer
  #  @param source The source of the item that is going to be modified
  #  @param attribute The name of the attribute that is going to be modified
  #  @param attributeValue The new value of the attribute being modified
  #
  #  @brief This function gives the user a way of modify any of the valid
  #         attributes for a backup item. It handles modifying at any
  #         level of nesting that is needed for the attribute.
  def ModifyItem(self, source, attribute, attributeValue):
    backupItems = self._GetAllBackupItems()

    itemForModification = None
    for backupItem in backupItems:
      if backupItem.get('src') == source:
        itemForModification = backupItem
    
    if itemForModification == None: #ensure that we actually have an item to modify
      return

    if attribute == 'last' or attribute == 'condition': #changing frequency condition or last
      frequency = itemForModification.find('frequency')
      frequency.set(attribute, attributeValue)
    elif attribute == 'title':#changing title
      title = itemForModification.find('title')
      title.text = attributeValue
    elif attribute == 'description':#changing description
      description = itemForModification.find('description')
      description.text = attributeValue

  ## Get the backup list from the element tree.
  #  @pre  The xml structure should be intact, and there should be
  #        a backup list tag(no more than one)
  #  @post None
  #  @param self the current instance
  #  @retval element The backup liste element instance
  #
  #  @brief This function is mainly a helper for use inside of the model class
  #         by allowing a simple easy to read way of getting back the backup list
  #         element directly.                               
  def _GetBackupList(self):
    return self._XmlTree.getroot().find('bl')

  ## Get a list of all the backup items
  #  @pre  The xml structure should be intact
  #  @post None
  #  @param self The current instance
  #  @retval list All the backup items in the db are returned as elements
  #
  #  @brief  This encapsulates the process of getting all the backup items out of the db
  def _GetAllBackupItems(self):
    return self._GetBackupList().findall('bi')

  ## Initialize an empty tree
  #  @pre  The main _XmlTree variable should NOT be set at this point
  #  @post The main _XmlTree variable is now set to an empty database
  #        effictively initializing the primary database to its minimal working
  #        state.
  #  @param self The current instance
  #
  #  @brief This function is a utility function for creating and setting up a default
  #         element tree. This allows us to create a new tree on the fly when necessary.
  def _InitElementTree(self):
    root = xml.Element('backdb')
    root.append(xml.Element('bl'))
    self._XmlTree = xml.ElementTree(root)


  ## Get a backup object by name
  #  @pre  The main _XmlTree variabe should be a valid tree
  #  @post The tree is searched for a backup object with a specific name
  #        and, if found, builds the backup_obj to contain that information
  #  @param self The current instance
  #  @param name The name of the object being searched for in the db
  #  @retval Backup_Obj Contains the data from the db, and None if it wasn't in the db
  #
  #  @brief Allows access to a specific item if necessary, that way if a handle isn't
  #         available for the specific element it is still possible to get its information
  def GetItemByName(self, name):
    bl = self._GetAllBackupItems()
    result = None
    for item in bl:
      if item.find('title').text == name:
        return ConvertElementToBackupObj(item)
  

  ## Convert a backup element into a backup_obj
  #  @pre None
  #  @post None
  #  @param self The current instance
  #  @param element The element to be converted
  #  @retval Backup_Obj The converted backup element
  #
  #  @brief This function allows conversion from a backup 
  #  @TODO Backup isn't set yet - need to figure this out
  def ConvertElementToBackupObj(element):
    source =  element.get('src')
    itemType = element.get('type')
    frequency = element.find('frequency')
    condition = element.find('frequency').get('condition')
    last = element.find('frequency').get('last')
    title = element.find('title').text
    description = element.find('description').text
    result = BackupObject()#Name=title, Description=description, Location=source, LastBackup=last)
    return result

#This is a testing interface for the model
#for the first tests of functionality
if __name__ == "__main__":
  model = Model()

  again = True
  while again:
    for item in model.GetBackupData():
      print (item)

    action = input('Command:')                
                                        
    #def AddBackUpItem(self, source, itemType, title, description=''):
    if action == 'add':
      itemType = input('type:')
      location = input('location:')
      name = input('name:')
      description = input('description:')
      model.AddBackUpItem(location, itemType, name, description)
    elif action == 'save':
      model.Save()
    elif action == 'remove':
      itemName = input('name:')
      obj = self.GetItemByName(itemName)
      model.RemoveBackUpItem(obj.Location)
    elif action == 'quit':
      again = False
    elif action == 'mod':
      model.ModifyItem('c:','description','testval')
    elif action == 'print':
      itemName = input('name:')
      print(backupItems.get(itemName, ''))
  print('\n')
