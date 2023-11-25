using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class Restaurant
{
    public string name;
    public string placeID;
    public string type;
    public string address;
    public Dictionary<string, string> location;
    public string command;
    public float GRating;
    public int raitingTotal;
    public List<float> detailRating;
    public string review;
}
