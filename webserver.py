import sys
import json
import datetime

from flask import Flask, request,jsonify,Response
from sqlalchemy import desc

from sqlserver import Database, Cryptocurrency

app = Flask(__name__)

settings = json.load(open("readonly.json",'r'))

@app.route('/select/<int:npts>',methods=['GET'])
def select(npts=100):
    # set up database connection 
    db = Database( settings=settings, dtype=Cryptocurrency )
    data = db.session.query(db.dtype).order_by(desc(db.dtype.timestamp)).limit(serverpts).all()
    db.close()
    del db

    jsons = {'data': [i.toDict() for i in recent] }
    resp = Response( json.dumps(jsons) ) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# http://ec2-18-220-171-141.us-east-2.compute.amazonaws.com:6969/
@app.route('/select/<int:binsize>/<int:npts>',methods=['GET'])
def select_bin(binsize=1,npts=100):
    
    # parse inputs
    binsize = int(binsize)
    npts = int(npts)
    if binsize < 0: binsize *= 1
    if npts < 0: npts *= 1
    serverpts = int(binsize * npts)
    
    # get data from database
    db = Database( settings=settings, dtype=Cryptocurrency )
    data = db.session.query(db.dtype).order_by(desc(db.dtype.timestamp)).limit(serverpts).all()
    db.close()
    del db

    # compute averages for each bin 
    binned_list = []
    for i in range(npts):
        
        coin = Cryptocurrency()

        # get the middle index
        idx = int( (i+0.5)*binsize )
        coin.timestamp = data[idx].timestamp

        # compute average price for each coin
        sub = data[i*binsize:(i+1)*binsize]
        for k in coin.keys():
            price_list = [sub[j][k] for j in range(len(sub))]
            coin[k] = round(sum(price_list)/len(price_list),2)

        binned_list.append(coin)

    jsons = {'data': [i.toDict() for i in binned_list] }
    resp = Response( json.dumps(jsons) ) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp 


@app.route('/',methods=['GET'])
def index():
    return "Official API for Crypto ViewAR - iOS App"

if __name__ == "__main__":
    print(' running on port =',sys.argv[1] )
    app.run(host='0.0.0.0',port=int(sys.argv[1]) )