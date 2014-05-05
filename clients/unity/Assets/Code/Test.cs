using UnityEngine;
using System.Collections;
using RGBPi;


public class Test : MonoBehaviour {

    private GUIElement test;

	// Use this for initialization
	void Start () {
        test = GetComponent<GUITexture>();
	}
	
	// Update is called once per frame
	void Update () {
        if (Input.GetMouseButtonUp(0) && test.HitTest(Input.mousePosition))
        {
            Debug.Log("hit");
            Socket socket = new Socket();
            socket.Connect("192.168.1.150", 4321);
            socket.Send("{}");
            string result;
            Debug.Log(result = socket.Receive());
            GUIText txt = GameObject.Find("TestText").GetComponent<GUIText>();
            txt.text = result;
            socket.Close();
        }
	}
}
