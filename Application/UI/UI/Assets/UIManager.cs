using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Linq;
using System;

public class UIManager : MonoBehaviour
{

    public static Queue<Package> pkgQueue;
    public List<Restaurant> restaurants;
    public int restaurantIndex;
    public int historyIndex;
    public List<GameObject> restaurantItem;
    public GameObject restaurantTemplate;
    public GameObject historyInfoTemplate;

    public history tempHistory;
    public List<GameObject> historyData;
    public List<history> historys;

    public static bool disconnect;
    public bool seeHistory;
    public bool resetButton;

    [Header("Middle")]
    public GameObject restaurantInfoFolder;
    public GameObject restaurantDetail;
    public GameObject historyFiled;
    public GameObject askGPTFiled;
    public GameObject requestRestaurantFiled;

    public static bool gMapScoreShow;

    [Header("GPTSearch")]
    public TMP_InputField LocationInput;
    public TMP_InputField TargetInput;
    public TMP_InputField restaurantNeedInput;
    public TMP_InputField randomNeedInput;

    [Header("restaurantRequest")]
    public TMP_InputField restaurantInput;

    [Header("Top")]
    public TMP_Dropdown scoreDisplay;
    public TMP_Dropdown scoreSortBy;

    public GameObject listTop;
    public GameObject detailTop;
    public GameObject historyTop;

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
        //NetworkManager.sendingQueue.Enqueue(test);
        gMapScoreShow = false;
        restaurantIndex = 0;
        historyIndex = 0;
        pkgQueue = new Queue<Package>();

        restaurants = new List<Restaurant>();
        historys = new List<history>();
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
        if (disconnect) {
            disconnectIcon.SetActive(true);
            reConnectedButton.interactable = true;
            searchingIcon.SetActive(false);
            askGPTButton.interactable = false;
            requestRestaurantButton.interactable = false;
            resetButton = false;
        } else {
            disconnectIcon.SetActive(false);
            reConnectedButton.interactable=false;
            if (!resetButton) {
                askGPTButton.interactable = true;
                requestRestaurantButton.interactable = true;
                resetButton = true;
            }

            packageAnalyze();
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
                    seeHistory = false;
                    UIUpdate();
                    if (tempHistory != null) {
                        tempHistory.restaurants = restaurants;
                        historys.Add(tempHistory);
                    }

                }
                break;
        }
    }

    void UIUpdate() {
        if (!seeHistory) {
            historyTop.SetActive(false);
            listTop.SetActive(true);
            historyFiled.SetActive(false);
            restaurantInfoFolder.SetActive(true);
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
        } else {
            historyTop.SetActive(true);
            listTop.SetActive(false);
            historyFiled.SetActive(true);
            restaurantInfoFolder.SetActive(false);
            foreach (GameObject obj in historyData) {
                Destroy(obj);
            }
            historyData.Clear();
            for (int i = historyIndex; i < Mathf.Min(historyIndex + 4, historys.Count); i++) {
                int index = i;
                GameObject temp = Instantiate(historyInfoTemplate, historyFiled.transform);
                HistoryDataUI data = temp.GetComponent<HistoryDataUI>();
                data.setData(historys[i]);
                Button but = temp.GetComponent<Button>();
                but.onClick.AddListener(() => switchHistory(index));
                historyData.Add(temp);
            }
        }

    }


    public void switchHistory(int index) {
        restaurants = historys[index].restaurants;
        seeHistory = false;
        UIUpdate();
    }

    public void seeHistoryList() {
        backToList();
        seeHistory = true;
        UIUpdate();
    }
    

    public void askGPTsend() {
        string loc = LocationInput.text;
        string target = TargetInput.text;
        int restaurantNeed = 0;
        int randomNeed = 0;
        if (loc == "") {
            loc = "嘉義市";
        }
        if (target == "") {
            target = "美食";
        }

        if(restaurantNeedInput.text == "") {
            restaurantNeed = 0;
        } else {
            try {
                restaurantNeed = Convert.ToInt32(restaurantNeedInput.text);
            } catch {
                Debug.Log("restaurantNeed input error");
                return;
            }
        }

        if (randomNeedInput.text == "") {
            randomNeed = 0;
        } else {
            try {
                randomNeed = Convert.ToInt32(randomNeedInput.text);
            } catch {
                Debug.Log("randomNeed input error");
                return;
            }
        }
        askGPTButton.interactable = false;
        requestRestaurantButton.interactable = false;
        Package package = new Package(ACTION.ASKGPT, loc, target, restaurantNeed, randomNeed);
        NetworkManager.sendingQueue.Enqueue(package);
        searchingIcon.SetActive(true);
        tempHistory = new history(null, 0, loc + " " + target, DateTime.Now);
   

        closeSearch();

    }

    public void requestRstaurantSend() {
        string target = restaurantInput.text;
        if (target == "") {
            return;
        }
        askGPTButton.interactable = false;
        requestRestaurantButton.interactable = false;
        Package package = new Package(ACTION.REQUESTRESTAURANT, target);
        NetworkManager.sendingQueue.Enqueue(package);
        searchingIcon.SetActive(true);
        tempHistory = new history(null, 1, target, DateTime.Now);

        closeSearch();
    }

    public void askGPT() {
        closeSearch();
        askGPTFiled.SetActive(true);
        
    }

    public void restaurantResuest() {
        closeSearch();
        requestRestaurantFiled.SetActive(true);
    }

    public void closeSearch() {
        askGPTFiled.SetActive(false);
        requestRestaurantFiled.SetActive(false);

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
        if (seeHistory) {
            if (historyIndex - 4 >= 0) {
                historyIndex -= 4;
                UIUpdate();
            }
        } else {
            if (restaurantIndex - 4 >= 0) {
                restaurantIndex -= 4;
                UIUpdate();
            }
        }


    }

    public void nextPage() {
        if (seeHistory) {
            if (historyIndex + 4 < historys.Count) {
                historyIndex += 4;
                UIUpdate();
            }
        } else {
            if (restaurantIndex + 4 < restaurants.Count) {
                restaurantIndex += 4;
                UIUpdate();
            }
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
        comment.text = r.command; // 暫時替代，記得改回comment
        comment.text = comment.text.Replace("/n", "\n");


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
