#-----------------------------------------------Imports
from scapy.all import sendp, get_if_hwaddr
from scapy.layers.l2 import Ether
from scapy.sendrecv import sniff
import threading

INTERFACE = "Ethernet"
SRC_MAC = get_if_hwaddr(INTERFACE)
ether_type_list = [0x88B5, 0x88B6, 0x88B7]

#-----------------------------------------------Send Function
def send_frame(interface, source_mac, destination_mac, ether_type, payload):
    frame = Ether(src=source_mac, dst=destination_mac, type=ether_type) / payload
    sendp(frame, iface=interface)
    print(f"[INFO] -- Packet send to : {destination_mac} with message :  {payload}")

#-----------------------------------------------Receive Function
def receive_frames(interface):
    sniff(iface=interface, prn=handle_packet)

#-----------------------------------------------Interpreter Function
def handle_packet(packet):
    if packet.haslayer(Ether):
        ether_layer = packet[Ether]

        if ether_layer.src == SRC_MAC:
            return

        if ether_layer.type not in ether_type_list:
            return

        if ether_layer.type == 0x88B5:
            payload = bytes(ether_layer.payload).rstrip(b'\x00')
            print(f"[INFO] -- Received message : {payload} from : {ether_layer.src}")
            if payload == b"Hey, I want to make a connection ! Is it ok ?":
                send_frame(INTERFACE, SRC_MAC, ether_layer.src, 0x88B5, b"No problem bro ;-)")
            elif payload == b"No problem bro ;-)":
                print("[INFO] -- The receiver is available for a connection")
            if choice1 == "S":
                main()

        if ether_layer.type == 0x88B7:
            payload = bytes(ether_layer.payload).rstrip(b'\x00')
            print(f"[INFO] -- Received message : {payload} from : {ether_layer.src}")
            if choice1 == "S":
                main()

#-----------------------------------------------Ask Choice Function
def main():
    choice2 = input("\nChoose your action (you can write \"help\") : ")
    if choice2 == "help":
        show_help()
    elif choice2 == "test":
        test_connection()
    elif choice2 == "key":
        enable_rsa()
    elif choice2 == "message":
        send_message()
    elif choice2 == "exit":
        print("\nBye...")
        exit()
    else:
        print("[ERROR] -- Wrong command !!!")
        main()

#-----------------------------------------------Show Help Function
def show_help():
    print("\n Here are all the commands you can use :")
    print("- \"test\" : Here you can test a connection with a device")
    print("- \"message\" : Send a message to a device")
    print("- \"exit\" : Exit the software")

#-----------------------------------------------Test Connection Function
def test_connection():
    DEST_MAC = input("Enter the destination mac address : ")
    ETHER_TYPE = 0x88B5
    PAYLOAD = b"Hey, I want to make a connection ! Is it ok ?"
    MIN_FRAME_SIZE = 64
    payload_length = len(PAYLOAD)
    if payload_length < (MIN_FRAME_SIZE - 14):
        PAYLOAD += b"\x00" * ((MIN_FRAME_SIZE - 14) - payload_length)
    send_frame(INTERFACE, SRC_MAC, DEST_MAC, ETHER_TYPE, PAYLOAD)

#-----------------------------------------------Enable RSA Function
def enable_rsa():
    DEST_MAC = input("Enter the destination mac address : ")
    ETHER_TYPE = 0x88B7

#-----------------------------------------------Send Message Function
def send_message():
    DEST_MAC = input("Enter the destination mac address : ")
    ETHER_TYPE = 0x88B7
    payload_str = input("Payload : ")
    PAYLOAD = payload_str.encode('utf-8')
    MIN_FRAME_SIZE = 64
    payload_length = len(PAYLOAD)
    if payload_length < (MIN_FRAME_SIZE - 14):
        PAYLOAD += b"\x00" * ((MIN_FRAME_SIZE - 14) - payload_length)
    send_frame(INTERFACE, SRC_MAC, DEST_MAC, ETHER_TYPE, PAYLOAD)


#-----------------------------------------------Main
if __name__ == "__main__":
    print("""
     _______  __   __  __    _  _______  _______ 
    |       ||  | |  ||  |  | ||       ||       |
    |    _  ||  |_|  ||   |_| ||    ___||_     _|
    |   |_| ||       ||       ||   |___   |   |  
    |    ___||_     _||  _    ||    ___|  |   |  
    |   |      |   |  | | |   ||   |___   |   |  
    |___|      |___|  |_|  |__||_______|  |___|  
    """)

    # -----------------------------------------------Ask Software Mode
    choice1 = input("\nDo you want to be a sender or a receiver ? (S/R) : ").strip().upper()

    while True:
        if choice1 == "S":
            sender_thread = threading.Thread(target=main())
            receiver_thread = threading.Thread(target=receive_frames(INTERFACE))

            sender_thread.start()
            receiver_thread.start()

            sender_thread.join()
            receiver_thread.join()
        elif choice1 == "R":
            receive_frames(INTERFACE)
        else:
            print("[ERROR] -- Wrong command !!!")