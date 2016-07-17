import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.Q = []
        self.statesList = []
        self.previousQstate = None 
        self.oldreward = None
        self.gamma = .8
        # TODO: Initialize any additional variables here

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t): ##new3
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        
        # TODO: Update state
        stateForq = str(inputs['state']['destination'][0]- inputs['state']['location'][0])+str(inputs['state']['destination'][1]- inputs['state']['location'][1])+str(inputs['state']['heading'])

        # TODO: Select action according to your policy
        action = random.choice([None, 'forward', 'left', 'right'])

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        if self.previousQstate is not None:
            maxQ = 0
            for val in self.Q:
                if val[0] == stateForq and val[2] > maxQ:
                    maxQ = val[2]

            newQ = self.oldreward+ self.gamma*maxQ

            self.Q.append([self.previousQstate, action, newQ])
            

        self.previousQstate = stateForq
        self.oldreward = reward

        print self.Q, '\n'
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        #print 'Q = {}\nlength  = {}\n'.format(self.Q[:][:][:],len(self.Q) if len(self.Q) else 'noneEE')
        #wait = input('press a key to continue ')

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
