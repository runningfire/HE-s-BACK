# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:06:31 2023

@author: home
"""

import csv, codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Парс и декодировки кириллицы 
#в csv исходниках с курсом за 2 месяца
def csv_parser_decoder(path):                
    csvfile = codecs.open(path, "r", "utf-8")
    reader = list(csv.reader(csvfile, delimiter=','))
    csvfile.close()
    return reader

#Скорее всего не оптимально её использовать, 
#но я пока сильно путаюсь в получаемых данных
#и перевода в выходную таблицу

def Formater(reader):         
    Itter = len(reader)
    datadict = {'Date': None, 'Price': None}
    pricelist = []
    datalist = []
    for i in range(Itter):
        if i != 0:
            price_for_month = reader[i][1].replace(',', '')
            pricelist.append(float(price_for_month))
            datalist.append(reader[i][0])
            datadict['Date'] = datalist
            datadict['Price'] = pricelist
    return datadict

#Здесь создается объект Pandas
#в таблицу записываются значения валют
def Pandas_Table(dictb, dicte):        
    df = pd.DataFrame(
    {
     'Date': pd.Series(dictb['Date']),
     'Bitcoin': np.array(dictb['Price']),
     'Ethereum': np.array(dicte['Price'])
     }
    )
    return df

def drawer_graph(arr1, arr2, text_title, text_axisy, text_axisx):
    fig, ax = plt.subplots()
    ax.set_title(text_title)
    ax.set_ylabel(text_axisy)
    ax.set_xlabel(text_axisx)
    ax.scatter(arr1, arr2, c='r', vmin=0, vmax=100)
    

quality_calman = lambda quality_prev, disp: (quality_prev*disp**2)/(quality_prev + disp**2)
Own_eth = lambda own_ethprev, disp, quality, eth: own_ethprev + (quality/disp**2)*(eth - own_ethprev)


pathb = r'C:\Users\home\Documents\Bitcoin.csv'
pathe = r'C:\Users\home\Documents\Ethereum.csv'
datab = csv_parser_decoder(pathb)
dictdatab = Formater(datab)    
datae = csv_parser_decoder(pathe)
dictdatae = Formater(datae)
new = []
for value in dictdatae['Price']:
    new.append(value*1000)      #В исходнике тысячи, перевёл в чистые доллары
dictdatae['Price'] = new    
print(dictdatae)    
pandatbl = Pandas_Table(dictdatab, dictdatae)
btcoin = list(pandatbl['Bitcoin'])
eth = list(pandatbl['Ethereum'])
btcoin = list(reversed(btcoin))
eth = list(reversed(eth))
print(pandatbl)


#Я использую в этом случае самый быстрый способ. Просто в numpy вбиваю и одной функцией считаю корреляцию, так как уже имею зависимую и независимую переменные
coefic_korr = np.corrcoef(btcoin, eth)[0][1]
disp_eth = np.var(eth)/3 #Дисперсия заранее неизвестна у шумов, то ориентируемся на дисперсию значений и то что она несколько меньше
print(coefic_korr, disp_eth) #Ого, какой большой. 0.955265... Близок к единице, придётся дополнительную обработку проводить. Может, Калман?

for i in range(len(eth)):
    if i == 0:
        qual = disp_eth**2
        Owne = eth[0]
        Owns = [Owne]
    else:
        qual = quality_calman(qual, disp_eth)
        Owne = Own_eth(Owne, disp_eth, qual, eth[i])
        Owns.append(Owne)   
New_korr = np.corrcoef(eth, Owns)
print(Owns[-1], qual)


drawer_graph(btcoin, eth, text_title='Зависимость Биткойна от Эфириума', text_axisy='Ethereum', text_axisx='Bitcoin')    
#Получилось так, что на Собственные значения влияет что-то помимо Биткойна, но в гораздо меньшей степени. Зависимость нелинейная у собственных значений. Новый коэффициент корреляции меньше 0.7 откуда линейная регрессия бессмыслена.