import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date

def pred_function(series):
    # Newton-Leibniz baseline
    # In 1665, following an outbreak of the bubonic plague in England, 
    # Cambridge University closed its doors, forcing Newton to return home and 
    # develop Differential calculus.
    # Leibniz's most prominent accomplishment was conceiving the ideas of differential and integral calculus, 
    # independently of Isaac Newton's contemporaneous developments.
    # Discrete backward derivative delta(x) = f(x) - f(x-1)
    # f(x+1)= delta(x)+f(x)
    
    delta = series[-1] - series[-2]
    pred = delta + series[-1]
    return pred

def mortality_estimate(data):
    # loop over countires and estimate ratio of predicted deaths and predicted confirmed cases
    
    cat2_idx = data['Province/State'].isnull()
    mortality_list=[]
    for tmp_location in set(data['Country/Region'][cat2_idx]):
        idx_location = data['Country/Region']==tmp_location
        next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
        next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
        next_mortality = next_deaths / next_confirmed 
        mortality_list.append(next_mortality)
    
    next_mortality_avg = np.average(np.asarray(mortality_list))
    
    return next_mortality_avg

data = pd.read_csv('time-series-19-covid-combined.csv') 

next_mortality_avg = mortality_estimate(data)
print(next_mortality_avg)

today = date.today()
file_str = "2day_prediction_" + str(today) + ".csv"
print(file_str)

next_pred_date = today+datetime.timedelta(days=2)
f = open(file_str,"w+")
#'Province/State, Country, prediction target date, N, varN, R, varR, D, varD, M, varM
#NaN, Switzerland, 14/03/2020, 1211, 1100-1400, 20, 10-60, 3, 3-5, 0.05, 0.01-0.1

f.write("Province/State, Country, prediction target date, N, varN, R, varR, D, varD, M, varM \n")

cat2_idx = data['Province/State'].isnull()
for tmp_location in set(data['Country/Region'][cat2_idx]):
    
    idx_location = data['Country/Region']==tmp_location
    next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
    next_recovered = pred_function(data['Recovered'][idx_location].to_numpy())
    next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
    
    
    loc1 = data['Province/State'][idx_location].iloc[0]
    loc2 = data['Country/Region'][idx_location].iloc[0]

    next_pred_date_str = str(next_pred_date)+","
    loc1_str = str(loc1).replace(',', ' ') + ","
    loc2_str = str(loc2).replace(',', ' ') + ","
    n_str = str(next_confirmed)+",nan,"
    r_str = str(next_recovered)+",nan,"
    d_str = str(next_deaths) + ",nan,"
    m_str = str(next_mortality_avg)+ ",nan\n"
    
    f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+m_str)

cat1_idx = data['Province/State'].notnull()
for tmp_location in set(data['Province/State'][cat1_idx]):

    idx_location = data['Province/State']==tmp_location
    next_confirmed = pred_function(data['Confirmed'][idx_location].to_numpy())
    next_recovered = pred_function(data['Recovered'][idx_location].to_numpy())
    next_deaths = pred_function(data['Deaths'][idx_location].to_numpy())
    
    loc1 = data['Province/State'][idx_location].iloc[0]
    loc2 = data['Country/Region'][idx_location].iloc[0]

    next_pred_date_str = str(next_pred_date)+","
    loc1_str = str(loc1).replace(',', ' ') + ","
    loc2_str = str(loc2).replace(',', ' ') + ","
    n_str = str(next_confirmed)+",nan,"
    r_str = str(next_recovered)+",nan,"
    d_str = str(next_deaths) + ",nan,"
    m_str = str(next_mortality_avg)+ ",nan\n"
    
    f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+m_str)
    
print("baseline predictions writtern to:"+file_str)    
f.close()

