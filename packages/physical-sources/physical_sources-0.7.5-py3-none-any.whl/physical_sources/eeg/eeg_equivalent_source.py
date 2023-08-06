import mne
import numpy as np
from pytimbre.waveform import Waveform
from PythonCoordinates.coordinates.coordinate_representations import CartesianCoordinate, SphericalCoordinate
from PythonCoordinates.measurables.physical_quantities import Length, Angle


class EEGEquivalentSource:
    """
    This class represents a conversion of the measured levels in the Electroencephalogram (EEG) files that are
    compatible with the MNE project. It will create a series of source levels at the scalp and fit this with a series
    of harmonic functions.
    """

    def __init__(self, filename: str):
        """
        This function loads the data from the file using the MNE module. A series of Waveform objects will be created
        to facilitate manipulation of the signals within PyTimbre.

        Parameters
        ----------

        :param filename: str
            The full path to the file that we are interested in loading.
        """

        self._eeg_data = None

        self._load_eeg_file(filename)

    def _load_eeg_file(self, filename: str):
        """
        This function will load the data from the binary file and create a series of Waveform objects that will be
        stored in the class.

        Parameters
        ----------

        :param filename: str
            The path to the file that we will load into the interface
        """

        #   Read the file
        self._eeg_data = mne.io.read_raw_edf(filename, preload=True, verbose=0)

        #   Set the reference of the EEG to the mastoids and apply a window to the data
        self._eeg_data.set_eeg_reference(['M1', 'M2'])
        self._eeg_data.filter(1., 40., fir_design='firwin')

    @staticmethod
    def raw_cartesian_location(electrode_index: int = 0, system_name: str = "biosemi64"):
        """
        Using the index of the electrode, query the system and determine the location of the electrode and return
        the location in the CartesianCoordinate object.

        Parameters
        ----------
        :param electrode_index: int
            The index within the system of the cap that we want to query
        :param system_name: str
            The name of the system that exists within the definition of the systems within MNE.
        :return: CartesianCoordinate
            The location from the montage within the MNE module
        """

        #   Get the montage based on the system name - this is an internal representation of the data
        montage = mne.channels.make_standard_montage(system_name)
        location = montage.dig[electrode_index]['r']

        #   Create the location information for the electrode
        return CartesianCoordinate(Length(location[0]),
                                   Length(location[1]),
                                   Length(location[2]))

    @staticmethod
    def electrode_name(electrode_index: int = 0, system_name: str = "biosemi64"):
        """
        This will query the montage within the system and provide the name of the electrode that is queried.

        Parameters
        ----------
         :param electrode_index: int
            The index within the system of the cap that we want to query
        :param system_name: str
            The name of the system that exists within the definition of the systems within MNE.
        :return: str
            The name of the electrode with the selected index
        """

        return mne.channels.make_standard_montage(system_name).ch_names[electrode_index]

    @property
    def sample_rate(self):
        return self._eeg_data.info["sfreq"]

    @property
    def time_data(self, channel_index: int = 0):
        return self._eeg_data._data[channel_index, :]

    @property
    def duration(self):
        return self._eeg_data.tmax

    def get_waveform(self, electrode_index: int = 0, t0: float = 10, t1: int = None) -> Waveform:
        """
        This will extract the information from the electrode within the file that was loaded and return the temporal
        data as a waveform.

        Parameters
        ----------
        :param electrode_index:
            The index within the data for the channel that we want to extract - see raw_cartesian_location and
            electrode_name
        :param t0:
            The start time of the waveform to obtain from the file
        :param t1:
            The end time of the waveform
        :return:
            A Waveform object that we can manipulate with PyTimbre
        """

        #   Get the samples that we need to extract based on the time window
        s0 = int(np.floor(t0 * self.sample_rate))

        #  Set the end sample
        if t1 is not None:
            s1 = int(np.floor(t1 * self.sample_rate))
        else:
            s1 = self._eeg_data.last_samp

        samples = self._eeg_data._data[electrode_index, s0:s1]

        return Waveform(samples, self.sample_rate, 0)










