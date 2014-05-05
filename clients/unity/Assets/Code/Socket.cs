using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using System.IO;
using System;

namespace RGBPi
{
    public class Socket
    {
        private bool socketReady = false;

        private TcpClient mySocket;
        private NetworkStream theStream;
        private StreamWriter theWriter;
        private StreamReader theReader;
        
        // **********************************************
        public bool Connect(string host, int port)
        {
            try
            {
                mySocket = new TcpClient(host, port);
                theStream = mySocket.GetStream();
                theWriter = new StreamWriter(theStream);
                theReader = new StreamReader(theStream);
                socketReady = true;
            }
            catch (Exception e)
            {
                Debug.Log("Socket error: " + e);
            }

            return socketReady;
        }

        public void Send(string theLine)
        {
            if (!socketReady)
                return;
            string foo = theLine;
            theWriter.Write(foo);
            theWriter.Flush();
        }

        public string Receive()
        {
            if (!socketReady)
                return "";
            if (theStream.DataAvailable)
                return theReader.ReadToEnd();
            return "";
        }
        
        public void Close()
        {
            if (!socketReady)
                return;
            theWriter.Close();
            theReader.Close();
            mySocket.Close();
            socketReady = false;
        }
    }
}
