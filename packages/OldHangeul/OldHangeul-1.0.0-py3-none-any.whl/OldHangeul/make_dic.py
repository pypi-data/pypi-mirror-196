
import os
import pickle

_ROOT=os.path.abspath(os.path.dirname(__file__))
_ROOT=os.path.abspath(os.path.join(_ROOT, os.pardir))

'''Dictionary'''
#초성 모음 
with open(os.path.join(_ROOT,'data','initial_jamo.pickle'), 'rb') as fr:
    initial_list = pickle.load(fr)

#중성 모음 
with open(os.path.join(_ROOT,'data','medial_jamo.pickle'), 'rb') as fr:
    medial_list = pickle.load(fr)

#종성 모음 
with open(os.path.join(_ROOT,'data','final_jamo.pickle'), 'rb') as fr:
    final_list = pickle.load(fr)

#ipf 모음
with open(os.path.join(_ROOT,'data','ipf.pickle'), 'rb') as fr:
    ipf = pickle.load(fr)

#jamo 기준 모음
with open(os.path.join(_ROOT,'data','jamo_list.pickle'), 'rb') as fr:
    jamo_list = pickle.load(fr)

#jamo 아닌 애들 모음
with open(os.path.join(_ROOT,'data','jamo_list_all.pickle'), 'rb') as fr:
    jamo_list_all = pickle.load(fr)


#jamo 아닌 애들 변환
with open(os.path.join(_ROOT,'data','jamo_list_key.pickle'), 'rb') as fr:
    jamo_list_key = pickle.load(fr)



