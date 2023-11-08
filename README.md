# Monte Carlo Tree Search
An implementation of MCTS used to play connect four.

## Usage
1. ``pip3 install -r requirements.txt``
2. python3 main.py

## Parameters
- ```iterations``` The number of times the tree is searched before a move is made
- ```initial_probability``` The initial probability of choosing a node
- ```selection_depth``` The depth of nodes generated during the selection step
- ```search_rollouts``` The number of rollouts performed during search 
- ```minimax_rollouts``` The number of rollouts performed for the purpose of giving each leaf a value of 1 or -1 for minimax