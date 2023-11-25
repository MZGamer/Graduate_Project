using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Linq;

public class UIManager : MonoBehaviour
{

    public static Queue<Package> pkgQueue;
    public List<Restaurant> restaurants;
    public int restaurantIndex;
    public List<GameObject> restaurantItem;
    public GameObject restaurantTemplate;

    public static bool disconnect;

    [Header("Middle")]
    public GameObject restaurantInfoFolder;
    public GameObject restaurantDetail;
    public GameObject searchFiled;

    public static bool gMapScoreShow;

    [Header("GPTSearch")]
    public TMP_InputField LocationInput;
    public TMP_InputField TargetInput;

    [Header("Top")]
    public TMP_Dropdown scoreDisplay;
    public TMP_Dropdown scoreSortBy;

    public GameObject listTop;
    public GameObject detailTop;

    [Header("Left")]
    public Button askGPTButton;
    public Button requestRestaurantButton;
    public Button historyButton;
    public Button reConnectedButton;
    
    [Header("Botton")]
    public GameObject listBotton;
    public GameObject detailBotton;
    public GameObject disconnectIcon;
    public GameObject searchingIcon;

    [Header("Detail")]
    public TMP_Text detailName;
    public TMP_Text detailAddress;
    public TMP_Text portionScoreText;
    public TMP_Text serviceScoreText;
    public TMP_Text environmentScoreText;
    public TMP_Text priceScoreText;
    public TMP_Text food_qulityScoreText;
    public TMP_Text comment;
    // Start is called before the first frame update
    void Start()
    {
        disconnect = true;
        NetworkManager.ip = "127.0.0.1";
        NetworkManager.port = 2933;
        NetworkManager.connectSettingComplete = true;
        Package test = new Package(ACTION.ASKGPT, "嘉義", "美食");
        //NetworkManager.sendingQueue.Enqueue(test);
        gMapScoreShow = false;
        restaurantIndex = 0;
        pkgQueue = new Queue<Package>();

        restaurants = new List<Restaurant>();
        Restaurant testr = new Restaurant();


        testr.type = "台式";
        testr.address = "600嘉義市東區小雅路382號";
        testr.name = "嘉義噴水雞肉飯-小雅旗艦店";
        testr.detailRating = new List<float>();
        testr.detailRating.Add(2.22f);
        testr.detailRating.Add(2.22f);
        testr.detailRating.Add(2.22f);
        testr.detailRating.Add(2.22f);
        testr.detailRating.Add(2.22f);

        testr.GRating = 3.5f;

        restaurants.Add(testr);
        restaurants.Add(testr);
        restaurants.Add(testr);
        restaurants.Add(testr);
        restaurants.Add(testr);
        restaurants.Add(testr);

        UIUpdate();

    }

    // Update is called once per frame
    void Update()
    {
        packageAnalyze();
        if (disconnect) {
            disconnectIcon.SetActive(true);
            reConnectedButton.interactable = true;
            searchingIcon.SetActive(false);
        } else {
            disconnectIcon.SetActive(false);
            reConnectedButton.interactable=false;
        }
    }

    void packageAnalyze() {
        Package package = null;
        if (pkgQueue.Count == 0) {
            return;
        } else {
            package = pkgQueue.Dequeue();
        }
        switch (package.ACTION) {
            case ACTION.RECEIVEDATA: {
                    /*
                    Debug.Log(package.restaurantRequestName);
                    Debug.Log(package.requestLocation);
                    Debug.Log(package.requestTarget);
                    Debug.Log(package.restaurantData);*/
                    restaurants = package.restaurantData;
                    restaurantIndex = 0;

                    askGPTButton.interactable = true;
                    requestRestaurantButton.interactable = true;
                    searchingIcon.SetActive(false);
                    UIUpdate();
                }
                break;
        }
    }

    void UIUpdate() {
        foreach (GameObject obj in restaurantItem) {
            Destroy(obj);
        }
        restaurantItem.Clear();
        for (int i = restaurantIndex; i < Mathf.Min(restaurantIndex + 4, restaurants.Count); i++) {
            int index = i;
            GameObject temp = Instantiate(restaurantTemplate, restaurantInfoFolder.transform);
            restaurantInfo info = temp.GetComponent<restaurantInfo>();
            info.setData(restaurants[i]);
            Button but = temp.GetComponent<Button>();
            but.onClick.AddListener(() =>  seeDetail(index));
            restaurantItem.Add(temp);
        }
    }

   

    

    public void send() {
        string loc = LocationInput.text;
        string target = TargetInput.text;
        if (loc == "") {
            loc = "嘉義市";
        }
        if (target == "") {
            target = "美食";
        }
        askGPTButton.interactable = false;
        requestRestaurantButton.interactable = false;
        Package package = new Package(ACTION.ASKGPT, loc, target);
        NetworkManager.sendingQueue.Enqueue(package);
        searchingIcon.SetActive(true);
        
        closeSearch();

    }

    public void askGPT() {
        searchFiled.SetActive(true);
        
    }
    public void closeSearch() {
        searchFiled.SetActive(false);
    }

    public void changeScoreDisplay() {
        if (scoreDisplay.value == 0) {
            gMapScoreShow = false;
        } else {
            gMapScoreShow = true;
        }
    }

    public void changeSoreSort() {
        if (scoreDisplay.value == 0) {
            restaurants = restaurants.OrderByDescending(r => r.GRating).ToList();
        } else {
            restaurants = restaurants.OrderByDescending(r => r.detailRating[scoreSortBy.value-1]).ToList();
        }

        UIUpdate();
    }

    public void LastPage() {
        if(restaurantIndex - 4 >= 0) {
            restaurantIndex -= 4;
            UIUpdate();
        }

    }

    public void nextPage() {
        if(restaurantIndex + 4 < restaurants.Count) {
            restaurantIndex += 4;
            UIUpdate();
        }
    }

    public void backToList() {
        detailTop.SetActive(false);
        listTop.SetActive(true);
        detailBotton.SetActive(false);
        listBotton.SetActive(true);

        restaurantDetail.SetActive(false);
        restaurantInfoFolder.SetActive(true);
    }

    public void seeDetail(int index) {
        Restaurant r = restaurants[index];

        detailName.text = r.name;
        detailAddress.text = r.address;
        portionScoreText.text = r.detailRating[0].ToString();
        serviceScoreText.text = r.detailRating[1].ToString();
        environmentScoreText.text = r.detailRating[2].ToString();
        priceScoreText.text = r.detailRating[3].ToString();
        food_qulityScoreText.text = r.detailRating[4].ToString();
        comment.text = r.review; // 暫時替代，記得改回comment
        comment.text = comment.text.Replace("\\", "\n");


        detailTop.SetActive(true);
        listTop.SetActive(false);
        detailBotton.SetActive(true);
        listBotton.SetActive(false);

        restaurantDetail.SetActive(true);
        restaurantInfoFolder.SetActive(false);
    }

    public void reconnectedButton() {
        NetworkManager.connectSettingComplete = true;
    }

}
