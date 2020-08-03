class message:
    load_arr = []

    def __init__(self, type, load_arr):
        self.type = type
        self.load_arr = load_arr

    def get_udp_data(self):
        array = bytearray()
        array.extend(self.type.to_bytes(length=4, byteorder="big"))
        for el in self.load_arr:
            array.extend(el.to_bytes(length=4, byteorder="big"))
        return array

    # condition: assumes self is a type 3 message
    def get_router_id(self):
        return self.load_arr[2]

    # condition: assumes self is a type 3 message
    def get_router_link_id(self):
        return self.load_arr[3]

    # condition: assumes self is a type 3 message
    def get_router_link_cost(self):
        return self.load_arr[4]

    # condition: assumes self is a type 3 message
    def get_sender_id(self):
        return self.load_arr[0]
    
    # condition: assumes self is a type 3 message
    def update_sender_id(self, new_sender_id):
        self.load_arr[0] = new_sender_id

    # condition: assumes self is a type 3 message
    def get_sender_link_id(self):
        return self.load_arr[1]

    # condition: assumes self is a type 3 message
    def update_sender_link_id(self, new_sender_link_id):
        self.load_arr[1] = new_sender_link_id

    @staticmethod
    def get_message_3(info_arr):
        array = bytearray()
        array.extend(int(3).to_bytes(length=4, byteorder="big"))
        for i in info_arr:
            array.extend(i.to_bytes(length=4, byteorder="big"))
        return array

    @staticmethod
    def parse_udp_data(UDPdata):
        type = int.from_bytes(UDPdata[0:4], byteorder="big")
        load_arr_len = 0
        if type == 4:
            load_arr_len = 1 + (2 * int.from_bytes(
                UDPdata[4:8],
                byteorder="big"))
            window_start = 4
            payload = []
            for i in range(window_start, window_start + (4 * load_arr_len), 4):
                payload.append(int.from_bytes(UDPdata[i:i+4], byteorder="big"))
            return message(4, payload)
        elif type == 3:
            load_arr_len = 5
            payload = []
            for i in range(1, 6):
                payload.append(int.from_bytes(
                    UDPdata[i*4:(i*4)+4], byteorder="big"))
            return message(3, payload)

