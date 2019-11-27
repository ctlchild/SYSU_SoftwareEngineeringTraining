import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import SimpleExpSmoothing,ExponentialSmoothing,ARIMA
from pmdarima.arima import auto_arima

def calcMSE(a,b,n):
    veca=np.array(a)
    vecb=np.array(b)
    sum=0.0
    sz=n
    for i in range(n):
        sum+=((veca[i]-vecb[i])/vecb[i])**2
    return sum/sz

def show(i,a,b,st,method):
    plt.cla()
    plt.title(method+str(i)+st)
    plt.plot(b,color='red',label="origin")
    plt.plot(a,color="green",label=method)
    plt.savefig(method+str(i)+st+".png")

    
def holtwinter():
    out=open("holtwinter_res.txt","w")
    for i in range(df.shape[0]):
        df1=df.loc[i][441:]
        df2=np.array(df.loc[i][1:441])
        mn=1e9
        per=0
        rescs1="add"
        rescs2="mul"
        ## choose parameter
        for jj in range(1,3):
            j=jj*7
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
                res=calcMSE(tmp,df1,110)
#                tmp=fit.fittedvalues
#                res=calcMSE(tmp,df2,440)
                if res<mn:
                    mn=res
                    per=j
                    rescs1=cs1
                    rescs2=cs2
        if (per>1): 
            fit=ExponentialSmoothing(df2, seasonal_periods=per,trend=rescs1, seasonal=rescs2, damped=True).fit(use_boxcox=True)
            mse1=calcMSE(df2,fit.fittedvalues,440)
            print(i)
            print("%d %d %.10lf %.10lf %s %s\n"%(i,per,mse1,calcMSE(df1,fit.forecast(110),110),rescs1,rescs2),file=out)
            show(i,df2,fit.fittedvalues,"fit","holtwinter")
            show(i,df1,fit.forecast(110),"forecast","holtwinter")
        else:
            print("%d can not fit\n"%(i),file=out)
    
    out.close()

def holtwinter_se():
     out=open("holtwinter_se_res.txt","w")
     for i in range(df.shape[0]):
         df1=df.loc[i][441:]
         df2=np.array(df.loc[i][1:441])
         mn=1e9
         per=0
         rescs1="add"
         rescs2="mul"
         ## choose parameter
         for jj in range(1,3):
             j=jj*7
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
                 res=calcMSE(tmp,df1,110)
                 if res<mn:
                     mn=res
                     per=j
                     rescs1=cs1
                     rescs2=cs2
         if (per>1):
             res=np.zeros(0,dtype=float)
             now=441
             fit=ExponentialSmoothing(df2, seasonal_periods=per,trend=rescs1, seasonal=rescs2, damped=True).fit(use_boxcox=True)
             show(i,df2,fit.fittedvalues,"fit","holtwinter_se")
             origin=df2
             while (1):
                 if (now>=551):
                     break
                 fit=ExponentialSmoothing(origin, seasonal_periods=per,trend=rescs1, seasonal=rescs2, damped=True).fit(use_boxcox=True)
                 tmp=fit.forecast(per)
                 
                 #nan处理
                 if (np.isnan(tmp).sum()==per):
                     tmp=res[res.size-per:res.size]
                 else:
                     tmp[np.isnan(tmp)] = np.mean(tmp[~np.isnan(tmp)])
                 
                 res=np.append(res,tmp)
                 origin=np.append(origin,np.array(df.loc[i][now:min(551,now+per)]))
                 now+=per
             print(i)
             mse1=calcMSE(df2,fit.fittedvalues,440)
             show(i,df1,res,"forecast","holtwinter_se")
             print("%d %d %.10lf %.10lf %s %s\n"%(i,per,mse1,calcMSE(df1,res,110),rescs1,rescs2),file=out)
         else:
             print("%d can not fit\n"%(i),file=out)
         
    
     out.close()

def arima_calc(df,noworder):
    model=ARIMA(df,order=noworder)
    fit=model.fit(disp=0)
    return calcMSE(df,fit.fittedvalues,440)

def arima_iterate(df,p_values,d_values,q_values):
    mn=1e9
    bestorder=(-1,-1,-1)
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order=(p,d,q)
                now=arima_calc(df,order)
                print(p,d,q,now)
                if (now<mn):
                    mn=now
                    bestorder=order
    return bestorder,mn
                    
def arima():
     out=open("arima_res.txt","w")
     p_values=[14,14]
     d_values=range(0,1)
     q_values=range(0,1)
     warnings.filterwarnings("ignore") 
     for i in range(df.shape[0]):
         df1=df.loc[i][441:]
         df2=np.array(df.loc[i][1:441])
         
         bestorder,mse=arima_iterate(df2,p_values,d_values,q_values)
         
         model=ARIMA(df2,order=bestorder)
         fit=model.fit(disp=0)
         show(i,fit.fittedvalues,df2,"fit","ARIMA")
         mse1=calcMSE(df2,fit.fittedvalues,440)
         print(bestorder)
         mse=0
         now=441
         origin=df2
         res=np.zeros(0,dtype=float)
         per=bestorder[0]
         while (1):
             if (now>=551):
                 break
             model=ARIMA(origin,order=bestorder)
             
             fit=model.fit(disp=0)
             
             tmp=fit.forecast(per)[0]
             #nan处理
             if (np.isnan(tmp).sum()==per):
                 tmp=res[res.size-per:res.size]
             else:
                 tmp[np.isnan(tmp)] = np.mean(tmp[~np.isnan(tmp)])
                 
             res=np.append(res,tmp)
             origin=np.append(origin,np.array(df.loc[i][now:min(551,now+per)]))
             now+=per
         mse=calcMSE(df1,res,110)
         show(i,df1,res,"forecast","ARIMA")
         print("%d %d %d %d %.10lf %.10lf\n"%(i,bestorder[0],bestorder[1],bestorder[2],mse1,mse),file=out)
         print(i)
                         
     out.close()


df=pd.read_csv("data.csv")

holtwinter()
holtwinter_se()
arima()





