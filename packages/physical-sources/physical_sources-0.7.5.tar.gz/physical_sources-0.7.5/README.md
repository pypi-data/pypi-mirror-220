# ![Image](./GhostEye.png "GhostEye") physical_sources

This is a collection of classes meant to provide access to acoustic source levels that were contained within the initial
release of the Counter Listener Acoustic Warfare Software (CLAWS). But with the changes to the releasibility of the code
and data from CLAWS, a number of classes were removed from the distribution. 

## NOISEFILE
The _NOISEFILE_ representation of the various aircraft is retained, since these source descriptions are deemed unclassified
and publically available through the various community noise releases. These data come as the static, ground-based measurements
that define the semicircular data from the nose to the tail, on the left side of the aircraft. The second set of data exists
within the flight database. This data is a collection of single spectra that were integrated as the __loudest__ portion of the
over-flight data. As such, it provides an over-estimate at the majority of the locations around the aircraft.

These datasets exist in a single library file, that can be loaded and then searched for the specific aircraft/power setting
combination that is desired. Each element within the library exists as its own class that can be extracted and then saved
externally as another file. These files can then be loaded without consideration for the remainder of the acoustic data.

### Usage - Loading Flight NOISEFILE data extracted from the library previously
    filename = str(Path(__file__).parents[3]) + "/_test data/physical_sources/acoustic_source/approach power.nf"
    nfas = NoiseFileAcousticSource(filename)
    s = SphericalCoordinate()

    spl1 = nfas._sound_pressure_levels
    spl2 = nfas.sound_pressure_level(s)