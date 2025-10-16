import numpy as np
import random
from scipy.spatial import distance

class WaterDistributionMDP:
    def __init__(self, num_tankers, total_water, demands, sources, num_houses_per_tanker):
        self.num_tankers = num_tankers
        self.total_water = total_water
        self.demands = demands
        self.sources = sources
        self.num_houses_per_tanker = num_houses_per_tanker

    def get_initial_state(self):
        # Initial state: all tankers have equal water distribution
        return np.array([self.total_water / self.num_tankers] * self.num_tankers)

    def get_transition_probabilities(self, state, action):
        # In this simple example, assume transitions are deterministic
        # and the action directly changes the state (e.g., transferring water)
        return None

    def apply_action(self, state, action):
        # Apply the action to the current state and return the new state
        i, j = action
        new_state = state.copy()
        transfer_amount = min(new_state[i], self.demands[j])  # Transfer amount limited by demand and available water

        # Ensure that the sender retains at least 10% of the water it had
        min_retained_amount = 0.1 * state[i]
        transfer_amount = max(transfer_amount, min_retained_amount)

        new_state[i] -= transfer_amount
        new_state[j] += transfer_amount
        return new_state

    def run_policy(self, policy, num_people_in_house, max_iterations=100):
        state = self.get_initial_state()
        total_water_given = {f"House {i+1}": 0 for i in range(sum(self.demands))}
        for _ in range(max_iterations):
            action = policy(state)
            if action is None:
                continue
            state = self.apply_action(state, action)
            for i, demand in enumerate(self.demands):
                house_start_index = sum(self.demands[:i])
                house_end_index = house_start_index + demand
                water_given = min(state[i], num_people_in_house[house_start_index:house_end_index])
                total_water_given[f"House {i+1}"] += water_given
        return total_water_given

# Randomly generate inputs within the specified ranges
num_sources = random.randint(1, 3)
num_tankers_per_source = random.randint(1, 4)
num_houses_per_tanker = [random.randint(1, 5) for _ in range(num_tankers_per_source)]
total_water = random.randint(100, 1000)

# Calculate total number of tankers
num_tankers = num_sources * num_tankers_per_source

# Generate number of houses and number of people in each house
num_houses = sum(num_houses_per_tanker)
num_people_in_house = [random.randint(1, 5) for _ in range(num_houses)]

# Generate demands of tankers based on the number of people falling under each tanker
total_people = sum(num_people_in_house)
demands = [int(total_water * (num_people / total_people)) for num_people in num_people_in_house]

# Generate random locations for sources and tankers
sources = np.random.rand(num_sources, 2) * 100
tankers = np.random.rand(num_tankers, 2) * 100

# Print the generated inputs
print("Randomly Generated Inputs:")
print("Number of Sources:", num_sources)
print("Number of Tankers per Source:", num_tankers_per_source)
print("Number of Houses per Tanker:", num_houses_per_tanker)
print("Total Water Available:", total_water)
print("Demands of Tankers (in Litres):", demands)
print("Number of Houses:", num_houses)
print("Number of People in Each House:", num_people_in_house)

# Define a function to find the nearest source for each tanker
def find_nearest_source(tanker, sources):
    distances = [distance.euclidean(tanker, source) for source in sources]
    nearest_source_idx = np.argmin(distances)
    return nearest_source_idx

# Create and run the MDP
mdp = WaterDistributionMDP(num_tankers, total_water, demands, sources, num_houses_per_tanker)

# Define a simple policy: transfer water from nearest source to each tanker
def simple_policy(state):
    actions = [(i, find_nearest_source(tanker, sources)) for i, tanker in enumerate(tankers)]
    return actions

# Run the policy
total_water_given = mdp.run_policy(simple_policy, num_people_in_house)

# Print the demand of each tanker
print("\nDemand of Each Tanker:")
for i, demand in enumerate(demands):
    print(f"Tanker {i+1}: {demand} litres")

# Print the water given to each house
print("\nWater Distribution to Houses:")
for house, water_given in total_water_given.items():
    print(f"{house} received {water_given} litres of water.")
