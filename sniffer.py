from scapy.all import sniff, IP, TCP

def packet_callback(packet):

    if packet.haslayer(IP) and packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        # Formato legível: IP_Origem:Porta -> IP_Destino:Porta
        print(f"[TCP] {src_ip}:{src_port} --> {dst_ip}:{dst_port}")


def main():
    print("Iniciando captura de pacotes TCP... (Pressione Ctrl+C para parar)")
    sniff(filter="tcp", prn=packet_callback, store=0)


if __name__ == "__main__":
    main()