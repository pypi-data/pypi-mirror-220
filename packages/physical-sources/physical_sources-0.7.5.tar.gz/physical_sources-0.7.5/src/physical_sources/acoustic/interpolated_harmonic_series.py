import xml.etree.ElementTree
from .harmonic_series_representation import HarmonicSeries, HarmonicSpectrumNoiseSource


class InterpolatedHarmonicSpectrumNoiseSource:
    """
    We understand the data collected at Owens-Corning can construct a surface for the acoustic emissions on the surface
    of a sphere.  The Static_NoiseSource class represents a single engine power value for the definition of the source.
    This provides the user with the interface to determine the source description at specific engine power settings.

    20220330 - FSM - Added properties to average the reference conditions across the low and high power settings
    """

    def __init__(self, filename: str = None):
        """
        This constructs the source definition for the interpolated static source description of the acoustic emissions
        for SUAS.
        :param filename: str - the path to the file that contains the definition
        """

        self.definitions = list()
        self._low_power = None
        self._high_power = None
        self._max_power = None
        self._name = None
        self.desired_power_setting = None
        self.SOURCE_DESCRIPTION_ERROR = "The low and high power settings must be HarmonicNoiseSource"

        if filename is None:
            return

        self.filename = filename

        tree = xml.etree.ElementTree.ElementTree()
        tree.parse(filename)

        #   Get the parameters for the definition from the root's attributes

        root = tree.getroot()

        self._low_power = float(root.attrib['lo_definition'])
        self._high_power = float(root.attrib['hi_definition'])
        self._max_power = float(root.attrib['max_definition'])
        self._name = root.attrib['name']
        self.desired_power_setting = self._low_power

        for defs in root[0]:
            self.definitions.append(HarmonicSpectrumNoiseSource(defs))

    @property
    def source_name(self):
        return self._name

    @source_name.setter
    def source_name(self, value):
        self._name = value

    @property
    def low_power_setting(self):
        return self.low_power_description.aircraft_power_setting

    @property
    def high_power_setting(self):
        return self.high_power_description.aircraft_power_setting

    @property
    def maximum_power_setting(self):
        return self.maximum_power_description.aircraft_power_setting

    @property
    def low_power_engine_parameter(self):
        return self._low_power

    @low_power_engine_parameter.setter
    def low_power_engine_parameter(self, value):
        self._low_power = value

    @property
    def hi_power_engine_parameter(self):
        return self._high_power

    @hi_power_engine_parameter.setter
    def hi_power_engine_parameter(self, value):
        self._high_power = value

    @property
    def max_power_engine_parameter(self):
        return self._max_power

    @max_power_engine_parameter.setter
    def max_power_engine_parameter(self, value):
        self._max_power = value

    @property
    def low_power_description(self):
        tmp = None

        for definition in self.definitions:
            if definition.aircraft_power_setting == self._low_power:
                tmp = definition
                break

        if tmp is not None:
            return tmp
        else:
            raise ValueError("The low power setting conditions could not be found in the collection of definitions")

    @property
    def high_power_description(self):
        tmp = None

        for definition in self.definitions:
            if definition.aircraft_power_setting == self._high_power:
                tmp = definition
                break

        if tmp is not None:
            return tmp
        else:
            raise ValueError("The high power setting conditions could not be found in the collection of definitions")

    @property
    def maximum_power_description(self):
        tmp = None

        for definition in self.definitions:
            if definition.aircraft_power_setting == self._max_power:
                tmp = definition
                break

        if tmp is not None:
            return tmp
        else:
            raise ValueError("The maximum power setting conditions could not be found in the collection of definitions")

    @property
    def static_definitions(self):
        return self.definitions

    @static_definitions.setter
    def static_definitions(self, value):
        self.definitions = value

    @property
    def desired_engine_power(self):
        return self.desired_power_setting

    @property
    def ref_temperature(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_temperature + self.high_power_description.ref_temperature) / 2

    @property
    def ref_pressure(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_pressure + self.high_power_description.ref_pressure) / 2

    @property
    def ref_humidity(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_humidity + self.high_power_description.ref_humidity) / 2

    @property
    def ref_distance(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_measurement_distance +
                self.high_power_description.ref_measurement_distance) / 2

    @desired_engine_power.setter
    def desired_engine_power(self, value):
        import warnings

        if value < self.low_power_setting:
            self.desired_power_setting = self.low_power_setting

            warnings.warn("The desired engine power setting was below the minimum within the definition.  The value "
                          "was reset to the lowest value in the definition")
        elif value > self.maximum_power_setting:
            self.desired_power_setting = self.maximum_power_setting

            warnings.warn("The desired engine power setting was above the maximum within the definition.  The value "
                          "was reset to the maximum value in the definition")
        elif (value > self.high_power_setting) and (value < self.maximum_power_setting):
            self.desired_power_setting = self.maximum_power_setting

            warnings.warn("The value was above the interpolation range for this aircraft definition.  The source "
                          "description used will be the maximum definition.")
        else:
            self.desired_power_setting = value

    def predict(self, location):
        """
        This function calculates the sound pressure level at a specific location and returns the entire spectrum
        :param location: SphericalCoordinate
            it is either the specific location on the surface as defined in Cartesian or spherical coordinates or the
            azimuthal angle
        :return: double, array-like
            the sound pressure level @ all frequencies within the definition
        """
        import numpy as np

        if self.desired_power_setting > self.high_power_setting:
            return self.maximum_power_description.predict(location)
        else:
            #   Determine the weighting function or the two coefficients
            lo_definition = self.low_power_description
            hi_definition = self.high_power_description

            w_lo = 1 + (self.desired_power_setting - lo_definition.aircraft_power_setting) / \
                   (lo_definition.aircraft_power_setting - hi_definition.aircraft_power_setting)
            w_hi = 1 - w_lo

            #   Determine the locations for the determination of the harmonic coefficient matrix
            spl = np.zeros((len(self.definitions[0].series_coefficients), 1))

            for i in range(len(spl)):
                #   Build the matrix that we will use to determine the real values after creating the interpolated
                #   coefficients.
                b = HarmonicSeries.harmonic_matrix(
                    self.low_power_description.series_coefficients[i].order,
                    azimuthal=location.azimuthal,
                    polar=location.polar)

                #   Use the weights to determine the linear combination of the coefficients
                c_lo = self.low_power_description.series_coefficients[i]
                c_hi = self.high_power_description.series_coefficients[i]

                c = w_lo * c_lo.coefficients + w_hi * c_hi.coefficients

                spl[i] = (b.dot(c))[0].real

        return spl

    def save(self, filename: str):
        """
        This function creates the source file description using the information within the class.  It uses the functions
        from the static source to build the tree for the individual definitions.

        :param filename: string - the path to write the output
        """

        root = xml.etree.ElementTree.Element("interpolated_harmonic_series_definition")

        #   Build the interpolated source definition tree
        root.set("name", self.source_name)
        root.set("lo_definition", str(self.low_power_engine_parameter))
        root.set("hi_definition", str(self.hi_power_engine_parameter))
        if self._max_power is not None:
            root.set("max_definition", str(self._max_power))
        else:
            root.set("max_definition", str(self.hi_power_engine_parameter))

        definition_set = xml.etree.ElementTree.SubElement(root, "definitions")
        for definition in self.definitions:
            definition_set.append(self.definitions[i].m)

        #   Set the root of the tree and write the structure to the output file

        tree._setroot(interp_src)

        print(tree)
        tree.write(filename, encoding="UTF-8", xml_declaration=True)