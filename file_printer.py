
class file_printer:
    filename = ""
    file = None
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "w")

    def write_topo(self, link_pairs, link_costs):
        self.file.write("TOPOLOGY\n")
        for lid, pair in link_pairs.items():
            if (len(pair) < 2):
                continue
            # FIXME: add cost
            self.file.write(f'router:{pair[0]},router:{pair[1]},linkid:{lid},cost:\n')
            self.file.write(f'router:{pair[1]},router:{pair[0]},linkid:{lid},cost:\n')

    def write_rt(self, rib):
        self.file.write("ROUTING\n")
        for router_id, el in rib.items():
            self.file.write(f'{router_id}:{el.next_hop},{el.get_cost()}\n')
