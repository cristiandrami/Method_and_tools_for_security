FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y gcc xinetd netcat net-tools && rm -rf /var/lib/apt/lists/* 


# Copy the xinetd configuration
COPY ctf.xinetd /etc/xinetd.d/ctf
RUN chmod 644 /etc/xinetd.d/ctf


# Copy the challenge code
COPY chall.c /root/challenge.c
WORKDIR /root
# Compile the challenge with ASLR enabled but without PIE and with NX enabled. No stack canaries.
RUN gcc -m64 -no-pie -fno-stack-protector -z noexecstack challenge.c -o challenge

# the flag
RUN echo "EMS{$(echo $RANDOM | md5sum | head -c 32)}" > /tmp/flag.txt
# Expose the port the service will run on
EXPOSE 9999

# Command to start xinetd
CMD ["xinetd", "-dontfork", "-stayalive", "-debug"]


