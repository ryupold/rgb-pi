
class PiGPIO_Mock(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def pi():
        return PiGPIO_Mock()

    def set_PWM_dutycycle(self, pin, value):
        pass







