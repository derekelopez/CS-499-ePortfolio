

\# Enhancement Two: Algorithms and Data Structures



\## Pirate Intelligent Agent — A\* Pathfinding and Deep Q-Learning



\### Project Overview



This project originated in CS-370: Current and Emerging Trends in Computer Science at Southern New Hampshire University.



The original project involved developing a pirate intelligent agent capable of navigating a maze to locate treasure using deep reinforcement learning.



The application uses a maze environment, a reinforcement-learning experience mechanism, and a Deep Q-Network (DQN) to evaluate possible movement decisions.



For the CS-499 Computer Science Capstone, I enhanced the original application by improving maze validation and reward handling, introducing A\* pathfinding, and quantitatively comparing the two approaches.



\## Original Artifact



The original implementation consisted of:



\- `TreasureMaze.py` — Maze environment and movement rules.

\- `GameExperience.py` — Reinforcement-learning experience replay.

\- `Lopez\_Derek\_TreasureHuntGame\_starterCode.ipynb` — DQN training and evaluation notebook.

\- `requirements.txt` — Python dependencies.



The original implementation provided a foundation for reinforcement learning but contained opportunities to improve invalid-move handling, input validation, and algorithmic evaluation.



\## Algorithm and Data Structure Enhancements



\### 1. Maze Environment Improvements



The enhanced `TreasureMaze.py` addresses several logic and reliability issues.



Improvements include:



\- Correcting movement-state handling to distinguish valid and invalid movements.

\- Evaluating invalid-move penalties before previously visited-cell penalties.

\- Providing fallback handling for unexpected maze states.

\- Validating maze dimensions and input values during construction.

\- Improving code organization and readability.



These changes make the environment more predictable and reduce unexpected behavior.



\### 2. A\* Pathfinding Implementation



I implemented an A\* pathfinding algorithm in `astar.py`.



A\* searches for a path to a defined goal by evaluating the combined cost of reaching a node and estimating the remaining distance.



The evaluation function is:



f(n) = g(n) + h(n)



Where:



\- g(n) represents the known path cost from the starting position to node n.

\- h(n) represents the heuristic estimate of the remaining distance to the goal.

\- f(n) represents the estimated total path cost.



The implementation uses the Manhattan-distance heuristic:



h(n) = |x\_goal - x\_n| + |y\_goal - y\_n|



This heuristic is appropriate for a grid environment with horizontal and vertical movement and uniform movement costs.



\### A\* Data Structures



The implementation uses several data structures:



| Data Structure | Purpose |

|---|---|

| Priority queue (`heapq`) | Selects the next candidate position |

| Dictionary of path costs | Maintains the best known cost to reach positions |

| Parent dictionary | Reconstructs the resulting path |

| Explored-position tracking | Records search progress and avoids unnecessary processing |



\### A\* Algorithm Pseudocode



&#x20;   function A\_STAR(maze, start, goal):

&#x20;       open\_set = priority queue

&#x20;       insert start with priority heuristic(start, goal)



&#x20;       g\_score\[start] = 0

&#x20;       parent\[start] = null



&#x20;       while open\_set is not empty:

&#x20;           current = remove lowest-priority node



&#x20;           if current == goal:

&#x20;               return reconstruct\_path(parent, goal)



&#x20;           for each valid neighbor of current:

&#x20;               tentative\_cost = g\_score\[current] + movement\_cost



&#x20;               if tentative\_cost < g\_score\[neighbor]:

&#x20;                   g\_score\[neighbor] = tentative\_cost

&#x20;                   parent\[neighbor] = current



&#x20;                   priority = tentative\_cost + heuristic(neighbor, goal)

&#x20;                   insert neighbor into open\_set



&#x20;       return no\_path\_found



This pseudocode summarizes the search logic rather than reproducing every implementation detail.



\### Computational Complexity



For a graph with V vertices and E edges, a heap-based shortest-path search can have a time-complexity bound of O((V + E) log V) when the priority queue maintains an appropriate number of entries.



For the grid maze, the number of traversable cells determines V, while valid movements between adjacent cells determine E.



The practical execution cost depends on the maze configuration, heuristic effectiveness, and implementation details.



The algorithm also requires memory to maintain candidate nodes, path costs, explored positions, and parent relationships.



Consequently, its auxiliary space requirement grows with the number of reachable states.



\## 3. DQN Evaluation



The existing Deep Q-Network uses reinforcement learning to learn movement decisions through training experiences.



Unlike A\*, which performs an explicit search using the known maze structure, DQN attempts to learn a movement policy based on training rewards.



DQN may be useful when the objective is to learn behavior from repeated experience, but its performance depends on training configuration, model architecture, exploration strategy, and reward design.



