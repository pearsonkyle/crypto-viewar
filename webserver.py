import json
import datetime

from flask import Flask, request,jsonify,Response
from sqlalchemy import desc

from sqlserver import Database, Cryptocurrency

app = Flask(__name__)

# set up database connection 
db = Database( settings=json.load(open("readonly.json",'r')),
               dtype=Cryptocurrency )

@app.route('/select/<int:npts>',methods=['GET'])
def select(key='btc',npts=100):
    recent = db.session.query(db.dtype).order_by(desc(db.dtype.timestamp)).limit(npts).all()
    jsons = [i.toJSON() for i in recent]
    resp = Response( json.dumps(jsons) ) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/',methods=['GET'])
def index():
    return "Official API for Crypto ViewAR - iOS App"

if __name__ == "__main__":
    try:
        print(' running on port =',sys.argv[1] )
        app.run(host='0.0.0.0',port=sys.argv[1])
    except:
        app.run(host='0.0.0.0',debug=True)