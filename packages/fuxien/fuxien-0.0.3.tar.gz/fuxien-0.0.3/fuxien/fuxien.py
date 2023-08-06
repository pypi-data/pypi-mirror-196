# coding:utf-8
#name:FuXi_ensystem
#author:Lixver

import random

#默认密钥加密
def fuxi_enc(enctext):
    encry_str = ""
    enctext = enctext.replace('\n','/n')
    for i in enctext:
        numbers = [1,2,3,4,5,6,7,8,9,0]
        chosen = random.choice(numbers)
        chosen = str(chosen)
        temp = str(ord(i)) + chosen + 'I'
        chosen = random.choice(numbers)
        chosen = str(chosen)
        encry_str = encry_str + chosen + temp
    return encry_str

#默认密钥解密
def fuxi_dec(dectext):
    dec_str = ""
    for i in dectext.split("I")[:-1]:
        i = i[:-1]
        i = i[1:]
        temp = chr(int(i))
        dec_str = dec_str+temp
        dec_str = dec_str.replace('/n','\n')
    return dec_str

#选择密钥加密
def fuxi_keyenc(*param):
    org_str = str(param[0])
    key_str = str(param[1])
    k = 0
    ke = 0
    n = 0
    for k in key_str:
        k = ord(k)
        k = int(k)
        ke = ke + k*10
        n = n + 1
    keys = int(ke/n)
    result = ""
    for i in org_str:
        t = i
        res = ord(t)
        res = str(int(res) + keys)
        radm1 = str(random.choice([1,2,3,4,5,6,7,8,9,0]))
        radm2 = str(random.choice([1,2,3,4,5,6,7,8,9,0]))
        result = result + radm1 + res + radm2 + 'I'
    enc_str = result
    return enc_str

#选择密钥解密
def fuxi_keydec(*param):
    org_str = str(param[0])
    key_str = str(param[1])
    k = 0
    ke = 0
    n = 0
    for k in key_str:
        k = ord(k)
        k = int(k)
        ke = ke + k*10
        n = n + 1
    keys = int(ke/n)
    result = ""
    for i in org_str.split("I")[:-1]:
        i = i[:-1]
        i = i[1:]
        i = int(i) - keys
        i = chr(i)
        result = result + i
        result = result.replace("/n","\n")
    dec_str = result
    return dec_str