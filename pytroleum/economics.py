import numpy as np
import pandas as pd
import locale

from config import config
from volumes import volumes
from pricing import pricing
from functions import annual_to_monthly_rate

vol=volumes()
prices=pricing(price_type=config['price_type'])
excel_output_file=''

econ=pd.concat([vol, prices], axis=1)

gas_cutoff=econ[econ['effective_decline_annual_gas']<=config['curves']['gas']['Dmin_annual']]
oil_cutoff=econ[econ['effective_decline_annual_oil']<=config['curves']['oil']['Dmin_annual']]

if oil_cutoff.index[0]<gas_cutoff.index[0]:
    index_cutoff=oil_cutoff.index[0]
else:
    index_cutoff=oil_cutoff.index[0]

econ=econ.loc[:index_cutoff]

econ['gross_sales_oil']=econ['gross_volume_oil']*econ['price_oil']*config['working_interest']
econ['gross_sales_gas']=econ['gross_volume_gas']*econ['price_gas']*config['working_interest']
econ['gross_sales_ngl']=econ['gross_volume_ngl']*econ['price_ngl']*config['working_interest']
econ['gross_sales_total']=econ['gross_sales_oil']+econ['gross_sales_gas']+econ['gross_sales_ngl']

econ['severance_tax_oil']=econ['gross_sales_oil']*config['taxes']['severance']['oil']*config['working_interest']
econ['severance_tax_gas']=econ['gross_sales_gas']*config['taxes']['severance']['gas']*config['working_interest']
econ['severance_tax_ngl']=econ['gross_sales_ngl']*config['taxes']['severance']['oil']*config['working_interest']
econ['severance_total']=econ['severance_tax_oil']+econ['severance_tax_gas']+econ['severance_tax_ngl']

econ['expenses_fixed']=config['expenses']['fixed']*config['working_interest']
econ['expenses_variable']=(config['expenses']['variable']['oil']*econ['gross_sales_oil']+config['expenses']['variable']['gas']*econ['gross_sales_gas']+config['expenses']['variable']['ngl']*econ['gross_sales_ngl'])*config['working_interest']

econ['expenses_total']=(econ['expenses_variable']+config['expenses']['fixed'])*config['working_interest']

econ['gross_revenue_after_sevtax_and_expenses']=econ['gross_sales_total']-econ['severance_total']-econ['expenses_total']

econ['ad_valorum_tax']=econ['gross_revenue_after_sevtax_and_expenses']*config['taxes']['ad_valorum']

econ['gross_revenue_after_sevtax_and_expenses_and_advaltax']=econ['gross_revenue_after_sevtax_and_expenses']-econ['ad_valorum_tax']

date_idx=pd.DatetimeIndex(start=config['capital_start_date'], end=config['production_start_date'], freq='M')
df_date_series=pd.DataFrame(index=date_idx, columns=[u'cum_prod_gas', u'cum_prod_ngl', u'cum_prod_oil', u'days_in_month',
       u'days_since_start', u'effective_decline_annual_gas',
       u'effective_decline_annual_oil', u'gross_volume_gas',
       u'gross_volume_ngl', u'gross_volume_oil', u'initial_rate_gas',
       u'initial_rate_ngl', u'initial_rate_oil', u'nominal_decline_annual_gas',
       u'nominal_decline_annual_oil', u'period_end_rate_gas',
       u'period_end_rate_oil', u'standard_time', u'price_oil', u'price_gas',
       u'price_ngl', u'date', u'gross_sales_oil', u'gross_sales_gas',
       u'gross_sales_ngl', u'gross_sales_total', u'severance_tax_oil',
       u'severance_tax_gas', u'severance_tax_ngl', u'severance_total',
       u'expenses_fixed', u'expenses_variable', u'expenses_total',
       u'gross_revenue_after_sevtax_and_expenses', u'ad_valorum_tax',
       u'gross_revenue_after_sevtax_and_expenses_and_advaltax', u'capital',
       u'gross_cash_flow', u'net_nondiscounted_cash_flow',
       u'cum_net_nondiscounted_cashflow', u'net_discounted_cashflow',
       u'cum_net_discounted_cashflow'])

econ_cap=pd.concat([econ, df_date_series], axis=1)
econ_cap.fillna(0.0, inplace=True)
econ_cap['capital']=0.0
econ_cap.ix[0,'capital']=(config['capital']['idc']+config['capital']['icc']+config['capital']['land'])*config['working_interest']

econ_cap['gross_cash_flow']=econ_cap['gross_revenue_after_sevtax_and_expenses_and_advaltax'].sub(econ_cap['capital'], axis='index')
econ_cap['net_nondiscounted_cash_flow']=(econ_cap['gross_revenue_after_sevtax_and_expenses_and_advaltax']*config['net_revenue_interest']).sub(econ_cap['capital'], axis='index')

econ_cap['cum_net_nondiscounted_cashflow']=econ_cap['net_nondiscounted_cash_flow'].cumsum()

econ_cap['net_discounted_cashflow']= econ_cap.apply(lambda row: row['net_nondiscounted_cash_flow']/((1+annual_to_monthly_rate(config['discount_rate_annual']))**(row['standard_time'])), axis=1)

econ_cap['cum_net_discounted_cashflow']=econ_cap['net_discounted_cashflow'].cumsum()


econ_cap.to_excel(excel_output_file)


npv=round(np.npv(annual_to_monthly_rate(config['discount_rate_annual']),econ_cap['net_nondiscounted_cash_flow']), 2)
irr=round(np.irr(econ_cap['net_nondiscounted_cash_flow']), 2)
pv5=round(np.npv(annual_to_monthly_rate(0.05),econ_cap['net_nondiscounted_cash_flow']), 2)
pv8=round(np.npv(annual_to_monthly_rate(0.08),econ_cap['net_nondiscounted_cash_flow']), 2)
pv10=round(np.npv(annual_to_monthly_rate(0.10),econ_cap['net_nondiscounted_cash_flow']), 2)
pv15=round(np.npv(annual_to_monthly_rate(0.15),econ_cap['net_nondiscounted_cash_flow']), 2)
pv20=round(np.npv(annual_to_monthly_rate(0.20),econ_cap['net_nondiscounted_cash_flow']), 2)

locale.setlocale(locale.LC_ALL, '')
print('''
    NPV: {}
    IRR: {}
    PV5: {}
    PV8: {}
    PV10: {}
    PV15: {}
    PV20: {}
    '''.format(locale.currency(npv, grouping=True), irr, locale.currency(pv5, grouping=True), locale.currency(pv8, grouping=True),
    locale.currency(pv10, grouping=True), locale.currency(pv15, grouping=True), locale.currency(pv20, grouping=True)))