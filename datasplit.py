import os
import random
import shutil
data_src = r'E:\ZB\cell\20200929-ACE2-RBD\output\img'
data_to = r'data'
trainset = 0.8
evalset = 1-trainset
dic = {}
for a,b,c in os.walk(data_src):
    if len(c)!=0:
        dic[os.path.basename(a)]=[]
    for i in c:
        if i.endswith('.jpg'):
            dic[os.path.basename(a)].append(os.path.join(a,i))
lst=[]
for _,v in dic.items():
    lst.append(len(v))
trainset_num = int(trainset*min(lst))
dic_new_train={}
dic_new_eval={}
for k,v in dic.items():
    random.shuffle(v)
    dic_new_train[k]=v[:trainset_num]
    dic_new_eval[k]=v[trainset_num:]
for k,v in dic_new_train.items():
    new_dir = os.path.join(data_to+'/train',k)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    for i in v:
        shutil.copy(i,os.path.join(new_dir,os.path.basename(i)))
for k,v in dic_new_eval.items():
    new_dir = os.path.join(data_to+'/val',k)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    for i in v:
        shutil.copy(i,os.path.join(new_dir,os.path.basename(i)))
