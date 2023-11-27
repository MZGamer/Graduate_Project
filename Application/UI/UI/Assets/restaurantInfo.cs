using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
public class restaurantInfo : MonoBehaviour
{
    public Restaurant restaurant;
    public TMP_Text type;
    public TMP_Text name;
    public TMP_Text address;

    public GameObject gMapScore;
    public TMP_Text gMapScoreText;

    public GameObject detailScoreFiled;
    public TMP_Text portionScore;
    public TMP_Text serviceScore;
    public TMP_Text environmentScore;
    public TMP_Text priceScore;
    public TMP_Text foodQualityScore;
    
    // Start is called before the first frame update
    void Start()
    {


    }

    public void setData(Restaurant res) {
        restaurant = res;
        type.text = restaurant.type;
        name.text = restaurant.name;
        address.text = restaurant.address;
        gMapScoreText.text = restaurant.GRating.ToString();
        portionScore.text = string.Format("份量 : {0} / 5.00", restaurant.detailRating[0]);
        serviceScore.text = string.Format("服務 : {0} / 5.00", restaurant.detailRating[1]);
        environmentScore.text = string.Format("環境 : {0} / 5.00", restaurant.detailRating[2]);
        priceScore.text = string.Format("價格 : {0} / 5.00", restaurant.detailRating[3]);
        foodQualityScore.text = string.Format("餐點 : {0} / 5.00", restaurant.detailRating[4]);
    }
    // Update is called once per frame
    void Update()
    {
        if (UIManager.gMapScoreShow) {
            gMapScore.SetActive(true);
            detailScoreFiled.SetActive(false);
        } else {
            gMapScore.SetActive(false);
            detailScoreFiled.SetActive(true);
        }
    }
}
