from pwn import *
from sage.all import *
from random import *

if __name__ == '__main__':

    poly = 0xaa0d3a677e1be0bf
    poly_bits = [int(char) for char in f'{poly:0b}']
    # print(len(poly_bits)) # 64

    func = {(64): 1}
    for i in range(len(poly_bits)):
        func[(i)] = poly_bits[i]

    F = PolynomialRing(GF(2), 'x')
    C = companion_matrix(F(func), format='left')

    # print(C.str().replace('[', '').replace(']', '').replace(' ', ''))# .replace('\n', '')

    r = remote('edu-ctf.csie.org', '42069')

    money = 1.2
    d = randint(0, 1)
    r.sendline(str(d).encode())
    # res = r.recvline().decode()

    _A = []
    _B = []
    for i in range(1, 65):

        res = r.recvline().decode()
        if res == 'E( G_G)':
            print(res)
            exit(0)
        else:
            _money = float(res.strip('> '))
            if money > _money:
                print('lose ', end='')
                b = 1 - d
            else:
                print('win ', end='')
                b = d
            money = _money
            print(f'M:{money}, B:{b}, D:{d}')

        _A.append(list((C ** (43 * i - 1))[0]))
        _B.append([b])

        X = matrix(_A).solve_right(matrix(_B))

        d = int((C ** (43 * (i+1) - 1) * X)[0][0])
        r.sendline(str(d).encode())

    print('get init state !!!!')
    i = 65
    while 1:

        res = r.recvline().decode()

        if res == "Here's your flag:\n":
            res = r.recvline().decode()
            print(res)
            exit(0)
        elif res == 'E( G_G)':
            exit(87)
        else:
            _money = float(res.strip('> '))
            if money > _money:
                print('lose ', end='')
                exit(87)
            else:
                print('win ', end='')
            money = _money
            print(f'M:{money}')
        i += 1
        d = int((C ** (43 * i - 1) * X)[0][0])
        r.sendline(str(d).encode())

