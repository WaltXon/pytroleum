from collections import OrderedDict
import pprint
import datetime
import pandas as pd

from arps import arps_hyp_rate
from decline import rate_at_t, cum_at_t, effective_decline_annual, nominal_decline_annual
from config import config
from utilities import get_products, annual_to_monthly_rate

def volumes():
    volumes={
            'oil': [],
            'gas': [],
            'ngl': [],
            }

    products=get_products()

    date_series=pd.date_range(config['production_start_date'], periods=config['max_life_months'], freq='M')

    df = pd.DataFrame(index=date_series)

    df['date']=df.index
    df['days_in_month']=df.index.days_in_month
    df['days_since_start']=df['days_in_month'].cumsum()
    df['standard_time']=df['days_since_start']/(config['standard_days_in_year']/12.0)

    zipped=zip(df.index.format(),
                    df['days_in_month'],
                    df['days_since_start'],
                    df['standard_time'],
                )

    volumes_template = {d[0]: {'days_in_month':d[1],
                    'days_since_start': d[2],
                    'standard_time': d[3],
                     }
                    for d in zipped}

    volumes = OrderedDict(sorted(volumes_template.items(), key=lambda t:datetime.datetime.strptime(t[0], '%Y-%m-%d')))

    for product in products:
        rate=[config['curves'][product]['Qi_monthly'],]
        cumulative=[0.0,]
        time=[0.0]
        for date, row in volumes.iteritems():
            row['initial_rate_{}'.format(product)]=rate[-1]
            row['period_end_rate_{}'.format(product)]=rate_at_t(config['curves'][product]['nominal_decline_monthly'],
                config['curves'][product]['Qi_monthly'],
                row['initial_rate_{}'.format(product)],
                config['curves'][product]['b_factor'],
                config['curves'][product]['b_factor_adj'],
                config['curves'][product]['Dmin_monthly'],
                row['standard_time'])
            row['cum_prod_{}'.format(product)]=cum_at_t(
                config['curves'][product]['nominal_decline_monthly'],
                config['curves'][product]['Qi_monthly'],
                row['initial_rate_{}'.format(product)],
                config['curves'][product]['b_factor'],
                config['curves'][product]['b_factor_adj'],
                config['curves'][product]['Dmin_monthly'],
                row['standard_time'],
                time[-1],
                cumulative[-1])
            row['gross_volume_{}'.format(product)]=row['cum_prod_{}'.format(product)]-cumulative[-1]
            row['nominal_decline_annual_{}'.format(product)]=nominal_decline_annual(
                config['curves'][product]['nominal_decline_annual'],
                row['initial_rate_{}'.format(product)],
                config['curves'][product]['Qi_monthly'],
                config['curves'][product]['b_factor'],
                config['curves'][product]['Dmin_annual'])
            row['effective_decline_annual_{}'.format(product)]=effective_decline_annual(
                row['nominal_decline_annual_{}'.format(product)])
            rate.append(row['period_end_rate_{}'.format(product)])
            cumulative.append(row['cum_prod_{}'.format(product)])
            time.append(row['standard_time'])


    if 'ngl' not in products:
            for date, row in volumes.iteritems():
                row['gross_volume_ngl']=0.0
                row['cum_prod_ngl']=0.0
                row['initial_rate_ngl']=0.0

    df_vol=pd.DataFrame(volumes)
    df_vol_t = df_vol.T
    df_vol_t.index=pd.to_datetime(df_vol_t.index)

    df_vol_t.to_excel(r'C:\Users\WaltN\Desktop\GitHub\curvey\output\volumes.xlsx')
    return df_vol_t