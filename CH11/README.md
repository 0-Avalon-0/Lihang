# CH11 条件随机场

## 前言

本章目录结构如下:

1. 概率无向图模型
   1. 模型定义
   1. 概率无向图的**因子分解**
1. 条件随机场的定义与形式
   1. 条件随机场的定义
   1. 条件随机场的**参数化形式**
   1. 条件随机场的**简化形式**
   1. 条件随机场的**矩阵形式**
1. 条件随机场的概率计算问题
   1. 前向-后向算法
   1. 概率计算
   1. 期望值计算
1. 条件随机场的学习方法
   1. 改进的迭代尺度法
   1. 拟牛顿法
1. 条件随机场的预测算法

整个这一章的介绍思路, 和前一章有点像, 尤其是学习算法部分.

## 概念

### 符号表

节点$\nu\in V$表示一个随机变量$Y_{\nu}$

边$e\in E$表示随机变量之间的概率依赖关系

图$G(V,E)$表示联合概率分布$P(Y)$

$Y\in \mathcal Y$是**一组随机变量**$Y=(Y_{\nu})_{\nu \in V}$

### 概率图模型

注意整个书中第一节的内容， 还不是条件随机场， 都是马尔可夫随机场，告诉读者可以用图来表示联合分布，以及拿到图之后， 怎么转化成概率表达形式。

#### 概率无向图模型

概率无向图模型又称**马尔可夫随机场(MRF)**, 是一个可以由**满足以下三个性质的无向图**表示的**联合概率分布**.

- 成对马尔可夫性
  给定随机变量组$Y_O$的条件下随机变量$Y_u$和$Y_v$是条件独立的
  $P(Y_u,Y_v|Y_O)=P(Y_u|Y_O)P(Y_v|Y_O)$

- 局部马尔可夫性
  给定随机变量组$Y_W$的条件下随机变量$Y_v$与随机变量组$Y_O$是独立的
  $P(Y_v,Y_O|Y_W)=P(Y_v|Y_W)P(Y_O|Y_W)$

- 全局马尔可夫性
  给定随机变量组$Y_C$的条件下随机变量组$Y_A$和$Y_B$是条件独立的
  $P(Y_A,Y_B|Y_C)=P(Y_A|Y_C)P(Y_B|Y_C)$

#### MRF的因子分解

> 将概率无向图模型的联合概率分布表示为其**最大团**上的随机变量的函数的乘积形式的操作，称为概率无向图模型的因子分解(factorization)
> 概率无向图模型的最大特点就是**易于因子分解**.

#### 团与最大团

#### 有向图模型

插入一点有向图模型

### 条件随机场

条件随机场是给定随机变量$X$条件下, 随机变量$Y$的马尔可夫随机场.

线性链条件随机场也是**对数线性模型**(定义在时序数据上的).

条件随机场可以看做是最大熵马尔可夫模型在标注问题上的推广.

条件随机场是计算**联合概率分布**的有效模型.

>现实中，一般假设$X$和$Y$有相同的图结构。
>
>本书主要考虑无向图为
>$$
>G=(V={1,2,\dots,n},E={(i,i+1)}),i=1,2,\dots,n-1
>$$
>在此情况下，$X=(X_1,X_2,\dots,X_n), Y=(Y_1, Y_2,\dots,Y_n)$

线性链条件随机场定义

> 设$X=(X_1,X_2,\dots,X_n), Y=(Y_1, Y_2,\dots,Y_n)$均为线性链表示的随机变量序列， 若在给定随机变量序列$X$的条件下， 随机变量序列$Y$的条件概率分布$P(Y|X)$构成条件随机场， 即满足马尔可夫性
> $P(Y_i|X,Y_1,\dots,Y_{i-1},Y_{i+1},\dots,Y_n)=P(Y_i|X,Y_{i-1},Y{i+1}), i=1,2,\dots,n$
>
> 则称$P(Y|X)$为线性链条件随机场

#### 参数化形式

