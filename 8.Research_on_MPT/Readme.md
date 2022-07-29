# ✅ Merkle Patricia Tree

### Merkle tree

在Bitcoin网络中，merkle树被用来归纳一个区块中的所有交易，同时生成整个交易集合的数字指纹。此外，由于merkle树的存在，使得在Bitcoin这种公链的场景下，扩展一种“轻节点”实现简单支付验证变成可能。

**特点**：

- Merkle tree是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，它都具有树结构的所有特点；
- Merkle tree叶子节点的value是数据项的内容，或者是数据项的哈希值；
- 非叶子节点的value根据其孩子节点的信息，然后按照Hash算法计算而得出的；

![](https://github.com/lunan0320/Crypto_projects/blob/main/8.Research_on_MPT/img/1.png)

**优势**：

- 快速重哈希
- 轻节点扩展

**劣势:**

- 存储空间开销大

### 概述

​	Merkle Patricia Tree（又称为Merkle Patricia Trie）是一种经过改良的、融合了Merkle tree和前缀树两种树结构优点的数据结构，是以太坊中用来组织管理账户数据、生成交易集合哈希的重要数据结构。

MPT树有以下几个**作用**：

- 存储任意长度的key-value键值对数据，符合以太坊的state模型；
- 提供了一种快速计算所维护数据集哈希标识的机制；
- 提供了快速状态回滚的机制；
- 提供了一种称为默克尔证明的证明方法，进行轻节点的扩展，实现简单支付验证；

### MPT结构

MPT树的特点如下:

- 叶子节点和分支节点可以保存value, 扩展节点保存key；
- 没有公共的key就成为2个叶子节点；key1=[1,2,3] key2=[2,2,3]
- 有公共的key需要提取为一个扩展节点；key1=[1,2,3] key2=[1,3,3] => ex-node=[1],下一级分支node的key
- 如果公共的key也是一个完整的key，数据保存到下一级的分支节点中；key1=[1,2] key2=[1,2,3] =>ex-node=[1,2],下一级分支node的key; 下一级分支=[3],上一级key对应的value

![](https://github.com/lunan0320/Crypto_projects/blob/main/8.Research_on_MPT/img/2.png)

### 特点

1）它能 **在一次插入、更新、删除操作后快速计算到树根** ，而不需要重新计算整个树的Hash。

2）树的 **深度是有限制** 的，即使考虑攻击者会故意地制造一些交易，使得这颗树尽可能地深。不然，攻击者可以通过操纵树的深度，执行拒绝服务攻击（DOS attack），使得更新变得极其缓慢。

### 原理

**值通过键来存储**

**键被编码到搜索树必须要经过的路径中**

每个节点有 **16个孩子** ，因此路径由16进制的编码决定：例如，键‘dog’的16进制编码是6 4 6 15 6 7，所以从root开始到第六个分支，然后到第四个，再到第六个，再到第十五个，这样依次进行到达树的叶子。

当树稀少时需要一些额外的优化

![](https://github.com/lunan0320/Crypto_projects/blob/main/8.Research_on_MPT/img/3.png)

### 参考文档

[以太坊中的Merkle Patricia Tree(1):基本概念](https://www.jianshu.com/p/d3eba79cc475)

[以太坊 Merkle Patricia Tree 全解析](https://zhuanlan.zhihu.com/p/46702178)