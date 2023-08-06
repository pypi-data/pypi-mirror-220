from enum import Enum
import numpy as np
from PythonCoordinates.measurables.physical_quantities import Length, Angle, Speed, Temperature, Humidity, Pressure
from PythonCoordinates.coordinates.coordinate_representations import SphericalCoordinate


class AircraftType(Enum):
    Military = 0, 'Military'
    Civilian = 1, 'Civilan'


class DataCollectionType(Enum):
    Measured = 0, 'Measured'
    Estimated = 1, 'Estimated'


class InterpolationCode(Enum):
    Fixed = 0, 'Fixed'
    Parallel = 1, 'Parallel'
    Variable = 2, 'Variable'


class NoiseFilePowerSetting:
    def __init__(self):
        self.value = 0.0
        self.units = ''
        self.upper_limit = 0.0
        self.lower_limit = 0.0


class NoiseFileAcousticSource:

    def __init__(self, filename=None):
        super().__init__()
        # in the C# code this is an observable collection. Not sure why...
        self._power_settings = []

        self._vehicle_type = None
        self._interpolation_code = None
        self._data_collection_type = None
        self._microphone_count = None
        self._directivity_angle = None
        self._perceived_noise_level = None
        self._tone_corrected_perceived_noise_level = None
        self._la = None
        self._lat = None
        self._effective_perceived_noise_level = None
        self._sound_exposure_level = None
        self._tone_corrected_sound_exposure_level = None
        self._tone_correction = None
        self._id = None
        self._operational_power_code = None
        self._operational_type_code = None
        self._engine_name = None
        self._engine_count = None
        self._drag_configuration = None
        self._source = None
        self._collection_date = None
        self._reference_distance = None
        self._reference_speed = None
        self._reference_temperature = None
        self._reference_humidity = None
        self._power_setting_description = None
        self._sound_pressure_levels = []
        self._frequency_resolution = 3
        self._minimum_frequency_band = 10
        self._maximum_frequency_band = 40

        if filename is not None:
            self.filename = filename
            f = open(self.filename)
            contents = f.readlines()
            f.close()
            self.load_data(contents, 0)

    @staticmethod
    def source_type():
        return 'FLIGHT'

    @property
    def frequency_resolution(self):
        return self._frequency_resolution

    @property
    def minimum_frequency_band(self):
        return self._minimum_frequency_band

    @property
    def maximum_frequency_band(self):
        return self._maximum_frequency_band

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @property
    def interpolation_code(self):
        return self._interpolation_code

    @property
    def data_collection_type(self):
        return self._data_collection_type

    @property
    def number_microphone_in_average(self):
        return self._microphone_count

    @property
    def directivity_angle(self):
        return self._directivity_angle

    @property
    def perceived_noise_level(self):
        return self._perceived_noise_level

    @property
    def tone_corrected_pnl(self):
        return self._tone_corrected_perceived_noise_level

    @property
    def a_weighted_level(self):
        return self._la

    @property
    def tone_corrected_a_weighted_level(self):
        return self._lat

    @property
    def sound_exposure_level(self):
        return self._sound_exposure_level

    @property
    def tone_corrected_sel(self):
        return self._tone_corrected_sound_exposure_level

    @property
    def effective_perceived_noise_level(self):
        return self._effective_perceived_noise_level

    @property
    def tone_correction(self):
        return self._tone_correction

    @property
    def aircraft_id(self):
        return self._id

    @property
    def operational_power_code(self):
        return self._operational_power_code

    @property
    def operational_type_code(self):
        return self._operational_type_code

    @property
    def engine_name(self):
        return self._engine_name

    @property
    def engine_count(self):
        return self._engine_count

    @property
    def drag_configuration(self):
        return self._drag_configuration

    @property
    def source(self):
        return self._source

    @property
    def collection_date(self):
        return self._collection_date

    @property
    def reference_distance(self):
        return self._reference_distance

    @property
    def reference_speed(self):
        return self._reference_speed

    @property
    def reference_temperature(self):
        return self._reference_temperature

    @property
    def reference_humidity(self):
        return self._reference_humidity

    @property
    def power_setting_description(self):
        return self._power_setting_description

    @property
    def power_settings(self):
        return self._power_settings

    def calculate_sound_pressure_levels(self, band, elevation, polar):
        index = band - 10
        spls = np.zeros((len(elevation),))
        for i in range(0, len(elevation), 1):
            spls[i] = self._sound_pressure_levels[index]

        return spls

    def sound_pressure_level(self, location_or_elevation, polar=None):
        return self._sound_pressure_levels

    def write_data(self, file):
        if self.vehicle_type == AircraftType.Military:
            record1 = 'MILITARY FM{:5d}{:2d}{:1d}'.format(self.aircraft_id, self.operational_power_code,
                                                          self.operational_type_code)
        else:
            record1 = 'CIVILIAN FC{:5d}{:2d}{:1d}'.format(self.aircraft_id, self.operational_power_code,
                                                          self.operational_type_code)

        if self.interpolation_code == InterpolationCode.Fixed:
            record1 = record1 + 'F'
        elif self.interpolation_code == InterpolationCode.Parallel:
            record1 = record1 + 'P'
        elif self.interpolation_code == InterpolationCode.Variable:
            record1 = record1 + 'V'
        other1 = '{:<20}{:<20}{:>2} {:<25}'.format(self.name, self.engine_name, self.engine_count,
                                                   self.drag_configuration)
        if self.data_collection_type == DataCollectionType.Measured:
            other2 = 'MEASURED  '
        else:
            other2 = 'ESTIMATED '
        other1 = other1 + other2
        record2 = '{}{:<12}{:>11}{:>5} FT{:>5} KTS  {:>3} F  {:>3} PCT'.format(
            other1, self.source, self.collection_date, int(self.reference_distance.feet),
            int(self.reference_speed.knots), int(self.reference_temperature.fahrenheit),
            int(self.reference_humidity.percentage))
        record3 = '{:<20}'.format(self.power_setting_description)
        for setting in self.power_settings:
            record3 = record3 + '{:>9} {:<10} {:>9}{:>9}'.format('{:.2f}'.format(setting.value), setting.units,
                                                                 '{:.2f}'.format(setting.lower_limit),
                                                                 '{:.2f}'.format(setting.upper_limit))

        record4 = '{:>4}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}'.format(self.number_microphone_in_average,
                                                                              self.directivity_angle.degrees,
                                                                              self.perceived_noise_level,
                                                                              self.tone_corrected_pnl,
                                                                              self.a_weighted_level,
                                                                              self.tone_corrected_a_weighted_level,
                                                                              self.effective_perceived_noise_level,
                                                                              self.sound_exposure_level,
                                                                              self.tone_corrected_sel,
                                                                              self.tone_correction)

        record5 = ''
        for level in self._sound_pressure_levels:
            record5 = record5 + '{:>4}'.format(int(level * 10))

        file.write(record1 + '\n')
        file.write(record2 + '\n')
        file.write(record3 + '\n')
        file.write(record4 + '\n')
        file.write(record5 + '\n')

    def load_data(self, contents, start_index):
        record1 = contents[start_index].rstrip()
        start_index += 1
        record2 = contents[start_index].rstrip()
        start_index += 1
        record3 = contents[start_index].rstrip()
        start_index += 1
        record4 = contents[start_index].rstrip()
        start_index += 1
        record5 = contents[start_index].rstrip()
        start_index += 1
        try:
            if record1[0:8] == 'MILITARY':
                self._vehicle_type = AircraftType.Military
            else:
                self._vehicle_type = AircraftType.Civilian
            self._id = int(record1[11:16])
            self._operational_power_code = int(record1[16:18])
            self._operational_type_code = int(record1[18:19])
            interp_code = record1[19:20]
            if interp_code == 'F':
                self._interpolation_code = InterpolationCode.Fixed
            elif interp_code == 'P':
                self._interpolation_code = InterpolationCode.Parallel
            elif interp_code == 'V':
                self._interpolation_code = InterpolationCode.Variable
            self.name = record2[0:20].strip()
            self._engine_name = record2[20:40].strip()
            self._engine_count = int(record2[40:42])
            self._drag_configuration = record2[43:43 + 25].strip()
            if record2[68:78].strip() == 'MEASURED':
                self._data_collection_type = DataCollectionType.Measured
            else:
                self._data_collection_type = DataCollectionType.Estimated
            self._source = record2[78:78 + 12].strip()
            self._collection_date = record2[90:90 + 11]
            self._reference_distance = Length(float(record2[101:101 + 5]), Length.Units.Feet)
            self._reference_speed = Speed(float(record2[109:109 + 5]), Speed.Units.Knots)
            self._reference_temperature = Temperature(float(record2[120:120 + 3]), Temperature.Units.Fahrenheit)
            self._reference_humidity = Humidity(float(record2[127:127 + 3]), Humidity.Units.Percentage)
            if len(record3) > 0:
                self._power_setting_description = record3[0:20].strip()
                record3 = record3[20:]
                while len(record3) > 0:
                    temp = NoiseFilePowerSetting()
                    temp.value = float(record3[0:9].strip())
                    temp.units = record3[10:10 + 10].strip()
                    temp.lower_limit = float(record3[20:20 + 9].strip())
                    temp.upper_limit = float(record3[30:30 + 9].strip())
                    self._power_settings.append(temp)
                    record3 = record3[39:]
            self._microphone_count = int(record4[0:4].strip())
            self._directivity_angle = Angle(float(record4[4:4 + 6].strip()))
            self._perceived_noise_level = float(record4[10:10 + 6].strip())
            self._tone_corrected_perceived_noise_level = float(record4[16:16 + 6].strip())
            self._la = float(record4[22:22 + 6].strip())
            self._lat = float(record4[28:28 + 6].strip())
            self._effective_perceived_noise_level = float(record4[34:34 + 6].strip())
            self._sound_exposure_level = float(record4[40:40 + 6].strip())
            self._tone_corrected_sound_exposure_level = float(record4[46:46 + 6].strip())
            self._tone_correction = float(record4[52:52 + 6].strip())

            for index in range(0, len(record5), 4):
                self._sound_pressure_levels.append(float(record5[index:index + 4].strip()) / 10.0)
        except Exception as e:
            raise ValueError('An error ocurred in the NOISEFILE formatted file at index = ' + str(
                start_index) + ' - error message: ' + str(e))
        return start_index


