import socket

def runZed():
    pass

def Tx(Ip, Port):
    socketTx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr_port = (Ip, Port)
    socketTx.sendto(str(1).encode(),addr_port)
    print('[info] Tx send success.')


def Rx(Ip, Port):
    socketRx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr_port=(Ip, Port)
    socketRx.bind(addr_port)
    while True:
        msg,addr = socketRx.recvfrom(1024)
        idx=int(msg.decode())
        if idx == 1:
            runZed()
            print('[info] Zed running.')
        else:
            print('[info] Error.')

def main():
    Ip = "127.0.0.1"
    Port = 5111
    Tx(Ip,Port)

if __name__ == "__main__":
    main()