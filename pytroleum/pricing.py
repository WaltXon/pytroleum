from collections import OrderedDict
import datetime
import calendar
import pandas as pd
from functions import adjust_date_to_EOM
from config import config


def pricing(price_type='strip', output_excel_file=''):

    date_series=pd.date_range(config['production_start_date'], periods=config['max_life_months'], freq='M')
    df_time_series= pd.DataFrame(index=date_series)
    df_time_series['date']=df_time_series.index.format()
    if price_type=='flat':
        prices=pd.DataFrame(index=df_time_series.index, columns=['price_oil','price_gas','price_ngl'])
        prices['price_oil']=config['price_oil_flat']
        prices['price_gas']=config['price_gas_flat']
        prices['price_ngl']=config['price_ngl_flat']
    elif price_type=='strip':
        working_oil=[]
        for k,v in config['price_oil_strip'].iteritems():
                working_oil.append((adjust_date_to_EOM(k), v))

        working_gas=[]
        for k,v in config['price_gas_strip'].iteritems():
                working_gas.append((adjust_date_to_EOM(k), v))

        working_ngl=[]
        for k,v in config['price_ngl_strip'].iteritems():
                working_ngl.append((adjust_date_to_EOM(k), v))

        df_oil=pd.DataFrame([x[1] for x in working_oil], index=[x[0] for x in working_oil], columns=['price_oil'])
        df_gas=pd.DataFrame([x[1] for x in working_gas], index=[x[0] for x in working_gas], columns=['price_gas'])
        df_ngl=pd.DataFrame([x[1] for x in working_ngl], index=[x[0] for x in working_ngl], columns=['price_ngl'])

        if df_ngl.empty==False:
            prices=pd.concat([df_oil, df_gas, df_ngl, df_time_series], axis=1)


        else:
            prices=pd.concat([df_oil, df_gas, df_time_series], axis=1)
            prices['price_ngl']=0.0

        idx_last_oil_price=prices['price_oil'][pd.notnull(prices['price_oil'])].idxmax()
        last_oil_price=prices.ix[idx_last_oil_price, 'price_oil']

        idx_last_gas_price=prices['price_gas'][pd.notnull(prices['price_gas'])].idxmax()
        last_gas_price=prices.ix[idx_last_gas_price, 'price_gas']

        idx_last_ngl_price=prices['price_ngl'][pd.notnull(prices['price_ngl'])].idxmax()
        last_ngl_price=prices.ix[idx_last_ngl_price, 'price_ngl']

        prices=prices.fillna(0)

        last_oil=[last_oil_price,]
        last_gas=[last_gas_price,]
        last_ngl=[last_ngl_price,]

        for idx,row in prices.iterrows():
            if row['price_oil']==0.0:
                new_oil_price=last_oil[-1]*config['after_strip_escalator_oil']
                if new_oil_price>=config['price_oil_max']:
                    prices.ix[idx, 'price_oil']=config['price_oil_max']
                    last_oil.append(config['price_oil_max'])
                else:
                    prices.ix[idx, 'price_oil']=new_oil_price
                    last_oil.append(new_oil_price)
            if row['price_gas']==0.0:
                new_gas_price=last_gas[-1]*config['after_strip_escalator_gas']
                if new_gas_price>=config['price_gas_max']:
                    prices.ix[idx, 'price_gas']=config['price_gas_max']
                    last_gas.append(config['price_gas_max'])
                else:
                    prices.ix[idx, 'price_gas']=new_gas_price
                    last_gas.append(new_gas_price)
            if row['price_ngl']==0.0:
                new_ngl_price=last_gas[-1]*config['after_strip_escalator_ngl']
                if new_ngl_price>=config['price_ngl_max']:
                    prices.ix[idx, 'price_ngl']=config['price_ngl_max']
                    last_ngl.append(config['price_ngl_max'])
                else:
                    prices.ix[idx, 'price_ngl']=new_ngl_price
                    last_ngl.append(new_ngl_price)
    else:
        print("pricing module, price_type unknown")
    prices.to_excel(output_excel_file)
    return prices



def dump_prices(oil_file, gas_file):
    oil=pd.DataFrame([x[1] for x in config['price_oil'].items()], index=[x[0] for x in config['price_oil'].items()])
    oil.to_excel(oil_file)
    oil=pd.DataFrame([x[1] for x in config['price_gas'].items()], index=[x[0] for x in config['price_gas'].items()])
    oil.to_excel(gas_file)


def update_oil_prices(oil_file, gas_file):
    oil=pd.read_excel(oil_file)
    oil_working=oil.to_dict()
    oil_new={}
    for k,v in oil_working[0].iteritems():
        if type(k)==datetime.datetime:
            oil_new[datetime.datetime.strftime(k, '%m/%d/%Y')]=round(v,2)
        elif type(k)==unicode:
            oil_new[str(k)]=round(v,2)
        else:
            oil_new[k]=round(v,2)
    #config['price_oil']=oil_new

def update_gas_prices(oil_file, gas_file):
    gas=pd.read_excel(gas_file)
    gas_working=oil.to_dict()
    gas_new={}
    for k,v in gas_working[0].iteritems():
        if type(k)==datetime.datetime:
            gas_new[datetime.datetime.strftime(k, '%m/%d/%Y')]=round(v,2)
        elif type(k)==unicode:
            gas_new[str(k)]=round(v,2)
        else:
            gas_new[k]=round(v,2)
    #config['price_gas']=new_gas

def update_prices():
    update_oil_prices()
    update_gas_prices()