import sys
from socket import *
from message import message
from link import link
from rib_entry import rib_entry
from printer import printer
from file_printer import file_printer
from collections import deque
import networkx as nx

NETEM_HOST = "127.0.0.1"
EGRESS_PORT = 9000
send_socket = socket(AF_INET, SOCK_DGRAM)

prt = printer()
r_id = 0
rib = {} # Router Information Base. Keeps track of the shortest-path link
link_pairs = {} # Keeps track of all the links we've come across
link_costs = {}
link_amt = 0
my_links = []
graph = nx.Graph()

topo_file = None
rt_file = None
# TODO: remove
# append_write = "w"
#if os.path.exists(CLIENT_FILENAME):
#    append_write = "a"

# send: sends pkt to (NETEM_HOST, EGRESS_PORT) using UDP
def send(msg):
  global NETEM_HOST, EGRESS_PORT, send_socket
  send_socket.sendto(msg.get_udp_data(), (NETEM_HOST, EGRESS_PORT))

# recv_packet: listens for and returns packet from UDP port
def recv_msg():
  data, client_addr = send_socket.recvfrom(4096)
  return message.parse_udp_data(data)
  

# do_init_phase: performs the init phase of the virtual router configuration
def do_init_phase():
    global my_links, link_amt, r_id
    init = message(1, [r_id])
    send(init) # send init data
    data = recv_msg().load_arr # receive init data
    link_amt = data[0]
    for i in range(1, (data[0] * 2) + 1, 2):
        my_links.append(link(data[i], data[i+1]))

# get_send_queue: fetches a queue of LSAs of the my_links of the current router
def get_send_queue():
    global r_id, my_links, link_pairs
    send_queue = deque()
    for l in my_links:
        link_pairs[l.lid] = [r_id]
        for sl in my_links:
            send_queue.append(message(3, [r_id, sl.lid, r_id, l.lid, l.cost]))
    return send_queue

# sync_rib: updates the routing information base according to the graph.
# Probably called after graph has updated
def sync_rib():
    global graph, rib, r_id, rt_file
    if not graph.has_node(r_id):
        return
    paths = nx.single_source_dijkstra_path(graph, r_id)
    costs = nx.single_source_dijkstra_path_length(graph, r_id)
    did_update = False
    for router, cost in costs.items():
        if router == r_id:
            continue
        if (router not in rib):
            did_update = True
            rib[router] = rib_entry(router, cost, paths[router][1])
        elif (cost < rib[router].get_cost()):
            did_update = True
            rib[router].update_path(cost, paths[router][1])
    if (did_update):
        rt_file.write_rt(rib)
        pass # TODO: print new rib to file

# handle_lsa: updates link_pairs, graph and the routing information base
# with the newly received info
def handle_lsa(msg):
    global link_pairs, link_costs, graph, topo_file
    if (msg.get_router_link_id() not in link_pairs): # added a new link
        link_pairs[msg.get_router_link_id()] = [msg.get_router_id()]
        link_costs[msg.get_router_link_id()] = msg.get_router_link_cost()
    else: # updated the link with a new router
        link_pairs[msg.get_router_link_id()].append(msg.get_router_id())
    # If link has both connections
    if (len(link_pairs[msg.get_router_link_id()]) == 2):
        graph.add_edge(
                link_pairs[msg.get_router_link_id()][0],
                link_pairs[msg.get_router_link_id()][1],
                weight=msg.get_router_link_cost()
        )
        topo_file.write_topo(link_pairs, link_costs)
    sync_rib()

# is_duplicate: True iff msg router_id, router_link_id and router_link_cost
# have already been seen by me (router) before
def is_duplicate(msg):
    # added a new link
    if (msg.get_router_link_id() in link_pairs
            and msg.get_router_id() in link_pairs[msg.get_router_link_id()]):
        return True
    return False

# propagate: sends msg to all other links
def propagate(msg):
    global r_id, my_links
    msg.update_sender_id(r_id)
    ingress_link_id = msg.get_sender_link_id()
    for l in my_links:
        if not ingress_link_id == l.lid:
            msg.update_sender_link_id(l.lid)
            prt.out('Sending(F)', msg)
            send(msg)

# do_fwd: performs the forwarding phase
def do_fwd():
    global prt
    send_queue = get_send_queue()
    for i in range(0, len(send_queue)):
        msg = send_queue.popleft()
        prt.out('Sending(E)', msg)
        send(msg)
    while True:
        msg = recv_msg()
        prt.out('Received', msg)
        if is_duplicate(msg): # skip if duplicate
            prt.out('Dropping', msg)
            continue
        handle_lsa(msg)
        propagate(msg)

def main():
    global NETEM_HOST, EGRESS_PORT, r_id, topo_file, rt_file
    args = sys.argv
    EGRESS_PORT = int(args[2])
    NETEM_HOST = args[1]
    r_id = int(args[3])
    topo_filename = "topology_" + str(r_id) + ".out"
    rt_filename = "routingtable_" + str(r_id) + ".out"
    topo_file = file_printer(topo_filename)
    rt_file = file_printer(rt_filename)
    do_init_phase() # Execute Init Phase
    do_fwd()        # Execute Foward Phase

if __name__ == "__main__":
    main()

