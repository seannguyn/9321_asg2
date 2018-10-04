class Predictor(object):
    """docstring for Predictor."""
    def __init__(self, arg):
        super(Predictor, self).__init__()
        self.arg = arg

    def computePrice(room, bath, suburb):
        return [
            {"room":room, "bath": bath, "suburb": suburb, "price": "1 530 000"},
            {"room":room, "bath": bath, "suburb": "kew", "price": "1 530 000"},
            {"room":room, "bath": bath, "suburb": "sydney", "price": "1 530 000"},
            {"room":room, "bath": bath, "suburb": "balwyn", "price": "1 530 000"},
        ]
