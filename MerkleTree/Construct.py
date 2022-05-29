import hashlib
import time
import string
import random



#sha256
def hash_function(origin,res='sha256'):
    #对输入过一次sha256
    res=getattr(hashlib,res)   
    origin=origin.encode("utf-8")   
    #哈希值以十六进制输出                    
    origin_hex=res(origin).hexdigest()          
    return origin_hex

#生成随机
def generate(size):
    #从数字和字母中随机生成size个值，作为初始的值
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(size)]
    random_str = ''.join(str_list)
    return random_str
    
#构造merkle tree
def merkle(leaves):
    length=len(leaves)    
    if (length==0):      
        #表示树，对空字符hash
        return hash_function('')
    elif(length==1):                   
        #只有一个结点时
        x=hash_function(chr(int('0x00',16))+leaves[0])
        return x
    elif(length>1):      
        #对子问题递归处理             
        partition=2**(len(bin(length-1))-3)     #分界点
        left=merkle(leaves[0:partition])         #左子问题
        right=merkle(leaves[partition:length])   #右子问题
        tree=hash_function(chr(int('0x01',16))+left+right)
        return tree

if __name__=='__main__':
    leaves=[]
    leaves_num = 100000
    for i in range (0,leaves_num):
        random_str=generate(10)
        leaves.append(random_str)
    begin = time.time()   
    print("哈希函数: Sha256")
    print("构造的Merkle Tree:",merkle(leaves))
    end = time.time()    
    time_all = end -begin
    print("生成时间:",format(time_all,'.3f',),'ms')
    
          
    
    
    
