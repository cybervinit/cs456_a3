
class printer:
    
    def __init__(self):
        pass
    
    def out_msg(self, msg):
        print(f'''SID({msg.get_el(0)}),SLID({msg.get_el(1)}),RID({msg.get_el(2)}),RLID({msg.get_el(3)}),LS({msg.get_el(4)})''')

    def out(self, msg_type, msg):
        print(f'{msg_type}:', end='')
        self.out_msg(msg)

