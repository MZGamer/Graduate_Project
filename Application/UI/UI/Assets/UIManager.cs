using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        NetworkManager.ip = "127.0.0.1";
        NetworkManager.port = 2933;
        NetworkManager.connectSettingComplete = true;
        Package test = new Package(ACTION.ASKGPT, "¹Å¸q", "¬ü­¹");
        NetworkManager.sendingQueue.Enqueue(test);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
