from tkinter import *
from time import sleep
import random
from random import randint
import sys
import os
import datetime
import json 
from tkinter.filedialog import askopenfilename
from pathlib import Path

root=Tk()
font = ("Calibri 30 bold")
class Person:
    def __init__(self, name,shot_count):
        self.name = name
        self.shot_count = shot_count

    def create_name(self,count, frame):
        name = Label(frame,text=str(self.name),font=("Calibri 30 bold"))
        name.grid(column=3,row=count,rowspan=2)
        
        label = Label(frame,text=self.shot_count,font=("Calibri 30 bold"))
        label.grid(column=0,row=count,rowspan=2)
        
        x = Label(frame,text="",font=("Calibri 30 bold"))
        x.grid(column=3,row=count+2,rowspan=2)
        
        button1 = Button(frame,text="↑",command= lambda label=label: self.increment(label))
        button1.grid(column=1,row=count)

        button2 = Button(frame,text="↓",command= lambda label=label: self.decrease(label))
        button2.grid(column=1,row=count + 1)
    

    def refreshLabel(self, label):
        if people_handler.reorder_appropriate():
            people_handler.gen_list()
        label.config(text=str(self.shot_count),font=("Calibri 30 bold"))

    def increment(self, label):
        self.shot_count = self.shot_count +1
        self.refreshLabel(label)

    def decrease(self, label):
        if self.shot_count > 0:
            self.shot_count = self.shot_count -1
        self.refreshLabel(label)

class People:
    def __init__(self):
        self.people = []
        self.home_frame = Frame(root)
        self.load_from_file(None)
        self.gen_list()
        Path("./saves").mkdir(parents=True, exist_ok=True)

    def save_to_file(self):
        dat_as_json = [{"name":x.name,"score":x.shot_count} for x in self.people]

        def format_date_better(number):
            if len(str(number)) < 2:
                return ( "0" + str(number))
            else:
                return (number)

        x = datetime.datetime.now()
        time = format_date_better(str(x.day)) + "-" + format_date_better(str(x.month))  + "-" + format_date_better(str(x.year))
        
        with open("./saves/" + str(time) +".json", "w") as f:
            f.write(json.dumps(dat_as_json, indent=4))
            
    def load_from_file(self, save_file_dr):
        if save_file_dr == None:
            file_contents = [ {"name": "Felix", "score":0} , {"name": "Nathan", "score":0},{"name": "Rob", "score":0} ]
        else:
            save_file = open(save_file_dr,"r")
            file_contents = json.load(save_file)
            
        temp = []
        for each_pair in file_contents:
            print(each_pair)
            temp.append(Person(each_pair.get("name"), each_pair.get("score")))

        if save_file_dr != None:
            self.gen_list()

        self.people = temp
        self.gen_list()

    def reorder_appropriate(self):
        # Have the numbers cahgne so the roder of naems should??
        current_order = [(person.name, person.shot_count,person) for person in self.people]
        sorted_by_shotcount = sorted(current_order, key=lambda tup: tup[1])
      #  if current_order != sorted_by_shotcount:
            #self.people = [person[2] for person in sorted_by_shotcount]
           # self.people.reverse()
           # print("CHANGE APPROPRIATE")
          #  return True
        return False
       # print(sorted_by_second)
        
    def gen_list(self):
        self.home_frame.destroy()
        self.home_frame = Frame(root)
        self.home_frame.grid(row=0,column=0)

        #Order self.people
        print("sdjkhfjkhdsfjk")

        self.count = 0
        for person in self.people:
            self.count = self.count + 4
            person.create_name(self.count, self.home_frame)
            
    def add_person(self, name):
        self.count = self.count + 4
        self.people.append(Person(name, 0))
        self.gen_list()

    def remove_person(self,person):
        print(person.name)
        self.people.remove(person)
        self.gen_list()

def choose_and_load():
    filename = askopenfilename(initialdir="./saves") # show an "Open" dialog box and return the path to the selected file
    people_handler.load_from_file(filename)

def close_popup(name, popupframe):
    popupframe.destroy()
    people_handler.add_person(name)
    
def add_a_man():
    popup = Toplevel(width=900,height=600)
    centeredFrame = Frame(popup,highlightbackground="Black", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")
    Label(centeredFrame,text="Add fuklin person im not drunk",font="Calibri 30 bold").grid(row=0,column=0,padx=10,pady=10)

    entry = Entry(centeredFrame,font="Calibri 30 bold")
    entry.grid(row=2,column=0,padx=10,pady=10,columnspan=2)
    
    Button(centeredFrame, font=font, text="Cancel", command=popup.destroy).grid(row=3,column=0)
    Button(centeredFrame, font=font, text="Add", command= lambda entry = entry: close_popup(entry.get(), popup)).grid(row=3,column=1)

def close_and_remove(popup, person):
    popup.destroy()
    people_handler.remove_person(person)
    
def remove_a_man():
    popup = Toplevel(width=900,height=600)
    centeredFrame = Frame(popup,highlightbackground="Black", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")
    Label(centeredFrame,text="Click on a boi \nto remove them forever :(",font="Calibri 30 bold").grid(row=0,column=0,padx=10,pady=10)
    c = 5
    for person in people_handler.people:
        Button(centeredFrame, font=font, text=person.name,width = 10,
               command= lambda person = person: close_and_remove(popup, person)).grid(row=c,column=1)
        c = c + 1
        
    Button(centeredFrame, font=font, text="Cancel", command=popup.destroy).grid(row=c+1,column=0)

def safely_shutdown():
    people_handler.save_to_file()
    root.destroy()

people_handler = People()
    
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda : add_a_man())

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add a New Human", command=lambda : add_a_man())
filemenu.add_command(label="Remove an Human", command=lambda : remove_a_man())
filemenu.add_command(label="Save", command=lambda : people_handler.save_to_file())
filemenu.add_command(label="Load", command=lambda : choose_and_load())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda: safely_shutdown())
menubar.add_cascade(label="File", menu=filemenu)

root.protocol("WM_DELETE_WINDOW", lambda: safely_shutdown())
root.title("Shortuis Progsrma")
root.config(menu=menubar)
root.mainloop()




            
    
