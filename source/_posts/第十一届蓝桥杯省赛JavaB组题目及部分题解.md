title: 第十一届蓝桥杯省赛JavaB组题目及部分题解
date: 2022-01-22 17:58:08
tags: 第十一届蓝桥杯省赛JavaB组题目及部分题解

# 真题链接：[点这里](https://www.lanqiao.cn/courses/2786/learning/?id=88906)

# 填空题

## 试题A：门牌制作（5分）

### 问题描述：



### 思路简述：

#### 解法一：

> while循环分解每一位上的数字

##### 代码：

```java
public static void main(String[] args) {
	int ans=0;
	for(int i=1;i<=2020;++i){
		int a=i;
		while(a!=0){
			if(a%10==2)ans++;
			a/=10;
		}
	}
	System.out.println(ans);
}
```

***

#### 解法二：

> 字符串遍历

##### 代码：

```java
public static void main(String[] args) {
	int ans=0;
	for(int i=1;i<=2020;++i){
		String s=String.valueOf(i);
		if(s.contains("2")){
			for(char c:s.toCharArray()){
				if(c=='2')ans++;
			}
		}
	}
	System.out.println(ans);
}
```


### 参考结果：

> 624

***

## 试题B：寻找2020（5分）

### 问题描述：



**2020.txt文件 [点这里](https://blog.csdn.net/Wsy221535/article/details/122642305) **

### 思路简述：

> 文件2020.txt有`300`行`300`列
>
> 遍历每个点找  当前点与右`3`，下`3`，斜下`3`  组合为`2020` 的个数 

### 代码：

```java
public static void main(String[] args) throws IOException {
    BufferedReader in=new BufferedReader(new FileReader("2020.txt"));
    String s;
    int n=300,k=0;
    int [][]a=new int[n][n];
    while((s=in.readLine())!=null){
        for(int i=0;i<n;++i)
            a[k][i]=s.charAt(i)-'0';
        ++k;
    }
//    for(int i=0;i<n;++i){ // 直接在控制台输入2020.txt文件内容
//        String s=scanner.next();
//        for(int j=0;j<n;++j){
//            a[i][j]=s.charAt(j)-'0';
//        }
//    }
    int ans=0;
    for(int i=0;i<n;++i){
        for(int j=0;j<n;++j){
            if(j<n-3){
                if(a[i][j]==2&&a[i][j+1]==0&&a[i][j+2]==2&&a[i][j+3]==0)ans++;
            }
            if(i<n-3){
                if(a[i][j]==2&&a[i+1][j]==0&&a[i+2][j]==2&&a[i+3][j]==0)ans++;
            }
            if(i<n-3&&j<n-3){
                if(a[i][j]==2&&a[i+1][j+1]==0&&a[i+2][j+2]==2&&a[i+3][j+3]==0)ans++;
            }
        }
    }
    System.out.println(ans);		
}
```

### 参考结果：

> 16520

***

## 试题C：蛇形填数（10分）

### 问题描述：



### 思路简述：

#### 解法一：

> 第20行第20列位于斜着数第 `20*2-1=39`行，找到39行的首和尾两个数，进行计算`742+(780-742)/2=761`。

##### 代码：

```java
public static void main(String[] args) {
    int n=39,a=0,sum=0;
    for(int i=1;i<=n;++i){
        a++;sum+=a;
        System.out.println(sum);
    }
    System.out.println("\n"+((sum-a+1)+a/2));
}
```

***

#### 解法二：

> 简单模拟。用二维数组`a`来存储这斜着数39行内容。

##### 代码：

```java
public static void main(String[] args) {
    int n=20*2-1;
    int [][]a=new int[n][n];
    int i=0,j=0,cnt=1;
    for(int k=0;k<n;++k){
        if(k%2==0){
            while(j<k){
                a[i][j]=cnt++;++j;--i;
            }
            if(j==k){
                a[i][j]=cnt++;++j;
            }
        }
        else{
            while(i<k){
                a[i][j]=cnt++;++i;--j;
            }
            if(i==k){
                a[i][j]=cnt++;++i;
            }
        }
    }
    for(int k=0;k<n;++k){
        for(int l=0;l<n-k;++l){
            System.out.print(a[k][l]+" ");
        }
        System.out.println();
    }
    System.out.println("\n"+a[19][19]);
}
```

### 参考结果：

> 761

***

## 试题D：七段码（10分）

### 问题描述：



### 思路简述：

#### 解法一：

> 枚举 2^n^种情况。
>
> * 只有一管灯亮符合条件
> * 若`x`灯亮，并且与`x`连接的其他管不亮，不符合条件
> * 最后扣除4管灯亮，2管灯连在一块的不符合条件的情况（abde,facd,bcef）

##### 代码：

```java
public static void main(String[] args) {
    int ans=0; 
    for(int a=0;a<2;++a){
        for(int b=0;b<2;++b){
            for(int c=0;c<2;++c){
                for(int d=0;d<2;++d){
                    for(int e=0;e<2;++e){
                        for(int f=0;f<2;++f){
                            for(int g=0;g<2;++g){
                                int sum=a+b+c+d+e+f+g;
                                if(sum==0)continue;
                                else if(sum==1){
                                    ans++;
                                }
                                else{
                                    int flag=0;
                                    if(a==1&&b==0&&f==0)flag=1;
                                    if(b==1&&a==0&&g==0&&c==0)flag=1;
                                    if(c==1&&b==0&&g==0&&d==0)flag=1;
                                    if(d==1&&c==0&&e==0)flag=1;
                                    if(e==1&&d==0&&f==0&&g==0)flag=1;
                                    if(f==1&&a==0&&e==0&&g==0)flag=1;
                                    if(g==1&&f==0&&e==0&&b==0&&c==0)flag=1;
                                    if(flag==0)ans++;								
                                }
                            }
                        }
                    }
                }
            }
        } 
    }
    System.out.println(ans-3); //减去abde,facd,bcef这三种情况 
}
```

***

#### 解法二：

> dfs + 并查集

##### 代码：

```java
private static int n=7;
private static int ans=0;
private static int[][]mp=new int[n][n];
private static int[]v=new int [n];
private static int[]f=new int [n];
private static void un(int a,int b) {
    mp[a][b]=1;mp[b][a]=1;
}
private static int find(int a) {
    if(a!=f[a])f[a]=find(f[a]); 
    return f[a];
}
private static void dfs(int c) {
    if(c==7){
        for(int i=0;i<n;++i)f[i]=i; // 初始化 
        for(int i=0;i<n;++i){ // 遍历所有可能亮灯的数码管 
            for(int j=i+1;j<n;++j){
                if(mp[i][j]==1&&v[i]==1&&v[j]==1){ 
                    // i,j右边且i,j两管都亮 
                    int a=find(i),b=find(j);
                    if(a!=b)f[b]=a;	// 合并两集合 
                }
            }
        }		
        int cnt=0;
        for(int i=0;i<n;++i)
            if(v[i]==1&&f[i]==i)cnt++;
        if(cnt==1)ans++; // 所有亮灯都属于同一个集合 
        return;
    }
    v[c]=1; // 亮灯 
    dfs(c+1);
    v[c]=0; // 灭灯 
    dfs(c+1);
}
public static void main(String[] args) {
    // 0~6 --> a~g
    // 连接能通的边
    un(0,1);un(0,5);
    un(1,2);un(1,6);
    un(2,6);un(2,3);
    un(3,4);
    un(4,5);un(4,6);
    un(5,6);
    dfs(0);
    System.out.println(ans);
}
```

#### 图解：



**转载自[点这里]**([https://blog.csdn.net/m0_46272108/article/details/109157960?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_default&utm_relevant_index=2](https://blog.csdn.net/m0_46272108/article/details/109157960?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1.pc_relevant_default&utm_relevant_index=2))

### 参考结果：

> 80

***

## 试题E：排序（15分）

### 问题描述：



### 思路简述：

> 14 `nmlkjihgfedcba` 91
> 15 `onmlkjihgfedcba` 105
> 答案应该为长度15的字符串
> 将`onmlkjihgfedcba`第6个字符移至第一位
> 得`jonmlkihgfedcba`，并进行验证

### 代码：

```java
public static void main(String[] args) {
	String s="";
	for(int i=0;i<20;++i){ // 先打表看看
		s=(char)(i+'a')+s;
		int cnt=count(s);
		System.out.println((i+1)+" "+s+" "+cnt);
	}
	s="jonmlkihgfedcba";
	int cnt=count(s); // 验证
	System.out.println(s+" "+cnt);
}
private static int count(String s) {
	char []c=s.toCharArray();
	int n=c.length,cnt=0;
	for(int i=0;i<n-1;++i){ // 冒泡排序
		for(int j=0;j<n-i-1;++j){
			if(c[j]>c[j+1]){
				char t=c[j];
				c[j]=c[j+1];
				c[j+1]=t;
				cnt++;
			}
		}
	}
	return cnt;
}
```

### 参考结果：

> jonmlkihgfedcba

***

***

# 程序题

## 试题F：成绩分析（15分）

### 答题链接：[点这里](http://lx.lanqiao.cn/problem.page?gpid=T2853)

### 问题描述：



* 样例输入

  ```java
  7
  80
  92
  56
  74
  88
  99
  10
  ```

* 样例输出

  ```java
  99
  10
  71.29
  ```

### 思路简述：

>简单模拟

### 代码：

```java
public static void main(String[] args) {
	Scanner scanner=new Scanner(System.in);
	int n=scanner.nextInt();
	double sum=0;
	int ma=0,mi=100;
	for(int i=0;i<n;++i){
		int a=scanner.nextInt();
		ma=Math.max(ma, a);
		mi=Math.min(mi, a);
		sum+=a;
	}
	System.out.println(ma);
	System.out.println(mi);
	System.out.printf("%.2f\n", sum/n);
}#include<iostream> 
using namespace std;
int main(){
	int n,score,pass=0,excellent=0;cin>>n;
	for(int i=0;i<n;++i){
		cin>>score;
		if(score>=60)pass++;
		if(score>=85)excellent++;
	}
	cout<<(int)(pass*100.0/n+0.5)<<"%"<<endl;
	cout<<(int)(excellent*100.0/n+0.5)<<"%"<<endl;
	return 0;
} 
```

## 试题G：单词分析（20分）

### 答题链接：[点这里](http://lx.lanqiao.cn/problem.page?gpid=T801)

### 问题描述：



* 样例输入1

  ```java
  lanqiao
  ```

* 样例输出1

  ```java
  a
  2
  ```
  
  * 样例输入2

  ```java
  longlonglongistoolong
  ```

* 样例输出2

  ```java
  o
  6
  ```

### 思路简述：

> 哈希表存字符

### 代码：

```java
public static void main(String[] args) {
	Scanner scanner=new Scanner(System.in);
	String s=scanner.next();
	HashMap<Character, Integer>mp=new HashMap<>();
	for(char c:s.toCharArray()){
		mp.put(c, mp.getOrDefault(c, 0)+1);
	}
	char a = 0;int cnt=0;
	for(char c='a';c<='z';c++){
		if(cnt<mp.getOrDefault(c, 0)){
			cnt=mp.get(c);a=c;
		}
	}
	System.out.println(a);
	System.out.println(cnt);
}
```

***

## 试题H：数字三角形（20分）

### 答题链接：[点这里](http://lx.lanqiao.cn/problem.page?gpid=T794)

### 问题描述：



* 样例输入

  ```java
  5
  7
  3 8
  8 1 0 
  2 7 4 4
  4 5 2 6 5
  ```

* 样例输出

  ```java
  27
  ```

### 思路简述：

>从上往下走，走到当前点的最大值和`=` `max`(左上点的值和，右上点的值和)`+`当前点的值
>
>向左下走的次数与向右下走的次数相差不能超过 1 表示
>
>* 奇数行只能走到最后一行的中间那个数
>* 偶数行只能走到最后一行的中间两个数

### 代码：

```java
public static void main(String[] args) {
	Scanner scanner=new Scanner(System.in);
	int n=scanner.nextInt();
	int [][]a=new int[n][n];
	int [][]sum=new int[n][n];
	for(int i=0;i<n;++i){
		for(int j=0;j<=i;++j){
			a[i][j]=scanner.nextInt();
			if(i==0)sum[i][j]=a[i][j];
			if(j<i)sum[i][j]=Math.max(sum[i-1][j]+a[i][j], sum[i][j]);
			if(j>0)sum[i][j]=Math.max(sum[i-1][j-1]+a[i][j], sum[i][j]);
		}
	}	
	int ans=sum[n-1][n/2];
	if(n%2==0){
		ans=Math.max(sum[n-1][n/2-1],ans);
	}
	System.out.println(ans);
}
```

***

## 试题I：子串分值和（25分）

### 答题链接：[点这里](http://lx.lanqiao.cn/problem.page?gpid=T793)

### 问题描述：



![image-20220118224708880](C:\Users\33199\AppData\Roaming\Typora\typora-user-images\image-20220118224708880.png)

* 样例输入

  ```cpp
  ababc
  ```

* 样例输出

  ```cpp
  28
  ```

* 样例说明

  ```cpp
  子串 f值
  a     1
  ab    2
  aba   2
  abab  2
  ababc 3
   b    1
   ba   2
   bab  2
   babc 3
    a   1
    ab  2
    abc 3
     b  1
     bc 2
      c 1
  ```

### 思路简述：

>用数组`a`来存储26个字母最后一次出现的位置
>
>假设每个区间都是第一个出现的字母有贡献值，则贡献值为与左边相同字母的距离`*`右边字母个数
>
>==注意开long==

### 代码：

```java
public static void main(String[] args) {
    Scanner scanner=new Scanner(System.in);
    int a[]=new int[26];
    Arrays.fill(a, -1);
    String s=scanner.next();
    int n=s.length();
    long ans=0;
    for(int i=0;i<n;++i){
        int b=s.charAt(i)-'a';
        ans+=(long)(n-i)*(i-a[b]);
        a[b]=i;
    }
    System.out.println(ans);
}
```

***

## 试题J：装饰珠（25分）

### 答题链接：[点这里](https://www.lanqiao.cn/problems/507/learning/)

###  问题描述：



* 样例输入

  ```java
  1 1
  2 1 2
  1 1
  2 2 2
  1 1
  1 3
  3
  1 5 1 2 3 5 8
  2 4 2 4 8 15
  3 2 5 10
  ```

* 样例输出

  ```java
  20
  ```

### 思路简述：

> 不会哦

***

==欢迎各位大佬在评论区发表见解哦==

***
