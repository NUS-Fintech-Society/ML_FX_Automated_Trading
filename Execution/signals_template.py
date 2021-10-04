class SignalTemplate:
    execute = False ##Either True of False
    def __init__(self, instru, unit, tp, sl):
        self.instru = instru
        self.unit = unit
        self.tp = tp
        self.sl = sl
