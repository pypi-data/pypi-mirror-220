import abc


class ISphereSource:
    """
    This class represents a single value on the surface of a sphere. The methods here are abstracted and must be
    implemented in any child class.
    """

    def __init__(self):
        """
        This is a generic constructor. It only creates the instances of the object's private or protected properties.
        """

        self._description = None

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @staticmethod
    @abc.abstractmethod
    def fit(x, y, order: int):
        """
        This function will determine the internal representation of the grid
        :param x:
            This is a doubly dimensioned array that represents the azimuthal and polar angles from the
        :param y:
        :param order:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def predict(self, location):
        """
        This will determine the value on the surface of the sphere at the specific location, or series of locations.
        :param location:
            This is either a collection (array or list) of locations or a SphericalCoordinate. If it is a list, it is
            expected that the list contains a collection of SphericalCoordinate objects.
        :return:
            The single value, or collection of values evaluated at the locations in the argument.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def parse_xml(root):
        """
        This function will parse the
        :param root:
        :return:
        """
        raise NotImplementedError

