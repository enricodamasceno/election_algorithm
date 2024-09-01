import random
import time
import logging
from threading import Lock
from Node import Node

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-s: %(message)s'
)

class Network:
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes else []
        self.network_lock = Lock() # Trava para prevenir o acesso simultâneo a recursos compartilhados

    def add_node(self, node):
        with self.network_lock:
            self.nodes.append(node)
            node.nodes = self.nodes
            if Node.current_leader and Node.current_leader.alive:
                # Garante que o nó reconhece o líder atual
                node.leader = Node.current_leader
                logger.debug(f"Nó {node.node_id} foi adicionado à rede e reconheceu o líder existente: Nó {node.leader.node_id}.")
            else:
                logger.debug(f"Nó {node.node_id} foi adicionado à rede.")
                node.elect_leader()

    def remove_node(self, node):
        with self.network_lock:
            self.nodes.remove(node)
            logger.debug(f"Nó {node.node_id} foi removido da rede.")
            if node == node.leader:
                logger.debug(f"Nó {node.node_id} era o líder. Iniciando nova eleição.")
                self.nodes[0].elect_leader()  # Inicia uma nova eleição feita pelo primeiro nó da lista.

    def net_comm(self, source_node, target_node):
        # Simula latência da rede
        latency = random.uniform(0.1, 1.0)
        time.sleep(latency)

        # Simula perda de pacotes
        if source_node.alive: # Apenas nós vivos enviam pacotes
            if random.random() < 0.1:  # 10% de chance de perda de pacotes
                logger.warning(f"Mensagem de Nó {source_node.node_id} para Nó {target_node.node_id} foi perdida.")
                return False

        source_node.communicate(target_node)
        return True