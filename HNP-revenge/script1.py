from random import randint
from Crypto.Util.number import *
from hashlib import sha256, md5
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature

from sage.all import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

E = SECP256k1
G, n = E.generator, E.order

d = randint(1, n)

pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)


def sig(msg):
    h = sha256(msg).digest()
    k = int(md5(b'secret').hexdigest() + md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16)
    print(f'key_: {int(md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16)}')
    sig = prikey.sign(bytes_to_long(h), k)
    return sig.r, sig.s


if __name__ == '__main__':

    msg1, msg2 = b'ABC', b'ABD'

    h1 = bytes_to_long(sha256(msg1).digest())
    r1, s1 = sig(msg1)

    h2 = bytes_to_long(sha256(msg2).digest())
    r2, s2 = sig(msg2)

    K = 2**128  # K = RR(n**(0.5))
    know = int(md5(b'secret').hexdigest(), 16) << 128

    N = n
    T = -(r1 * s2) * inverse(r2 * s1, n)
    const_know = (T+1) * know
    U = (h1*r2 - h2*r1)*inverse(r2*s1, n) + const_know

    L = matrix(ZZ, [
        [N, 0, 0],
        [T, 1, 0],
        [U, 0, K]
    ])

    assert RR(L.determinant())**(1/L.rank()) < RR(N)

    vs = L.LLL()
    v = vs[0]
    # assert RR(L.determinant()**(1/L.rank())) > RR(v.norm())
    print(v)

    _k1 = -v[0]
    _k2 = v[1]
    _K = v[2]

    k1 = _k1 + know
    k2 = _k2 + know
    print(f'_K1: {_k1}')
    print(f'_K2: {_k2}')
    # _d1 = ((k1 * s1 - h1) * inverse(r1, n))% n
    # _d2 = ((k2 * s2 - h2) * inverse(r2, n))% n
    #
    # print(_d1)
    # print(_d2)
    # print(d)