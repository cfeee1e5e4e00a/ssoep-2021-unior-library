maxNumberOfCoefficients = 16

class IIRFilterBase:
    def __init__(self):
        self.number_of_coefficients = 0
        self.input_values = [0] * (maxNumberOfCoefficients + 1)
        self.output_values = [0] * (maxNumberOfCoefficients + 1)
        self.input_coeffs = [0] * maxNumberOfCoefficients
        self.output_coeffs = [0] * maxNumberOfCoefficients
        self.FGain = 0

    def filter(self, input_value: float) -> float:
        for i in range(self.number_of_coefficients):
            self.input_values[i] = self.input_values[i + 1]
            self.output_values[i] = self.output_values[i+1]
        result = input_value * self.FGain
        self.input_values[self.number_of_coefficients] = result
        for i in range(self.number_of_coefficients):
            result = result + self.input_values[i] * self.input_coeffs[i] + self.output_values[i] * self.output_coeffs[i]

        self.output_values[self.number_of_coefficients] = result
        return result


class BSF50(IIRFilterBase):
    def __init__(self):
        super().__init__()
        self.number_of_coefficients = 4
        self.FGain = 8.37089190566345E-001
        self.input_coeffs = [
            1.00000000000000E+000,
            -1.24589220970327E+000,
            2.38806184954982E+000,
            -1.24589220970327E+000
        ]
        self.output_coeffs = [
            -7.00896781188402E-001,
            9.49760308799785E-001,
            -1.97230236060631E+000,
            1.13608549390706E+000
        ]

class LPF5(IIRFilterBase):
    def __init__(self):
        super().__init__()
        self.number_of_coefficients = 2
        self.FGain = 3.62168151492862E-003
        self.input_coeffs = [
            1.00000000000000E+000,
            2.00000000000000E+000
        ]
        self.output_coeffs = [
            -8.37181651256023E-001,
            1.82269492519631E+000
        ]

class HPF01(IIRFilterBase):
    def __init__(self):
        super().__init__()
        self.number_of_coefficients = 1
        self.FGain = 9.98744939433549E-001
        self.input_coeffs = [
            -1.00000000000000E+000
        ]
        self.output_coeffs = [
            9.97489878867098E-001
        ]

    def init(self, start: float):
        self.input_values[0] = start * self.FGain
        self.input_values[1] = start * self.FGain
