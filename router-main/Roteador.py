from TabelaRoteamento import Rota, TabelaRoteamento  # Importação das classes Rota e TabelaDeRoteamento do módulo RouterTable
from EnviadorMensagem import EnviadorMensagem  # Importação da classe EnviadorDeMensagem do módulo MessageSender
from ReceptorMensagem import ReceptorMensagem  # Importação da classe ReceptorDeMensagem do módulo MessageReceiver

import time
import threading
import socket

class Roteador:

    def __init__(self):
        self.tabela_de_roteamento = TabelaRoteamento('IPS.txt')  # Criação de uma instância da classe TabelaDeRoteamento, passando o arquivo 'IPS.txt' como argumento
        self.tabela_de_roteamento.popular_do_arquivo()  # Popula a tabela de roteamento a partir do arquivo 'IPS.txt'
        self.host_ip = self.obter_ip_do_host()  # Obtém o IP do host em que o roteador está sendo executado
        self.tabela_de_roteamento.vizinhos = self.tabela_de_roteamento.obter_vizinhos()  # Obtém os vizinhos do roteador

        self.enviador_de_mensagem = EnviadorMensagem()  # Criação de uma instância da classe EnviadorDeMensagem
        self.receptor_de_mensagem = ReceptorMensagem(host_ip=self.host_ip)  # Criação de uma instância da classe ReceptorDeMensagem, passando o IP do host como argumento

    def receber(self):
        self.receptor_de_mensagem.recebe_mensagem(self.tabela_de_roteamento)  # Chama o método recebe_mensagem do objeto receptor_de_mensagem, passando a tabela de roteamento como argumento
        
    def enviar(self):
        while True:
            self.enviador_de_mensagem.enviar_tabelaRoteamento(self.tabela_de_roteamento)  # Chama o método enviar_tabelaRoteamentoo do objeto enviador_de_mensagem, passando a tabela de roteamento como argumento
            time.sleep(10)  # Aguarda 10 segundos antes de enviar novamente
    
    def obter_ip_do_host(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Criação de um socket IPv4 e UDP
        try:
            s.connect(('10.255.255.255', 1))  # Conecta o socket a um endereço IP de broadcast
            IP = s.getsockname()[0]  # Obtém o endereço IP do socket
        except Exception:
            IP = '127.0.0.1'  # Caso ocorra algum erro, atribui o endereço IP localhost (127.0.0.1)
        finally:
            s.close()  # Fecha o socket
        return IP
    
    def verificar_rotas(self):
        while True:
            self.tabela_de_roteamento.aumentar_temporizador()  # Incrementa o temporizador de todas as rotas da tabela de roteamento
            self.tabela_de_roteamento.verificar_remocao_rotas()  # Verifica se alguma rota deve ser removida da tabela
            time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente

if __name__ == '__main__':
    roteador = Roteador()  # Criação de uma instância da classe Roteador
    roteador.tabela_de_roteamento.popular_dicionario()  # Popula o dicionário de endereços IP e máscaras da tabela de roteamento
    
    thread_receptor = threading.Thread(target=roteador.receber)  # Criação de uma thread para executar o método receber
    thread_enviador = threading.Thread(target=roteador.enviar)  # Criação de uma thread para executar o método enviar
    thread_contador = threading.Thread(target=roteador.verificar_rotas)  # Criação de uma thread para executar o método verificar_rotas
    iterecao = 0  # Inicializa a variável iterecao com 0

    thread_receptor.start()  # Inicia a execução da thread receptor
    thread_enviador.start()  # Inicia a execução da thread enviador
    thread_contador.start()  # Inicia a execução da thread contador

    while True:
        roteador.tabela_de_roteamento.imprimir_rotas()  # Imprime as rotas da tabela de roteamento
        print(f"\n iteração: {iterecao} \n")  # Imprime a versão atual
        iterecao += 1  # Incrementa a versão
        time.sleep(5)  # Aguarda 5 segundos antes de imprimir novamente
