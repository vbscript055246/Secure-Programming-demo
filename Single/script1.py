import hashlib
from sage.all import *
import warnings
warnings.filterwarnings("ignore")
from collections import namedtuple
from Crypto.Util.number import inverse


Point = namedtuple("Point", "x y")

ENC = bytes.fromhex("1536c5b019bd24ddf9fc50de28828f727190ff121b709a6c63c4f823ec31780ad30d219f07a8c419c7afcdce900b6e89b37b18b6daede22e5445eb98f3ca2e40")
p = 9631668579539701602760432524602953084395033948174466686285759025897298205383
gx = 5664314881801362353989790109530444623032842167510027140490832957430741393367
gy = 3735011281298930501441332016708219762942193860515094934964869027614672869355
G = Point(gx, gy)

a = -1
O = 'INFINITY'


def is_on_curve(P):
    global a, b
    if P == O:
        return True
    else:
        return (P.y ** 2 - (P.x ** 3 + a * P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p


def point_inverse(P):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P, Q):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            s = (3 * P.x ** 2 + a) * inverse(2 * P.y, p) % p
        else:
            s = (Q.y - P.y) * inverse((Q.x - P.x), p) % p
    Rx = (s ** 2 - P.x - Q.x) % p
    Ry = (s * (P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    # if a != -1:
    #     assert is_on_curve(R)
    return R


def point_multiply(P, d):
    bits = bin(d)[2:]
    Q = O
    for bit in bits:
        Q = point_addition(Q, Q)
        if bit == '1':
            Q = point_addition(Q, P)
    assert is_on_curve(Q)
    return Q


ax = 3829488417236560785272607696709023677752676859512573328792921651640651429215
ay = 7947434117984861166834877190207950006170738405923358235762824894524937052000
A = Point(ax, ay)
bx = 9587224500151531060103223864145463144550060225196219072827570145340119297428
by = 2527809441042103520997737454058469252175392602635610992457770946515371529908
B = Point(bx, by)

GA = point_addition(G, A)
GAG = point_addition(GA, G)
G2 = point_addition(GAG, point_inverse(A))

S = ((G2.y + G.y) * inverse(G.x-G2.x, p)) % p
a = (S * 2 * G.y - 3 * G.x**2) % p
b = (G.y**2 - G.x**3 - a * G.x) % p

assert is_on_curve(G)
assert is_on_curve(A)
assert is_on_curve(B)


shift = GF(p)(-4*3*a).square_root() * inverse(6, p)

ra = -7925182757193285961316626419940151258451119718064102936455321651294650340555
rb = -853242911173207820721903052331400912971957115055181874915218687301323932414


def phi(poi):
    delta = GF(p)(ra-rb).square_root() * (poi.x-ra)
    U = poi.y + delta
    D = poi.y - delta
    return (U/D) % p


A_ = Point(A.x - shift, A.y)
G_ = Point(G.x - shift, G.y)

# print(phi(G_) * phi(A_), phi(point_addition(G_, A_)))
# assert phi(G_) * phi(A_) == phi(point_addition(G_, A_))

dA = discrete_log(phi(A_), phi(G_))

#Decryption
k = point_multiply(B, dA).x
k = hashlib.sha512(str(k).encode('ascii')).digest()

for ci, ki in zip(ENC, k):
    print(chr(ci ^ ki), end='')
print()