随机变量$X$取值为$x$的**条件**下，随机变量$Y$取值为$y$的条件概率具有如下形式：
$$
P(y|x)=\frac{1}{Z}\exp\left(\sum_{i,k}\lambda_kt_k(y_{i-1},y_i,x,i+\sum_{i,l}\mu_ls_l(y_i,x,i)\right)
$$
其中
$$
Z(x)=\sum_y\left(\sum_{i,k}\lambda_kt_k(y_{i-1},y_i,x,i)+\sum_{i,l}\mu_ls_l(y_i,x,i)\right)
$$
$k,l$对应特征函数的编号，注意这里用了$k,l$两个编号，$i$对应了输出序列的每个位置
$$
\begin{align}
t_1&=t_1(y_{i-1}=1,y_i=2,x,i),&i&=2,3,&\lambda_1&=1 \\
t_2&=t_2(y_{i-1}=1,y_i=1,x,i),&i&=2,&\lambda_2&=0.5\\
\color{red}t_3&=t_3(y_{i-1}=2,y_i=1,x,i),&i&=3,&\lambda_3&=1\\
\color{red}t_4&=t_4(y_{i-1}=2,y_i=1,x,i),&i&=2,&\lambda_4&=1\\
t_5&=t_5(y_{i-1}=2,y_i=2,x,i),&i&=3,&\lambda_5&=0.2\\
s_1&=s_1(y_i=1,x,i),&i&=1,&\mu_1&=1\\
s_2&=s_2(y_i=1,x,i),&i&=1,2,&\mu_2&=0.5\\
s_3&=s_3(y_i=1,x,i),&i&=2,3,&\mu_3&=0.8\\
s_4&=s_4(y_i=2,x,i),&i&=3&\mu_4&=0.5\\
\end{align}
$$
可以抽象成上面这种形式。



#### 简化形式

上面的结构，包含了两个部分，表达式不够简单，如何落地？

$K_1$个转移特征， $K_2$个状态特征

$$
f_k(y_{i-1},y_i,x,i)=
\begin{cases}
t_k(y_{i-1},y_i,x,i),&k=1,2,\dots,K_1\\
s_l(y_i,x,i),&k=K_1+l;l=1,2,\dots,K_2
\end{cases}
$$
然后，对转和状态特征在各个位置$i$求和，记作
$$
f_k(y,x)=\sum_{i=1}^nf_k(y_{i-1},y_i,x,i),k=1,2,\dots,K
$$
用$w_k$表示特征$f_k(y,x)$的权值
$$
w_k=
\begin{cases}
\lambda_k,&k=1,2,\dots,K_1\\
\mu_l,&k=K1+l;l=1,2,\dots,K_2
\end{cases}
$$
于是条件随机场可以表示为
$$
\begin{align}
P(y|x)&=\frac{1}{Z(x)}\exp\sum_{k=1}^Kw_kf_k(y,x)\\
Z(x)&=\sum_y\exp\sum_{k=1}^Kw_kf_k(y,x)
\end{align}
$$
若以$w$表示权值向量， 即
$$
w=(w_1,w_2,\dots,w_K)^T
$$
以$F$表示全局特征向量，即
$$
F(y,x)=(f_1(y,x),f_2(y,x),\dots,f_K(y,x))^T
$$
条件随机场可以表示成向量内积的形式
$$
\begin{align}
P_w(y|x)&=\frac{\exp(w\cdot F(y,x))}{Z_w(x)}\\
Z_w(x)&=\sum_y\exp\left(w\cdot F(y,x)\right)
\end{align}
$$
在参数化形式的展示中，书中的公式已经做了删减。
而实际上这里应该是展开的。
$$
\begin{align}
f_k&=t_1(y_{i-1}=1,y_i=2,x,i),&i&=2,&w_k&=1,&k=1 \\
f_k&=t_1(y_{i-1}=1,y_i=2,x,i),&i&=3,&w_k&=1,&k=1 \\
f_k&=t_2(y_{i-1}=1,y_i=1,x,i),&i&=2,&w_k&=0.5,&k=2\\
f_k&=t_2(y_{i-1}=1,y_i=1,x,i),&i&=3,&w_k&=0.5,&k=2\\
\color{red}f_k&=t_3(y_{i-1}=2,y_i=1,x,i),&i&=2,&w_k&=1,&k=3\\
\color{red}f_k&=t_3(y_{i-1}=2,y_i=1,x,i),&i&=3,&w_k&=1,&k=3\\
\color{red}f_k&=t_4(y_{i-1}=2,y_i=1,x,i),&i&=2,&w_k&=1,&k=4\\
\color{red}f_k&=t_4(y_{i-1}=2,y_i=1,x,i),&i&=3,&w_k&=1,&k=4\\
f_k&=t_5(y_{i-1}=2,y_i=2,x,i),&i&=2,&w_k&=0.2,&k=5\\
f_k&=t_5(y_{i-1}=2,y_i=2,x,i),&i&=3,&w_k&=0.2,&k=5\\
\\
f_k&=s_1(y_i=1,x,i),&i&=1,&w_k&=1,&k=6\\
f_k&=s_1(y_i=1,x,i),&i&=2,&w_k&=1,&k=6\\
f_k&=s_1(y_i=1,x,i),&i&=3,&w_k&=1,&k=6\\
f_k&=s_2(y_i=1,x,i),&i&=1,&w_k&=0.5,&k=7\\
f_k&=s_2(y_i=1,x,i),&i&=2,&w_k&=0.5,&k=7\\
f_k&=s_2(y_i=1,x,i),&i&=3,&w_k&=0.5,&k=7\\
f_k&=s_3(y_i=1,x,i),&i&=1,&w_k&=0.8,&k=8\\
f_k&=s_3(y_i=1,x,i),&i&=2,&w_k&=0.8,&k=8\\
f_k&=s_3(y_i=1,x,i),&i&=3,&w_k&=0.8,&k=8\\
f_k&=s_4(y_i=2,x,i),&i&=1,&w_k&=0.5,&k=9\\
f_k&=s_4(y_i=2,x,i),&i&=2,&w_k&=0.5,&k=9\\
f_k&=s_4(y_i=2,x,i),&i&=3,&w_k&=0.5,&k=9
\end{align}
$$

这里对于$w_k$的理解再体会下。



#### 矩阵形式

针对线性链条件随机场

引入起点和终点状态标记$y_0=start,y_{n+1}=end$， 这时$P_w(y|x)$可以矩阵形式表示。

对应观测序列的每个位置$i=1,2,\dots,n+1$，定义一个$m$阶矩阵（$m$是标记$y_i$取值的个数）
$$
\begin{align}
M_i(x)&=\left[M_i(y_{i-1},y_i|x)\right]\\
M_i(y_{i-1},y_i)&=\exp\left(W_i(y_{i-1},y_i|x)\right)\\
W_i(y_{i-1},y_i|x)&=\sum_{k=1}^Kw_kf_k(y_{i-1},y_i|x)
\end{align}
$$
把整个向量乘法按照**观测位置**拆成矩阵形式， 每个观测位置对应一个矩阵

这个过程和$CNN$中的卷积实际上有点像，这里面卷积模板有两种$k\times 1$和$k\times 2$， 以1和2进行滑窗。

## 例子

> 条件随机场完全由特征函数$t_k,s_l$和对应的权值$\lambda_k,\mu_l$确定
接下来的三个例子
- 例11.1

  已知上述四个参数的情况下，求概率
- 例11.2

  假设了$y_0=start=1, y_4=stop=1$

  矩阵形式的表示是为了后面的前向后向算法中递推的使用。 
- 例11.3
  decode问题实例
### 例11.1

特征函数部分的内容理解下.

这里整理下题目中的特征函数，这里和书上的格式稍有不同，希望用这样的描述能看到这些特征函数中抽象的地方。
$$
\begin{align}
t_1&=t_1(y_{i-1}=1,y_i=2,x,i),&i&=2,3,&\lambda_1&=1 \\
t_2&=t_2(y_{i-1}=1,y_i=1,x,i),&i&=2,&\lambda_2&=0.5\\
\color{red}t_3&=t_3(y_{i-1}=2,y_i=1,x,i),&i&=3,&\lambda_3&=1\\
\color{red}t_4&=t_4(y_{i-1}=2,y_i=1,x,i),&i&=2,&\lambda_4&=1\\
t_5&=t_5(y_{i-1}=2,y_i=2,x,i),&i&=3,&\lambda_5&=0.2\\
s_1&=s_1(y_i=1,x,i),&i&=1,&\mu_1&=1\\
s_2&=s_2(y_i=1,x,i),&i&=1,2,&\mu_2&=0.5\\
s_3&=s_3(y_i=1,x,i),&i&=2,3,&\mu_3&=0.8\\
s_4&=s_4(y_i=2,x,i),&i&=3&\mu_4&=0.5\\
\end{align}
$$
注意上面红色标记的$t_3,t_4$是可以合并的。

```python
# transition feature
# i-1, i
f_k[0] = np.sum([1 if tmp[0] == 1 and tmp[1] == 2 else 0 for tmp in list(zip(Y[:-1], Y[1:]))])
f_k[1] = np.sum([1 if tmp[0] == 1 and tmp[1] == 1 else 0 for tmp in list(zip(Y[:-1], Y[1:]))])
f_k[2] = np.sum([1 if tmp[0] == 2 and tmp[1] == 1 else 0 for tmp in list(zip(Y[:-1], Y[1:]))])
f_k[3] = np.sum([1 if tmp[0] == 2 and tmp[1] == 1 else 0 for tmp in list(zip(Y[:-1], Y[1:]))])
f_k[4] = np.sum([1 if tmp[0] == 2 and tmp[1] == 2 else 0 for tmp in list(zip(Y[:-1], Y[1:]))])
# state feature
# i
f_k[5] = np.sum([1 if tmp == 1 else 0 for tmp in [Y[0]]])
f_k[6] = np.sum([1 if tmp == 2 else 0 for tmp in Y[:2]])
f_k[7] = np.sum([1 if tmp == 1 else 0 for tmp in Y[1:]])
f_k[8] = np.sum([1 if tmp == 2 else 0 for tmp in [Y[2]]])

# 生成全局特征向量
proba = np.sum(w_k*f_k)
# w的维度和f_k的维度匹配，一一对应
```



引用一下书中的解，注意看

>$$
>P(y|ｘ)\varpropto \exp \left[\sum_{k=1}^5\lambda_k\color{red}\sum_{i=2}^3\color{black}t_k(y_{i-1}, y_i, x, i)+\sum_{k=1}^4\mu_k\color{red}\sum_{i=1}^3\color{black}s_k(y_i,x,i)\right]
>$$
>

注意，按照这里红色部分的表达$\sum\limits_{i=2}^3 \sum\limits_{i=1}^3$，实际上特征函数会遍历每一个可能的点和边。书中有这样一句**取值为０的条件省略**, 这个仔细体会下

### 例11.2

这里使用SymPy推导一下这个例子
```python
from sympy import *
a01,a02, b11, b12, b21, b22, c11, c12, c21, c22  = symbols("a01, a02, \
                                                            b11, b12,b21, b22, \
                                                            c11, c12, c21, c22")
M1 = Matrix([[a01, a02],
             [0,   0]])
M2 = Matrix([[b11, b12],
             [b21, b22]])

M3 = Matrix([[c11, c12],
             [c21, c22]])

M4 = Matrix([[1, 0],
             [1, 0]])
Z = expand(M1*M2*M3*M4)
P = str(expand(M1*M2*M3*M4)[0]).replace(" ","").split("+")
# 体会各个路径之间关系
for i in range(2):
   for j in range(2):
       for k in range(2):
           logger.info(str(M1[0, i] * M2[i, j] * M3[j, k]))
print(Z)
print(P)
```
本章代码有设计这个例子的测试案例, 可以参考.
这里有个点要注意下, 书中强调了$Z$的**第一行和第一列**
$$
Z(x)=\alpha_n^T(x)\cdot \mathrm{1}=\mathrm{1}^T\cdot \beta_1(x)
$$
### 例11.3

## CRF与LR比较

都是对数线性模型



## 应用

词性标注

## 参考

