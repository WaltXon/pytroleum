import requests
import pprint

api_key=''

def get_eia_wti_monthly(addr=r'http://api.eia.gov/series/',data={'api_key': api_key, 'series_id': 'PET.RWTC.M'}):
    r = requests.get(addr, params=data)
    rdict=r.json()['series'][0]
    data=rdict['data']
    del rdict['data']
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rdict)
    return data

def get_eia_wti_annual(addr=r'http://api.eia.gov/series/',data={'api_key': api_key, 'series_id': 'PET.RWTC.A'}):
    r = requests.get(addr, params=data)
    rdict=r.json()['series'][0]
    data=rdict['data']
    del rdict['data']
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rdict)
    return data

def get_eia_henryhub_monthly(addr=r'http://api.eia.gov/series/',data={'api_key': api_key, 'series_id': 'NG.RNGWHHD.M'}):
    r = requests.get(addr, params=data)
    rdict=r.json()['series'][0]
    data=rdict['data']
    del rdict['data']
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rdict)
    return data

def get_eia_henryhub_annual(addr=r'http://api.eia.gov/series/',data={'api_key': api_key, 'series_id': 'NG.RNGWHHD.A'}):
    r = requests.get(addr, params=data)
    rdict=r.json()['series'][0]
    data=rdict['data']
    del rdict['data']
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rdict)
    return data