## ✅Length_extension_attack_SM3

### 1.代码说明

#### Attack:

**padding:** SM3的消息长度是64字节或者它的倍数，如果消息的长度不足则需要padding。在padding时，首先填充一个1，随后填充0，直到消息长度为56(或者再加整数倍的64)字节，最后8字节用来填充消息的长度。

**SM3**:在SM3函数计算时，首先对消息进行分组，每组64字节，每一次加密一组，并更新8个初始向量(初始值已经确定)，下一次用新向量去加密下一组，以此类推。

**length_extension:**  得到第一次加密后的向量值时，再人为构造一组消息用于下一次加密，就可以在不知道M1的情况下得到合法的hash值，这是因为8个向量中的值便能表示第一轮的加密结果。

#### Steps：

1、随机生成M1，此处是初始化指定即可。通过SM3算法，计算哈希值SM3(M1)。

2、附加消息M2，此处也是初始化值定即可。

3、计算SM3(M1||padding||M2)的值。

4、执行长度扩展攻击，通过SM3(M1)生成8个向量的值，作为初始向量，加密M2，得到SM3(M2)。

5、若SM3(M1||padding||M2) == SM3(M2)，则攻击成功。

### 2.运行方式

python文件，直接在命令行中输入:

`python3 length_attack_SM3.py`

### 3.实现效果

![](https://github.com/lunan0320/Crypto_projects/blob/main/3.Length_extension_attack_SM3/length_attack_sm3.png)
