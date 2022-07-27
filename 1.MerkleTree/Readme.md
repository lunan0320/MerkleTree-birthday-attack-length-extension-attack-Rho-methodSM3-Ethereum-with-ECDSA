# ✅ MerkleTree

### 1.代码说明

#### **ImplRFC6962.py**

Impl Merkle Tree following RFC6962

#### **Construct10w.py**

Construct a Merkle tree with 10w leaf nodes

#### **proof_verify.py**

Build inclusion proof for specified element

Build exclusion proof for specified element

### MerkleTree

**哈希函数**：Sha-256

二叉树结构

**结构**：每一个中间节点都是两个叶子结点的哈希，叶子本身可以是数据，也可以是数据的哈希或者签名

![](https://github.com/lunan0320/Crypto_projects/blob/main/1.MerkleTree/MerkleTree.png)

**用途**：证明存储在块中的交易数据的完整性

**proof**: 用Merkle Tree存储区块数据，因为这样的验证非常有效，称为Merkle Proof

> 按照RFC 6962的标准要求，叶节点和其余节点的进行哈希的前缀不同（叶节点前缀为0x00， 其余节点前缀为0x01)

**几类情况**：

```python
 #空的hash tree
   MTH({}) = SHA-256().
```

```python
 # 只有一个条目
MTH({d(0)}) = SHA-256(0x00 || d(0))
```

```python
 #条目>1
 MTH(D[n]) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n]))
```

### 2.运行方式

python文件，直接在命令行中输入:

`python3 Construct10w.py`

`python3 ImplRFC6962.py`

`python3 proof_verify.py`

### 3.实现效果

**1）Implement Merkle Tree as of RFC 6962**

*此处展示初始化7个节点，实现3层MerkleTree的效果图*

![](https://github.com/lunan0320/Crypto_projects/blob/main/1.MerkleTree/ImplRFC6962.png)

**2) Construct a merkle tree with 100k leaf nodes**

*此处展示在构造完成后，打印出的根节点的hash值*

![](https://github.com/lunan0320/Crypto_projects/blob/main/1.MerkleTree/Construct10w.png)

*核心代码递归求解*

```python
#对子问题递归处理             
partition=2**(len(bin(length-1))-3)     #分界点
left=merkle(leaves[0:partition])         #左子问题
right=merkle(leaves[partition:length])   #右子问题
tree=hash_function(chr(int('0x01',16))+left+right)
```

**3）proof for specified element & verify**

此处指定要查找的节点和节点序号，判断该节点是否在MerkleTree中

为了测试方便，实现了两种机制：**简单模式**和**随机模式**

区别只是初始的叶子节点不同。简单模式有固定的叶子节点，随机模式则每次随机生成。



简单模式

参考：[RFC6962](https://www.rfc-editor.org/rfc/rfc6962.html)

