import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import numbers
import decimal
import sys
import os
import datetime


def pred_function(series, k=1):
    # Newton-Leibniz baseline -- local prediction by derivative
    # In 1665, following an outbreak of the bubonic plague in England, 
    # Cambridge University closed its doors, forcing Newton to return home and 
    # develop Differential calculus.
    # Leibniz's most prominent accomplishment was conceiving the ideas of differential and integral calculus, 
    # independently of Isaac Newton's contemporaneous developments.
    # Local prediction by derivative
    # Discrete backward derivative delta(x) = f(x) - f(x-1)
    # f(x+1)= delta(x)+f(x)
    # k - number of steps (days), for prediction
    
    delta = series[-1] - series[-2]
    pred = k*delta + series[-1]
    return pred


# -------------main ---------------------
num_day_pred = 2


# download data
try:
    os.system("wget -N https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

    os.system("wget -N https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

    os.system("wget -N https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    
except:
    print("ERROR Downloading data")
    print("Unexpected error:", sys.exc_info()[0])
    

confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('time_series_covid19_recovered_global.csv')

colnames = confirmed.columns.tolist()

start = datetime.datetime.strptime(colnames[4], "%m/%d/%y")
end = datetime.datetime.strptime(colnames[-1], "%m/%d/%y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]


last_date = date_generated[-1]
last_date_str = last_date.strftime("%Y-%m-%d")
next_pred_date = last_date+datetime.timedelta(days=num_day_pred)
file_str = str(num_day_pred)+"day_prediction_" + last_date_str + ".csv"
print(file_str)

print("Number of locations:")
print(confirmed.shape[0])

f = open("newton-leibniz_baseline_predictions/"+file_str,"w+")

f.write("Province/State,Country,Target/Date,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")

province_null_idx = confirmed['Province/State'].isnull()

for idx in range(0,confirmed.shape[0]):

    try:
        if (province_null_idx[idx] == True):
            loc1_str = ","
        else:
            loc1 = confirmed['Province/State'].iloc[idx]
            loc1_str = str(loc1).replace(',', ' ') + ","


        loc2 = confirmed['Country/Region'].iloc[idx]
        loc2_str = str(loc2).replace(',', ' ') + ","
        
        print("Estimating short-term forecasts:" + loc2_str)

        try:
            next_confirmed = pred_function(confirmed.iloc[idx][colnames[4:]].to_numpy(),2)
            n_str = str(next_confirmed)+",,,"
        except:
            next_confirmed = float("NaN")
            n_str = ",,,"

        try:
            next_deaths = pred_function(deaths.iloc[idx][colnames[4:]].to_numpy(),2)
            d_str = str(next_deaths) + ",,,"
        except:
            next_deaths = float("NaN")
            d_str = ",,,"

        try:
            next_recovered = pred_function(recovered.iloc[idx][colnames[4:]].to_numpy(),2)
            r_str = str(next_recovered)+",,,"
        except:
            next_recovered = float("NaN")
            r_str = ",,,"

        if (next_confirmed > 0):
            if (next_deaths>0):
                next_mortality = next_deaths / next_confirmed 
                m_str = str(next_mortality)+",,,"
            else:
                m_str = "0,,,"
        else:
            next_mortality = float("NaN")
            m_str = ",,,"

        next_pred_date_str = next_pred_date.strftime("%Y-%m-%d")+","
        t_str = ",,,"
        c_str = ",,\n"

        try:
            f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+t_str+m_str+c_str)
        except:
            print("CAN NOT WRITE to file\n")
    except:
        print("Unexpected error:", sys.exc_info()[0])

f.close()
print("Finished Leibniz baseline!")
print("Written to "+ "newton-leibniz_baseline_predictions/"+file_str)


try:
    os.system("python files_combine_leibniz.py")
except:
    print("Could not write predictions in combined format")
    print("Unexpected error:", sys.exc_info()[0])
    

