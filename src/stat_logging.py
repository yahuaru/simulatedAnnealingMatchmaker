from collections import defaultdict


class Logger:
    def __init__(self):
        super().__init__()
        self.iterations = []

    def cleanup(self):
        self.iterations = []

    def log_iteration(self, iteration, temperature, prob, total_energy, energy_difference, energy):
        iteration_data = {'iteration': iteration, 'temperature': temperature, 'probability': prob, "total_energy": total_energy, "energy_difference": energy_difference}
        iteration_data.update(energy)
        self.iterations.append(iteration_data)

stat_logging = Logger()