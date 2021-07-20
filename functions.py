import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import functions as F
import random as rnd


def getDataset(small,lenght,random):
    dataset_path = "D:/Desktop/dataspaces/bank_full.csv"
    if(small==1):
        if(random==1):
            n = sum(1 for line in open(dataset_path)) - 1
            skip = sorted(rnd.sample(range(1,n+1),n-lenght)) 
            dataset = pd.read_csv(dataset_path,delimiter=";", skiprows=skip)
        else:
            dataset=pd.read_csv(dataset_path,delimiter=";", nrows=lenght)
    else:
        dataset=pd.read_csv(dataset_path,delimiter=";")

    dataset.drop(["duration","month","day_of_week"
              ,"pdays"], axis=1, inplace=True) # elimino attributi

    dataset=F.deleteMissingValues(dataset, "unknown")
   
    for i in range(2,rnd.randint(3,6)):#mescolo il dataset
        for j in range(2,rnd.randint(3,6)):
            if(random==1):
                dataset = dataset.sample(frac=1).reset_index(drop=True) 
    return dataset
            
def deleteMissingValues(ds,att):
    dataset=ds
    indexRows=[]
    index=-1
    for row in dataset.iloc:
        index=index+1
        percentage="Delete missing values: "+str(int(100*index/len(dataset)))+"%"
        sys.stdout.write('\r'+percentage)
        if("unknown" in row.values):
            indexRows.append(index)
    sys.stdout.write('\r'+"                                             "+'\r')
    dataset.drop(indexRows , inplace=True)  #elimino missing values
    dataset.reset_index(drop=True, inplace=True) 
    return dataset

def OneHotEncoder(ds,attributes):
    dataset=ds
    for att in attributes:
        one_hot = pd.get_dummies(dataset[att])
        dataset = dataset.drop(att,axis = 1)
        dataset = dataset.join(one_hot)
        for i in range(0,len(one_hot.columns)):
            dataset = dataset.rename(columns={one_hot.columns[i]: att+"_"+one_hot.columns[i]})
    attributes=[]
    for att in dataset.columns:
        if(att!="y"):
            attributes.append(att)
    attributes.append("y")
    dataset= dataset[attributes]
    return dataset

def labelEncoder(ds,attributes):
    dataset=ds
    le = LabelEncoder()
    for att in attributes:
        dataset[att]=le.fit(dataset[att]).transform(dataset[att])
    return dataset

def getOccurrences(ds,attribute,normalize=0,order=0):
    column=ds[attribute]
    total_sum=len(column)
    values={}
    for v in column:
        if(v not in values):
            values[v]=[0,0]
    
    for i in range(0,len(ds)):
        value=ds.iloc[i][attribute]
        c=ds.iloc[i]["y"]
        if(c=="no" or c==0):
            values[value]=[values[value][0]+1,values[value][1]]
        else:
            values[value]=[values[value][0],values[value][1]+1]

    keys=list(values.keys())
    for i in range(0,len(keys)):
        tmp=keys[i]+"\n"+str(round((values[keys[i]][0]+values[keys[i]][1])*100/total_sum,1))+"%"
        keys[i]=tmp+"\n"+str(values[keys[i]][0]+values[keys[i]][1])
    no_list=[]
    yes_list=[]
    for k in values.keys():
        sum=values[k][0]+values[k][1]
        if(normalize==0):
            sum=1
        no_list.append(values[k][0]/sum)
        yes_list.append(values[k][1]/sum)
    if(order==1):
        if(normalize==1):
            for i in range(0,len(yes_list)-1):
                for j in range(0,len(yes_list)-1):
                    if(yes_list[j]>yes_list[j+1]):
                        yes_list[j], yes_list[j+1] = yes_list[j+1], yes_list[j]
                        no_list[j], no_list[j+1] = no_list[j+1], no_list[j]
                        keys[j], keys[j+1] = keys[j+1], keys[j]
        else:
            for i in range(0,len(yes_list)-1):
                for j in range(0,len(yes_list)-1):
                    if(yes_list[j]+no_list[j]<yes_list[j+1]+no_list[j+1]):
                        yes_list[j], yes_list[j+1] = yes_list[j+1], yes_list[j]
                        no_list[j], no_list[j+1] = no_list[j+1], no_list[j]
                        keys[j], keys[j+1] = keys[j+1], keys[j]
    
    return keys,no_list,yes_list
    
def getStatistic(ds,attribute):
    column=ds[attribute]
    statistics={}
    statistics["Min"]=min(column)
    statistics["1st Q."]=np.quantile(column, 0.25)
    statistics["Median"]=np.quantile(column, 0.5)
    statistics["Mean"]=(sum(column)/len(column))
    statistics["Std"]=np.std(column, axis=0)
    statistics["3st Q."]=np.quantile(column, 0.75)
    statistics["Max"]=max(column)
    return statistics  
    
def drawStatisticsTable(data,columns,rows):
    data_tmp=np.array(data).T.tolist()
    for i in range(0,len(rows)):
        for j in range(0,len(columns)):
            if(int(data_tmp[i][j])==data_tmp[i][j]):
                data_tmp[i][j]=int(data_tmp[i][j])
            else:
                data_tmp[i][j]=round(data_tmp[i][j],3)
    Rcolors = plt.cm.BuPu(np.linspace(0.3, 0.3, len(rows)))
    Ccolors = plt.cm.BuPu(np.linspace(0.3, 0.3, len(columns)))
    cell_text = []
    for row in data_tmp:
        cell_text.append(row)
    the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=Rcolors,
                      colColours=Ccolors,
                      colLabels=columns,
                      cellLoc="center",
                      loc='center')
    the_table.scale(0.6, 3)
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.box(on=None)
