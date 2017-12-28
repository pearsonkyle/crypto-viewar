# crypto-viewar
Official API for the crypto-viewAR app on iOS


API URL: https://crypto-viewar.herokuapp.com

You can retrieve the most recent prices using the URL: 
https://crypto-viewar.herokuapp.com/select/<int:npts>

For example, if you want want the most recent hour of data the url would be: 
https://crypto-viewar.herokuapp.com/select/60

Only the most recent data is returned. Data is mined every minute from the GDAX exchange. 


Accessing this API from Unity is shown in the "TestServerAPI.cs" file
