import xml.etree.ElementTree as xml #holds our database object
from os import path #for checking if the xml file exists

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
  #pre:  We should have a valid xmltree to be saved
  #post: The current version of the db is saved - incase there is some issue
  def save(self):
    file = open('PyBakUP.xml', 'wb')
    self._XmlTree.write(file)
    file.close()

  #AddBackUpItem
  #PARAM self the object
  #PARAM itemLocation a file on the disk to be inserted into the backup list
  #PARAM itemName the name that will be displayed to the user
  def AddBackUpItem(self, itemLocation, itemName):

    bl = self._XmlTree.getroot().find('bl')
    backupList = bl.findall('bi')
    #check to see if the backup item was already in the tree
    #if it was, exit the function
    for backupItem in backupList:
      folder = backupItem.find('folder')
      if folder.attrib['src'] == itemLocation:
        return
                         
    #if we reached here, the src wasn't already being backed up
    #so we add it to the list
    newItem = xml.Element('bi')
    newFolder = xml.Element('folder')
    newFolder.attrib['src'] = itemLocation
    newFolder.text = itemName
    newItem.append(newFolder)
    bl.append(newItem) #add the item to our back up list

#temporary interface to the model
#for the first tests of functionality
#will be deleted
model = Model()
loc = input('location')
name = input('name')
model.AddBackUpItem(loc, name)
model.save()
