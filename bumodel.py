import xml.etree.ElementTree as xml  #holds our database object
from os import path                  #for checking if the xml file exists
import sys                           #allows us to abort if there is an issue

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
  #        and leaves it.
  #  @param self The current instance pointer
  def __init__(self):
    if not path.exists('PyBakUP.xml'): #if the file doens't exist lets make it and set defaults
      root = xml.Element('backdb')
      root.append(xml.Element('bl'))
      file = open('PyBakUP.xml', 'wb')
      xml.ElementTree(root).write(file)
      file.close()
    self._XmlTree = xml.parse('PyBakUP.xml')#parse our tree


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
      self._XmlTree.write(file)
    except:
      print("unable to save - xml tree is corrupt")
    finally:
      file.close()

  ## Add a new backup item to our database.
  #  @pre  We must give either a file or folder.
  #  @post The new backup item is created and added to the element tree
  #  @param self The current instance pointer
  #  @param itemLocation a file on the disk to be inserted into the backup list
  #  @param itemType should be either file or folder
  #  @param itemName the name that will be displayed to the user
  #  @retval bool true if element was inserted false otherwise
  #
  #  @brief A folder or file is added to our back up list.
  #  This includes adding the source, name, and type to the back up item
  #  It doesn't actually perform the insert until it is confirmed that the new entry
  #  isn't a duplicate.
  def AddBackUpItem(self, itemLocation, itemType,itemName):
    bl = self._XmlTree.getroot().find('bl')
    backupList = bl.findall('bi')

    if itemType != 'folder' and itemType != 'file':
      return False #we had a bad entry

    #check to see if the backup item was already in the tree
    #if it was, exit the function
    for backupItem in backupList:
      item = backupItem.find('folder')
      
      if item == None:#if item isn't a folder then it MUST be a file
        item = backupItem.find('file')

      try:
        if item.attrib['src'] == itemLocation or item.text == itemName:
          return False
      except AttributeError:
        print("Bad xml error couldn't parse db")
        sys.exit(1)#we need to abort and not save our db
          
                         
    #if we reached here, the src wasn't already being backed up
    #so we add it to the list
    newItem = xml.Element('bi')
    newFolder = xml.Element(itemType)
    newFolder.attrib['src'] = itemLocation
    newFolder.text = itemName
    newItem.append(newFolder)
    bl.append(newItem) #add the item to our back up list
    return True
  

  ## Get a detailed list of elements in the database.
  #  @pre  The tree must not be corrupt
  #  @post None
  #  @param self The current instance pointer
  #  @retval dicitonary The elements in the backup list are placed inside this dictionary 
  #                     of tuples containing the elements data. 
  #
  #  @brief This function is used to get detailed information about the items in the backup
  #         list. It gives the program a way to take all the attributes associated with
  #         a given node and apply it to however is necessary. The dictionary is indexed
  #         by the nodes text value.
  def GetBackUpList(self):
    bl = self._XmlTree.getroot().find('bl')
    backupList = bl.findall('bi')
    #the list we of all file/folder names
    backupListValues = {}
    
    for backupItem in backupList:
      itemType = 'folder'#will be used for building the info tuple
      item = backupItem.find(itemType)

      if item == None:
        itemType = 'file'
        item = backupItem.find(itemType)        

      #there can be much more added to our tuple
      #we just must make sure that if a value isn't set to 
      #add a default value
      itemData = itemType, item.attrib['src']
      backupListValues[item.text] = itemData

    return backupListValues

  ## Remove a backup item from the database.
  #  @pre  The xml structure must be intact
  #  @post The internal xml tree is modified such that
  #        the backup item sent is no longer in the tree
  #  @param self The current instance pointer
  #  @param itemName the text of the item being removed
  #  @param itemType the type either file or folder for looking up values
  #
  #  @brief This function gives a way of deleting an item from out
  #         xml database. It only deletes backup items.
  def RemoveBackUpItem(self, itemName, itemType):
    bl = self._XmlTree.getroot().find('bl')
    backupList = bl.findall('bi')
    
    for backupItem in backupList:
      item = backupItem.find(itemType)
      if item != None and item.text == itemName:
        print("@nremoving item\n")
        bl.remove(backupItem)
        break

  ## Modify an attribute for a backup item
  #  @pre  The xml structure must be intact, the element should
  #        have the given attribute.
  #  @post The element tree is modified so the backup item with the text
  #        provided will have a modified attribute set to the value passed
  #        to this function.
  #  @param self The current instance pointer
  #  @param itemName The name of the item being modified
  #  @param attribute The attribute of the item being modifiied
  #  @param attributeValue The new value of the attribute
  #  @retval bool This will be true if the attribute was successfully set, false otherwise
  #  @brief This function allows us to make changes to the database so that
  #         any attribute can be modified for the backup items. Basically,
  #         these items are used to determine the settings for an element. This allows us
  #         to change them as needed.
  #  @todo Implement this function
  def ModifyBackupItemAttribute(self, itemName, attribute, attributeValue):
    raise NotImplementedError('This is not implemented yet')

''''''''''''''''''
'''DELETE BELOW'''
''''''''''''''''''
#temporary interface to the model
#for the first tests of functionality
#will be deleted
model = Model()

again = True
while again:
  backupItems = model.GetBackUpList()
  for item in sorted(backupItems, key = lambda item: item.lower()):
    print (item)

  action = input('Command:')                

  if action == 'add':
    itemType = input('type:')
    location = input('location:')
    name = input('name:')
    model.AddBackUpItem(location, itemType, name)
  elif action == 'save':
    model.Save()
  elif action == 'remove':
    itemName = input('name')
    model.RemoveBackUpItem(itemName, backupItems[itemName][0])
  elif action == 'quit':
    again = False
  elif action == 'mod':
    model.ModifyBackupItemAttribute('','','')

