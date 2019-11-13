import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import SimpleExpSmoothing,ExponentialSmoothing

def calc(a,b,n):
    veca=np.array(a)
    vecb=np.array(b)
    sum=0.0
    for i in range(n):
        sum+=((veca[i]-vecb[i])/vecb[i])**2
    return sum/n

def mxpara(df1,df2):
    mn=1e9
    per=0
    rescs1="add"
    rescs2="mul"
    for j in range(2,20):
        for k in range(4):
            if k&1:
                cs1="add"
            else:
                cs1="mul"
            if k&2:
                cs2="add"
            else:
                cs2="mul"
            fit = ExponentialSmoothing(df2, seasonal_periods=j,trend=cs1, seasonal=cs2, damped=True).fit(use_boxcox=True)
            tmp=fit.forecast(110)
            res=calc(tmp,df1,110)
            if res<mn:
                mn=res
                per=j
                rescs1=cs1
                rescs2=cs2
    return per,rescs1,rescs2,mn

def showpic(df):
    for i in range(5):
        df1=df.loc[i][1:]
        plt.cla()
        plt.title(str(i)+":"+df.loc[i][0])
        plt.plot(df1)
        plt.savefig(str(i)+".png")

def showfit(i,a,b):
    plt.cla()
    plt.title(str(i)+":fit")
    plt.plot(b,color='red')
    plt.plot(a,color="green")
    plt.savefig(str(i)+"fit.png")

df=pd.read_csv("imp.csv")
out=open("res.txt","w")
showpic(df)
for i in range(1,2):
    df0=df.loc[i][1:440]
    df1=df.loc[i][440:]
    df2=np.array(df.loc[i][1:440])
    per,rescs1,rescs2,mn=mxpara(df1,df2)    
    fit=ExponentialSmoothing(df2, seasonal_periods=per,trend=rescs1, seasonal=rescs2, damped=True).fit(use_boxcox=True)
    print("%d %d %.10lf %.10lf %s %s\n"%(i,per,mn,calc(df0,fit.fittedvalues,439),rescs1,rescs2),file=out)
    showfit(i,df0,fit.fittedvalues)
    tmp=fit.forecast(110)    
    plt.cla()
    plt.title(str(i)+":forecast")
    plt.plot(tmp,color='red')
    plt.plot(df1,color="green")
    plt.savefig(str(i)+"forecast.png")
out.close()




