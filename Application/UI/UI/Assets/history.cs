using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class history
{
    public history(List<Restaurant> restaurants, int questionType, string question, DateTime time) {
        this.restaurants = restaurants;
        this.questionType = questionType;
        this.question = question;
        this.time = time;
    }
    public List<Restaurant> restaurants;
    public int questionType { get; set; }
    public string question { get; set; }

    public DateTime time { get; set; }
}
