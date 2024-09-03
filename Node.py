import logging

logger = logging.getLogger(__name__)

class Node:
    def __init__(self, node_id, nodes=None):
        self.node_id = node_id
        self.nodes = nodes if nodes else []
        self.leader = None
        self.alive = True  # Indica se o nó está vivo

    def activate(self, nodes):
        self.nodes = nodes
        logger.info(f"Nó {self.node_id} foi adicionado à rede.")

    def elect_leader(self):
        if self.leader and self.leader.alive:
            if self.communicate(self.leader):
                logger.debug(f"Nó {self.node_id} detectou líder existente: Nó {self.leader.node_id}")
                return
        
        logger.info(f"Nó {self.node_id} iniciando processo de eleição.")
        max_priority_node = min(
            [node for node in self.nodes if node.alive], 
            key=lambda node: node.node_id
        )
        
        self.leader = max_priority_node
        
        for node in self.nodes:
            if node != self: # Não se comunica consigo mesmo
                self.communicate(node)
        
        logger.info(f"Eleição concluída. Líder eleito: Nó {self.leader.node_id}")

    def communicate(self, target_node):
        if not self.alive: # Apenas nós vivos enviam pacotes
            return 
        
        if self == target_node: # Evitar que se comuniquem consigo mesmos
            return
        
        if not target_node.alive:
            logger.warning(f"Nó {self.node_id} detectou que o Nó {target_node.node_id} está desativado.")
            try:
                self.nodes.remove(target_node)
            except ValueError:
                logger.error(f"Tentativa de remover Nó {target_node.node_id} da lista de nós do Nó {self.node_id}, mas ele não está na lista.")
            except Exception as e:
                logger.error(f"Erro inesperado ao tentar remover Nó {target_node.node_id} da lista de nós do Nó {self.node_id}: {e}")
                
            if self.leader and target_node.leader and target_node == self.leader:
                logger.debug(f"Nó {self.node_id} chamando nova eleição devido à morte do líder.")
                self.elect_leader()
                
            # Informa os outros nós da desativação do anterior.
            for node in self.nodes:
                self.communicate(node)
                
        else:                        
            if self.leader and target_node == self.leader:
                logger.debug(f"Nó {self.node_id} tentando contatar o líder: Nó {target_node.node_id}")
                
                if target_node.leader != self.leader:
                    target_node.leader = self.leader
                    logger.debug(f"Nó {self.node_id} informando o Nó {target_node.node_id} que ele será o líder.")
                
                return True
            
            else:
                if target_node.leader and target_node.leader != self.leader:
                    target_node.leader = self.leader
                    logger.debug(f"Nó {self.node_id} está informando Nó {target_node.node_id} do líder: {target_node.leader.node_id}.")
                    
                return True
            
    def kill(self):
        logger.warning(f"Nó {self.node_id} caiu.")
        self.alive = False