class NoiseFileStaticAcousticSource(NoiseFileAcousticSource):
    def __init__(self, filename=None):
        self.noise_suppression_system = ''
        self._reference_pressure = Pressure()

        if filename is None:
            super().__init__()
            self.polar_sound_pressure_levels = {}
        else:
            self.filename = filename
            self._power_settings = []
            self.polar_sound_pressure_levels = {}
            with open(filename, 'r') as file:
                contents = file.readlines()
                self._load_data(contents, 0)

    @property
    def measurement_count(self):
        return self.polar_sound_pressure_levels.shape[0]

    @property
    def reference_pressure(self):
        return self._reference_pressure

    def _load_data(self, contents, start_index):
        record1 = contents[start_index].rstrip()
        start_index += 1
        try:
            #   Record or line 1
            if record1[0:8] == 'MILITARY':
                self._vehicle_type = AircraftType.Military
            else:
                self._vehicle_type = AircraftType.Civilian
            self._id = int(record1[11:11 + 5])
            self._operational_power_code = int(record1[16:16 + 2])
            interpolation_code = record1[18:18 + 1]
            if interpolation_code == 'F':
                self._interpolation_code = InterpolationCode.Fixed
            elif interpolation_code == 'P':
                self._interpolation_code = InterpolationCode.Parallel
            elif interpolation_code == 'V':
                self._interpolation_code = InterpolationCode.Variable

            #   Record 2
            record2 = contents[start_index].rstrip()
            start_index += 1
            self.name = record2[0:20].strip()
            self._engine_name = record2[20:20 + 20].strip()
            self.noise_suppression_system = record2[40:40 + 14].strip()
            self._engine_count = int(record2[54:54 + 2])
            if 'MEASURED' in record2[57:57 + 10]:
                self._data_collection_type = DataCollectionType.Measured
            else:
                self._data_collection_type = DataCollectionType.Estimated
            self._source = record2[67:67 + 12].strip()
            self._collection_date = record2[79:79 + 11]

            #   Record 3
            record3 = contents[start_index].rstrip()
            start_index += 1
            self._power_setting_description = record3[0:20].strip()
            for i in range(0, 3, 1):
                substring = record3[20 + (i * 20): 20 + (i * 20) + 21]
                try:
                    power_setting_value = float(substring[0:9])
                    power_setting_units = substring[10:10 + 10].strip()
                    power_setting = NoiseFilePowerSetting()
                    power_setting.value = power_setting_value
                    power_setting.units = power_setting_units
                    self.power_settings.append(power_setting)
                except Exception as ee:
                    print('FAILURE: {}'.format(str(ee)))
                    break

            self._reference_distance = Length(float(record3[80:80 + 5]), Length.Units.Feet)
            self._reference_speed = Speed()
            self._reference_temperature = Temperature(float(record3[89:89 + 3]), Temperature.Units.Fahrenheit)
            self._reference_pressure = Pressure(float(record3[103:103 + 6]), Pressure.Units.InchesMercury)
            self._reference_humidity = Humidity(float(record3[95:95 + 3]))

            self.polar_sound_pressure_levels = np.zeros((19, 31))
            start_index += 1
            for band_index in range(10, 41, 1):
                data_record = contents[start_index].rstrip()
                start_index += 1
                temp_elements = data_record.split(' ')
                elements = [x for x in temp_elements if x != '']
                n = 1
                for angle_index in range(19):
                    self.polar_sound_pressure_levels[angle_index, band_index - 10] = float(elements[n]) / 10.0
                    n += 1
        except Exception as ee:
            raise ValueError('{} occurred in the NOISEFILE file at index = {}'.format(str(ee), start_index))
        return start_index

    def write_data(self, writer):
        if self.vehicle_type == AircraftType.Military:
            record = 'MILITARY FM{:5d}{:2d}'.format(self.aircraft_id, self.operational_power_code)
        else:
            record = 'CIVILIAN FC{:5d}{:2d}'.format(self.aircraft_id, self.operational_power_code)

        if self.interpolation_code == InterpolationCode.Fixed:
            record = record + 'F'
        elif self.interpolation_code == InterpolationCode.Parallel:
            record = record + 'P'
        elif self.interpolation_code == InterpolationCode.Variable:
            record = record + 'V'
        writer.write(record + '\n')

        record = '{:<20}{:<20}{:<14}{:>2} '.format(self.name, self.engine_name, self.noise_suppression_system,
                                                   self.engine_count)
        if self.data_collection_type == DataCollectionType.Measured:
            record = record + 'MEASURED  '
        else:
            record = record + 'ESTIMATED '

        record = record + '{:<12}{:>11} Single Engine Data'.format(self.source, self.collection_date)

        writer.write(record + '\n')
        record = '{:<20}'.format(self.power_setting_description)
        for setting in self.power_settings:
            record = record + '{:>9} {:<10}'.format('{:.2f}'.format(setting.value), setting.units)
        while len(record) < 80:
            record = record + ' '

        record = record + '{:>5} FT {:>3} F {:>3} PCT {:>6} IN HG'.format(int(self.reference_distance.feet),
                                                                          int(self.reference_temperature.fahrenheit),
                                                                          int(self.reference_humidity.percentage),
                                                                          self.reference_pressure.inches_mercury)
        writer.write(record + '\n')
        record = ' BAND  '
        for angle in range(0, 181, 10):
            record = record + '{:>5}'.format(angle)
        writer.write(record + '\n')

        for band_index in range(10, 41, 1):
            record = '  {:>2}   '.format(band_index)
            for angle_key in range(19):
                record = record + '{:>5}'.format(int(self.polar_sound_pressure_levels[angle_key, band_index - 10] * 10))

            writer.write(record + '\n')

    def sound_pressure_level(self, coord_or_polar, azimuthal=None) -> list:
        if isinstance(coord_or_polar, SphericalCoordinate):
            return self.__sound_pressure_level__(coord_or_polar.azimuthal)
        elif isinstance(coord_or_polar, Angle) and azimuthal is not None:
            return self.__sound_pressure_level__(azimuthal)
        else:
            raise ValueError("You must use the PythonCoordinates module to define the location on the source")

    def __sound_pressure_level__(self, polar) -> list:
        if isinstance(polar, Angle):
            angle = polar.normalized.degrees
            if angle > 180:
                angle = 360 - angle
            degree_angle_key = int(np.floor(angle / 10))
            return self.polar_sound_pressure_levels[degree_angle_key]
        else:
            raise ValueError("You must use the PythonCoordinates module to define the location on the source")