For this enhancement, I retained the DQN implementation to provide a comparison with the deterministic A\* approach.



\## 4. Benchmark Results



The enhanced project was evaluated using an 8×8 maze with 50 valid starting positions.



| Metric | A\* | DQN |

|---|---|---|

| Evaluation starts | 50 | 50 |

| Successful starts | 50 | 1 |

| Success rate | 100% | 2% |

| Average successful path length | 15.64 moves | 1.00 move |

| Training requirement | None | Up to 1,000 training epochs in the recorded run |



A\* successfully located a path from every evaluated starting position.



DQN solved one of the 50 evaluated starting positions under the recorded training configuration.



The 1.00-move average for DQN applies only to its single successful starting position and should not be interpreted as superior pathfinding efficiency.



These findings demonstrate that A\* was more reliable for the tested deterministic maze environment.



However, the results do not establish that A\* is universally superior to DQN. Additional DQN training, hyperparameter tuning, or different environments could produce different results.



\## 5. Design Decisions and Trade-Offs



\### A\* Advantages



\- Produces paths using explicit search rather than a training process.

\- Uses a heuristic to prioritize promising positions.

\- Supports predictable evaluation for a known maze.

\- Provides interpretable paths and search results.



\### A\* Limitations



\- Requires access to the maze structure and available movement information.

\- Maintains search-state information in memory.

\- May require repeated searches if the environment changes.



\### DQN Advantages



\- Supports learning policies through repeated experience.

\- Can potentially generalize across states encountered during training.

\- Provides a foundation for more advanced intelligent-agent research.



\### DQN Limitations



\- Requires training and computational resources.

\- Is sensitive to reward design and hyperparameters.

\- May fail to learn a reliable policy under limited training.

\- Does not inherently guarantee shortest-path solutions.



For the evaluated maze, A\* was the more reliable solution under the tested conditions.



\## 6. Testing and Verification



The following project components were verified during development:



\- TreasureMaze environment functionality.

\- GameExperience replay functionality.

\- DQN model creation.

\- DQN training execution.

\- Notebook completion checks.

\- DQN evaluation.

\- A\* pathfinding benchmark.



The enhanced notebook contains the evaluation workflow, and `astar.py` contains the search implementation.



\## 7. Security and Reliability Considerations



The enhanced maze constructor validates the shape and permitted values of the maze input.



Unexpected states and invalid movements are handled explicitly, reducing the risk of incorrect behavior caused by malformed input or inconsistent state transitions.



The project is an educational research prototype rather than a security-hardened production service.



Additional safeguards would be needed when loading untrusted model files, accepting externally supplied maze data, or deploying the agent in a larger application.



\## 8. CS-499 Course Outcomes



\### Collaboration and Decision-Making



The project uses clearer code organization and documented evaluation results to support technical reviews and informed algorithm selection.



\### Professional Communication



The README, source code, notebooks, and benchmark comparison communicate design decisions and results to technical audiences.



\### Algorithmic Design and Evaluation



The project demonstrates heuristic search, reinforcement learning, path reconstruction, computational complexity, and trade-off analysis.



\### Computing Techniques and Tools



Python, TensorFlow, Jupyter Notebook, NumPy, and heap-based search techniques support the implementation and evaluation of intelligent agents.



\### Security Mindset



Maze input validation, defensive state handling, and consideration of untrusted input improve the reliability of the enhanced application.



\## 9. Project Files



\### Original Artifact



\- \[Original TreasureMaze.py](Original/TreasureMaze.py)

\- \[Original GameExperience.py](Original/GameExperience.py)

\- \[Original Jupyter notebook](Original/Lopez\_Derek\_TreasureHuntGame\_starterCode.ipynb)

\- \[Original requirements](Original/requirements.txt)



\### Enhanced Artifact



\- \[A\* pathfinding implementation](Enhanced/astar.py)

\- \[Enhanced TreasureMaze.py](Enhanced/TreasureMaze.py)

\- \[Enhanced GameExperience.py](Enhanced/GameExperience.py)

\- \[Enhanced Jupyter notebook](Enhanced/Lopez\_Derek\_TreasureHuntGame\_Enhanced.ipynb)

\- \[Saved DQN model](Enhanced/dqn\_pirate\_agent\_1000.keras)

\- \[Enhanced requirements](Enhanced/requirements.txt)



\## 10. Conclusion



Enhancement Two demonstrates the application of algorithmic principles to a practical computing problem.



By improving maze-state handling, introducing A\* pathfinding, and comparing it with an existing DQN agent, I evaluated alternative approaches using measurable evidence.



This enhancement strengthened my experience with algorithm design, data structures, computational complexity, testing, and engineering trade-offs.



