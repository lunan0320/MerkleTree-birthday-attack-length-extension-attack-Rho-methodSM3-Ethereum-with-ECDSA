### 文件结构

**ImplRFC6962.py**

Impl Merkle Tree following RFC6962

**Construct10w.py**

Construct a Merkle tree with 10w leaf nodes

**proof_verify.py**

Build inclusion proof for specified element

Build exclusion proof for specified element

### MerkleTree

**哈希函数**：Sha-256

二叉树结构

**结构**：每一个中间节点都是两个叶子结点的哈希，叶子本身可以是数据，也可以是数据的哈希或者签名

**用途**：证明存储在块中的交易数据的完整性

**proof**: 用Merkle Tree存储区块数据，因为这样的验证非常有效，称为Merkle Proof

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

参考：[RFC6962](https://www.rfc-editor.org/rfc/rfc6962.html)

