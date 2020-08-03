import sys
from socket import *
from message import message
from link import link
from collections import deque

NETEM_HOST = "127.0.0.1"
EGRESS_PORT = 9000
send_socket = socket(AF_INET, SOCK_DGRAM)

r_id = 0
rib = {} # Router Information Base. Keeps track of the shortest-path link
link_amt = 0
links = []

# send: sends pkt to (NETEM_HOST, EGRESS_PORT) using UDP
def send(msg):
  global NETEM_HOST, EGRESS_PORT, send_socket
  send_socket.sendto(msg, (NETEM_HOST, EGRESS_PORT))

# recv_packet: listens for and returns packet from UDP port
def recv_msg():
  data, client_addr = send_socket.recvfrom(4096)
  return message.parse_udp_data(data)
  

# do_init_phase: performs the init phase of the virtual
# router configuration
def do_init_phase():
    global links, link_amt, r_id
    init = message(1, [r_id])
    send(init.get_udp_data()) # send init data
    data = recv_msg().msg_load_arr # receive init data
    link_amt = data[0]
    for i in range(1, (data[0] * 2) + 1, 2):
        links.append(link(data[i], data[i+1]))

# do_fwd: performs the forwarding phase
def do_fwd():
    global r_id, links
    print('fwd phase time!')
    send_queue = deque()
    print('My links:')
    for l in links:
        type_3_msg = message.get_message_3([
            r_id, l.lid, r_id, l.lid, l.cost
            ])
        print([r_id, l.lid, r_id, l.lid, l.cost])
        send_queue.append(type_3_msg)
    print('Received Messages:')
    while ((not len(send_queue)) == 0): # while not empty
        # FIXME: if you got the message already then discard
        # TODO: send to other links (not the one you got it from)
        for i in range(0, len(send_queue)):
            send(send_queue.popleft())
        msg = recv_msg()
        print(msg.msg_load_arr)
        # TODO: receive from neighbours

    pass

def main():
    global NETEM_HOST, EGRESS_PORT, r_id
    args = sys.argv
    EGRESS_PORT = int(args[2])
    NETEM_HOST = args[1]
    r_id = int(args[3])
    do_init_phase()
    do_fwd()

if __name__ == "__main__":
    main()

