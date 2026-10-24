# This class stores the episodes, all the states that come in between the initial state and the terminal state. 
# This is later used by the agent for learning by experience, called "exploration". 

import numpy as np
import tensorflow as tf
from collections import deque

class GameExperience(object):
    
    # model = neural network model
    # max_memory = number of episodes to keep in memory. The oldest episode is deleted to make room for a new episode.
    # discount = discount factor; determines the importance of future rewards vs. immediate rewards
###STORES TRANSITIONS IN REPLAY MEMORY 
    def __init__(self, model, target_model, max_memory=100, discount=0.95):
        self.model = model
        self.target_model = target_model
        self.max_memory = max_memory
        self.discount = discount
        self.memory = deque(maxlen = max_memory)
        self.num_actions = model.output_shape[-1]
    
    # Stores episodes in memory
    
    def remember(self, episode):
        """
        Store one experience in replay memory.
        When the buffer reaches max_memory, deque automatically
        removes the oldest experience.
        """

        if not isinstance(episode, (list, tuple)):
            raise TypeError(
                "Episode must be a list or tuple."
            )

        if len(episode) != 5:
            raise ValueError(
                "Episode must contain exactly five values: " \
                "state, action, reward, next_state, done."
            )

        state, action, reward, next_state, done = episode

        #Validate action
        if not isinstance(action, (int, np.integer)):
            raise TypeError(
                "Action must be an integer."
            )

        if not 0 <= action < self.num_actions:
            raise ValueError(
                f"Action must be between 0 and {self.num_actions - 1}."
            )

        #Validate reward.
        if not isinstance(reward, (int, float, np.number)):
            raise TypeError(
                "Reward must be a number."
            )
        #Validate terminal flag.
        if not isinstance(done, (bool, np.bool_)):
            raise TypeError(
                "Done must be a Boolean value."
            )

        #Validate arrays
        state = np.asarray(state, dtype = np.float32)
        next_state = np.asarray(next_state, dtype = np.float32)

        if state.size == 0 or next_state.size == 0:
            raise ValueError(
                "State and next_state cannot be empty."
            )

        if state.shape != next_state.shape:
            raise ValueError(
                "State and next_state must have matching shapes."
            )

        validated_episode = (
            state,
            int(action),
            float(reward),
            next_state,
            bool(done)
        )

        self.memory.append(validated_episode)


###PREDICTS Q-VALUES
    # Predicts the next action based on the current environment state        
    def predict(self, envstate):
        envstate = np.asarray(envstate, dtype=np.float32)
        if envstate.ndim == 1:
          envstate = np.expand_dims(envstate, axis=0)
        return self.model(envstate, training=False).numpy()[0]
###RANDOMLY SAMPLES EXPERIENCES
    def sample(self, batch_size=32):
      """
      Randomly sample a batch of episodes from memory.
      """

      if batch_size <= 0:
          raise ValueError(
              "batch_size must be greater than zero."
          )

      if len(self.memory) == 0:
          raise ValueError(
              "Cannot sample from an empty replay buffer."
          )

      memory_list = list(self.memory)

      idx = np.random.choice(
          len(memory_list),
          size = batch_size,
          replace = (len(memory_list) < batch_size)
      )

      return [memory_list[i] for i in idx]

    
    def get_data(self, batch_size=32):
        """
        Generate training inputs and targets from memory.
        Prepares one batch for custom train_step() method.
        """
        if self.model is None or self.target_model is None:
            raise ValueError(
                "Both `model` and `target_model` must be provided"
            )

        if not isinstance(batch_size, int):
            raise TypeError(
                "batch_size must be an integer."
            )

        if batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than zero."
            )

        if len(self.memory) == 0:
            raise ValueError(
                "Replay memory is empty."
            )

        batch = self.sample(batch_size)

        first_state = np.asarray(
            batch[0][0],
            dtype = np.float32
        )

        if first_state.ndim == 1:
            env_size = first_state.shape[0]
        elif first_state.ndim == 2 and first_state.shape[0] == 1:
            env_size = first_state.shape[1]
        else:
            raise ValueError(
                "State must be a flat vector or a signle-row vector."
            )
        

        inputs = np.zeros(
            (batch_size, env_size), 
            dtype=np.float32
        )

        targets = np.zeros(
            (batch_size, self.num_actions), 
            dtype=np.float32
        )

        # Stack states for batched prediction
        states = np.vstack([
            np.asarray(item[0], dtype = np.float32).reshape(1, -1)
            for item in batch
        ])

        next_states = np.vstack([
            np.asarray(item[3], dtype = np.float32).reshape(1, -1)
            for item in batch
        ])

        if states.shape[1] != env_size:
            raise ValueError(
                "All states must have the same size."
            )

        if next_state.shape != states.shape:
            raise ValueError(
                "State and next_state batches must have matching shapes."
            )

        q_values = self.model(
            states, 
            training=False).numpy()
        
        q_next = self.target_model(
            next_states, 
            training=False).numpy()

        for i, (
            state, 
            action, 
            reward, 
            next_state, 
            done
        ) in enumerate(batch):
            inputs[i] = np.asarray(
                state,
                dtype = np.float32
            ).reshape(-1)

            targets[i] = q_values[i]

            if done:
                targets[i, action] = reward

            else:
                targets[i, action] = (
                    reward + self.discount * np.max(q_next[i])
                )

        return inputs, targets