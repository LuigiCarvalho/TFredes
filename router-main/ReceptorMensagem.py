import socket
from TabelaRoteamento import Rota
from EnviadorMensagem import EnviadorMensagem

TAMANHO_BUFFER = 1024

class ReceptorMensagem:
    def __init__(self, host_ip, port=5000):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
        self.sock.bind(('', self.port))  # Vincula o socket à porta
        self.host_ip = host_ip

    def __del__(self):
        self.sock.close()  # Fecha o socket quando terminar de usá-lo

    def recebe_mensagem(self, router_table):
        while True:
            dado, addr = self.sock.recvfrom(TAMANHO_BUFFER)  # Recebe até TAMANHO_BUFFER bytes do cliente
            message = dado.decode()  # Decodifica os bytes para uma string
            sender_ip = addr[0]  # Obtém o endereço IP do remetente

            print("recebeu")

            router_table.ultima_mensagem_ip[sender_ip] = 0

            if message.startswith("!"):
                tableString = EnviadorMensagem.routes_to_message(routes=router_table.routes)
                self.sock.sendto(tableString.encode(), (sender_ip, self.port))
            else:
                newRoutes = self.from_message(message, sender_ip)
                router_table.atualizar_tabela(newRoutes, sender_ip, self.host_ip)
                print("tabela de roteamento atualizada\n")

    @staticmethod
    def from_message(message, received_from_ip):
        # Divide a mensagem em rotas
        route_strings = message.split('*')[1:]

        # Cria uma instância de Route para cada string usando compreensão de lista
        routes = [Rota(route_string.split(';')[0], int(route_string.split(';')[1]), received_from_ip) for route_string in route_strings]

        return routes
