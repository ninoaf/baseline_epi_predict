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

confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('time_series_covid19_recovered_global.csv')

colnames = confirmed.columns.tolist()

delta_arr = [0]

for delta in delta_arr:
    
    start = datetime.datetime.strptime(colnames[4], "%m/%d/%y")
    end = datetime.datetime.strptime(colnames[-1], "%m/%d/%y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days-delta+1)]
    
    countries = ['Switzerland', 'Italy', 'Germany', 'US', 'France', 'Spain', 'Netherlands', 'Poland', 'Portugal', 'United Kingdom', 'Croatia', 'Czechia', 'Austria', 'Belgium', 'Luxembourg']
    population = [8.57e6, 60.5e6, 82.8e6, 327.2e6, 66.99e6, 46.66e6, 17.18e6, 37.98e6, 10.29e6, 66.44e6, 4076246, 10.65e6, 8.822e6, 11.4e6, 602005]
    
    herd_imm_ratio = 0.66
    death_prob = 0.01
    # time delta for prediction in days
    prediction_delta = 2
    
    today = date.today()-datetime.timedelta(days=delta)
    next_pred_date = today+datetime.timedelta(days=prediction_delta)
    
    file_str = "logistic_baseline_predictions/2day_prediction_" + str(today) + ".csv"
    print(file_str)
    
    f = open(file_str,"w+")
        #Province/State,Country/Region,Target/Date,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M
    f.write("Province/State,Country,Target/Date,N,low95N,high95N,R,low95R,high95R,D,low95D,high95D,T,low95T,high95T,M,low95M,high95M,C,low95C,high95C\n")
    
    for i in range(len(countries)):
    
        confirmed_region = confirmed.loc[confirmed['Country/Region'] == countries[i]]
        confirmed_region = confirmed_region.loc[confirmed_region['Province/State'].isnull()]
        
        deaths_region = deaths.loc[deaths['Country/Region'] == countries[i]]
        deaths_region = deaths_region.loc[deaths_region['Province/State'].isnull()]
        
        recovered_region = recovered.loc[recovered['Country/Region'] == countries[i]]
        recovered_region = recovered_region.loc[recovered_region['Province/State'].isnull()]
                
        confirmed_region = np.asarray([float(sum(confirmed_region[colnames[4+i]])) for i in range(len(date_generated))])
        deaths_region = np.asarray([float(sum(deaths_region[colnames[4+i]])) for i in range(len(date_generated))])
        recovered_region = np.asarray([float(sum(recovered_region[colnames[4+i]])) for i in range(len(date_generated))])
        days = np.linspace(0, len(date_generated)-1, len(date_generated))
        
        days_prediction = np.linspace(0, len(date_generated)-1+prediction_delta, len(date_generated)+prediction_delta)
        dates_prediction = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days-delta+prediction_delta+1)]
    
        conf_flag = 0
        d_flag = 0
        rec_flag = 0

        try:
            confirmed_pred, confirmed_pred_lower, confirmed_pred_upper = pred_logistic(days, confirmed_region, days_prediction, population[i]*herd_imm_ratio)
        except:
            conf_flag = 1
        
        try:
            deaths_pred, deaths_pred_lower, deaths_pred_upper = pred_logistic(days, deaths_region, days_prediction, population[i]*herd_imm_ratio*death_prob)
        except:
            d_flag = 1
    
        try:        
            recovered_pred, recovered_pred_lower, recovered_pred_upper = pred_logistic(days, recovered_region, days_prediction, population[i]*herd_imm_ratio*(1-death_prob))
        except:
            rec_flag = 1
            
#        fig, ax = plt.subplots()
#        plt.title('%s'%countries[i])
#        plt.plot(date_generated, confirmed_region, 'o', label = 'confirmed cases')
#        plt.plot(date_generated, deaths_region, '^', label = 'deaths')
#        plt.plot(date_generated, recovered_region, 's', label = 'recovered')
#        plt.plot(dates_prediction, confirmed_pred, 'grey', label = 'prediction')
#        
#        # plotting the confidence intervals
#        plt.fill_between(dates_prediction, confirmed_pred_lower, confirmed_pred_upper,
#                     color = 'blue', alpha = 0.15)
#        plt.fill_between(dates_prediction, deaths_pred_lower, deaths_pred_upper,
#                     color = 'orange', alpha = 0.15)
#        plt.fill_between(dates_prediction, recovered_pred_lower, recovered_pred_upper,
#                     color = 'green', alpha = 0.15)
#                              
#        plt.plot(dates_prediction, deaths_pred, 'grey')
#        plt.plot(dates_prediction, recovered_pred, 'grey')
#        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
#        plt.xlim([min(dates_prediction), max(dates_prediction)])
#        ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
#        plt.xticks(rotation = 45)
#        plt.legend(loc = 2)
#        plt.ylabel('cases')
#        plt.tight_layout()
#        plt.show()
        
        if np.logical_and(d_flag == 0, conf_flag == 0):
            next_mortality = deaths_pred[-1]/confirmed_pred[-1]
            next_mortality_lower = deaths_pred_lower[-1]/confirmed_pred_upper[-1]
            next_mortality_upper = deaths_pred_upper[-1]/confirmed_pred_lower[-1]
        else:
            next_mortality = ''
            next_mortality_lower = ''
            next_mortality_upper = ''
            
        # fraction of confirmed cases that require hospitalization
        fserious = 0.05
        if np.logical_and(conf_flag == 0, len(confirmed_pred) > 15):
            serious = (confirmed_pred[len(confirmed_pred)-1]-confirmed_pred[len(confirmed_pred)-16])*fserious
            serious_lower = (confirmed_pred_lower[len(confirmed_pred)-1]-confirmed_pred[len(confirmed_pred)-16])*fserious
            serious_upper = (confirmed_pred_upper[len(confirmed_pred)-1]-confirmed_pred[len(confirmed_pred)-16])*fserious
        elif conf_flag == 0:
            serious = (confirmed_pred[j])*fserious
            serious_lower = (confirmed_pred_lower[j])*fserious
            serious_upper = (confirmed_pred_upper[j])*fserious
        else:
            serious = ""
            serious_lower = ""
            serious_upper = ""

        next_pred_date_str = str(next_pred_date)+","
        loc1_str = ","
        loc2_str = str(countries[i]).replace(',', ' ')+","
        if conf_flag == 0:
            n_str = str(confirmed_pred[-1])+","+str(confirmed_pred_lower[-1])+","+str(confirmed_pred_upper[-1])+","
        else:
            n_str = ","+","+","
            
        if rec_flag == 0:
            r_str = str(recovered_pred[-1])+","+str(recovered_pred_lower[-1])+","+str(recovered_pred_upper[-1])+","
        else:
            r_str = ","+","+","
          
        if d_flag == 0:
            d_str = str(deaths_pred[-1])+","+str(deaths_pred_lower[-1])+","+str(deaths_pred_upper[-1])+","
        else:
            d_str = ","+","+","
         
        t_str = ","+","+","
        m_str = str(next_mortality)+","+str(next_mortality_lower)+","+str(next_mortality_upper) + ","
        c_str = str(serious)+","+str(serious_lower)+","+str(serious_upper)+ "\n"         
        
        f.write(loc1_str+loc2_str+next_pred_date_str+n_str+r_str+d_str+t_str+m_str+c_str)
    
    print("baseline predictions writtern to:"+file_str)    
    f.close()

