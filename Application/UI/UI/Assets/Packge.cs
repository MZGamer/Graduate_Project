using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using UnityEngine;

public enum ACTION {
    NULL,
    RECEIVEDATA,
    ASKGPT,
    REQUESTRESTAURANT
}

[System.Serializable]
public class Package {
    public ACTION ACTION;
    public string restaurantRequestName;
    public string requestLocation;
    public string requestTarget;
    public int restaurantNeed;
    public int randomNeed;
    public List<Restaurant> restaurantData;

    public Package(ACTION ACTION = ACTION.NULL, string requestLacation = "", string requestTarget = "", int restaurantNeed = 0, int randomNeed = 0) {
        this.ACTION = ACTION;
        this.restaurantRequestName = "";
        this.requestLocation = requestLacation;
        this.requestTarget = requestTarget;
        this.restaurantData = new List<Restaurant>(0);
        this.restaurantNeed = restaurantNeed;
        this.randomNeed = randomNeed;
    }
    public Package(ACTION ACTION = ACTION.NULL, string restaurantRequestName = "") {
        this.ACTION = ACTION;
        this.restaurantRequestName = restaurantRequestName;
        this.requestLocation = "";
        this.requestTarget = "";
        this.restaurantData = new List<Restaurant>(0);
        this.restaurantNeed = 0;
        this.randomNeed = 0;
    }

    public Package(ACTION ACTION = ACTION.NULL, List<Restaurant> restaurantData = null) {
        this.ACTION = ACTION;
        this.restaurantRequestName = "";
        this.requestLocation = "";
        this.requestTarget = "";
        this.restaurantData = restaurantData;
        this.restaurantNeed = 0;
        this.randomNeed = 0;
    }
    public Package(ACTION ACTION, string restaurantRequestName = "", string requestLocation = "", string requestTarget = "", List<Restaurant> restaurantData = null) {
        this.ACTION = ACTION;
        this.restaurantRequestName=restaurantRequestName;
        this.requestLocation = requestLocation;
        this.requestTarget = requestTarget;
        this.restaurantData = restaurantData;
        this.restaurantNeed = 0;
        this.randomNeed = 0;
    }
    public string toString() {
        string s = "";

        return s;
    }
}
