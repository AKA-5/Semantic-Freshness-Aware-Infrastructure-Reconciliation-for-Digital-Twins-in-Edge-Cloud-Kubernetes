import sys
import os
from edge_sim_py import Simulator, Service, EdgeServer, User

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sample_dataset2.json"))

# Global reference to the simulator so our policy can read the clock
GLOBAL_SIMULATOR = None
SYNTHETIC_DEMAND = {}

SEMANTIC_STATE = {
    "evaluations": 0,
    "reconciliations": 0,
    "telemetry_interval": 5,
    "significance_threshold": 4.0,
    "confirmation_ticks": 3,
    "pending_confirmations": {}
}

import random

# This is a simple semantic policy that uses a synthetic "physical" state to determine when to migrate services between edge servers. It simulates demand changes and only triggers migrations when the demand change persists for a certain number of telemetry updates.
def semantic_policy(parameters):
    current_tick = GLOBAL_SIMULATOR.schedule.steps
    
    # Initialize synthetic demand for services if not exists
    for service in Service.all():
        if service.id not in SYNTHETIC_DEMAND:
            SYNTHETIC_DEMAND[service.id] = 5.0

    # 1. Initial Placement
    for service in Service.all():
        if service.server is None and not service.being_provisioned:
            for server in EdgeServer.all():
                if server.has_capacity_to_host(service=service):
                    print(f"[Tick {current_tick}] Placing Service {service.id} on Server {server.id}")
                    service.provision(target_server=server)
                    SEMANTIC_STATE["pending_confirmations"][service.id] = 0
                    break

    # 2. Update Synthetic "Physical" State (Random Walk)
    for service in Service.all():
        if service.server is not None:
            # Small drift
            SYNTHETIC_DEMAND[service.id] += random.gauss(0, 1.0)
            
            # Occasional sustained jump (to trigger our policy)
            if random.random() < 0.05: 
                SYNTHETIC_DEMAND[service.id] += 10.0
                
            # Keep it bounded
            SYNTHETIC_DEMAND[service.id] = max(1.0, min(50.0, SYNTHETIC_DEMAND[service.id]))

    # 3. Semantic Evaluation Gate (Only run every 5 ticks)
    if current_tick % SEMANTIC_STATE["telemetry_interval"] != 0:
        return
        
    SEMANTIC_STATE["evaluations"] += 1
    
    # 4. Evaluate and Reconcile
    for service in Service.all():
        if service.server is not None:
            # We use our synthetic demand instead of the static EdgeSimPy one
            current_demand = SYNTHETIC_DEMAND[service.id]
            
            if current_demand > 15.0: # Threshold for "significant change"
                SEMANTIC_STATE["pending_confirmations"][service.id] = SEMANTIC_STATE["pending_confirmations"].get(service.id, 0) + 1
            else:
                SEMANTIC_STATE["pending_confirmations"][service.id] = 0
                
            # If the change persists for 3 telemetry updates, RECONCILE!
            if SEMANTIC_STATE["pending_confirmations"][service.id] >= SEMANTIC_STATE["confirmation_ticks"]:
                SEMANTIC_STATE["reconciliations"] += 1
                SEMANTIC_STATE["pending_confirmations"][service.id] = 0
                
                # Reconcile (Migrate)
                for new_server in EdgeServer.all():
                    if new_server != service.server and new_server.has_capacity_to_host(service=service):
                        print(f"[Tick {current_tick}] Reconciling Service {service.id}: Migrating from Server {service.server.id} to Server {new_server.id}")
                        service.provision(target_server=new_server)
                        # Reset demand after migration
                        SYNTHETIC_DEMAND[service.id] = 5.0
                        break

def run_edgesimpy_experiment():
    global GLOBAL_SIMULATOR
    
    print(f"Loading dataset from: {DATASET_PATH}")
    
    def stopping_criterion(model):
        return model.schedule.steps >= 100 # 100 ticks for testing

    GLOBAL_SIMULATOR = Simulator(
        tick_duration=1,
        tick_unit="seconds",
        stopping_criterion=stopping_criterion,
        resource_management_algorithm=semantic_policy,
    )

    GLOBAL_SIMULATOR.initialize(input_file=DATASET_PATH)

    print("Starting EdgeSimPy simulation...")
    GLOBAL_SIMULATOR.run_model()

    print("\n--- Simulation Finished ---")
    print(f"Total Semantic Evaluations: {SEMANTIC_STATE['evaluations']}")
    print(f"Total Reconciliations (Migrations): {SEMANTIC_STATE['reconciliations']}")
    
    for service in Service.all():
        server_id = service.server.id if service.server else "None"
        print(f"Service {service.id} is hosted on EdgeServer {server_id}")

if __name__ == "__main__":
    run_edgesimpy_experiment()