#league copilot v2
#Author : Arno LAURIE
#Date : 25/08/2022
# -*- coding: utf-8 -*-

import pyautogui, time, os, sys, subprocess, psutil
from tkinter import *
from PIL import ImageGrab
from tkinter import messagebox

#-----------------------------------------------------------------------------------------------------------
#                                  ROLES INPUT
ROLES=[]

class ButtonRole():
    def __init__(self, role):
        self.name = role
        self.RBt = Button(frame2, text = self.name, command = self.RoleClicked)
        self.RBt.pack()

    def RoleClicked(self):
        self.RBt.config(bg = "green")
        ROLES.append(self.name)

window = Tk()
window.title("Arno's LoL Copilot")
frame_container = Frame(window)
canvas_container = Canvas(frame_container, width = 255, height = 130)
canvas_container.create_text(180, 50, text = "Choose your roles")
canvas_container.create_text(160, 80, text = "Click your main role, then secondary", font = 'Arial 7 bold')
canvas_container.create_text(170, 110, text = "Exit when finished.")
frame2 = Frame(canvas_container)
myscrollbar = Scrollbar(frame_container,orient = "vertical",command = canvas_container.yview)
canvas_container.create_window((0,0),window = frame2,anchor = 'nw')

TopBt = ButtonRole('TOP')
JglBt = ButtonRole('JUNGLE')
MidBt = ButtonRole('MID')
AdcBt = ButtonRole('ADC')
SupBt = ButtonRole('SUPPORT')

frame2.update()
canvas_container.configure(yscrollcommand = myscrollbar.set, scrollregion = "0 0 0 %s" % frame2.winfo_height())
canvas_container.pack(side = LEFT)
myscrollbar.pack(side = RIGHT, fill = Y)
frame_container.pack()

window.mainloop()

if len(ROLES) == 2:
    messagebox.showinfo(f"Roles Selected", f"Main role : {ROLES[0]}, Secondary role : {ROLES[1]}")

#------------------------------------------------------------------------------------------------------------
#                                  CHAMPION INPUT
root= Tk()

canvas1 = Canvas(root, width = 400, height = 300)
canvas1.pack()

entry1 = Entry (root) 
canvas1.create_window(200, 140, window = entry1)
canvas1.create_text(180, 50, text = "Type in your champion name")

def getName():
    global CHAMPION_SELECTED
    x1 = entry1.get()
    CHAMPION_SELECTED = str(x1)
    root.destroy()
    
button1 = Button(text = 'ok', command = getName)
canvas1.create_window(200, 180, window = button1)

root.mainloop()

messagebox.showinfo(f"You have selected {CHAMPION_SELECTED.upper()}")

#---------------------------------------------------------------------------------------------------------------------
#                                   FUNCTIONS

def playbuttonavailable():
    while (ImageGrab.grab().getpixel((490, 215)) != (1, 106, 140)):
        #print("league play button not available or not detected")
        #print(f"rgb value right now : {ImageGrab.grab().getpixel((490, 215))}")
        time.sleep(0.4)
    else:
        #print("league play button is available")
        return True

def check_for_dodge_timer():
    if (ImageGrab.grab().getpixel((980, 580)) != (80, 57, 29)):
        return False
    else:
        return True

def game_found():
    while (ImageGrab.grab().getpixel((962, 717)) != (155, 189, 189)): #while no accept queue annoucement image
        time.sleep(0.4)
        #print("waiting for accept game")
    else:
        pyautogui.click(962, 717) #accept game

def launch_league_client():
    if ("RiotClientServices.exe" in (i.name() for i in psutil.process_iter())) == False:
        #print("league not launched, launching now")
        #subprocess.call(['C:\Riot Games\Riot Client\RiotClientServices.exe', '--launch-product=league_of_legends', '--launch-patchline=live'])
        launch = subprocess.Popen(['C:\Riot Games\Riot Client\RiotClientServices.exe', '--launch-product=league_of_legends', '--launch-patchline=live'])
        #launch.kill()
    else:
        #print("league already launched")
        pass


def select_role(r):
    if (r == "MID"):
        pyautogui.click(942, 785)
    elif (r == "SUPPORT"):
        pyautogui.click(1050, 784)
    elif (r == "TOP"):
        pyautogui.click(833, 786)
    elif (r == "JUNGLE"):
        pyautogui.click(887, 785)
    elif (r == "ADC"):
        pyautogui.click(995, 784)

def launch_game(role1, role2):
    time.sleep(1)
    pyautogui.click(440, 201) #play
    time.sleep(1)
    pyautogui.click(395, 706) #draft pick
    time.sleep(1)
    pyautogui.click(851, 849) #confirm
    time.sleep(1.5)

    pyautogui.click(975, 842) #select first role
    time.sleep(0.6)
    select_role(role1)
    time.sleep(0.6)

    pyautogui.click(1016, 841) #select second role
    time.sleep(0.6)
    select_role(role2)
    time.sleep(0.6)

    pyautogui.click(847, 845) #click on find match

def champ_select(champion):
    pyautogui.click(1096, 263)
    pyautogui.write(str(champion))
    time.sleep(1)
    pyautogui.click(707,328)

#---------------------------------------------------------------------------------------------------
#                                     MAIN

dodgeflag = False
launch_league_client()
if playbuttonavailable():
    launch_game(ROLES[0], ROLES[1])
    time.sleep(1.5)
    if check_for_dodge_timer() == True:
        dodgeflag = True
        #print("dodge timer detected")
        pyautogui.click(980, 580)
    if dodgeflag == True: #if dodge was recently detecated --> click find game again
        pyautogui.click(847, 845)
    game_found()
    time.sleep(17) #approx time after champion select -- not failproof - depends on other 9 people in the server session
    champ_select(CHAMPION_SELECTED)

sys.exit() #end script
