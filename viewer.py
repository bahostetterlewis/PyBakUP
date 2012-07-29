from tkinter import *
import bumodel

## Main function
#  This is the programs starting point
def Main():
  instance = bumodel.GetInstance()
  itemList = instance.GetBackUpData()

  master = Tk()

  listbox = Listbox(master)
  listbox.pack()
  PopulateList(listbox)

  mainloop()

## Populate the listbox with all values in the database.
#  @pre:  None.
#  @post: The model is instantiated if it hasn't been yet. The items from 
#         the database are added to the list in alphabetical order
def PopulateList(listbox):
  for item in sorted(bumodel.GetInstance().GetBackUpData(), key = lambda item: item.lower()):
    listbox.insert(END, item)


# This allows for easier to read code
if __name__ == "__main__":
  Main()
