
import turicreate as tc
import numpy as np
from utils import en2ja_title
import pandas as pd
class AnimeRecommenderAPI:
    def __init__(self,):
        self.model = None
    def load(self,):
        #weight = model.get_weights()
        #aemb = weight[1]
        self.rankMFmodel = tc.load_model("./models/rankMF_all.model")
        self.MFmodel = tc.load_model("./models/MF_all.model")

    def cos_sim(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def filter(self,df,k):

        ja_items = en2ja_title(df.similar.values)
        ja_items = np.unique(ja_items).tolist()
        if len(df)!=0:
            key = en2ja_title([df.name.values[0]])[0]
            if key in ja_items:
                del ja_items[ja_items.index(key)]

            
        sim_item = ja_items[:k]
        return sim_item

    def Deep_simlality_anime(self,key):
        pass
    """
        choice = aemb[key,:]
        dot = [self.cos_sim(choice, v) for v in aemb]
        sim_dic = {k:v for k,v in enumerate(dot)}
        sim_n_top = sorted(sim_dic.items(), key = lambda x : -x[1])[1:11]
        anime_n_top = [(id2anime[id[0]],id[1]) for id in sim_n_top]

        return anime_n_top
    """
    

    def MF_similar_anime(self, anime_title, k=10):
        df = self.MFmodel.get_similar_items([anime_title],k=50).to_dataframe() #columns: name similar score rank
        filter_item = self.filter(df,k)
    
        return self.response_format(filter_item,df.score.values[:k])

    def RankMF_similar_anime(self,anime_title,k=10):
        df = self.rankMFmodel.get_similar_items([anime_title],k=50).to_dataframe()
        filter_item = self.filter(df,k)
        return self.response_format(filter_item,df.score.values[:k])
    
    def response_format(self,sim_item,sim_score ):
        res = [{"rank":i+1,"recommend_title":t,"score":round(s,3)}
                 for i,(t,s) in enumerate(zip(sim_item,sim_score))
                 ] 
        return res 
    def recommend(self, model, anime_title,num_item):
        if model == "RankMF":
            sim_itm = self.RankMF_similar_anime(anime_title,num_item)
        else:
            sim_itm = self.MF_similar_anime(anime_title,num_item)
        return sim_itm
 


