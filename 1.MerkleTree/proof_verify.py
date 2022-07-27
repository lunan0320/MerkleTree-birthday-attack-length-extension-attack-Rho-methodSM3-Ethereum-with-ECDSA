import copy
import hashlib
import random
import string
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




def MerkleTree(leaves,hash_function = 'sha256'):
    lst_hash = []
    for i in leaves:
        lst_hash.append(hash_leaf(i))
    merkle_tree = [copy.deepcopy(lst_hash)]

    if len(lst_hash)<2:print("no tracnsactions to be hashed");return 0
    h = 0
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
            merkle_tree.append(v[:])#merkle树更新一层
            lst_hash = v
    return merkle_tree,h

#构造第n个叶子节点存在性和验证
def proof(merkle_tree,h,n,leaf,hash_function = 'sha256'):#h为Merkle树高度，n为查找的序号
    if n>=len(merkle_tree[0]):print("ERROR！");return 0
    j=0 #第j层,最底层需要计算叶子节点哈希值
    L = len(merkle_tree[0])
    if L%2 == 1 and L-1==n:#叶节点为奇数个，且n为最后一个节点
        hash_value = hash_leaf(leaf)
        print('第{0}层\nHash值:{1}'.format(j+1,hash_value))
    elif n%2==1:
        hash_value = hash_func(merkle_tree[0][n-1]+hash_leaf(leaf),hash_function)
        print('第{0}层\n查询值:{1}\nHash值:{2}'.format(j+1,merkle_tree[0][n-1],hash_value))
    elif n%2==0:
        hash_value = hash_func(hash_leaf(leaf)+merkle_tree[0][n+1],hash_function)
        print('第{0}层\n查询值:{1}\nHash值:{2}'.format(j+1,merkle_tree[0][n+1],hash_value))
    n = n//2
    j += 1 
    while j<h:#查询兄弟节点哈希值，生成新哈希值
        L = len(merkle_tree[j])
        if L%2 == 1 and L-1==n:#节点为奇数个，且n为最后一个节点
            print('第{0}层\nHash值:{1}'.format(j+1,hash_value))
        elif n%2==1:
            hash_value = hash_func(merkle_tree[j][n-1]+hash_value,hash_function)
            print('第{0}层\n查询值:{1}\nHash值:{2}'.format(j+1,merkle_tree[j][n-1],hash_value))
        elif n%2==0:
            hash_value = hash_func(hash_value+merkle_tree[j][n+1],hash_function)
            print('第{0}层\n查询值:{1}\nHash值:{2}'.format(j+1,merkle_tree[j][n+1],hash_value))
        n = n//2
        j += 1

    #print(hash_value)
    print('\nRoot:',merkle_tree[h][0])
    if hash_value==merkle_tree[h][0]:print("Success~\n节点%s在MerkleTree"%leaf)
    else:print("Failed\n节点%s不在MerkleTree"%leaf)

#生成随机
def generate(size):
    #从数字和字母中随机生成size个值，作为初始的值
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(size)]
    random_str = ''.join(str_list)
    return random_str

if __name__ == '__main__':
    #两种模式的区别只是初始的叶子节点不同
    flag = int(input('请选择模式:\n简单模式:0\n随机模式:1\n'))
    if flag == 1:   
        leaves = []
        #随机生成结点，包括字符和数字
        leaf_number = int(input('请输入初始的叶子节点数量:'))
        for i in range (0,leaf_number):
            random_str=generate(10)
            leaves.append(random_str)   
    elif flag == 0:
        leaves = ['1','2','3','4','5','6','7']
        print("初始叶子结点:"," ".join(leaves))
    leaf = input('请输入需要查找的节点值：')
    p = int(input('请输入需要查找的节点的初始编号：'))
    #构造MerkleTree
    merkle_tree,h = MerkleTree(leaves)
    proof(merkle_tree,h,p,leaf)
