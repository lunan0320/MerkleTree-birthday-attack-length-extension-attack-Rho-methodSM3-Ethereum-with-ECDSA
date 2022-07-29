import collections
import random


EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')
curve = EllipticCurve(
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    # Subgroup cofactor.
    h=1,
)

# Modular arithmetic ##########################################################
def inverse_mod(k, p):
    """Returns the inverse of k modulo p.
    This function returns the only integer x such that (x * k) % p == 1.
    k must be non-zero and p must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # 扩展欧几里得算法求模逆
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


# 椭圆曲线上运算 #########################################
def is_on_curve(point):
    """Returns True if the given point lies on the elliptic curve."""
    if point is None:
        # None represents the point at infinity.
        return True

    x, y = point
    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point):
    """Returns -point."""
    assert is_on_curve(point)

    if point is None:
        # -0 = 0
        return None

    x, y = point
    result = (x, -y % curve.p)

    assert is_on_curve(result)

    return result


def point_add(point1, point2):#点加
    """Returns the result of point1 + point2 according to the group law."""
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None

    if x1 == x2:
        # This is the case point1 == point2.
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        # This is the case point1 != point2.
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p,
              -y3 % curve.p)

    assert is_on_curve(result)
    return result


def scalar_mult(k, point):#多倍点(标量乘)
    """Returns k * point computed using the double and point_add algorithm."""
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None
    if k < 0:
        # k * point = -k * (-point)
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point
    
    while k:
        if k & 1:
            # Add.
            result = point_add(result, addend)

        # Double.
        addend = point_add(addend, addend)
        k >>= 1
        
    assert is_on_curve(result)
    return result

# Keypair generation and ECDSA ################################################
def make_keypair():
    """Generates a random private-public key pair."""
    private_key = random.randrange(1, curve.n)      #私钥d
    public_key = scalar_mult(private_key, curve.g)  #公钥P=dG
    return private_key, public_key


# forge a signature to pretend that you are Satoshi        
if __name__ == "__main__":
    
    print('Forge a signature to pretend that you are Satoshi:')
    # 初始化密钥对
    d, P = make_keypair()
    print("私钥sk:", hex(d))
    print("公钥pk: (0x{:x}, 0x{:x})".format(*P))

    # 随机挑选u，v
    u = random.randrange(1, curve.n)
    v = random.randrange(1, curve.n)
    print("u = 0x{:x}".format(u))
    print("v = 0x{:x}".format(v))
    # 构造R'
    (x,y) = point_add(scalar_mult(u,curve.g),scalar_mult(v,P))
    print("R' = 0x{:x}".format(x),",0x{:x}".format(y))
    # 构造得到r'_x e' s' 
    r_ = x%curve.n
    e_ = r_*u*inverse_mod(v,curve.n)
    s_ = r_*inverse_mod(v,curve.n)
    print("e' = 0x{:x}".format(e_))
    print("s' = 0x{:x}".format(s_))
    print("signature' = (0x{:x}".format(r_),",0x{:x})".format(s_))
    # 验证伪造的签名的正确性
    w = inverse_mod(s_, curve.n)
    u1 = (e_ * w) % curve.n
    u2 = (r_ * w) % curve.n
    (r_forge,s_forge)=point_add(scalar_mult(u1,curve.g),
                                scalar_mult(u2,P))
    if r_forge % curve.n == r_:
        print("Verify passed!")
        print('Forge_signature_Success!')
    else:
        print("Falid!")
