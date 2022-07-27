# ✅ Birthday_attack_SM3

### 1、代码说明

​	此处通过生日攻击的方法，实现了SM3算法的前8、16位的碰撞。

​	*更高bit的攻击需要更多的时间*

​	对于任意给定的msg： M，可以计算出H = SM3(M)，并不是传统的计算两个随机串的哈希值来穷举碰撞。

### 2、运行方式

python文件，直接在命令行中输入:

`python3 birthday_attack_sm3_8bit.py`

`python3 birthday_attack_sm3_16bit.py`

### 3、实现效果

#### 1）8bit

![8bit](https://github.com/lunan0320/Crypto_projects/blob/main/2.Birthday_Attack_SM3/8bit.png)

#### 2）16bit

![16bit](https://github.com/lunan0320/Crypto_projects/blob/main/2.Birthday_Attack_SM3/16bit.png)

### 