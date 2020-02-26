import json
import xmltodict
from bs4 import BeautifulSoup

WifiConfigStore='./WifiConfigStore.xml'

def arr2json(d=[],d1=''):
    t=d1.split(',')
    result={}
    for (k,v) in zip(t,d):
        result[k]=v
    return result

def parse(cc=""):
    if len(cc) == 0 : return {}
    y=BeautifulSoup(cc,features="html.parser")
    find_key= lambda y: [y.text for y in y.next_siblings if y!='\n'][1].replace("\"",'')
    return dict([(x.text.replace("\"",''),find_key(x)) for x in y.findAll('string') if x.get_attribute_list('name')[0]=='SSID'])

def parse1(cc=""):
    if len(cc) == 0 : return []
    y=BeautifulSoup(cc,features="html.parser")
    parse_item=lambda d:dict([(x.get('name'),x.text) for x in d.children if x!='\n'])
    z=[x.wificonfiguration for x in y.wificonfigstoredata.networklist if  x!=None  and x!='\n' and x.find('wificonfiguration')]
    r=[parse_item(x) for x in z]
    print(r)
    return r

def parse2(cc=""):
    return xmltodict.parse(cc)


def save(dd={},name='./wifi.json'):
    z=json.dumps(dd,indent=4)
    with open(name,'w') as f:
        f.write(z)

def test(file_name=WifiConfigStore):
    with open(file_name) as f:
        cc=f.read()
        d1=parse(cc)
        d2=parse1(cc)
        d3=parse2(cc)
        save(d1,"1.json")
        save(d2,"2.json")
        save(d3,"3.json")

test()
