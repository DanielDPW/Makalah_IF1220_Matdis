import axelrod as axl
import random
import networkx as nx
import matplotlib.pyplot as plt

# Simulation parameters
THRESHOLD = 0  # Only allow matches if the weight is above this threshold
REBUILD_CHANCE = 0.05  # Chance to rebuild severed relationships
NUM_ROUNDS = 20  # Number of rounds in the simulation
NUM_TURNS = 20 # Number of turns each round between each player
USE_MORAN_PROCESS = True  # Toggle for Moran process
RANDOM_PLAYERS = True # Toggle for randomized player
PLAYER_COUNT = 10 # Player count for randomize player
INIT_WEIGHT = 100 # Initial weights of the edges

# Initialization

# List of strategies
strategies = [
    axl.Cooperator(),
    axl.Defector(),
    axl.TitForTat(),
    axl.Grudger(),
    axl.Random(),
    axl.Adaptive(),
    axl.AdaptiveTitForTat(),
    axl.Forgiver(),
    axl.ForgivingTitForTat(),
    axl.Bully(),
    axl.Grumpy(),
    axl.Punisher(),
    axl.Resurrection(),
    axl.Gradual(),
    axl.GradualKiller(),
    axl.CycleHunter(),
    axl.AntiTitForTat(),
    axl.Aggravater(),
    axl.HardTitForTat(),
    axl.HardGoByMajority(),
    axl.UsuallyCooperates(),
    axl.UsuallyDefects(),
    axl.SuspiciousTitForTat(),
    axl.WorseAndWorse(),
    axl.DoubleCrosser(),
    axl.Predator(),
    axl.Prober(),
    axl.NiceAverageCopier(),
    axl.CycleHunter(),
    axl.AntiCycler(),
    axl.EasyGo(),
    axl.OriginalGradual(),
    axl.Detective(),
    axl.NTitsForMTats(),
    axl.SneakyTitForTat(),
    axl.AverageCopier(),
    axl.WinStayLoseShift(),
    axl.WinShiftLoseStay()
]

# Define the players
if RANDOM_PLAYERS:
    players = [random.choice(strategies) for i in range(PLAYER_COUNT)] # Randomize players
else:
    players = [
        axl.Cooperator(), 
        axl.Defector(), 
        axl.Defector(), 
        axl.Cooperator(), 
        axl.Cooperator(), 
        axl.Defector(), 
        axl.Cooperator(), 
        axl.Cooperator(), 
        axl.Defector(), 
        axl.Defector()
    ]

# Initialize the relationship graph
relationship_graph = nx.Graph()
for i, player in enumerate(players, start=1):
    relationship_graph.add_node(f"Player_{i}")

# Initialize graph edges
for i in range(len(players)):
    for j in range(i + 1, len(players)):
        relationship_graph.add_edge(f"Player_{i+1}", f"Player_{j+1}", weight=INIT_WEIGHT)

# Payoff accumulator for each player
payoff_accumulator = {f"Player_{i+1}": 0 for i in range(len(players))}

def apply_thresholds(graph):
    # Sever relationship below the threshold

    edges_to_remove = [(u, v) for u, v, data in graph.edges(data=True) if data['weight'] <= THRESHOLD]
    graph.remove_edges_from(edges_to_remove)

def rebuild_relationships(graph, players, rebuild_chance=REBUILD_CHANCE):
    # Rebuild relationship based on random chances

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            if not graph.has_edge(f"Player_{i+1}", f"Player_{j+1}"):
                if random.random() < rebuild_chance:
                    graph.add_edge(f"Player_{i+1}", f"Player_{j+1}", weight=INIT_WEIGHT // 2)

def update_relationships(graph, i, j, relationship_change):
    # Update the relationship after each round

    current_weight = graph.get_edge_data(f"Player_{i+1}", f"Player_{j+1}", default={'weight': 0})['weight']
    graph.add_edge(f"Player_{i+1}", f"Player_{j+1}", weight=current_weight + relationship_change)

def moran_process(players, payoffs):
    # Evolve strategies using the Moran process

    total_payoff = sum(payoffs.values())
    if total_payoff == 0:
        return  # Avoid division by zero

    # Calculate selection probabilities based on payoffs
    selection_probs = [payoffs[f"Player_{i+1}"] / total_payoff for i in range(len(players))]

    # Select a player to reproduce based on probabilities
    reproducing_index = random.choices(range(len(players)), weights=selection_probs, k=1)[0]

    # Select a player to be replaced
    replaced_index = random.choice([i for i in range(len(players)) if i != reproducing_index])

    # Replace the strategy of the selected player
    players[replaced_index] = type(players[reproducing_index])() 

def play_matches(players, graph):
    # Play matches based on the relationship graph

    results = {}
    for i, player_a in enumerate(players):
        for j in range(i + 1, len(players)):
            if graph.has_edge(f"Player_{i+1}", f"Player_{j+1}"):
                match = axl.Match((player_a, players[j]), turns=NUM_TURNS)
                interactions = match.play()
                payoffs = axl.interaction_utils.compute_final_score(interactions)
                a_payoff, b_payoff = int(payoffs[0]), int(payoffs[1])
                results[(f"Player_{i+1}", f"Player_{j+1}")] = (interactions, (a_payoff, b_payoff))

                payoff_accumulator[f"Player_{i+1}"] += a_payoff
                payoff_accumulator[f"Player_{j+1}"] += b_payoff

                relationship_change = 0
                for action_a, action_b in interactions:
                    if action_a == axl.Action.C and action_b == axl.Action.C:
                        relationship_change += 1
                    elif (action_a == axl.Action.C and action_b == axl.Action.D) or \
                         (action_a == axl.Action.D and action_b == axl.Action.C):
                        relationship_change -= 1
                    elif action_a == axl.Action.D and action_b == axl.Action.D:
                        relationship_change -= 2

                update_relationships(graph, i, j, relationship_change)

    return results

def visualize_graph(graph):
    # Visualize the relationship graph

    pos = nx.kamada_kawai_layout(graph)
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weights, font_size=10)
    plt.show()

# Simulation loop
for round_number in range(NUM_ROUNDS):
    print(f"Round {round_number + 1}")

    # Play matches
    match_results = play_matches(players, relationship_graph)

    # Apply thresholds
    apply_thresholds(relationship_graph)

    # Rebuild relationships
    rebuild_relationships(relationship_graph, players, rebuild_chance=REBUILD_CHANCE)

    # Apply Moran process
    if USE_MORAN_PROCESS:
        moran_process(players, payoff_accumulator)

    # Print results after each round
    print(f"Total Payoffs and Strategies after Round {round_number + 1}:")
    for i, player in enumerate(players):
        strategy_name = type(player).__name__
        total_payoff = payoff_accumulator[f"Player_{i+1}"]
        print(f"Player_{i+1}: {total_payoff} (Strategy: {strategy_name})")

print("\nFinal Total Payoffs and Strategies after simulation:")
for i, player in enumerate(players):
    strategy_name = type(player).__name__
    total_payoff = payoff_accumulator[f"Player_{i+1}"]
    print(f"Player_{i+1}: {total_payoff} (Strategy: {strategy_name})")

visualize_graph(relationship_graph)
