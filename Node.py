import logging
from threading import Lock

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-s: %(message)s'
)

class Node:
    election_lock = Lock()  # Trava compartilhada para prevenir eleições simultâneas
    current_leader = None  # Variável de classe para manter registro do líder atual

    def __init__(self, node_id, nodes=None, network=None):
        self.node_id = node_id
        self.nodes = nodes if nodes else []
        self.network = network
        self.leader = None
        self.alive = True  # Indica se o nó está vivo
        logger.debug(f"Nó {self.node_id} inicializado.")

    def elect_leader(self):
        with Node.election_lock:
            if Node.current_leader and Node.current_leader.alive:
                logger.debug(f"Nó {self.node_id} detectou líder existente: Nó {Node.current_leader.node_id}")
                return
            
            logger.debug(f"Nó {self.node_id} começando processo de eleição.")
            max_priority_node = min(
                [node for node in self.nodes if node.alive], 
                key=lambda node: node.node_id
            )

            Node.current_leader = max_priority_node
            self.notify_leader(Node.current_leader)
            logger.debug(f"Nó {self.node_id} - Eleição concluída. Líder eleito: Nó {Node.current_leader.node_id}")

    def notify_leader(self, leader_node):
        for node in self.nodes:
            node.leader = leader_node
            if node != self:
                logger.debug(f"Nó {node.node_id} notificado para reconhecer o novo líder: Nó {leader_node.node_id}")

    def communicate(self, target_node):
        if target_node == self:
            return
        
        if not target_node.alive:
            logger.warning(f"Nó {self.node_id} detectou que o líder Nó {target_node.node_id} está morto.")
            if target_node == self.leader:
                logger.debug(f"Nó {self.node_id} iniciando nova eleição devido à morte do líder.")
                self.elect_leader()
        else:
            logger.debug(f"Nó {self.node_id} comunicando-se com Nó {target_node.node_id}.")

    def kill(self):
        logger.debug(f"Nó {self.node_id} está sendo morto.")
        self.alive = False
        if self.network:
            self.network.remove_node(self)
            logger.debug(f"Nó {self.node_id} foi removido da lista de nós ativos.")