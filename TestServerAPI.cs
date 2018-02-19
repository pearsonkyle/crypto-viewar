using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;
using UnityEngine;
using System;




public class CoroutineWithData
{

    public Coroutine coroutine { get; private set; }
    public object result;
    private IEnumerator target;

    public CoroutineWithData(MonoBehaviour owner, IEnumerator target)
    {
        this.target = target;
        this.coroutine = owner.StartCoroutine(Run());
    }

    private IEnumerator Run()
    {
        while (target.MoveNext())
        {
            result = target.Current;
            yield return result;
        }
    }
}


[System.Serializable]
public class ApiObject
{
    public string timestamp;
    public float btc;
    public float eth;
    public float ltc;

    // default constructor 
    public ApiObject()
    {
        btc = 14000f;
        eth = 700f;
        ltc = 200f;
        timestamp = "2017-04-20 00:00:00";
    }

    public string toString()
    {
        return JsonUtility.ToJson(this);
    }
}

[System.Serializable]
public class Response
{
    public ApiObject[] data;
}


public class TestServerAPI : MonoBehaviour {

    private string base_url = "https://crypto-viewar.herokuapp.com/select/";
    public int n_points = 10;

    ApiObject[] data;

    // Use this for initialization
    public IEnumerator Start () {
        CoroutineWithData cd = new CoroutineWithData(this, TestGet());
        yield return cd.coroutine;
        data = (ApiObject[]) cd.result;
        Debug.Log("result is :" + cd.result);
        Debug.Log("Litecoin Price: " + data[0].ltc);

        // load timestamp into DateTime object
        // from Datetime you can compute time-delta for x-axis
        // output from server in format: %Y-%m-%d %H:%M:%S
        DateTime myDate = DateTime.ParseExact(data[0].timestamp, "yyyy-MM-dd HH:mm:ss", null);
        Debug.Log(myDate.ToString());
    }


    public IEnumerator TestGet()
    {
        // call URL 
        WWW www = new WWW(base_url+n_points.ToString());
        yield return www;

        Debug.Log(www.text);

        // load in value from api
        Response r = new Response();
        r = JsonUtility.FromJson<Response>(www.text);

        Debug.Log("Bitcoin Price: " + r.data[0].btc);
        Debug.Log("Ethereum Price: " + r.data[0].eth);
        
        Debug.Log("Length of Data:" + r.data.Length);

        // just return image data from server 
        yield return r.data; // will go to cd.result in Start()
    }


    // Update is called once per frame
    void Update () {
		
	}
}
