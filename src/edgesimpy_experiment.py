import sys
import os
from edge_sim_py import Simulator, Service, EdgeServer, User

# We need to make sure EdgeSimPy can find our local dataset
DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sample_dataset2.json"))

# This is our policy injection point
def semantic_policy(parameters):
    # EdgeSimPy calls this function automatically at every step
    # We will put our logic here later
    pass

def run_edgesimpy_experiment():
    print(f"Loading dataset from: {DATASET_PATH}")
    
    # 1. Setup the stopping criterion (how long to simulate)
    # Let's simulate for 300 ticks (each tick is 1 second)
    def stopping_criterion(model):
        return model.schedule.steps >= 300
    
    # 2. Create the Simulator instance
    simulator = Simulator(
        tick_duration=1,
        tick_unit="seconds",
        stopping_criterion=stopping_criterion,
        resource_management_algorithm=semantic_policy, # Plugging in our function
    )

    # 3. Load the real dataset
    simulator.initialize(input_file=DATASET_PATH)

    # 4. Run the model
    print("Starting EdgeSimPy simulation...")
    simulator.run_model()

    # 5. Inspect the final state
    print("\n--- Simulation Finished ---")
    print(f"Total Edge Servers: {len(EdgeServer.all())}")
    print(f"Total Services: {len(Service.all())}")
    
    # Check where services ended up
    for service in Service.all():
        server_id = service.server.id if service.server else "None"
        print(f"Service {service.id} is hosted on EdgeServer {server_id}")

if __name__ == "__main__":
    run_edgesimpy_experiment()