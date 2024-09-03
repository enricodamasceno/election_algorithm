import random
import logging
from Node import Node

# Configuração do logger
log_filename = 'simulation.log'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)8s - %(message)s')

# Cria um handler para exibir no terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Cria um handler para gravar em arquivo
file_handler = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Adiciona os handlers ao logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def run_simulation(nodes, num_nodes):
    """Função para executar a simulação de comunicação e falhas de nós."""
    while len(nodes) > 1:
        # Escolhe dois nós aleatórios para tentar comunicar
        source_node = random.choice(nodes)
        target_node = None

        # Evita que o nó se comunique consigo mesmo e verifica se o nó alvo está vivo
        while target_node == source_node or not target_node:
            target_node = random.choice(source_node.nodes) if source_node.nodes else None
        
        # Evita que um nó desativado tente se comunicar
        while not source_node.alive:
            nodes.remove(source_node)
            if not nodes:  # Garante que sempre haverá pelo menos um nó vivo
                num_nodes += 1
                new_node = Node(num_nodes)
                nodes.append(new_node)
                new_node.activate(nodes)
            source_node = random.choice(nodes)
        
        if target_node != source_node:
            # Realiza a comunicação entre os nós
            logger.info(f"COMUNICAÇÃO ALEATÓRIA: Nós {source_node.node_id} e {target_node.node_id}")
            source_node.communicate(target_node)
        
        # Possível queda inesperada de um nó
        if random.random() < 0.1:  # 10% de chance de um nó falhar
            candidate_node = random.choice([node for node in nodes if node.alive])
            logger.warning(f"DESATIVAÇÃO ALEATÓRIA: Nó {candidate_node.node_id}")
            candidate_node.kill()
        
        # Adiciona um novo nó dinamicamente
        if random.random() < 0.05:  # 5% de chance de adicionar um novo nó
            num_nodes += 1
            new_node = Node(num_nodes)
            logger.info(f"ATIVAÇÃO ALEATÓRIA: Nó {new_node.node_id}")
            nodes.append(new_node)
            new_node.activate(nodes)

def main():
    try:
        num_nodes = 5

        # Lista auxiliar para iterar e controlar na função principal
        nodes = [Node(i) for i in range(1, num_nodes + 1)]
        
        # Atribuir manualmente a lista inicial para cada nó
        for node in nodes:
            node.activate(nodes)

        # Iniciar manualmente a eleição do líder pelo primeiro nó
        nodes[0].elect_leader()

        # Desativa o líder
        for node in nodes:
            if node.leader == node:
                node.kill()
                nodes.remove(node) # Remove o nó da lista auxiliar
        
        # Adiciona um novo nó dinamicamente
        num_nodes += 1
        new_node = Node(num_nodes)
        nodes.append(new_node)
        new_node.activate(nodes)

        # Executa a simulação de comunicação e falhas
        run_simulation(nodes, num_nodes)
    except KeyboardInterrupt:
        logger.info("Simulação interrompida pelo usuário.")
    except Exception as e:
        logger.error(f"Erro na simulação: {e}")
    finally:
        logger.info(f"Fim da simulação. Nós restantes:")
        for node in nodes:
            logger.info(f"Nó {node.node_id}")

if __name__ == '__main__':
    main()