from datetime import datetime


class Dummy:
    def __init__(self, bias:float):
        self.__bias: float = bias
        self.__baseline: float = 1/3

    @property
    def bias(self):
        return self.__bias

    @property
    def baseline(self):
        return self.__baseline

    @baseline.setter
    def baseline(self, value:float):
        self.__baseline = value

    def multiply(self, multiplier: float) -> float:
        result = multiplier*self.__baseline + self.__bias
        return round(result, 3)

    def current_date_time(self) -> str:
        now = datetime.now()
        return now.strftime("%H:%M:%S %d/%m/%y")



if __name__ == '__main__':
    dummy = Dummy(1.0)
    print(dummy.bias)

    print(dummy.baseline)
    dummy.baseline = 5.0
    print(dummy.baseline)

    multiplied = dummy.multiply(8977.7897)
    print(multiplied)

    current = dummy.current_date_time()
    print(current)
