from Node import Node
import logging

# Configuração do logger para o módulo principal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Criação dos nós com IDs únicos e limiar de eleição
    nodes = []
    while len(nodes) < 10:
        nodes.append(Node(len(nodes), 10, nodes))
            
    # Atribuindo corretamente a lista de nós em cada nó
    for node in nodes:
        node.nodes = nodes
    
    # Executando o processo de eleição
    for node in nodes:
        node.run_election()
    
    # Exibindo o líder de cada nó
    for node in nodes:
        logger.info(f"Nó {node.node_id} tem como líder: {node.leader}")

if __name__ == "__main__":
    main()
