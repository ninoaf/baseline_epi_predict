import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from datetime import date

f = open("logistic_baseline_predictions_combined/2day_prediction_combined.csv", "w+")
f.write("Date,Country,Province/State,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")
    
start = datetime.datetime.strptime('2020-03-04', "%Y-%m-%d")
end = datetime.date.today()-datetime.timedelta(days=1)

date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start.date()).days)]
    
for date in date_generated:
    
    data = pd.read_csv('logistic_baseline_predictions/2day_prediction_'+date.strftime("%Y-%m-%d")+'.csv')
    
    data = data.fillna("")
    for i in range(len(data['Country'])):
        f.write(str(data['Target/Date'][i])+","+data['Country'][i]+","+","+str(data['N'][i])+","+str(data['low95N'][i])+","+str(data['high95N'][i])+","+str(data['R'][i])+","+str(data['low95R'][i])+","+str(data['high95R'][i])+","+str(data['D'][i])+","+str(data['low95D'][i])+","+str(data['high95D'][i])+","+str(data['T'][i])+","+str(data['low95T'][i])+","+str(data['high95T'][i])+","+str(data['M'][i])+","+str(data['low95M'][i])+","+str(data['high95M'][i])+","+str(data['C'][i])+","+str(data['low95C'][i])+","+str(data['high95C'][i])+"\n")    

f.close()

f = open("logistic_baseline_predictions_combined/7day_prediction_combined.csv", "w+")
f.write("Date,Country,Province/State,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")
    
start = datetime.datetime.strptime('2020-03-04', "%Y-%m-%d")
end = datetime.date.today()-datetime.timedelta(days=1)

date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start.date()).days)]
    
for date in date_generated:
    
    data = pd.read_csv('logistic_baseline_predictions/7day_prediction_'+date.strftime("%Y-%m-%d")+'.csv')
    
    data = data.fillna("")
    for i in range(len(data['Country'])):
        f.write(str(data['Target/Date'][i])+","+data['Country'][i]+","+","+str(data['N'][i])+","+str(data['low95N'][i])+","+str(data['high95N'][i])+","+str(data['R'][i])+","+str(data['low95R'][i])+","+str(data['high95R'][i])+","+str(data['D'][i])+","+str(data['low95D'][i])+","+str(data['high95D'][i])+","+str(data['T'][i])+","+str(data['low95T'][i])+","+str(data['high95T'][i])+","+str(data['M'][i])+","+str(data['low95M'][i])+","+str(data['high95M'][i])+","+str(data['C'][i])+","+str(data['low95C'][i])+","+str(data['high95C'][i])+"\n")    

f.close()

f = open("logistic_baseline_predictions_combined/30day_prediction_combined.csv", "w+")
f.write("Date,Country,Province/State,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")

start = datetime.datetime.strptime('2020-03-04', "%Y-%m-%d")
end = datetime.date.today()-datetime.timedelta(days=1)

date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start.date()).days)]
    
for date in date_generated:
    
    data = pd.read_csv('logistic_baseline_predictions/30day_prediction_'+date.strftime("%Y-%m-%d")+'.csv')
    
    data = data.fillna("")
    for i in range(len(data['Country'])):
        f.write(str(data['Target/Date'][i])+","+data['Country'][i]+","+","+str(data['N'][i])+","+str(data['low95N'][i])+","+str(data['high95N'][i])+","+str(data['R'][i])+","+str(data['low95R'][i])+","+str(data['high95R'][i])+","+str(data['D'][i])+","+str(data['low95D'][i])+","+str(data['high95D'][i])+","+str(data['T'][i])+","+str(data['low95T'][i])+","+str(data['high95T'][i])+","+str(data['M'][i])+","+str(data['low95M'][i])+","+str(data['high95M'][i])+","+str(data['C'][i])+","+str(data['low95C'][i])+","+str(data['high95C'][i])+"\n")    

f.close()