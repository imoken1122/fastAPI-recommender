import Levenshtein
import pickle
import pykakasi
import re
from googletrans import Translator

kks = pykakasi.kakasi()
translator = Translator()
with open("./pickle/id2anime.pkl", "rb") as f:
    id2anime = pickle.load(f)
with open("./pickle/en2ja.pkl", "rb") as f:
    en2ja = pickle.load(f)

def get_sim_str(title):

    #name2levdist = {v:1 - round(Levenshtein.distance(title,v)/(max(len(title),len(v))),4) for k,v in id2anime.items()}
    name2jarodist = {v:round(Levenshtein.jaro_winkler(title,v),4) for k,v in id2anime.items()}
    name2esmb ={v:round(Levenshtein.jaro_winkler(title,v),4)* 0.3 + 
                (1 - round(Levenshtein.distance(title,v)/(max(len(title),len(v))),4)) * 0.7
                       for k,v in id2anime.items()}
  #  return sorted(name2levdist.items(),key =lambda x : -x[1])
    #return sorted(name2jarodist.items(),key =lambda x : -x[1])
    return sorted(name2esmb.items(),key =lambda x : -x[1])

def convert_title(title):

    p = re.compile('[\ァ-ヿ]+')
    tmp = p.findall(title)

    if len(tmp) != 0:
        for word in tmp:
            title = title.replace(word,translator.translate(word).text)


    res = kks.convert(title)
    title = "".join([r["passport"] for r in res])
    a = get_sim_str(title)[:10]

    return a[0][0]

def en2ja_title(title_list):
    return [en2ja[t] for t in title_list]
