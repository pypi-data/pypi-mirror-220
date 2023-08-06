import signal8

env = signal8.env()
env.reset(options={'problem_instance': 'corners'})
start_state = env.state()
observation, _, terminations, truncations, _ = env.last()
env.step(2)
observation, _, _, _, _ = env.last()
env.close()
