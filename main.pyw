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
    def __init__(self, name,consumption_count):
        self.name = name
        self.consumption_count = consumption_count
        self.score = 0

    def create_name(self,count, frame):
        # Name label and placeholder label
        name = Label(frame,text=str(self.name),font=("Calibri 30 bold"))
        name.grid(column=0,row=count,rowspan=2,padx = 20)
        x = Label(frame,text="",font=("Calibri 30 bold"))
        x.grid(column=0,row=count+2)

        # Dynamically generate buttons and counters based on loaded drinks
        c = 1
        for drink in self.consumption_count:
            for name_key in drink:
                pass

            if name_key != "TOTAL SCORE":
                label = Label(frame,text=drink.get(name_key),font=("Calibri 30 bold"))
                label.grid(column=c,row=count,rowspan=2,padx=10)
            
                button1 = Button(frame,text="↑",command= lambda label=label, name_key = name_key: self.increment(label, name_key))
                button1.grid(column=c+1,row=count)

                button2 = Button(frame,text="↓",command= lambda label=label, name_key = name_key: self.decrease(label, name_key))
                button2.grid(column=c+1,row=count + 1)
                c = c + 2
                
            else:
                self.score_label = Label(frame,text=str(self.score),font=("Calibri 30 bold"))
                self.score_label.grid(column=c,row=count,rowspan=2,padx=10)
                

    def refreshLabel(self, label, count):
        self.refresh_score_label()
        label.config(text=str(count),font=("Calibri 30 bold"))

    def refresh_score_label(self):
        print("refreshing label")
        print(self.score)
        self.score_label.config(text=str(self.score),font=("Calibri 30 bold"))
        

    def increment(self, label, key):
        for drink in self.consumption_count:
            for name_key in drink:
                pass
            if name_key == key:
                drink[key] = drink[key] + 1
                count = drink[key]
        self.refreshLabel(label, count)
        do_score_refresh()

    def decrease(self, label, key):
        for drink in self.consumption_count:
            for name_key in drink:
                pass
            if name_key == key:
                if drink[key] > 0:
                    drink[key] = drink[key] - 1
                    self.refreshLabel(label, drink.get(key))
        do_score_refresh()
                    
        

class People:
    def __init__(self):
        self.people = []
        self.drinks = self.load_drinks()
        self.home_frame = Frame(root)
        self.load_from_file(None)
        self.gen_list()
        Path("./saves").mkdir(parents=True, exist_ok=True)

    def load_drinks(self):
        save_file = open("./drinks.json","r")
        return json.load(save_file)         

    def edit_drink(self, pframe, drink, new_name, new_units):
        self.drinks.remove(drink)
        self.add_drink(pframe, new_name, new_units)
        self.save_drinks_to_file()
        edit_a_drink()
        self.gen_list()

    def remove_drink(self,drink):
        self.drinks.remove(drink)
        key_to_remove = drink.get("name")
        for person in self.people:
            for local_drink in person.consumption_count:
                for name in local_drink:
                    pass
                if name == key_to_remove:
                    local_drink_to_remove = local_drink
                    person_to_remove_from = person

            person_to_remove_from.consumption_count.remove(local_drink_to_remove)

        self.gen_list()        

    def add_drink(self, popup, drink_name, units):
        popup.destroy()
        self.drinks.append({"name":drink_name,"units_per_drink":units})
        for person in self.people:
            person.consumption_count.append({drink_name:0})
        self.gen_list()

    def save_drinks_to_file(self):
        with open("./drinks.json", "w") as f:
            f.write(json.dumps(self.drinks, indent=4))        

    def save_to_file(self):
        self.save_drinks_to_file()
        dat_as_json = [{"name":x.name,"score":x.consumption_count} for x in self.people]

        def format_date_better(number):
            if len(str(number)) < 2:
                return ( "0" + str(number))
            else:
                return (number)

        x = datetime.datetime.now()
        time = format_date_better(str(x.day)) + "-" + format_date_better(str(x.month))  + "-" + format_date_better(str(x.year))
        
        with open("./saves/" + str(time) +".json", "w") as f:
            f.write(json.dumps(dat_as_json, indent=4))

    def default_score(self):
        score = [{x.get("name"):0} for x in self.drinks]
        score.append({"TOTAL SCORE": 0 })
        return score
    
    def load_from_file(self, save_file_dr):
        if save_file_dr == None:
            file_contents = [ {"name": "Felix", "score":self.default_score()} ,
                              {"name": "Nathan", "score":self.default_score()},
                              {"name": "Rob", "score":self.default_score()} ]
        else:
            save_file = open(save_file_dr,"r")
            file_contents = json.load(save_file)
            
        temp = []
        for each_pair in file_contents:
            temp.append(Person(each_pair.get("name"), each_pair.get("score")))

        if save_file_dr != None:
            self.gen_list()

        self.people = temp
        self.gen_list()

    def reorder_appropriate(self):
        return False
        
    def gen_list(self):
        self.home_frame.destroy()
        self.home_frame = Frame(root)
        self.home_frame.grid(row=0,column=0)
        Label(self.home_frame,text="",font=("Calibri 30 bold")).grid(column=0,row=0,padx = 20)
        c = 1
        for drink in self.drinks:
            Label(self.home_frame,text=drink.get("name"),font=("Calibri 30 bold")).grid(column=c,row=0,columnspan=2,padx=15)
            c = c + 2
        Label(self.home_frame,text="TOTAL SCORE",font=("Calibri 30 bold")).grid(column=c,row=0,columnspan=2,padx=20)

        self.count = 4
        for person in self.people:

            # Calculate score here
            score = 0
            for person_drink in person.consumption_count:
                for drink_name in person_drink:
                    pass

                if drink_name != "TOTAL SCORE":
                    drinks_taken = person_drink.get(drink_name)

                    units = 0
                    for global_drink in self.drinks:
                        if global_drink.get("name") == drink_name:
                            units = global_drink.get("units_per_drink",0)
                            score = round (score + ( float(units) * int(drinks_taken) ), 3)
                    
            person.score = score

            self.count = self.count + 4
            person.create_name(self.count, self.home_frame)
            person.refresh_score_label()

    def do_refresh_score(self):

        for person in self.people:

            # Calculate score here
            score = 0
            for person_drink in person.consumption_count:
                for drink_name in person_drink:
                    pass

                if drink_name != "TOTAL SCORE":
                    drinks_taken = person_drink.get(drink_name)

                    units = 0
                    for global_drink in self.drinks:
                        if global_drink.get("name") == drink_name:
                            units = global_drink.get("units_per_drink",0)
                            score = round (score + ( float(units) * int(drinks_taken) ), 3)
                    
            person.score = score
            print(score, person.score)
            person.refresh_score_label()   
            
    def add_person(self, name):
        self.count = self.count + 4
        self.people.append(Person(name, self.default_score()))
        self.gen_list()

    def remove_person(self,person):
        self.people.remove(person)
        self.gen_list()

