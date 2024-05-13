import time 

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

time_in_day = ["08:00", "12:00", "18:00","20:00", "00:00"]

for day in days_of_week:
    for time_day in time_in_day:
     print("Day:", day, "Time in day:", time_day)
     time.sleep(2)
