
class rib_entry:
    dest = 0
    cost = 0
    next_hop = 0

    def __init__(self, dest, cost, next_hop):
        self.dest = dest
        self.cost = cost
        self.next_hop = next_hop

    def set_dest(new_dest):
        self.dest = new_dest

    def set_cost(new_cost):
        self.cost = new_cost

    def set_next_hop(new_next_hop):
        self.next_hop = new_next_hop

    def get_cost(self):
        return self.cost

    def update_path(self, new_cost, new_next_hop):
        self.cost = new_cost
        self.next_hop = new_next_hop
