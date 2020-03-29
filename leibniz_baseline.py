import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date
import numbers
import decimal
import math
import sys

def pred_function(series, k=2):
    # Newton-Leibniz baseline
    # In 1665, following an outbreak of the bubonic plague in England, 
    # Cambridge University closed its doors, forcing Newton to return home and 
    # develop Differential calculus.
    # Leibniz's most prominent accomplishment was conceiving the ideas of differential and integral calculus, 
    # independently of Isaac Newton's contemporaneous developments.
    # Discrete backward derivative delta(x) = f(x) - f(x-1)
    # f(x+1)= delta(x)+f(x)
    
    delta = series[-1] - series[-2]
    #k-day ahead prediction
    pred = series[-1] + k*delta
    return pred

def mortality_estimate(data):
    # loop over countires and estimate ratio of predicted deaths and predicted confirmed cases
    cat2_idx = data['Province/State'].isnull()
    moratlity_list=[]
    for tmp_location in set(data['Country/Region'][cat2_idx]):
        idx_location = data['Country/Region']==tmp_location
        next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
        next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
        if next_confirmed > 0:
            next_mortality = next_deaths / next_confirmed 
            moratlity_list.append(next_mortality)
            
    cat1_idx = data['Province/State'].notnull()
    for tmp_location in set(data['Province/State'][cat1_idx]):

        idx_location = data['Province/State']==tmp_location
        next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
        next_recovered = pred_function(data['Recovered'][idx_location].to_numpy())
        next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
        if next_confirmed > 0:
            next_mortality = next_deaths / next_confirmed 
            moratlity_list.append(next_mortality)
    
    next_mortality_avg = np.average(np.asarray(moratlity_list))
    return next_mortality_avg

data = pd.read_csv('time-series-19-covid-combined.csv') 

next_mortality_avg = mortality_estimate(data)
print(next_mortality_avg)

num_days = 2
last_date_str = data['Date'].to_numpy()[-1]
file_str = str(num_days)+"day_prediction_" + last_date_str + ".csv"
print(file_str)

next_pred_date = datetime.datetime.strptime( last_date_str, "%Y-%m-%d")+datetime.timedelta(days=2)
f = open(file_str,"w+")
f = open(file_str,"w+")

f.write("Province/State,Country,Target/Date,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")

cat2_idx = data['Province/State'].isnull()
for tmp_location in set(data['Country/Region'][cat2_idx]):
    
    try:
        idx_location = data['Country/Region']==tmp_location
        next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy(), num_days)
        next_recovered = pred_function(data['Recovered'][idx_location].to_numpy(), num_days)
        next_deaths = pred_function(data['Deaths'][idx_location].to_numpy(), num_days)

        if (math.isnan(next_confirmed)==True):
            next_confirmed = 0
        if (math.isnan(next_recovered)==True):
            next_recovered = 0
        if (math.isnan(next_deaths)==True):
            next_deaths = 0
        if next_confirmed > 0:
            next_mortality = next_deaths / next_confirmed 
            m_str = str(next_mortality)+",,,"
        else:
            next_mortality = 0
            m_str = ",,,"

        loc1 = data['Province/State'][idx_location].iloc[0]
        loc2 = data['Country/Region'][idx_location].iloc[0]

        next_pred_date_str = next_pred_date.strftime("%Y-%m-%d")+","
        loc1_str = str(loc1).replace(',', ' ') + ","
        loc2_str = str(loc2).replace(',', ' ') + ","

        if (isinstance(next_confirmed, numbers.Number)):
            n_str = str(next_confirmed)+",,,"
        else:
            n_str = ",,,"
        if (isinstance(next_recovered, numbers.Number)):
            r_str = str(next_recovered)+",,,"
        else:
            r_str = ",,,"
        if (isinstance(next_deaths, numbers.Number)):
            d_str = str(next_deaths) + ",,,"
        else:
            d_str = ",,,"
        t_str = ",,,"
        c_str = ",,\n"
        f.write(","+loc2_str+next_pred_date_str+n_str+r_str+d_str+t_str+m_str+c_str)
        
    except:
        print("Unexpected error:", sys.exc_info()[0])

cat1_idx = data['Province/State'].notnull()
for tmp_location in set(data['Province/State'][cat1_idx]):

    try:
        idx_location = data['Province/State']==tmp_location
        next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy(), num_days)
        next_recovered = pred_function(data['Recovered'][idx_location].to_numpy(), num_days)
        next_deaths = pred_function(data['Deaths'][idx_location].to_numpy(), num_days)

        if (math.isnan(next_confirmed)==True):
            next_confirmed = 0
        if (math.isnan(next_recovered)==True):
            next_recovered = 0
        if (math.isnan(next_deaths)==True):
            next_deaths = 0   
        if next_confirmed > 0:
            next_mortality = next_deaths / next_confirmed 
            m_str = str(next_mortality)+",,,"
        else:
            next_mortality = 0
            m_str = ",,,"

        loc1 = data['Province/State'][idx_location].iloc[0]
        loc2 = data['Country/Region'][idx_location].iloc[0]

        next_pred_date_str = next_pred_date.strftime("%Y-%m-%d")+","
        loc1_str = str(loc1).replace(',', ' ') + ","
        loc2_str = str(loc2).replace(',', ' ') + ","

        if (isinstance(next_confirmed, numbers.Number)):
            n_str = str(next_confirmed)+",,,"
        else:
            n_str = ",,,"


        if (isinstance(next_recovered, numbers.Number)):
            r_str = str(next_recovered)+",,,"
        else:
            r_str = ",,,"


        if (isinstance(next_deaths, numbers.Number)):
            d_str = str(next_deaths) + ",,,"
        else:
            d_str = ",,,"
        t_str = ",,,"
        c_str = ",,\n"

        f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+t_str+m_str+c_str)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        
print("baseline predictions writtern to:"+file_str)    
f.close()

