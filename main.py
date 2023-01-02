import shutil       #For roots
import os           #For all OS
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from multiprocessing import Process
from tkinter import simpledialog
from subprocess import Popen

root = Tk(baseName="Filesync")
root.geometry("1000x500")
root.title("Synchronizer")
root['bg']='RoyalBlue1'
class App(Frame):

  def __init__(self, master):
    super().__init__(master)
    self.pack()
    self.add_btn = Button(master, text="Create File", command=self.create_file)
    self.add_btn.pack()
    self.del_btn = Button(master, text="Delete File", command=self.delete_file)
    self.del_btn.pack()
    self.rename_btn = Button(master, text="Rename File",command=self.rename_file)
    self.rename_btn.pack()
    self.refresh_btn=Button(master, text="List Files(refresh)", command=self.list_files)
    self.refresh_btn.pack()
    self.dirA = filedialog.askdirectory(mustexist=True)
    self.dirB = filedialog.askdirectory(mustexist=True)
    self.files = Variable(value=os.listdir(self.dirA))
    self.filebox = Listbox(master, height=10, listvariable=self.files)
    self.filebox.pack()
    self.files2 = Variable(value=os.listdir(self.dirB))
    self.filebox2=Listbox(master, height=10, listvariable=self.files2)
    self.filebox2.pack()

  def create_file(self):
    filename = simpledialog.askstring("Create File", "Enter filename")
    while filename in os.listdir(self.dirA):
      messagebox.showerror("Error", "A File with the same name already exists!")
      filename = simpledialog.askstring("Create File", "Enter filename")
    if filename is not None:
      file = open(os.path.join(self.dirA, filename), 'w').close()
      shutil.copy2(os.path.join(self.dirA, filename),os.path.join(self.dirB, filename)) #copy2 copy ccopies with metadata
    self.files.set(os.listdir(self.dirA))
    self.files2.set(os.listdir(self.dirB))
    
  def list_files(self):
      self.files.set(os.listdir(self.dirA))
      self.files2.set(os.listdir(self.dirB))
     #list/refresh files in GUI

  def delete_file(self):
    #will raise IndexError if nothing is selected
    
    try:
        file = self.files.get()[self.filebox.curselection()[0]]
        os.remove(os.path.join(self.dirA, file))
        os.remove(os.path.join(self.dirB, file))
    except IndexError:
        file = self.files2.get()[self.filebox2.curselection()[0]]
        os.remove(os.path.join(self.dirA, file))
        os.remove(os.path.join(self.dirB, file))
    self.files.set(os.listdir(self.dirA))
    self.files2.set(os.listdir(self.dirB))
  def rename_file(self):
    #will raise IndexError if nothing is selected
    try:
        file = self.files.get()[self.filebox.curselection()[0]]
    except IndexError:
        file = self.files2.get()[self.filebox2.curselection()[0]]
    new_filename = simpledialog.askstring("Rename file", "Enter new filename")
    while new_filename in os.listdir(self.dirA):
        messagebox.showerror("Error", "A file with the same name already exists!")
        new_filename = simpledialog.askstring("Rename file", "Enter new filename")
    if new_filename is not None:
        new_filepath = os.path.join(self.dirA, new_filename)
        os.rename(os.path.join(self.dirA, file), new_filepath)
        os.rename(os.path.join(self.dirB, file), os.path.join(self.dirB, new_filename))
        self.files.set(os.listdir(self.dirA))
        self.files2.set(os.listdir(self.dirB))
        
        

app = App(root)
p = Popen(['python', 'sync.py', app.dirA, app.dirB])
root.mainloop()
p.kill()