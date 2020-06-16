import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from datetime import date
import sys

# python files_combine_leibniz.py start_date_[%Y-%m-%d] end_date_[%Y-%m-%d] folder_source folder_target num_days_pred
print('Argument List:'+ str(sys.argv))
print(len(sys.argv))

if len(sys.argv)==6:
    try:
        start = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
        end = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
        source_folder_str = sys.argv[3]
        target_folder_str  = sys.argv[4]
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        num_pred_days = int(sys.argv[5])
    except:
        print("Error in passing argument: python files_combine_leibniz.py start_date_[%Y-%m-%d] end_date_[%Y-%m-%d]")
        print("Unexpected error:", sys.exc_info()[0])
else:
    print("No arguments given, assuming previous day is the end date")
    start = datetime.datetime.strptime('2020-01-22', "%Y-%m-%d")
    end = datetime.date.today()+datetime.timedelta(days=1)
    #end = datetime.date.today()
    print(start.strftime("%Y-%m-%d")+"  "+end.strftime("%Y-%m-%d"))
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start.date()).days)]
    print("No argument given for source, assuming:")
    source_folder_str = "newton-leibniz_baseline_predictions/"
    print("No argument given for target, assuming:")
    target_folder_str = "newton-leibniz_baseline_predictions_combined/"
    print("No argument given for num_pred_days, assuming 2")
    num_pred_days = 2
    
print( source_folder_str )
print( target_folder_str )

try:
    print(target_folder_str+str(num_pred_days)+"day_prediction_combined.csv")
    f = open(target_folder_str+str(num_pred_days)+"day_prediction_combined.csv", "w+")
    f.write("Date,Country,Province/State,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")
except:
    print("Error opening combined file predictions \n")
    print("Unexpected error:", sys.exc_info()[0])
    
    
for date in date_generated:
    try:
        print("Combining: "+date.strftime("%Y-%m-%d"))
        print(source_folder_str+str(num_pred_days)+'day_prediction_'+date.strftime("%Y-%m-%d")+'.csv')
        data = pd.read_csv(source_folder_str+str(num_pred_days)+"day_prediction_"+date.strftime("%Y-%m-%d")+'.csv')

        data = data.fillna("")
        for i in range(len(data['Country'])):
            f.write(str(data['Target/Date'][i])+","+data['Country'][i]+","+data['Province/State'][i]+","+\
                    str(data['N'][i])+","+str(data['low95N'][i])+","+str(data['high95N'][i])+","+\
                    str(data['R'][i])+","+str(data['low95R'][i])+","+str(data['high95R'][i])+","+\
                    str(data['D'][i])+","+str(data['low95D'][i])+","+str(data['high95D'][i])+","+\
                    str(data['T'][i])+","+str(data['low95T'][i])+","+str(data['high95T'][i])+","+\
                    str(data['M'][i])+","+str(data['low95M'][i])+","+str(data['high95M'][i])+","+\
                    str(data['C'][i])+","+str(data['low95C'][i])+","+str(data['high95C'][i])+"\n")    
    except:
        print("Error processing day"+"day_prediction_"+date.strftime("%Y-%m-%d")+".csv")
        print("Unexpected error:", sys.exc_info()[0])

        
f.close()
print("Finished written to "+ target_folder_str+str(num_pred_days)+"day_prediction_combined.csv")
