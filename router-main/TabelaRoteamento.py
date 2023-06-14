class Rota:
    def __init__(self, ip_destino, metrica_salto=1, ip_saida=None):
        self.ip_destino = ip_destino
        self.metrica_salto = metrica_salto
        self.ip_saida = ip_saida

    def __str__(self):
        return f'IP de Destino: {self.ip_destino}, Métrica de Salto: {self.metrica_salto}, IP de Saída: {self.ip_saida}'


class TabelaRoteamento:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.rotas = []
        self.vizinhos = []
        self.ultima_mensagem_ip = {}

    def popular_do_arquivo(self):
        # Abre o arquivo usando um gerenciador de contexto
        with open(self.nome_arquivo, "r") as arquivo:
            # Lê cada linha do arquivo
            for linha in arquivo:
                linha = linha.strip()
                rota = Rota(ip_destino=linha, ip_saida=linha)
                self.rotas.append(rota)

    def popular_dicionario(self):
        for rota in self.obter_vizinhos():
            self.ultima_mensagem_ip[rota.ip_destino] = 0

    def aumentar_temporizador(self):
        for ip in self.ultima_mensagem_ip:
            self.ultima_mensagem_ip[ip] += 1

    def verificar_remocao_rotas(self):
        for rota in self.obter_vizinhos():
            if self.ultima_mensagem_ip[rota.ip_destino] >= 30:
                self.remover_rotas_por_ip_saida(rota.ip_saida)

    def atualizar_tabela(self, novas_rotas, ip_remetente, ip_anfitriao):
        novos_destinos = {rota.ip_destino for rota in novas_rotas}
        self.rotas = [
            rota
            for rota in self.rotas
            if rota.ip_saida != ip_remetente or (rota.ip_saida == ip_remetente and rota.ip_destino in novos_destinos)
        ]

        for rota in novas_rotas:
            rotas_existentes = [r for r in self.rotas if r.ip_destino == rota.ip_destino]

            if rotas_existentes:
                rota_existente = rotas_existentes[0]
                if rota_existente.metrica_salto > rota.metrica_salto + 1:
                    rota_existente.metrica_salto = rota.metrica_salto + 1
                    rota_existente.ip_saida = rota.ip_saida
            elif rota.ip_destino != ip_anfitriao:
                nova_rota = Rota(ip_destino=rota.ip_destino, metrica_salto=rota.metrica_salto + 1, ip_saida=ip_remetente)
                self.rotas.append(nova_rota)

        if not any(rota.ip_destino == ip_remetente for rota in self.rotas):
            nova_rota = Rota(ip_destino=ip_remetente, metrica_salto=1, ip_saida=ip_remetente)
            self.rotas.append(nova_rota)

    def remover_rotas_por_ip_saida(self, ip_saida):
        self.rotas = [rota for rota in self.rotas if rota.ip_saida != ip_saida]

    def obter_vizinhos(self):
        return [rota for rota in self.rotas if rota.metrica_salto == 1]

    def imprimir_rotas(self):
        print("---------------------------------------------------------")
        print(f"| {'IP de Destino':^15} | {'Métrica de Salto':^10} | {'IP de Saída':^15} |")
        print("---------------------------------------------------------")
        for rota in self.rotas:
            print(f"| {rota.ip_destino:^15} | {rota.metrica_salto:^10} | {rota.ip_saida:^15} |")
        print("---------------------------------------------------------")
