#include<bits/stdc++.h>
#define rep(i,l,r) for (int i=l;i<=r;i++)
using namespace std;
const int maxn=1005000;
char s[maxn];
string line,tmp;
struct node{
    int sum,id;
}a[maxn];
int jud(){
    int res=0;
    int len=tmp.length();
    for (int i=0;i<len;i++) {
        if (!isdigit(tmp[i])) return -1;
        res=res*10+tmp[i]-'0';
    }
    return res;
}
void readcsv(int cnt){
    a[cnt].id=cnt;
    int len=line.length();
    for (int i=0,j;i<len;i=j+1){
        tmp="";
        j=i;
        while (line[j]!=',') tmp+=line[j],j++;
        int x=jud();
        if (x>=0) a[cnt].sum+=x; 
    }
//    printf("sum %d\n",a[cnt].sum);
}
bool cmp(node a,node b){
    return a.sum>b.sum;
}
map<int,int> mp;
int main(){
    freopen("big30.csv","w",stdout);
    ifstream fin("train_1.csv");
    int cnt=0;
    while (getline(fin,line)){
        cnt++;
        if (cnt==1) continue;
        readcsv(cnt);
    }
    sort(a+1,a+1+cnt,cmp);
    rep(i,1,30){
        mp[a[i].id]=1;
//        printf("%d\n",a[i].id);
        //for (auto x:a[i].vec) printf("%d ",x);
//        puts("");
    }
    ifstream fin2("train_1.csv");
    cnt=0;
    while (getline(fin2,line)){
        cnt++;
        if (cnt==1||mp[cnt]) cout<<line<<endl;
    }
    return 0;
}