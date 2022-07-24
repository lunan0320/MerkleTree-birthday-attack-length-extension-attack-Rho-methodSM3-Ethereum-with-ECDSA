### Rho_attack_SM3

**原理**：
从一个初始值x，这里采用随机化初始值，不断计算它的SM3的哈希值，在前nbit中就可能形成环

代码实现参考Floyd的判环的过程，通过调节碰撞bit数量，得到不同要求下的攻击结果。

最朴素的方法就是不断计算哈希值，把计算好的哈希值保存下，对于每次新得到的SM3的哈希值去判断是否曾出现过，若出现过，则说明找到了环，也就找到了SM3的前n比特的一个碰撞。

**实现**

该方法类似于Floyd的判环的过程：

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

