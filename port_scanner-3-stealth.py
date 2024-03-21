from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP
import sys
from datetime import datetime
from time import strftime

SYNACK = 0x12
RSTACK = 0x14

banner_intro = """
███╗   ███╗ █████╗ ██╗  ██╗ ██████╗ 
████╗ ████║██╔══██╗██║ ██╔╝██╔═══██╗
██╔████╔██║███████║█████╔╝ ██║   ██║
██║╚██╔╝██║██╔══██║██╔═██╗ ██║   ██║
██║ ╚═╝ ██║██║  ██║██║  ██╗╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
 ==================================
 """                                   

# Check That target is Up
def checkhost(ip):
    """
    Check That target is Up
    """
    conf.verb = 0
    try:
        ping = sr1(IP(dst = ip)/ICMP(), timeout=1, verbose=0)
        if ping:
            print("\n[*] Target is Up, Begin SCan...")
        else:
            print("[!] No response")
            print("[!] Exiting...")
            sys.exit(1)
    except Exception:
        print("[!] Couldn't Resolve Target")
        print("[!] Exiting...")
        sys.exit(1)

def scanport(port, target):
    # Randshort: this a function within scapy that generates a small random number to use as a source port. 
    srcport = RandShort()
    #  conf.verb to 0, this prevents output from sending packets from being printed to the screen.
    conf.verb = 0
    # print(srcport)
    # print(type(srcport))
    # print(port)
    # print(type (port))
    # craft and send our SYN packet.
    # sr1() function from scapy send the packet.
    # and then the packet we receive will be assigned to the variable, SYNACKpkt
    SYNACKpkt = sr1(IP(dst = target)/TCP(sport = srcport, dport = port, flags = "S"))
    
    # extract the flags from our received packet and assign them to a variable
    pktflags = SYNACKpkt.getlayer(TCP).flags

    
    #  compare the flag to set values we set earlier, and if they match, return True, if they don't, return False

    if pktflags == SYNACK:
    #  craft our RST packet. u
    # Uses the send() function. No response is expected.
     RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R")
     send(RSTpkt)    
     return True
    else:
     return False



def main():

    print (banner_intro)

    # Get User Input
    
    try:
        target = input("[*] Enter Target IP Address: ")
        min_port = input("[*] Enter Minimun Port Number: ")
        max_port = input("[*] Enter Maximun Port Number: ")
        try:
            if int(min_port) >= 0 and int(max_port) >=0 and int(max_port) >= int(max_port):
                pass
            else:
                print("\n[!] Invalid Range of Ports")
                print("[!] Exiting...")
                sys.exit(1)
        except Exception:
            print("\n[!] Invalid Range of Ports")
            print("[!] Exiting...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] User Requested Shutdown...")
        print("[!] Exiting...")
        sys.exit(1)

    # Settings some values
        
    # Ports range
    ports = range(int(min_port), int(max_port)+1)
    start_clock = datetime.now()


    checkhost(target)
    print ("[*] Scanning Started at " + strftime("%H:%M:%S") + "!\n")

    print("IP: " + str(target))

    for port in ports:
     #   print("port: " + str(port) )
        status = scanport(port, target)
        if status == True:
            print("Port " + str(port) + ": Open")

    stop_clock = datetime.now()
    total_time = stop_clock - start_clock
    print("\n[*] Scanning Finished!")
    print("[*] Total Scan Duration:" + str(total_time))


if __name__ == '__main__':
    main()
