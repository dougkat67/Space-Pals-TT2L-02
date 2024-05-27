from tkinter import Tk
from tkinter import Label
import time
import sys

#modified tutorial by adding days

#create window
master = Tk()
master.title('Game Clock')

specific_times = ["08:00", "08:15", "08:30", "09:00", "09:15", "09:30"]

time_index = 0


#updates the label
def update_time_date(): 
    global time_index                
    current_time = time.strftime("%H:%M")
    current_day = time.strftime("%A")

    day_label.config(text=current_day)

    if time_index < len(specific_times):
        time_label.config(text=specific_times[time_index])

    time_index = (time_index + 1) % len(specific_times)

    master.after(2000, update_time_date)     #200 is every 0.2 of a second, run function again


day_label = Label(master, font=('Calibri', 40), bg='grey', fg='white')
day_label.pack(pady=20)

time_label = Label(master, font=('Calibri', 90), bg='grey', fg='white')
time_label.pack(pady=20)

update_time_date() 

master.mainloop()



