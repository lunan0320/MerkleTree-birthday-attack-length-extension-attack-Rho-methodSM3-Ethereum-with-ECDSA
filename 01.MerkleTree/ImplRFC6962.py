import copy
import hashlib

#叶子结点的hash
def hash_leaf(data,hash_function = 'sha256'):
    hash_function = getattr(hashlib, hash_function)
    data = b'\x00'+data.encode('utf-8')
    return hash_function(data).hexdigest()

#内部结点的hash
def hash_func(data,hash_function = 'sha256'):
    hash_function = getattr(hashlib, hash_function)
    data = b'\x01'+data.encode('utf-8')
    return hash_function(data).hexdigest()

#构造树结构
def MerkleTree(lst,hash_function = 'sha256'):
    #对每个输入的叶子结点，找hash
    lst_hash = []
    for i in lst:
        lst_hash.append(hash_leaf(i))
    merkle_tree = [copy.deepcopy(lst_hash)]
    #小于2个叶子结点
    if len(lst_hash)<2:print("ERROR!");return 0
    h = 0 #树高
    while len(lst_hash) >1:
        h += 1
        if len(lst_hash)%2 == 0:#偶数节点
            v = []
            while len(lst_hash) >1 :
                a = lst_hash.pop(0)
                b = lst_hash.pop(0)
                v.append(hash_func(a+b, hash_function))
            merkle_tree.append(v[:])
            lst_hash = v
        else:#奇数节点
            v = []
            last_node = lst_hash.pop(-1)
            while len(lst_hash) >1 :
                a = lst_hash.pop(0)
                b = lst_hash.pop(0)
                v.append(hash_func(a+b, hash_function))
            v.append(last_node)
            merkle_tree.append(v[:])
            lst_hash = v
    return merkle_tree,h


if __name__ == '__main__':
    leaves = ['1','2','3','4','5','6','7']
    merkle_tree,h = MerkleTree(leaves)
    print('叶子节点:',' '.join(leaves)," 树高:",h)
    for i in range(h+1):
        print('第{0}层:\n{1}\n'.format(i + 1,",\n".join(merkle_tree[i])))
    print()