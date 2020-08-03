class message:
    msg_load_arr = []

    def __init__(self, type, msg_load_arr):
        self.type = type
        self.msg_load_arr = msg_load_arr

    def get_udp_data(self):
        array = bytearray()
        array.extend(self.type.to_bytes(length=4, byteorder="big"))
        for el in self.msg_load_arr:
            array.extend(el.to_bytes(length=4, byteorder="big"))
        return array

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
        msg_load_arr_len = 0
        if type == 4:
            msg_load_arr_len = 1 + (2 * int.from_bytes(UDPdata[4:8], byteorder="big"))
            window_start = 4
            payload = []
            for i in range(window_start, window_start + (4 * msg_load_arr_len), 4):
                payload.append(int.from_bytes(UDPdata[i:i+4], byteorder="big"))
            return message(4, payload)
        elif type == 3:
            msg_load_arr_len = 5
            payload = []
            for i in range(1, 6):
                payload.append(int.from_bytes(UDPdata[i*4:(i*4)+4], byteorder="big"))
            return message(3, payload)

