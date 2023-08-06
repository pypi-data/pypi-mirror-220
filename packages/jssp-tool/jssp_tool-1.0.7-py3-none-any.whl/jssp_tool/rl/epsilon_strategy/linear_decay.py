class LinearDecay:
    def __init__(self, start_epsilon, end_epsilon, decay_steps):
        self.start_epsilon = start_epsilon
        self.end_epsilon = end_epsilon
        self.decay_steps = decay_steps
        self.epsilon = start_epsilon

    def update_epsilon(self, t):
        if t > self.decay_steps:
            self.epsilon = self.end_epsilon
        else:
            epsilon_diff = self.end_epsilon - self.start_epsilon
            self.epsilon = self.start_epsilon + epsilon_diff * (t / self.decay_steps)
