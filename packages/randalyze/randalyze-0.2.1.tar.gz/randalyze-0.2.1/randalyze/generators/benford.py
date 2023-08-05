from random import Random


class BenfordRandom(Random):
    """
    Random number generator whose output follows a Benford distribution.
    Derived from the standard Python random.Random class.

    https://docs.python.org/3.10/library/random.html
    """

    def __init__(self, seed=None, adjustments: int = 5):
        """

        :param seed:
        :param adjustments: The number of "adjustments" to make to every random number.
        """
        super().__init__(x=seed)
        self._adjustments = adjustments

    def random(self) -> float:
        result = 1

        for _ in range(self._adjustments):
            result *= super().random()

        return result
