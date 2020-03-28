import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date

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
today = date.today()
file_str = str(num_days)+"day_prediction_" + str(today) + ".csv"
print(file_str)

next_pred_date = today+datetime.timedelta(days=num_days)
f = open(file_str,"w+")

f.write("Province/State,Country,Target/Date,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")

cat2_idx = data['Province/State'].isnull()
for tmp_location in set(data['Country/Region'][cat2_idx]):
    
    idx_location = data['Country/Region']==tmp_location
    next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
    next_recovered = pred_function(data['Recovered'][idx_location].to_numpy())
    next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
    
    
    loc1 = data['Province/State'][idx_location].iloc[0]
    loc2 = data['Country/Region'][idx_location].iloc[0]

    next_pred_date_str = next_pred_date.strftime("%Y-%m-%d")+","
    loc1_str = str(loc1).replace(',', ' ') + ","
    loc2_str = str(loc2).replace(',', ' ') + ","
    n_str = str(next_confirmed)+",,,"
    r_str = str(next_recovered)+",,,"
    d_str = str(next_deaths) + ",,,"
    t_str = ",,,"
    m_str = ",,,\n"

    f.write(","+loc2_str+next_pred_date_str+n_str+r_str+d_str+t_str+m_str)

cat1_idx = data['Province/State'].notnull()
for tmp_location in set(data['Province/State'][cat1_idx]):

    idx_location = data['Province/State']==tmp_location
    next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
    next_recovered = pred_function(data['Recovered'][idx_location].to_numpy())
    next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
    
    loc1 = data['Province/State'][idx_location].iloc[0]
    loc2 = data['Country/Region'][idx_location].iloc[0]

    next_pred_date_str = next_pred_date.strftime("%Y-%m-%d")+","
    loc1_str = str(loc1).replace(',', ' ') + ","
    loc2_str = str(loc2).replace(',', ' ') + ","
    n_str = str(next_confirmed)+",,,"
    r_str = str(next_recovered)+",,,"
    d_str = str(next_deaths) + ",,,"
    t_str = ",,,"
    m_str = ",,,\n"

    f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+t_str+m_str)
    
print("baseline predictions writtern to:"+file_str)    
f.close()

