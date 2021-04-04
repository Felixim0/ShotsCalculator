from tkinter import *
from time import sleep
import random
from random import randint
import sys
import os
root=Tk()
font = ("Calibri 30 bold")
class Person:
    def __init__(self, name,shot_count):
        self.name = name
        self.shot_count = shot_count

    def create_name(self,count, frame):
        name = Label(frame,text=str(self.name),font=("Calibri 30 bold"))
        name.grid(column=3,row=count,rowspan=2)
        
        label = Label(frame,text="0",font=("Calibri 30 bold"))
        label.grid(column=0,row=count,rowspan=2)
        
        x = Label(frame,text="",font=("Calibri 30 bold"))
        x.grid(column=3,row=count+2,rowspan=2)
        
        button1 = Button(frame,text="↑",command= lambda label=label: self.increment(label))
        button1.grid(column=1,row=count)

        button2 = Button(frame,text="↓",command= lambda label=label: self.decrease(label))
        button2.grid(column=1,row=count + 1)
    

    def refreshLabel(self, label):
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
        
        self.people = self.load_from_file()
        self.home_frame = Frame(root)

        self.gen_list()
        self.output_people()

    def load_from_file(self):
        file_contents = [ {"name": "Felix", "score":0} , {"name": "Nathan", "score":0},{"name": "Rob", "score":0} ]
        temp = []
        for each_pair in file_contents:
            temp.append(Person(each_pair.get("name"), each_pair.get("score")))
        return temp
            

    def gen_list(self):
        self.home_frame.destroy()
        self.home_frame = Frame(root)
        self.home_frame.grid(row=0,column=0)

        self.count = 0
        for person in self.people:
            self.count = self.count + 4
            person.create_name(self.count, self.home_frame)
            
    def add_person(self, name):
        self.count = self.count + 4
        self.people.append(Person(name, 0))
        self.gen_list()
        self.output_people()

    def remove_person(self,person):
        print(person.name)
        self.people.remove(person)
        self.gen_list()
        self.output_people()

    def output_people(self):
        for p in self.people:
            print(p.name)
        print("")


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


people_handler = People()
    
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda : add_a_man())

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add a New Human", command=lambda : add_a_man())
filemenu.add_command(label="Remove an Human", command=lambda : remove_a_man())
filemenu.add_command(label="Save", command=lambda : save_all())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.title("Shortuis Progsrma")
root.config(menu=menubar)
root.mainloop()




            
    
