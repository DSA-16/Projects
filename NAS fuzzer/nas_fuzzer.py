import socket
import random
import time

AMF_IP = "127.0.0.5"
AMF_PORT = 38412

BASE_NAS = bytes.fromhex(
    "7e00"  # Extended protocol discriminator + security header type (Plain NAS)
    "41"    # Message type: Registration Request
    "00"    # Registration type: Initial
    "f0"    # SUCI format (fake)
    "01" * 10  # IMSI filler
)

def mutate_nas(base):
    mutated = bytearray(base)
    for _ in range(random.randint(1, 2)):  # mutate 1–2 bytes
        idx = random.randint(4, len(mutated) - 1)
        mutated[idx] = random.randint(0, 255)
    return bytes(mutated)

def send_to_amf(payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP) as s:
            s.settimeout(2)
            s.connect((AMF_IP, AMF_PORT))
            s.send(payload)
            print(f"Sent mutated NAS: {payload.hex()}")
    except Exception as e:
        print(f"[!] Connection failed: {e}")

# Send 10 fuzzed messages
for _ in range(10):
    fuzzed_msg = mutate_nas(BASE_NAS)
    send_to_amf(fuzzed_msg)
    time.sleep(0.2)
