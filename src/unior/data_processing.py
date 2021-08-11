from .filters import BSF50, LPF5, HPF01

class BreathProcessor:
    def __init__(self):
        self.bsf = BSF50()
        self.lpf = LPF5()
        self.hpf = HPF01()
        self.counter = -1

    def process(self, input: float) -> float:
        if self.counter == 0:
            self.hpf.init(input * 10)
        self.counter += 1

        input = self.lpf.filter(self.hpf.filter(self.bsf.filter(input * 10)))
        return input
