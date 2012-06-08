import xml.etree.ElementTree as xml  #holds our database object
from os import path                  #for checking if the xml file exists

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

TODO - Figure out most elegent way to create a singleton so that we aren't having to 
       worry about multiple instances of our db, that way we don't have undefined exit behavior
'''
class Model:
  #member vars
  _XmlTree = None
  #end member vars

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
    self._XmlTree.write(file)
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
    #check to see if the backup item was already in the tree
    #if it was, exit the function
    for backupItem in backupList:
      item = backupItem.find(itemType)
      if folder.attrib['src'] == itemLocation:
        return
                         
    #if we reached here, the src wasn't already being backed up
    #so we add it to the list
    newItem = xml.Element('bi')
    newFolder = xml.Element(itemType)
    newFolder.attrib['src'] = itemLocation
    newFolder.text = itemName
    newItem.append(newFolder)
    bl.append(newItem) #add the item to our back up list

  
  #TODO We need to set up an array of tuples so we can send back all pertinate info
  #     with the list
  #GetBackUpList
  #PARAM self the object
  #RETURN list of elements that are to be backed up. This can be used for display
  #       or any other purpose we need the elements for. The list is sorted
  def GetBackUpList(self):
    bl = self._XmlTree.getroot().find('bl')
    backupList = bl.findall('bi')
    #the list we of all file/folder names
    backupListValues = []
    for backupItem in backupList:
      itemType = "folder"#will be used for building the info tuple
      item = backupItem.find(itemType)
      if item == None:
        itemType = "file"
        item = backupItem.find(itemType)        
      backupListValues.append(item.text)
      backupListValues.sort()
    return backupListValues

''''''''''''''''''
'''DELETE BELOW'''
''''''''''''''''''
#temporary interface to the model
#for the first tests of functionality
#will be deleted
model = Model()
checkList = model.GetBackUpList()
print (checkList)
model.Save()
