from datetime import  date, timedelta

time = []
for i in range(0, 10):
    time.append(date.today()+timedelta(days=i))



print(time)