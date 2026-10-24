# Enhancement Two — Testing Evidence

## Pirate Intelligent Agent

### Evaluation Configuration

- Maze size: 8 × 8
- Valid starting positions evaluated: 50
- Algorithms: A* and Deep Q-Network (DQN)
- Recorded DQN training budget: Up to 1,000 epochs

## Benchmark Results

| Metric | A* | DQN |
|---|---|---|
| Starting positions | 50 | 50 |
| Successful starts | 50 | 1 |
| Success rate | 100% | 2% |
| Average successful path length | 15.64 | 1.00 |

The DQN average successful path length is based on one
successful start and is not a representative measure
of overall pathfinding efficiency.

## Verification

Previously recorded notebook checks passed for:

- TreasureMaze functionality
- GameExperience functionality
- DQN model initialization
- DQN training
- Notebook completion checks
- DQN evaluation

## Supporting Files

- [A* implementation](../Enhanced/astar.py)
- [Enhanced notebook](../Enhanced/Lopez_Derek_TreasureHuntGame_Enhanced.ipynb)
- [Saved DQN model](../Enhanced/dqn_pirate_agent_1000.keras)

## Conclusion

For the recorded evaluation configuration, A* successfully
solved all 50 starting positions, while DQN solved one.

These results are specific to the evaluated maze and
training configuration.
