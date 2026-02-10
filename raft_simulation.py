import asyncio
import random
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Set

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

@dataclass
class RaftNode:
    node_id: int
    peers: List[int]
    state: State = State.FOLLOWER
    current_term: int = 0
    voted_for: int = None
    votes_received: Set[int] = field(default_factory=set)
    election_timeout: float = field(default_factory=lambda: random.uniform(1.5, 3.0))
    last_heartbeat: float = field(default_factory=time.time)

    def __post_init__(self):
        self.reset_election_timeout()

    def reset_election_timeout(self):
        self.election_timeout = random.uniform(1.5, 3.0)
        self.last_heartbeat = time.time()
        print(f"  [Node {self.node_id}] Reset election timeout to {self.election_timeout:.2f}s")

    async def run(self):
        print(f"[Node {self.node_id}] Started as FOLLOWER (Term {self.current_term})")
        while True:
            if self.state == State.FOLLOWER:
                await self.follower_loop()
            elif self.state == State.CANDIDATE:
                await self.candidate_loop()
            elif self.state == State.LEADER:
                await self.leader_loop()
            await asyncio.sleep(0.1)

    async def follower_loop(self):
        if time.time() - self.last_heartbeat > self.election_timeout:
            print(f"[Node {self.node_id}] Election Timeout! Transitioning to CANDIDATE.")
            self.state = State.CANDIDATE
            self.current_term += 1
            self.voted_for = self.node_id
            self.votes_received = {self.node_id}
            self.reset_election_timeout()

    async def candidate_loop(self):
        print(f"[Node {self.node_id}] Campaigning for Term {self.current_term}...")
        # Simulate requesting votes from peers
        for peer in self.peers:
            await asyncio.sleep(random.uniform(0.01, 0.05))
            if random.random() > 0.2: # 80% chance to get a vote
                self.votes_received.add(peer)
        
        if len(self.votes_received) > (len(self.peers) + 1) // 2:
            print(f"[Node {self.node_id}] Elected LEADER for Term {self.current_term}!")
            self.state = State.LEADER
        else:
            print(f"[Node {self.node_id}] Election Failed. Reverting to FOLLOWER.")
            self.state = State.FOLLOWER
            self.voted_for = None
            self.reset_election_timeout()

    async def leader_loop(self):
        print(f"[Node {self.node_id}] Sending Heartbeat (Term {self.current_term})...")
        await asyncio.sleep(0.5)
        # Randomly crash leader for simulation
        if random.random() < 0.1:
            print(f"[Node {self.node_id}] CRASHED!")
            self.state = State.FOLLOWER
            self.voted_for = None
            self.reset_election_timeout()
            await asyncio.sleep(2) # Simulate recovery time

async def main():
    print("--- RAFT CONSENSUS SIMULATION (Leader Election) ---")
    nodes = [
        RaftNode(node_id=1, peers=[2, 3, 4, 5]),
        RaftNode(node_id=2, peers=[1, 3, 4, 5]),
        RaftNode(node_id=3, peers=[1, 2, 4, 5]),
        RaftNode(node_id=4, peers=[1, 2, 3, 5]),
        RaftNode(node_id=5, peers=[1, 2, 3, 4]),
    ]
    
    await asyncio.gather(*(node.run() for node in nodes))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
