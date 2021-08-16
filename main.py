from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import seaborn
import keyboard
import os

def clear():  
   os.system('cls' if os.name == 'nt' else 'clear')

def SaveData(data):
    df = pd.DataFrame(data)
    df.to_excel("equity.xlsx", sheet_name = "Equity")

def LoadData():
    try:
        data = pd.read_excel("equity.xlsx")
    except:
        return None
    return data

def GraphicData(data):
    equity = data['Equity']
    MA = data['MA']
    
    equity = equity.tolist()
    MA = MA.tolist()
    
    plt.subplots(constrained_layout=True)
    plt.plot(equity, label='Equity')
    plt.plot(MA, label='MA 14')
    plt.legend(loc='upper right')
    plt.title("Account Performance")
    plt.xlabel("Operation Number")
    plt.ylabel("Equity")
    plt.show()

def isGhostMode():
    data = LoadData()

    equity = data['Equity']
    MA = data['MA']
    
    equity = equity.tolist()
    MA = MA.tolist()

    el = len(equity)
    mal = len(MA)
    
    return equity[el - 1] <= MA[mal - 1]

def AddOperation():
    data = LoadData()
    try:
        if len(data['Equity']) > 0:
            rs = data['R']
            rs = rs.tolist()
            equity = data['Equity']
            equity = equity.tolist()
            MA = data['MA']
            MA = MA.tolist()
        else:
            rs = list()
            equity = list()
            MA = list()
        
    except:
        rs = list()
        equity = list()
        MA = list()
    
    parsingsucc = False
    r = 0
    while parsingsucc == False:
        clear()
        print("Ingrese el r de la operación")
        r = input()
        try:
            r = int(r)
            parsingsucc = True;
        except:
            parsingsucc = False
        

    rs.append(r)
    l = len(rs)
    eq = 0
    if l == 1:
        equity.append(r)
    elif l > 1:
        init = l-1
        j = init
        while j >= 0:
            eq += rs[j]
            j -= 1

        equity.append(eq)
    
    sum = 0
    if l >= 14:
        for i in range(13, l):
            sum = 0
            for k in range(i - 13, i):
                sum += equity[k]
            
            ma = sum / 14
            MA.append(ma)
        
    

    sizediference = l - len(MA)
    if sizediference > 0:
        for i in range(0, sizediference):
            MA.insert(0,0)
    elif sizediference < 0:
        for i in range(0, (-sizediference)):
            del MA[0]
    
    data = {'R': rs, 'Equity': equity, 'MA': MA}
    SaveData(data)
    clear()


isthereenoughdata = False
while True:
    data = LoadData()   
    try:
        equity = data['Equity']
        equity = equity.tolist()
        if len(equity) >= 14:
            isthereenoughdata = True
        else:
            isthereenoughdata = False
        
    except:
        isthereenoughdata = False
    
    if isthereenoughdata != True:
        print("NO HAY SUFICIENTES DATOS")
    else:
        isGM = isGhostMode()
        if isGM == True:
            print("MODO CUENTA FANTASMA")
        else:
            print("MODO CUENTA REAL")


    print("\n\n")
    print("0_Salir")
    print("1_Agregar operación")
    print("2_Graficar")

    keyboard.read_key()
    clear()

    if keyboard.is_pressed("0"):
        break;
    
    if keyboard.is_pressed("1"):
        AddOperation()

    if keyboard.is_pressed("2"):
        GraphicData(data);

    clear()