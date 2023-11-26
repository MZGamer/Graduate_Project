using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System.Net;
using System;
using System.Threading;
using System.Text;
using UnityEngine.SceneManagement;
using TMPro;

public class NetworkManager : MonoBehaviour
{
    static Socket clinetSocket;
    List<Socket> gateway = new List<Socket>();
    private static byte[] result = new byte[2048];
    public static Queue<Package> sendingQueue = new Queue<Package>();
    public static bool connectSettingComplete = false;
    public static string ip;
    public static int port;
    bool connect = false;
    string temp = "";

    int chkIndex = 0;
    string chktemp = "";
    string chkStr = "ENDCOMMUNICATION";

    // Start is called before the first frame update
    void Start()
    {
        Application.runInBackground = true;
        //StartConnect();
        connectSettingComplete = false;
    }

    // Update is called once per frame
    void Update() {

        if (connectSettingComplete)
            StartConnect();
        //listenSocket();
        packageSend();

    }

    public void StartConnect() {
        if (connect)
            return;
        connectSettingComplete = false;
        IPEndPoint ipe;
        try {
            IPAddress ipAddress = IPAddress.Parse(ip);
            ipe = new IPEndPoint(ipAddress, port);
        } catch {
            return;
        }

        try {

            clinetSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            clinetSocket.ReceiveBufferSize = 2048;
            clinetSocket.Connect(ipe);
            //clinetSocket.Blocking = false;
            connect = true;
            UIManager.disconnect = false;
            temp = "";
            chkIndex = 0;
            chktemp = "";

            StartCoroutine(listenSocket());
        } catch (System.Net.Sockets.SocketException sockEx) {
            Debug.Log(sockEx);
            Disconnected();
            connect = false;
        }
        

    }


    IEnumerator listenSocket() {
        while (true) {
            if (!connect)
                break;
            gateway.Add(clinetSocket);
            Socket.Select(gateway,null,null,100);
            //Debug.Log(gateway.Count);
            try {
                if (gateway.Count != 0) {
                    //通過clientSocket接收資料
                    int receiveNumber = clinetSocket.Receive(result);
                    if (receiveNumber <= 0) {
                        connect = false;
                        Debug.Log(" You lost connection with server");
                        Debug.Log("Disconnected");
                        UIManager.disconnect = true;
                    } else {
                        
                        string json = Encoding.UTF8.GetString(result);
                        json = json.Replace("\0", string.Empty);
                        Debug.Log("Receive : " + json);
                        Array.Clear(result, 0, result.Length);
                        for (int i = 0; i < json.Length; i++) {
                            if (json[i] != '{' && temp == "") {
                                temp = "";
                                Debug.LogWarning("JunkPackage");
                                break;
                            }
                            if (json[i] == chkStr[chkIndex]) {
                                chkIndex++;
                                chktemp += json[i];
                            } else {
                                chkIndex = 0;
                                temp = temp + chktemp + json[i];
                                chktemp = "";

                                /*if (temp.Length == 7 && temp != "{\"src\":") {
                                    temp = "";
                                    Debug.LogWarning("JunkPackage");
                                    break;
                                }*/
                            }
                            if (chkIndex == chkStr.Length){
                                Debug.LogWarning("Package Get" + temp);
                                Debug.LogWarning(JsonUtility.FromJson<Package>(temp));
                                UIManager.pkgQueue.Enqueue(JsonUtility.FromJson<Package>(temp));
                                temp = "";
                                chkIndex = 0;
                                chktemp = "";
                            }
                        }
                    }
                }

            } catch (System.Net.Sockets.SocketException sockEx) {
                Debug.Log(sockEx);
                Disconnected();
                break;
            }
            yield return new WaitForSeconds(0.1f);
        }
        yield return null;
    }

    void packageSend() {
        if (!connect)
            return;

        while(sendingQueue.Count != 0) {
            try {
                Package pkg = sendingQueue.Dequeue();
                string json = JsonUtility.ToJson(pkg) + chkStr;
                clinetSocket.Send(Encoding.UTF8.GetBytes(json));
                Debug.Log("pkg Send");
            } catch (System.Net.Sockets.SocketException sockEx) {
                Debug.Log(sockEx);
                Disconnected();
            }

        }

    }

    public void MessageUpdate(string message) {
        //UI_Manager.talkMessage += message;
    }

    private void OnApplicationQuit() {
        Disconnected();


    }
    private void Disconnected() {
        UIManager.disconnect = true;
        if (connect) {
            try {
                clinetSocket.Dispose();
            } catch {

            }
            Debug.Log("Disconnected");
        }
    }
}
