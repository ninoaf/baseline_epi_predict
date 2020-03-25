wget -N wget -N https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv

python3 logistic_baseline_2days.py
python3 logistic_baseline_7days.py
python3 logistic_baseline_30days.py
