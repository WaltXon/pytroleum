import requests
import pprint

url = r'http://api.eia.gov/series'
api_key = ''

eia_series = {
    'wti': {
        'daily': 'PET.RWTC.D',
        'weekly': 'PET.RWTC.W',
        'monthly': 'PET.RWTC.M',
        'annual': 'PET.RWTC.A',
    },
    'henryhub': {
        'daily': 'NG.RNGWHHD.D',
        'weekly': 'NG.RNGWHHD.W',
        'monthly': 'NG.RNGWHHD.M',
        'annual': 'NG.RNGWHHD.A',
    },
    'nglp': {
        'daily': 'NG.NGM_EPG0_PLC_NUS_DMMBTU.D',
        'weekly': 'NG.NGM_EPG0_PLC_NUS_DMMBTU.W',
        'monthly': 'NG.NGM_EPG0_PLC_NUS_DMMBTU.M',
        'annual': 'NG.NGM_EPG0_PLC_NUS_DMMBTU.A',
    },
}


def get_eia_price_data(series, freq):
    addr = url
    data = {
            'api_key': api_key,
            'series_id': eia_series[series][freq],
            }

    r = requests.get(addr, params=data)
    rdict = r.json()['series'][0]
    data = rdict['data']
    del rdict['data']
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rdict)
    return data
