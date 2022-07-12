from distutils.log import ERROR, error
import tkinter as tk
import tkinter.ttk as ttk
from unicodedata import name
from numpy import append
import pandas as pd
import matplotlib.pyplot as plt
from datetime import *
from pyparsing import col
from tkcalendar import *

df = pd.read_csv("GPU.csv")
ETH_THB = pd.read_csv("ราคาย้อนหลัง ETH_THB Satang Pro.csv")


Income_list = []
Total_day_payback_list = []
unit_ = []
power_bill = []
Sum_profit = []
last_day_list = []
time = []

month_list = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
window = tk.Tk()

def click():
    Days()
    ETH_average()
    engine()
    day_for_graph()
    sum()
    best_gpu.configure(text="Best GPU for mining : "+ df["GPU"][index])
    Price.configure(text="Price : "+ str(df["Price"][index])+" THB")
    profit.configure(text="Profit per day : "+ str(df["Profit"][index])+" THB")
    power.configure(text="Power usage : "+ str(df["Power (W)"][index])+" Watt")
    ETH.configure(text="ETH average (To THB) : "+str(E_avg)+" THB")
    mathpltlip()
    print(df)

def ETH_average():
    global E_avg, last_day
    ETH_sum = 0
    last_day = delta0.days
    for i in range(delta.days+1):
        ETH_sum += ETH_THB_Dict['data'][last_day][1]
        last_day_list.append(last_day)
        last_day += 1
    if delta.days == 0:
        E_avg = ETH_sum
    if delta.days > 0:
        E_avg = (ETH_sum/(delta.days+1))


def day_for_graph():
    day_cal = last_day-delta0.days
    print(day_cal)
    if day_cal >= 0 and day_cal < 30:
        time.append(delta0.days)
        for m in range(day_cal):
            time.append(delta0.days + m)

    if day_cal >= 30 and day_cal < 90:
        time.append(delta0.days)
        for n in range(day_cal):
            if n % 3 == 0:
                time.append(n)

    if day_cal >= 90 and day_cal < 200:
        time.append(delta0.days)
        for o in range(day_cal):
            if o % 7 == 0:
                time.append(o)

    if day_cal >= 200 and day_cal < 365:
        time.append(delta0.days)
        for p in range(day_cal):
            if p % 30 == 0:
                time.append(p)

    if day_cal >= 365 and day_cal < 730:
        time.append(delta0.days)
        for q in range(day_cal):
            if q % 50 == 0:
                time.append(q)

    if day_cal >= 730 and day_cal < 1500:
        time.append(delta0.days)
        for r in range(day_cal):
            if r % 100 == 0:
                time.append(r)


def engine():
    global E_avg
    if E_avg != 0:
        for j in range(len(df["GPU"])):
            Income_list.append(df["ETH/DAY"][j]*E_avg)
            unit_.append(df["Power (W)"][j]/1000*24)
        df["Power_unit"] = unit_
        df["Income/Day"] = Income_list

        for l in range(len(df["GPU"])):
            Sum_profit.append(df["Income/Day"][l] - df["Power_unit"][l])
        df["Profit"] = Sum_profit

        for k in range(len(df["GPU"])):
            Price = df["Price"][k]
            power_bill.append(df["Power_unit"][k]*4.4217)
            Days = 0
            while Price >= 0:
                Price -= Sum_profit[k]
                Days += 1
            Total_day_payback_list.append(Days)
        df["Power_Bill"] = power_bill
        df["Total_day_payback"] = Total_day_payback_list


def Days():
    global delta, last_day, ETH_THB_Dict, delta0,d0,d1
    day = int(day_value.get())
    month = month_value.get()
    year = int(year_value.get())
    day2 = int(day2_value.get())
    month2 = month2_value.get()
    year2 = int(year2_value.get())
    for n in range(len(month_list)):
        if month_value.get() == month_list[n]:
            month = n+1
            d0 = date(year, month, day)
        if month2_value.get() == month_list[n]:
            month2 = n+1
            d1 = date(year2, month2, day2)
    day00 = date(2022, 5, 1)
    delta0 = day00 - d0
    delta = d0 - d1
    ETH_THB_Dict = ETH_THB.to_dict('tight')


def mathpltlip():
    y = df["Total_day_payback"]
    x = df["GPU"]

    plt.figure(figsize=(10, 20))
    plt.title("Total day for payback")
    plt.barh(x, y, color="magenta")
    plt.show()

    y = df["Profit"]
    x = df["GPU"]
    plt.figure(figsize=(10, 20))
    plt.title("Profit per day")
    plt.barh(x, y, color="red")
    plt.show()

    print(time)
    print(ETH_THB["ล่าสุด"][time])
    print(ETH_THB["วันเดือนปี"][time])
    y = ETH_THB["ล่าสุด"][time]
    x = ETH_THB["วันเดือนปี"][time]
    plt.figure(figsize=(10, 20))
    plt.title("ETH to BTH")
    plt.plot(x, y, color="green")
    plt.xticks(rotation=90)
    plt.show()
 

def sum():
    global index
    index = Total_day_payback_list.index(min(Total_day_payback_list))


def UI():
    global day_value, month_value, year_value, day2_value, month2_value, year2_value, best_gpu, profit, Price, power, ETH
    window.title("GPU mining calculator")
    window.geometry("400x400")

    day_value = tk.StringVar()
    month_value = tk.StringVar()
    year_value = tk.StringVar()
    day2_value = tk.StringVar()
    month2_value = tk.StringVar()
    year2_value = tk.StringVar()


    lb = tk.Label(window, text="วันที่ :", font=(40))
    lb.grid(column=0, row=2)

    txt = tk.Entry(window, textvariable=day_value, width=5)
    txt.grid(column=1, row=2)

    lb = tk.Label(window, text="เดือน :", font=(40))
    lb.grid(column=2, row=2)

    combo = ttk.Combobox(window, width=5, textvariable=month_value)
    combo["values"] = month_list
    combo.grid(column=3, row=2)

    lb = tk.Label(window, text="ปี :", font=(40))
    lb.grid(column=4, row=2)

    txt = tk.Entry(window, textvariable=year_value, width=10)
    txt.grid(column=5, row=2)

    lb = tk.Label(window, text="ถึง", font=(40))
    lb.grid(column=6, row=2)

    lb = tk.Label(window, text="วันที่ :", font=(40))
    lb.grid(column=0, row=3)

    txt = tk.Entry(window, textvariable=day2_value, width=5)
    txt.grid(column=1, row=3)

    lb = tk.Label(window, text="เดือน :", font=(40))
    lb.grid(column=2, row=3)

    combo = ttk.Combobox(window, width=5, textvariable=month2_value)
    combo["values"] = month_list
    combo.grid(column=3, row=3)

    lb = tk.Label(window, text="ปี :", font=(40))
    lb.grid(column=4, row=3)

    txt = tk.Entry(window, textvariable=year2_value, width=10)
    txt.grid(column=5, row=3)

    btn = tk.Button(window, text="Calculate", command=click)
    btn.grid(column=7, row=3)

    best_gpu = tk.Label(window, text="", font=(40))
    best_gpu.place(x = 10, y = 60)

    Price = tk.Label(window, text="", font=(40))
    Price.place(x = 10, y = 90)
    
    profit = tk.Label(window, text="", font=(40))
    profit.place(x = 10, y = 120)

    power = tk.Label(window, text="", font=(40))
    power.place(x = 10, y = 150)

    ETH = tk.Label(window, text="", font=(40))
    ETH.place(x = 10, y = 180)

    window.mainloop()

UI()
