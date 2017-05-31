import requests

api_key =''

base_url = 'https://app.drillinginfo.com/direct/#/'
rigs_base_url = r'http://di-api.drillinginfo.com/v1/direct-access/rigs?format=json&page=1&pagesize=5000'
permits_base_url = r'https://di-api.drillinginfo.com/v1/direct-access/permits?&format=json&page=1&pagesize=5000'
production_header_base_url=r'https://di-api.drillinginfo.com/v1/direct-access/producing-entities?state_province=TX&format=json&page=1&pagesize=5000'
production_monthly_base_url=r'https://di-api.drillinginfo.com/v1/direct-access/producing-entities-details?format=json&page=1&pagesize=5000'
#http_request_character_limit=2000

base_error_codes = { 200: 'Success',
                400: 'Invalid input parameter',
                500: 'The service encountered an unexpected error',
                401: 'Indicates the request contains an invalid Authorization token',
                405: 'Indicates the request contains a non-GET operation; only GET is supported',
                502: 'Indicates a necessary downstream service is unavailable; try again later',
            }


def api_request(api_url, api_key=api_key, error_codes=base_error_codes):
    print("begin api_request to url, qry str len == {}".format(len(api_url)))
    s = requests.Session()
    s.headers.update({'X-API-KEY': api_key})
    r=s.get(api_url)
    if r.status_code in error_codes.keys():
        error=error_codes[r.status_code]
    else:
        error='Unknown Error Code'

    print('response status {} {}'.format(r.status_code, error))
    j = r.json()
    print('end api_request...')
    return j


def production_header(api, url=production_header_base_url):
    print('begin production header request')
    url=production_header_base_url+r'&api_uwi={}'.format(api)
    data=api_request(url)
    print('end production header request')
    return data

def production_monthly(entity_id, url=production_header_base_url):
    print('begin production monthly request')
    url=production_monthly_base_url+r'&entity_id={}'.format(entity_id)
    data=api_request(url)
    print('end production monthly request')
    return data

def rigs_by_date(min_spud_date, max_spud_date, url=rigs_base_url):
    print('begin rig request from {} to {}'.format(min_spud_date, max_spud_date))
    url+=r'&min_spud_date={}&max_spud_date={}'.format(min_spud_date, max_spud_date)
    print('request url: {}'.format(url))
    data=api_request(url)
    print('request returned {} values'.format(len(data)))
    print('end rig request')
    return data

def permits_by_approved_date(states, min_approved_date, max_approved_date, url=permits_base_url):
    print('begin permits request from {} to {}'.format(min_approved_date, max_approved_date))
    url+=r'&state_province={}&min_approved_date={}&max_approved_date={}'.format(states, min_approved_date, max_approved_date)
    print('request url: {}'.format(url))
    data=api_request(url)
    print('request returned {} values'.format(len(data)))
    print('end permits request')
    return data