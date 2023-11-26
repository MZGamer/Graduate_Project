using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using TMPro;

public class HistoryDataUI : MonoBehaviour {



    public TMP_Text type;
    public TMP_Text questionText;
    public TMP_Text timeText;
    public TMP_Text restaurantNumText;

    public void setData(history data) {
        if (data.questionType == 0) {
            type.text = "∞›GPT";
        } else {
            type.text = "ß‰¿\∆U";
        }
        questionText.text = data.question;
        timeText.text = data.time.ToString();
        restaurantNumText.text = String.Format("¿\∆Uº∆∂q : {0}", data.restaurants.Count);

    }



}
