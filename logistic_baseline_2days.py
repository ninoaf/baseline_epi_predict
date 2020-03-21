import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import scipy.optimize as opt
import numpy as np
import datetime
from datetime import date

def logistic(x, k, x0):
    return 1 / (1. + np.exp(-k * (x - x0)))

def pred_logistic(x_train, y_train, x_pred, L):
    # This prediction uses a logistic curve f(x)=L/(1+exp(-k*(x-x0))) as fit.
    # L can be estimated from the herd immunity fraction of a given population
    # In this estimate, we use a herd immunity fraction of p=1-1/R0=1-1/2.91=0.66.    
        

    x_pred = np.copy(x_pred)/max(x_train)

    x_train = np.copy(x_train)/max(x_train)    
    y_train = np.copy(y_train)/L
    

    popt, pcov = opt.curve_fit(logistic, x_train, y_train)
    
    # simple error estimator without intrinsic errors in data points
    sigma_ab = np.sqrt(np.diagonal(pcov))
    
    y_pred = logistic(x_pred, popt[0], popt[1])
    y_pred_upper = logistic(x_pred, popt[0]-1.96*sigma_ab[0], popt[1]-1.96*sigma_ab[1])
    y_pred_lower = logistic(x_pred, popt[0]+1.96*sigma_ab[0], popt[1]+1.96*sigma_ab[1])
    
    if y_pred_lower[-1] <= y_train[-1]:
        y_pred_lower[-1] = y_train[-1]
        
    y_pred_lower *= L    
    y_pred_upper *= L    
    y_pred *= L    
    
    return y_pred, y_pred_lower, y_pred_upper

confirmed = pd.read_csv('time_series_19-covid-Confirmed.csv')
deaths = pd.read_csv('time_series_19-covid-Deaths.csv')
recovered = pd.read_csv('time_series_19-covid-Recovered.csv')

colnames = confirmed.columns.tolist()

start = datetime.datetime.strptime(colnames[4], "%m/%d/%y")
end = datetime.datetime.strptime(colnames[-1], "%m/%d/%y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

countries = ['Switzerland', 'Italy', 'Germany', 'US', 'France', 'Spain']
population = [8.57e6, 60.5e6, 82.8e6, 327.2e6, 66.99e6, 46.66e6]

herd_imm_ratio = 0.66
# time delta for prediction in days
prediction_delta = 2

today = date.today()
next_pred_date = today+datetime.timedelta(days=prediction_delta)

file_str = "2day_prediction_" + str(today) + ".csv"
print(file_str)

f = open(file_str,"w+")
    #'Province/State, Country, prediction target date, N, varN, R, varR, D, varD, M, varM
    #NaN, Switzerland, 14/03/2020, 1211, 1100-1400, 20, 10-60, 3, 3-5, 0.05, 0.01-0.1
f.write("Province/State,Country,Prediction Target Date,N,varN,R,varR,D,varD,M,varM \n")

    
    
for i in range(len(countries)):
    confirmed_region = confirmed.loc[confirmed['Country/Region'] == countries[i]]
    deaths_region = deaths.loc[deaths['Country/Region'] == countries[i]]
    recovered_region = recovered.loc[recovered['Country/Region'] == countries[i]]
    
    confirmed_region = np.asarray([float(sum(confirmed_region[colnames[4+i+1]])) for i in range(len(date_generated))])
    deaths_region = np.asarray([float(sum(deaths_region[colnames[4+i+1]])) for i in range(len(date_generated))])
    recovered_region = np.asarray([float(sum(recovered_region[colnames[4+i+1]])) for i in range(len(date_generated))])
    days = np.linspace(0, len(date_generated)-1, len(date_generated))
    
    days_prediction = np.linspace(0, len(date_generated)-1+prediction_delta, len(date_generated)+prediction_delta)
    dates_prediction = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+prediction_delta)]
    
    confirmed_pred, confirmed_pred_lower, confirmed_pred_upper = pred_logistic(days, confirmed_region, days_prediction, population[i]*herd_imm_ratio)
    deaths_pred, deaths_pred_lower, deaths_pred_upper = pred_logistic(days, deaths_region, days_prediction, population[i]*herd_imm_ratio)
    recovered_pred, recovered_pred_lower, recovered_pred_upper = pred_logistic(days, recovered_region, days_prediction, population[i]*herd_imm_ratio)
    
#    fig, ax = plt.subplots()
#    plt.title('%s'%countries[i])
#    plt.plot(date_generated, confirmed_region, 'o', label = 'confirmed cases')
#    plt.plot(date_generated, deaths_region, '^', label = 'deaths')
#    plt.plot(date_generated, recovered_region, 's', label = 'recovered')
#    plt.plot(dates_prediction, confirmed_pred, 'grey', label = 'prediction')
#    
#    
#    # plotting the confidence intervals
#    plt.fill_between(dates_prediction, confirmed_pred_lower, confirmed_pred_upper,
#                 color = 'blue', alpha = 0.15)
#    plt.fill_between(dates_prediction, deaths_pred_lower, deaths_pred_upper,
#                 color = 'orange', alpha = 0.15)
#    plt.fill_between(dates_prediction, recovered_pred_lower, recovered_pred_upper,
#                 color = 'green', alpha = 0.15)
#                          
#    plt.plot(dates_prediction, deaths_pred, 'grey')
#    plt.plot(dates_prediction, recovered_pred, 'grey')
#    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
#    plt.xlim([min(dates_prediction), max(dates_prediction)])
#    ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
#    plt.xticks(rotation = 45)
#    plt.legend(loc = 2)
#    plt.ylabel('cases')
#    plt.tight_layout()
#    plt.show()
    
    next_mortality = deaths_pred/confirmed_pred
    next_mortality_lower = deaths_pred_lower[-1]/confirmed_pred_upper[-1]
    next_mortality_upper = deaths_pred_upper[-1]/confirmed_pred_lower[-1]

    next_pred_date_str = str(next_pred_date)+","
    loc1_str = ","
    loc2_str = str(countries[i]).replace(',', ' ')+","
    n_str = str(confirmed_pred[-1])+","+str(confirmed_pred_lower[-1])+"-"+str(confirmed_pred_upper[-1])+","
    r_str = str(deaths_pred[-1])+","+str(deaths_pred_lower[-1])+"-"+str(deaths_pred_upper[-1])+","
    d_str = str(recovered_pred[-1])+","+str(recovered_pred_lower[-1])+"-"+str(recovered_pred_upper[-1])+","
    m_str = str(next_mortality[-1])+","+str(next_mortality_lower)+"-"+str(next_mortality_upper)+ "\n"
    
    f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+m_str)

print("baseline predictions writtern to:"+file_str)    
f.close()

