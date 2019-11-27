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
vector<string> vec;
int cs[105];
int main(){
    freopen("data.csv","w",stdout);
    ifstream fin("train_1.csv");
    int cnt=0;
    while (getline(fin,line)){
        cnt++;
        if (cnt==1) continue;
        readcsv(cnt);
    }
    sort(a+1,a+1+cnt,cmp);
    rep(i,1,50){
        mp[a[i].id]=1;
    }
    ifstream fin2("train_1.csv");
    cnt=0;
    vec.clear();
    int c=0;
    
    cs[12]=
    cs[44]=
    cs[39]=
    cs[25]=
    cs[4]=
    cs[13]=
    cs[49]=
    cs[29]=
    cs[43]=
    cs[14]=1;
    while (getline(fin2,line)){
        cnt++;
        if (cnt==1) {
			cout<<line<<endl;
    		continue;
		}
		if (mp[cnt]) {
            if (cs[c]) cout<<line<<endl;
            c++;
        }
    }
    return 0;
}
