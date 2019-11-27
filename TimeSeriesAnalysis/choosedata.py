import pandas as pd
import matplotlib.pyplot as plt
def showpic(df):
    plt.rcParams['savefig.dpi'] = 300 #图片像素
    plt.rcParams['figure.dpi'] = 300 #分辨率
    for i in range(df.size):
        df1=df.loc[i][1:]
        plt.cla()
        plt.title(str(i)+":"+df.loc[i][0])
        plt.plot(df1)
        plt.savefig("data"+str(i)+".png")

df=pd.read_csv("data.csv")
showpic(df)
