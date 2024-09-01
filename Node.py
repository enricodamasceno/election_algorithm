import logging
from threading import Lock

logger = logging.getLogger(__name__)

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
            if self.leader and self.leader.alive:
                if self.network.net_comm(self, self.leader):
                    logger.debug(f"Nó {self.node_id} detectou líder existente: Nó {self.leader.node_id}")
                    return
            
            logger.debug(f"Nó {self.node_id} iniciando processo de eleição.")
            max_priority_node = min(
                [node for node in self.nodes if node.alive], 
                key=lambda node: node.node_id
            )
            
            self.leader = max_priority_node
            self.network.leader = self.leader
            
            for node in self.nodes:
                if node != self: # Não se comunica consigo mesmo
                    self.network.net_comm(self, node)
            
            logger.debug(f"Eleição concluída. Líder eleito: Nó {self.leader.node_id}")

    def communicate(self, target_node):
        if not self.alive: # Apenas nós vivos podem se comunicar
            return
        
        if target_node == self: # Evita que se comuniquem consigo mesmos
            return
        
        if not target_node.alive:
            logger.warning(f"Nó {self.node_id} detectou que o Nó {target_node.node_id} está desativado.")
            try:
                self.nodes.remove(target_node)
            except ValueError:
                logger.error(f"Tentativa de remover Nó {target_node.node_id} da lista de nós do Nó {self.node_id}, mas ele não está na lista.")
            except Exception as e:
                logger.error(f"Erro inesperado ao tentar remover Nó {target_node.node_id} da lista de nós do Nó {self.node_id}: {e}")
                
            if target_node == self.leader:
                logger.debug(f"Nó {self.node_id} chamando nova eleição devido à morte do líder.")
                self.elect_leader()
                
            # Informa os outros nós da desativação do anterior.
            for node in self.nodes:
                self.network.net_comm(self, node)
                
        else:
            if target_node.nodes != self.nodes:
                target_node.nodes = self.nodes
                        
            if target_node == self.leader:
                logger.debug(f"Nó {self.node_id} tentando contatar o líder: Nó {target_node.node_id}")
                
                if target_node.leader != self.leader:
                    target_node.leader = self.leader
                    logger.debug(f"Nó {self.node_id} informando o Nó {target_node.node_id} que ele será o líder.")
                
                return True
            
            else:
                if target_node.leader != self.leader:
                    target_node.leader = self.leader
                    logger.debug(f"Nó {self.node_id} está informando Nó {target_node.node_id} do líder: {target_node.leader.node_id}.")
                
                else:
                    logger.debug(f"Nó {self.node_id} se comunicou com Nó {target_node.node_id}.")
                    
                return True
            
    def kill(self):
        logger.error(f"Nó {self.node_id} caiu.")
        self.alive = False
