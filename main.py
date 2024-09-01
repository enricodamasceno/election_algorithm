from Node import Node
from Network import Network
import logging

# Configuração do logger para o módulo principal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    num_nodes = 5
    network = Network()

    nodes = [Node(i, network=network) for i in range(1, num_nodes + 1)]
    for node in nodes:
        network.add_node(node)

    # Debugging para mostrar qual nó foi eleito como líder
    for node in nodes:
        logger.debug(f"Nó {node.node_id}: Líder eleito - Nó {node.leader.node_id if node.leader else 'Nenhum'}")

    # Desativa o líder informando a rede
    Node.current_leader.deactivate()
    
    # A desativação programada do líder informa a rede da necessidade de uma nova eleição.
    # O Nó 2 é eleito.

    # Adiciona um novo nó dinamicamente
    new_node = Node(num_nodes + 1, network=network)
    network.add_node(new_node)
    nodes.append(new_node)
    
    # Desativa o líder inesperadamente:
    # Assim, os nós só saberão de sua queda durante a tentativa de comunicação.
    Node.current_leader.kill()

    # Os nós tentam se comunicar com o líder e detectam que ele está morto
    for node in nodes:
        network.net_comm(node, node.leader) # Cada nó tenta se comunicar com "seu próprio líder".

    # Mostra qual nó foi eleito como líder após a morte do nó anterior
    for node in nodes:
        if node.alive:
            logger.debug(f"Nó {node.node_id}: Líder eleito após a atualização - Nó {node.leader.node_id if node.leader else 'Nenhum'}")

if __name__ == '__main__':
    main()