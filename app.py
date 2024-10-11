from flask import Flask, jsonify, render_template  
from threading import Thread  
import time  
import random  
  
app = Flask(__name__, static_folder='static')  
  
class AIAgent(Thread):  
    def __init__(self, agent_id, total_agents):  
        super().__init__()  
        self.agent_id = agent_id  
        self.status = 'Initializing'  
        self.data = {}  
        self.current_task = 'Starting up...'  
        self.alive = True  
        self.total_agents = total_agents  
        self.messages = []  
        self.logic_steps = [  
            'Initializing parameters',  
            'Loading data',  
            'Preprocessing data',  
            'Training model',  
            'Evaluating model',  
            'Optimizing hyperparameters',  
            'Generating report',  
            'Idle',  
        ]  
  
    def run(self):  
        while self.alive:  
            # Simulate agent activity  
            self.status = 'Working'  
            self.current_task = random.choice(self.logic_steps)  
            self.data['value'] = random.random()  
  
            # Simulate sending a message to another agent  
            if random.random() < 0.5:  # 50% chance to send a message  
                recipient_id = random.choice([i for i in range(self.total_agents) if i != self.agent_id])  
  
                # Generate meaningful message content based on current task and include current time
                current_time = time.strftime("%H:%M:%S", time.localtime())
                
                message_types = ['Info', 'Warning', 'Error', 'Debug']  
                message_type = random.choice(message_types)  
                #message_content = f"{message_type}: Agent {self.agent_id} is {self.current_task}"  
                message_content = f"Agent {self.agent_id} says at {current_time}: '{self.current_task}'"
  
                timestamp = time.time()  
                message = {  
                    'sender': self.agent_id,  
                    'recipient': recipient_id,  
                    'content': message_content,  
                    'timestamp': timestamp  
                }  
                # Send the message  
                agents[recipient_id].receive_message(message)  
                # Record message sent  
                self.messages.append(message)  
                # Keep only the last 5 messages  
                self.messages = self.messages[-5:]  
  
            time.sleep(random.uniform(1, 3))  
  
    def receive_message(self, message):  
        if not hasattr(self, 'received_messages'):  
            self.received_messages = []  
        self.received_messages.append(message)  
        # Keep only the last 5 messages  
        self.received_messages = self.received_messages[-5:]  
  
    def stop(self):  
        self.alive = False  
  
agents = {}  
  
def start_agents(num_agents):  
    for i in range(num_agents):  
        agent = AIAgent(agent_id=i, total_agents=num_agents)  
        agents[i] = agent  
        agent.start()  
  
start_agents(8)  # Start with 8 agents  
  
@app.route('/')  
def index():  
    return render_template('index.html')  
  
@app.route('/api/agents')  
def get_agents():  
    agents_data = []  
    for agent in agents.values():  
        agent_info = {  
            'agent_id': agent.agent_id,  
            'status': agent.status,  
            'current_task': agent.current_task,  
            'data': agent.data,  
            'messages': agent.messages[-5:],  
            'received_messages': getattr(agent, 'received_messages', [])[-5:],  
        }  
        agents_data.append(agent_info)  
    return jsonify(agents_data)  
  
if __name__ == '__main__':  
    try:  
        app.run(debug=True)  
    finally:  
        # Stop all agents on exit  
        for agent in agents.values():  
            agent.stop()  
        for agent in agents.values():  
            agent.join()  
