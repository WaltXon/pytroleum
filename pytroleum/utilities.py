from config import config
from calendar import monthrange
import datetime

def get_products():
    products=[]
    for product, params in config['curves'].iteritems():
        if params!={}:
            products.append(product)
        else:
            continue
    return products

def annual_to_monthly_rate(annual_rate):
    return ((1+annual_rate)**(1/12.))-1

def get_num_days_in_month(year, month):
    return monthrange(year, month)[1]

def convert_to_standard_time(day):
    return day/(365.25/12.0)


def adjust_date_to_EOM(date_string):
    date=datetime.datetime.strptime(date_string, '%m/%d/%Y')
    adj_date = datetime.datetime(date.year, date.month,calendar.monthrange(date.year, date.month)[1])
    return adj_date