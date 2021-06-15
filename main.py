'''
:Data Breach Capture Through Censys
:Project: By Sanyam Jain
:EmailID: sanyam.jain2602@gmail.com
'''

from censys import Censys
from screenshot_machine import Screenshot
import time


def censys_results(api_id, secret, query, count=0):
    x = Censys(api_id, secret)
    ip_collect = []
    cursor = None
    for i in range(count+1):
        if count == 0:
            x1 = x.query(query)
            cursor = x1['result']['action_response']['result']['links']['next']
        else:
            x1 = x.query('services.service_name=ELASTICSEARCH', cursor=cursor)
            cursor = x1['result']['action_response']['result']['links']['next']
            #print(cursor)
        x1 = x1['result']['action_response']['result']['hits']
        for ips in x1:
            ip = ips['ip']
            port = [i.get('port') for i in ips['services']
                    if i['service_name'] == 'ELASTICSEARCH']
            for i in port:
                s = "{0}:{1}".format(ip, i)
                ip_collect.append(s)
    return ip_collect


def main():
    print('Process Start')
    print('Gathering URLs')
    #query = 'services.service_name=ELASTICSEARCH'
    query = '(services.software.product=`Elasticsearch`) and location.country=`United States`'
    results = censys_results(api_key, secret, query=query,
                             count=2)
    #print(results)
    print('Targeted URL Gathered')
    q = '/_cat/indices?v&s=docs.count'
    print('Generating Screenshots')
    for i in results:
        print(i)
        time.sleep(8)
        Screenshot(api_id).fetch_screenshot(i, q)
    print('All Screenshots are Generated')
    print('Process Done')

if __name__ == "__main__":
    main()
