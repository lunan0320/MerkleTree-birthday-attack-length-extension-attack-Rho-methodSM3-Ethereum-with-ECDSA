# ✅ Rho_attack_SM3

### 1.代码说明

#### **原理**：

从一个初始值x，这里采用随机化初始值，不断计算它的SM3的哈希值，在前nbit中就可能形成环

代码实现参考Floyd的判环的过程，通过调节碰撞bit数量，得到不同要求下的攻击结果。

最朴素的方法就是不断计算哈希值，把计算好的哈希值保存下，对于每次新得到的SM3的哈希值去判断是否曾出现过，若出现过，则说明找到了环，也就找到了SM3的前n比特的一个碰撞。

#### **实现**

该方法类似于**Floyd的判环**的过程：

```python
def Rho_attack(n):
    h1=random.randint(0,pow(2,64))
    h2=[]
    for i in range(0,pow(2,32)):
        h2.append(sm3(h1)[:int(n/4)])
        h1=2*h1+1
        if(sm3(h1)[:int(n/4)] in h2):
            print("环路点的哈希值:",sm3(h1))
            print("Succeed")
            return
    print("Failed")
```

![](https://github.com/lunan0320/Crypto_projects/blob/main/4.Rho_method_of_reduced_SM3/Rho.png)

### 2.运行方式

python文件，直接在命令行中输入:

`python3 Rho_attack_SM3.py`

### 3.实现效果

### 1) 8bit

![](https://github.com/lunan0320/Crypto_projects/blob/main/4.Rho_method_of_reduced_SM3/8bit.png)

#### 2) 16bit

![](https://github.com/lunan0320/Crypto_projects/blob/main/4.Rho_method_of_reduced_SM3/16bit.png)

#### 3) 24bit

![](https://github.com/lunan0320/Crypto_projects/blob/main/4.Rho_method_of_reduced_SM3/24bit.png)

