from flask import Flask
import sys 
import optparse
import time
import json
import urllib
from bs4 import BeautifulSoup


app=Flask(__name__)
start=int(round(time.time()))

@app.route("/")
def hello_world():
    url="https://www.codechef.com/contests"
    page=urllib.request.urlopen(url)
    soup=BeautifulSoup(page,"lxml")
    mydivs=soup.find_all("table",{"class" : "dataTable"})
    ln=len(mydivs)
    link=[]
    name=[]
    start=[]
    end=[]
    for i in range(0,(ln-1)):
      tbody=mydivs[i].find("tbody")
      trs=tbody.findAll("tr")
      ln2=len(trs)
      for j in range (0,ln2):
        tds=trs[j].findAll("td")
        link.append("/"+tds[0].string)
        name.append(tds[1].string)
        start.append(tds[2]["data-starttime"])
        end.append(tds[3]["data-endtime"])    
    contest={"result":[{"link":l,"name":n,"start":s,"end":e} for l,n,s,e in zip(link,name,start,end)]} 
    return json.dumps(contest)


if __name__=='__main__':
    parser=optparse.OptionParser("usage=simpleapp.py -p")
    parser.add_option('-p','--port',action='store',dest='port',help='The port to listen on.')
    (args, _)=parser.parse_args()
    if args.port==None:
        print ("Missing required arguments: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0',port=int(args.port),debug=False)
    
