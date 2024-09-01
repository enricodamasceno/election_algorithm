import random
import time
import logging
from threading import Lock
from Node import Node

logger = logging.getLogger(__name__)

class Network:
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes else []
        self.leader = None

    def add_node(self, node):
        # Simula latência da rede
        latency = random.uniform(0.1, 1.0)
        time.sleep(latency)
        
        self.nodes.append(node)
        node.nodes = self.nodes
        if self.leader:
            node.leader = self.leader
            logger.debug(f"Nó {node.node_id} foi adicionado à rede e reconheceu o líder existente: Nó {node.leader.node_id}. Informado pela rede.")
        
        else:
            logger.debug(f"Nó {node.node_id} foi adicionado à rede.")
            node.elect_leader()

    def remove_node(self, node):
        # Simula latência da rede
        latency = random.uniform(0.1, 1.0)
        time.sleep(latency)
        
        self.nodes.remove(node)
        node.alive = False
        logger.debug(f"Nó {node.node_id} foi removido da rede. Informando outros nós.")
            
        if node == self.leader:
            logger.debug(f"Nó {node.node_id} era o líder. Iniciando nova eleição.")
            self.leader = None # A rede fica sem um líder até outro ser eleito.
            self.nodes[0].elect_leader()  # Inicia uma nova eleição feita pelo primeiro nó da lista.
            
        for node in self.nodes:
            node.nodes = self.nodes

    def net_comm(self, source_node, target_node, retries=3):
        # Simula latência da rede
        latency = random.uniform(0.1, 1.0)
        time.sleep(latency)

        # Simula perda de pacotes
        if not source_node.alive: # Apenas nós vivos enviam pacotes
            return 
        
        if source_node == target_node: # Evitar que se comuniquem consigo mesmos
            return
        
        if random.random() < 0.1:  # 10% de chance de perda de pacotes
            logger.warning(f"Mensagem de Nó {source_node.node_id} para Nó {target_node.node_id} foi perdida.")
            if retries > 0:
                logger.info(f"Tentando reenviar... ({retries} tentativas restantes)")
                return self.net_comm(source_node, target_node, retries - 1)
            else:
                logger.error(f"Falha na comunicação após múltiplas tentativas entre Nó {source_node.node_id} e Nó {target_node.node_id}.")
                return False

        source_node.communicate(target_node)
        return True
