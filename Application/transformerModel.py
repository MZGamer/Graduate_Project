import pandas as pd
import json
from tensorflow.keras import layers
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import sequence
from keras.models import Sequential,Model
from keras.layers import Dense,Input, Dropout, Embedding, Flatten,MaxPooling1D,Conv1D,SimpleRNN,LSTM,GRU,Multiply,GlobalMaxPooling1D
from keras.layers import Bidirectional,Activation,BatchNormalization,GlobalAveragePooling1D,MultiHeadAttention
from keras.callbacks import EarlyStopping
from keras.layers import concatenate
from tensorflow.keras.models import clone_model
import numpy as np
from dataclasses import dataclass
from dataclasses import field
from restaurant import Restaurant
import emoji
import re

class TransformerEncoder(layers.Layer):
    def __init__(self, embed_dim, dense_dim, num_heads, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self.attention = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.dense_proj = keras.Sequential(
            [layers.Dense(dense_dim, activation="relu"),layers.Dense(embed_dim),] )
        self.layernorm_1 = layers.LayerNormalization()
        self.layernorm_2 = layers.LayerNormalization()

    def call(self, inputs, mask=None):
        if mask is not None:
            mask = mask[:, tf.newaxis, :]
        attention_output = self.attention(inputs, inputs, attention_mask=mask)
        proj_input = self.layernorm_1(inputs + attention_output)
        proj_output = self.dense_proj(proj_input)
        return self.layernorm_2(proj_input + proj_output)

    def get_config(self):
        config = super().get_config()
        config.update({
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "dense_dim": self.dense_dim, })
        return config

class PositionalEmbedding(layers.Layer):
    def __init__(self, sequence_length, input_dim, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.token_embeddings = layers.Embedding(input_dim=input_dim, output_dim=output_dim)
        self.position_embeddings = layers.Embedding(input_dim=sequence_length, output_dim=output_dim)
        self.sequence_length = sequence_length
        self.input_dim = input_dim
        self.output_dim = output_dim

    def call(self, inputs):
        length = tf.shape(inputs)[-1]
        positions = tf.range(start=0, limit=length, delta=1)
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tf.math.not_equal(inputs, 0)

    def get_config(self):
        config = super().get_config()
        config.update({
            "output_dim": self.output_dim,
            "sequence_length": self.sequence_length,
            "input_dim": self.input_dim,})
        return config
    
def dicImoprt(path, mode, version):
    dic = {}
    path = path + f"/{mode}/{version}/model{version}dict.json"
    with open(path) as json_file:
        dic = json.load(json_file)
    reverseDic=dict([(value,key) for (key,value) in dic.items()])
    return dic, reverseDic



def decode(encText, reverseDic):
  dectext = ""
  for id in encText:
    if id in reverseDic:
      dectext += reverseDic[id]
    else:
      dectext += "#"
  return dectext

def build_model(top_words,max_words,num_labels,mode, path, modelVersion):
    inputs = Input(name='inputs',shape=[max_words,], dtype='float64')
    embed_dim = 32
    x= PositionalEmbedding(sequence_length=max_words, input_dim=top_words, output_dim=embed_dim)(inputs)
    x = TransformerEncoder(embed_dim, 32, 4)(x)
    x = GlobalMaxPooling1D()(x)
    x = Dropout(0.5)(x)
    outputs = Dense(num_labels, activation='softmax')(x)
    model = Model(inputs, outputs)

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    if(mode == "restaurantType"):

        model.load_weights(f"{path}/restaurantType/{modelVersion}/restaurantType_modelV{modelVersion}.h5")
        return model
    elif(mode == "reviewLabel"):
        modelList = [clone_model(model), clone_model(model), clone_model(model), clone_model(model), clone_model(model)]
        modelType = ["portion","service","environment","price","food_quality"]
        for i in range(len(modelList)):
            modelList[i].load_weights(f"{path}/reviewLabel/{modelVersion}/{modelType[i]}V{modelVersion}.h5")
        return modelList

@dataclass
class transformerModel:
    path : str
    typeVersion : str
    reviewVersion : str
    typeDic : dict
    typeReverseDic : dict
    reviewDic : dict
    reviewReverseDic : dict
    restaurantTypeModel : Model
    reviewLabelModel : list
    predToType : dict
    def __init__(self,path,typeVersion, reviewVersion):
        self.path = path
        self.typeVersion = typeVersion
        self.reviewVersion = reviewVersion
        self.typeDic, self.typeReverseDic = dicImoprt(path, "restaurantType", typeVersion)
        self.reviewDic, self.reviewReverseDic = dicImoprt(path, "reviewLabel", reviewVersion)
        self.restaurantTypeModel = build_model(len(self.typeDic), 1000, 12, "restaurantType", path, typeVersion)
        self.reviewLabelModel = build_model(len(self.reviewDic), 1000, 6, "reviewLabel", path, reviewVersion)
        self.predToType = {0: '飲料',1: '甜點',2: '港式',3: '韓式',4: '歐美',5: '素食',6: '東南亞',7: '中式',8: '健康餐',9: '台式',10: '日式',11: '小吃'}

    def textEnc(self, dic, testCase):
        encText = []
        encs = []
        maxlen = 1000

        testCase = emoji.demojize(testCase)
        testCase = re.sub(':\S+?:', ' ', testCase)
        if len(testCase) > maxlen:
            testCase = testCase[:maxlen]

        print(len(testCase))
        for i in range(maxlen):
            if(i<len(testCase) and testCase[i] in dic):
                encs.append(dic[testCase[i]])
            else:
                encs.append(0)


        if (encs != None) :
            encText.append(encs)
        
        return encText

    def textPreProcess(self, text):
        forType = ""
        forReview = []
        forFinal = []
        text = text.split("|")
        for t in text:
            original = t
            if(t == ""):
                continue
            
            t = t.split("^")
            if(len(t) == 0):
                continue
            if (t[len(t)-1] != ""):
                if(forType != ""):
                    forType += "|"
                forType += t[len(t)-1]
                forReview.append(t[len(t)-1])
                forFinal.append(f"{t[len(t)-2]}^{t[len(t)-1]}")
        return forType, forReview, forFinal

    def typePredict(self, text):
        encText = self.textEnc(self.typeDic, text)
        pred = self.restaurantTypeModel.predict(encText)
        return self.predToType[pred.argmax(axis=-1)[0]]
    
    def reviewPredict(self, textList):
        encText = []
        for t in textList:
            encText.append(self.textEnc(self.reviewDic, t)[0])
        scoreToAnalyze = []
        for i in range(len(self.reviewLabelModel)):
            test = self.reviewLabelModel[i].predict(encText)
            #print(test)
            scoreToAnalyze.append(test)

        reviewEachScore = [[],[],[],[],[]]

        finalScore = [0.0,0.0,0.0,0.0,0.0]
        reviewTypeInd = 0
        inp = input("checkPoint Enter anything to continue")
        for sc in scoreToAnalyze:
            totalScore = 0
            count = 0
            for i in range(len(sc)):
                score = np.argmax(sc[i])
                #print(score)
                reviewEachScore[reviewTypeInd].append(score)
                if(np.argmax(sc[i]) != 0):
                    count +=1
                    totalScore += score
            if(count == 0):
                finalScore[reviewTypeInd] = 0
            else:
                finalScore[reviewTypeInd] = round(totalScore / count,2)
            reviewTypeInd += 1
        return finalScore, reviewEachScore 