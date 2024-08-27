import random
import logging

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-s: %(message)s'
)

class Node:
    def __init__(self, node_id, threshold, nodes):
        self.node_id = node_id
        self.priority_score = random.randint(1, 100)
        self.threshold = threshold
        self.nodes = nodes
        self.leader = None
        self.votes = {}

    def communicate(self):
        for node in self.nodes:
            if node.node_id != self.node_id:
                # Voto ponderado baseado na diferença de prioridade
                vote = max(0, self.priority_score - node.priority_score)
                logger.debug(f"Nó {self.node_id} comunica com Nó {node.node_id} - Prioridade: {self.priority_score}, Voto: {vote}")
                if self.priority_score >= self.threshold:
                    node.receive_vote(self.node_id, vote)

    def receive_vote(self, other_node_id, vote):
        logger.debug(f"Nó {self.node_id} recebeu voto de Nó {other_node_id} com Voto: {vote}")
        if other_node_id in self.votes:
            self.votes[other_node_id] += vote
        else:
            self.votes[other_node_id] = vote

    def determine_leader(self):
        if self.votes:
            # Seleciona o nó com a maior soma de votos
            max_votes = max(self.votes.values())
            candidates = [node_id for node_id, votes in self.votes.items() if votes == max_votes]
            # No caso de empate, seleciona o nó com o maior ID
            if candidates:
                self.leader = max(candidates)
                logger.debug(f"Nó {self.node_id} determinou Líder como Nó {self.leader}")
            else:
                self.leader = self.node_id
                logger.debug(f"Nó {self.node_id} se nomeia Líder por padrão")

    def run_election(self):
        logger.debug(f"Nó {self.node_id} iniciando eleição com Prioridade: {self.priority_score}")
        if self.priority_score >= self.threshold:
            self.leader = self.node_id
            logger.debug(f"Nó {self.node_id} se nomeia como Líder")
        self.communicate()
        self.determine_leader()
