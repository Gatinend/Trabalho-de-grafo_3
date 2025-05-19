from algoritimos import dijkstra_tempo, dijkstra_trajeto
from extras import VariavelLimitada
from no import Agua, Arvore, Brigadista


class Caminhao:
    def __init__(self, nome, posicao, capacidade):
        self.nome = nome
        self.posicao = posicao              # Aqui deve ser o NOME do nó (string)
        self.carga = VariavelLimitada(capacidade)
        self.em_transito = False
        self.destino = None                 # Vai guardar o objeto No destino
        self.trajeto = []                   # Lista de nomes de nós
        self.tempo_restante = VariavelLimitada(0)
        self.acabou_de_chegar = False

    def apagar_fogo(self, ativos, grafo):
        """Se estiver sobre uma árvore em chamas, tenta apagar com a carga disponível."""
        no_atual = grafo.nos[self.posicao]
        if isinstance(no_atual, Arvore) and no_atual.queimando:
            faltante = no_atual.potencia_queima.maximo - no_atual.potencia_queima.valor
            if self.carga.valor >= faltante:
                no_atual.queimando = False
                no_atual.set_estado_final("apagado")
                ativos.discard(self.posicao)
                print(f"[{self.nome}] {self.posicao}: fogo completamente apagado.")
                self.carga.valor -= faltante
            else:
                # Apaga parcialmente
                no_atual.potencia_queima.definir_minimo(
                    no_atual.potencia_queima.valor - self.carga.valor
                )
                print(f"[{self.nome}] {self.posicao}: apagou {self.carga.valor} de água, "
                      f"energia restante: {no_atual.potencia_queima.valor}")
                self.carga.valor = 0

    def coletar_agua(self, grafo):
        """Se estiver sobre Brigadista ou Agua, recarrega totalmente."""
        no_atual = grafo.nos[self.posicao]
        if isinstance(no_atual, (Brigadista, Agua)):
            self.carga.valor = self.carga.maximo
            print(f"[{self.nome}] Reabasteceu em {self.posicao}. Carga agora {self.carga.valor}/{self.carga.maximo}")

    def controle_caminhao(self, grafo, caminhoes):
        """Resolve conflitos de destino entre caminhões."""
        adj = grafo.get_dict_adjacencia()  # ✅ Adicionado aqui

        for outro in caminhoes:
            if outro is self:
                continue
            if self.destino and outro.destino \
            and self.destino.nome == outro.destino.nome:
                t_self = dijkstra_tempo(adj, self.posicao, self.destino.nome)  # ✅
                t_out  = dijkstra_tempo(adj, outro.posicao, outro.destino.nome)  # ✅
                print(f"[Controle] {self.nome}({t_self}) vs {outro.nome}({t_out}) em {self.destino.nome}")
                if t_out <= t_self and outro.carga.valor >= outro.destino.potencia_queima.valor:
                    print(f"[Controle] {self.nome} cede para {outro.nome}")
                    self.destino = None; self.trajeto.clear()
                    return
                elif t_self < t_out and self.carga.valor >= self.destino.potencia_queima.valor:
                    print(f"[Controle] {outro.nome} cede para {self.nome}")
                    outro.destino = None; outro.trajeto.clear()
                    outro.escolher_destino(grafo, caminhoes)


    def verificar_e_adicionar_recarga(self, grafo):
        """Insere um desvio para recarga se destino exigir mais carga do que há disponível."""
        if not self.destino:
            return

        demanda = self.destino.potencia_queima.valor
        if demanda > self.carga.maximo:
            for no in self.trajeto:
                if isinstance(grafo.nos[no], (Brigadista, Agua)):
                    return

            candidatos = []
            adj = grafo.get_dict_adjacencia()  # ✅
            for nome, no_obj in grafo.nos.items():
                if isinstance(no_obj, (Brigadista, Agua)):
                    traj = dijkstra_trajeto(adj, self.posicao, nome)  # ✅
                    t = len(traj) if traj else float('inf')  # segurança
                    candidatos.append((t, traj))

            if not candidatos:
                return
            candidatos.sort(key=lambda x: x[0])
            _, caminho_recarga = candidatos[0]

            if caminho_recarga and caminho_recarga[-1] == self.trajeto[0]:
                caminho_recarga.pop()

            self.trajeto = caminho_recarga + self.trajeto

    def escolher_destino(self, grafo, caminhoes):
        """Escolhe o próximo foco de fogo considerando conflitos e recarga."""
        if self.em_transito:
            return

        opcoes = []

        # ✅ Pega o dicionário de adjacência no formato certo
        adj = grafo.get_dict_adjacencia()

        for nome, no in grafo.nos.items():
            if isinstance(no, Arvore) and no.queimando:
                t = dijkstra_tempo(adj, self.posicao, nome)  # <-- agora usa o dict correto
                opcoes.append((t, nome))

        opcoes.sort(key=lambda x: x[0])

        for _, nome in opcoes:
            self.destino = grafo.nos[nome]
            traj = dijkstra_trajeto(adj, self.posicao, nome)
            if not traj:
                continue

            if traj[0] == self.posicao:
                self.trajeto = traj[1:]
            else:
                self.trajeto = traj

            self.controle_caminhao(grafo, caminhoes)
            if not self.trajeto:
                continue

            self.verificar_e_adicionar_recarga(grafo)
            print(f"[{self.nome}] Trajeto definido: {'->'.join(self.trajeto)}")
            return

        # Nenhuma opção viável
        self.destino = None
        self.trajeto.clear()
        print(f"[{self.nome}] Sem destino viável.")

    def atualizar_movimento(self, grafo, caminhoes, ativos):
        """Executa um passo de tempo: movimenta, coleta água, apaga fogo e redireciona."""

        acabou_de_chegar = False  # Flag usada para identificar se acabou de chegar a um nó

        if self.em_transito:
            # ─── Em trânsito ───
            self.tempo_restante.valor -= 1
            if self.tempo_restante.valor > 0:
                print(f"[{self.nome}] em trânsito, {self.tempo_restante.valor} unidades restantes")
                return  # ainda em trânsito, não faz mais nada neste passo

            # ─── Chegou ao próximo nó ───
            self.posicao = self.trajeto.pop(0)
            print(f"[{self.nome}] chegou em {self.posicao}")
            self.em_transito = False
            acabou_de_chegar = True  # Marca que chegou neste passo de tempo

        # ─── Ações no nó atual ───
        if acabou_de_chegar or not self.trajeto:  # Executa ações ao chegar ou se for o início
            self.coletar_agua(grafo)
            self.apagar_fogo(ativos, grafo)

        # ─── Tenta escolher ou redefinir destino ───
        if not self.destino or not self.trajeto:
            self.escolher_destino(grafo, caminhoes)

        # ─── Inicia movimento, se houver trajeto ───
        if self.trajeto:
            prox = self.trajeto[0]
            
            # ======= Coloque esses prints para debug =======
            print(f"[DEBUG] Posicao atual: {self.posicao}, Proximo destino no trajeto: {prox}")
            print(f"[DEBUG] Adjacentes de {self.posicao}: {[v for v, _ in grafo.nos[self.posicao].adjacentes]}")
            # ===============================================

            peso = None
            for vizinho, p in grafo.nos[self.posicao].adjacentes:
                if vizinho == prox:
                    peso = p
                    break

            if peso is None:
                print(f"[{self.nome}] Erro: {prox} não é adjacente de {self.posicao}")
                return  # erro: destino inválido, não anda
            
            self.tempo_restante.definir_maximo(peso)
            self.tempo_restante.valor = peso
            self.em_transito = True
            print(f"[{self.nome}] iniciando para {prox}, tempo {peso}")
        else:
            print(f"[{self.nome}] parado em {self.posicao}")