def do_score_refresh():
    people_handler.do_refresh_score()

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

def close_drink(pframe):
    pframe.destroy()
    people_handler.gen_list()

def delete_drink(pframe, drink):
    pframe.destroy()
    people_handler.remove_drink(drink)

def add_a_drink():
    popup = Toplevel(width=900,height=600)
    centeredFrame = Frame(popup,highlightbackground="Black", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")
    Label(centeredFrame,text="Add Drink Info >:D",font="Calibri 30 bold").grid(row=0,column=0,padx=10,pady=10)

    Label(centeredFrame,text="Drink Name:",font="Calibri 30 bold").grid(row=1,column=0,padx=10,pady=10)
    entry1 = Entry(centeredFrame,font="Calibri 30 bold")
    entry1.grid(row=1,column=1,padx=10,pady=10,columnspan=2)
    Label(centeredFrame,text="Units Per Drink",font="Calibri 30 bold").grid(row=2,column=0,padx=10,pady=10)
    entry2 = Entry(centeredFrame,font="Calibri 30 bold")
    entry2.grid(row=2,column=1,padx=10,pady=10,columnspan=2)
    
    Button(centeredFrame, font=font, text="Cancel", command=popup.destroy).grid(row=3,column=0)
    Button(centeredFrame, font=font, text="Save", command=lambda : people_handler.add_drink(popup, entry1.get(), entry2.get()) ).grid(row=3,column=1)    

def edit_drink(pframe,drink):
    pframe.destroy()
    popup = Toplevel(width=900,height=600)
    centeredFrame = Frame(popup,highlightbackground="Black", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")
    Label(centeredFrame,text="Edit Drink Options",font="Calibri 30 bold").grid(row=0,column=0,padx=10,pady=10)
    
    Label(centeredFrame,text="Drink Name:",font="Calibri 30 bold").grid(row=1,column=0,padx=10,pady=10)
    entry1 = Entry(centeredFrame,font="Calibri 30 bold")
    entry1.grid(row=1,column=1,padx=10,pady=10,columnspan=2)
    Label(centeredFrame,text="Units Per Drink",font="Calibri 30 bold").grid(row=2,column=0,padx=10,pady=10)
    entry2 = Entry(centeredFrame,font="Calibri 30 bold")
    entry2.grid(row=2,column=1,padx=10,pady=10,columnspan=2)
    entry1.insert(END, str(drink.get("name")))
    entry2.insert(END, str(drink.get("units_per_drink")))
    
    Button(centeredFrame, font=font, text="Cancel", command=lambda: close_drink(popup)).grid(row=3,column=0)
    Button(centeredFrame, font=font, text="Save", command=lambda : people_handler.edit_drink(popup, drink, entry1.get(), entry2.get()) ).grid(row=3,column=1)   
    
def edit_a_drink():
    popup = Toplevel(width=1100,height=1200)
    centeredFrame = Frame(popup,highlightbackground="Black", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")
    Label(centeredFrame,text="Select a Drink",font="Calibri 30 bold").grid(row=0,column=0,padx=10,pady=10)
    c = 5
    for drink in people_handler.drinks:
        Button(centeredFrame, font=font, text=f'{drink.get("name")}:  {drink.get("units_per_drink")}',width = 23,
               command= lambda drink = drink: edit_drink(popup ,drink)).grid(row=c,column=1)
        
        Button(centeredFrame, font=font, text=f'Delete',width = 23,
               command= lambda drink = drink: delete_drink(popup ,drink)).grid(row=c,column=0)
        c = c + 1
        
    Button(centeredFrame, font=font, text="Cancel", command=popup.destroy).grid(row=c+1,column=0)

    
people_handler = People()
    
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add a New Human", command=lambda : add_a_man())
filemenu.add_command(label="Remove an Human", command=lambda : remove_a_man())
filemenu.add_command(label="Save", command=lambda : people_handler.save_to_file())
filemenu.add_command(label="Load", command=lambda : choose_and_load())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda: safely_shutdown())
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="New Drink", command=lambda : add_a_drink())
editmenu.add_command(label="Edit Existing Drink", command=lambda : edit_a_drink())

menubar.add_cascade(label="Edit", menu=editmenu)


root.protocol("WM_DELETE_WINDOW", lambda: safely_shutdown())
root.title("Shortuis Progsrma")
root.config(menu=menubar)
root.mainloop()




            
    
