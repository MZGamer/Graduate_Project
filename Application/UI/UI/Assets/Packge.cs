using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

public enum ACTION {
    NULL,
    RECEIVEDATA,
    ASKGPT,
    REQUESTRESTAURANT
}
public class Package {
    public int src;
    public ACTION ACTION;
    public int index;
    public List<int> target;
    public List<PlayerStatus> playerStatuses;
    public bool askCounter;

    public Package(int src, ACTION ACTION = ACTION.NULL, int index = -1, List<int> target = null, bool askCounter = false, List<PlayerStatus> playerStatuses = null) {
        this.src = src;
        this.ACTION = ACTION;
        this.playerStatuses = playerStatuses;
        this.index = index;
        this.target = target;
        this.askCounter = askCounter;
    }
    public Package(int src, ACTION ACTION = ACTION.NULL, int index = -1, int target = 0, bool askCounter = false, List<PlayerStatus> playerStatuses = null) {
        this.src = src;
        this.ACTION = ACTION;
        this.playerStatuses = playerStatuses;
        this.index = index;
        this.target = new List<int>();
        this.target.Add(target);
        this.askCounter = askCounter;
    }
}
