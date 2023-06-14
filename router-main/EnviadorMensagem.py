import socket

PORTA_PADRAO = 5000  # Define uma porta padrão para o socket

class EnviadorMensagem:
    def __init__(self, porta=PORTA_PADRAO):
        self.porta = porta
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP 

    def __del__(self):
        self.sock.close()  # Fecha o socket quando o objeto é destruído

    def enviar_mensagem(self, mensagem, ip_destino):
        self.sock.sendto(mensagem.encode(), (ip_destino, self.porta))  # Codifica a mensagem em bytes e envia para o IP de destino

    def rotas_para_mensagem(self, rotas):
        if not rotas:
            return '!'  # Retorna um caractere de exclamação se não houver rotas
        
        strings_rota = [f'*{rota.ip_destino};{rota.metrica_salto}' for rota in rotas]  # Cria uma lista de strings formatadas para cada rota
        return ''.join(strings_rota)  # Junta as strings em uma única mensagem

    def enviar_tabelaRoteamento(self, tabela_rotas):
        mensagem = self.rotas_para_mensagem(tabela_rotas.rotas)  # Converte a tabela de rotas em uma mensagem
        for rota in tabela_rotas.vizinhos:
            self.enviar_mensagem(mensagem, rota.ip_destino)  # Envia a mensagem para cada vizinho na tabela de rotas
