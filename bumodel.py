import xml.etree.ElementTree as xml  #holds our database object
from os import path                  #for checking if the xml file exists
import sys                           #allows us to abort if there is an issue

'''
This class maintains interactions between the program and the database
It takes the xml database we create and builds our element tree.
Once we have that we can run queries on it and allow for varied settings on all
back up items in the database.
It handles reading and writing to and from our database file.
This will be used by our two main driver programs.
The first is that allows user interactions with the database file, and the second
is the one that is run to actually complete the backup process.
Since it will be the common api it will save a lot of the work of duplicate programming

Created: Barrett Lewis
Date: 5/7/2012
PyBakUP
'''
class Model:

#==================#
  #member vars     #
  _XmlTree = None  #
  #end member vars #
#==================#

  #constructor
  #pre: None
  #post: Ensures the the file PyBakUP.xml exists - and if it doesn't creates it
  #      and leaves it.
  def __init__(self):
    if not path.exists('PyBakUP.xml'): #if the file doens't exist lets make it and set defaults
      root = xml.Element('backdb')
      root.append(xml.Element('bl'))
      file = open('PyBakUP.xml', 'wb')
      xml.ElementTree(root).write(file)
      file.close()
    self._XmlTree = xml.parse('PyBakUP.xml')#parse our tree


  #save
  #This function allows us to save the tree to an xml database.
  #It essentially overwrites the whole file because the tree in memory
  #is the most recent version
  #pre:  We should have a valid xmltree to be saved
  #post: The current version of the db is saved - incase there is some issue
  def Save(self):
    file = open('PyBakUP.xml', 'wb')

    try:
      self._XmlTree.write(file)
    except:
      print("unable to save - xml tree is corrupt")
      file.close()
      sys.exit(1)

    file.close()


  #AddBackUpItem
  #A folder or file is added to our back up list.
  #This includes adding the source, name, and type to the back up item
  #PARAM self the object
  #PARAM itemLocation a file on the disk to be inserted into the backup list
  #PARAM itemType should be either file or folder
  #PARAM itemName the name that will be displayed to the user
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
  

  #GetBackUpList
  #PARAM self the object
  #RETURN dicitonary of elements that are to be backed up. This can be used for display
  #       or any other purpose we need the elements for. The list is NOT sorted
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

  #RemoveBackupItem
  #pre:  The xml structure must be intact
  #post: The internal xml tree is modified such that
  #      the backup item sent is no longer in the tree
  #This function gives a way of deleting an item from out
  #xml database. It only deletes backup items.
  #PARAM self the current object
  #PARAM itemName the text of the item being removed
  #PARAM itemType the type either file or folder for looking up values
  def RemoveBackUpItem(self, itemName, itemType):
    bl = self._XmlTree.getroot().find('bl')
    backupList = bl.findall('bi')
    
    for backupItem in backupList:
      item = backupItem.find(itemType)
      if item != None and item.text == itemName:
        print("\nremoving item\n")
        bl.remove(backupItem)
        break



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