class FlightNoiseFileDatabase:
    def __init__(self, filename):
        """
        This constructor will load the entire noise database from the flight01.dat file that is passed to the 
        constructor
        :param filename: str - the path to the NOISEFILE database which we want to load 
        """
        self.filename = filename
        self.sources = []
        with open(filename, 'r') as f:
            contents = f.readlines()
        line_index = 0
        while line_index < len(contents):
            src_data = NoiseFileAcousticSource()
            try:
                line_index = src_data.load_data(contents, line_index)
            except Exception as eee:
                raise ValueError('An incorrect formatted NOISEFILE entry found at index {}: {}'.format(
                    line_index, str(eee)))
            self.sources.append(src_data)


class GroundNoiseFileDatabase:
    def __init__(self, path):
        """
        This will read a file with multiple NOISEFILE_Static_AcousticSource definition in a single file and place the
        elements into an internal array
        """

        self.filename = path
        self.sources = []

        with open(self.filename, 'rt') as f:
            contents = f.readlines()

        line_index = 0

        while line_index < len(contents):
            src_data = NoiseFileStaticAcousticSource()
            try:
                line_index = src_data.load_data(contents, line_index)
            except Exception as eee:
                raise ValueError("An incorrect formatted NOISEFILE entry found at index {}: {}".format(
                    line_index, str(eee)
                ))

            self.sources.append(src_data)
