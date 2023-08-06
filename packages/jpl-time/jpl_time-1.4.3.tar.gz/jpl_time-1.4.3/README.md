# jpl_time

jpl_time is a Python library which allows users to perform conversions and math with times and durations. The library can be imported into Python scripts or run as an executable. See the guides on the right panel for usage and installation.

## SpiceyPy
SpiceyPy is a Python wrapper of CSPICE which allows users to make SPICE calls directly from Python scripts. It gives the user a list of SPICE functions to perform conversions and calculations.

## Use of SpiceyPy in jpl_time
jpl_time imports SpiceyPy and uses it for all conversions involving SPICE. The purpose of jpl_time is to allow for the use of SPICE in object-oriented programming. jpl_time also adds many features not available in SPICE/SpiceyPy, such as conversions to all timezones, custom time formats, LMST/LTST conversions, rounding, comparisons, time and duration math, etc.

## NAIF documentation for time types
The NAIF website has several documents and pages which describe the basics of time conversion and representation. It is recommended that you familiarize yourself with these if you need to do anything beyond basic time math or conversions.
https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html

# Loading Kernels
SPICE kernels are files which SPICE uses to calculate positions and times. There are kernels for leap seconds, spacecraft position, spacecraft clocks conversions, and several others. These files will need to be loaded into SPICE before any Time objects are created using jpl_time, which is done by either loading kernels directly or by having jpl_time parse a CHRONOS config file.

## Default Chronos config import
By default when importing or running jpl_time, the library will run a function which checks environment variables described below to find the CHRONOS_SETUP file which is in the environment variables. If none is found then the error will be caught and you will need to load kernels yourself. The default behavior will also set the spacecraft ID and LMST SCLK ID. This should work by default for M2020, MSL, InSight, and any other mission where the CHRONOS_SETUP environment variable is set correctly. If you are running locally then you can create a Chronos config file (described below) and then run the following:
```
setenv CHRONOS_SETUP <path to chronos config file>
```

# Installing jpl_time
## First time installation
Install with pip or pip3, depending on whether you are using Python2 or Python3: (note that --user is not needed if you are using a virtual environment or have root permissions.
### Python3:
```
pip3 install jpl_time
```
### Python2:
```
pip install -U pip setuptools==38.0.0
pip install wheel==0.34.2
pip install numpy==1.16.4
pip install spiceypy==2.3.2
pip install jpl_time
```

## Updating version of jpl_time
To update the version of jpl_time being used, run pip again:
```
pip3 install jpl_time
```

## Installing jpl_time for use in Pycharm
To use a custom Python library in Pycharm as an import to another script, you will need to follow the same installation instructions as the normal installation, but pointing to the version of pip or pip3 corresponding to the project interpreter.

### Identify the project interpreter
This can be done by going into preferences in the project you are trying to import jpl_time into by hitting `⌘,` or clicking on the Pycharm dropdown. Next, click on project and then project interpreter. The drop down will give you the path to the version of Python being used.

### Install jpl_time for that version of Python
Next, on the terminal, do the following:
```
cd jpl_time
<path to project interpreter pip3>/pip3 install jpl_time For example:
/Users/forrestr/Documents/m2020/git_repos/surface/jpl_time/venv/pip3 install jpl_time
```


# Setting up the CLI Locally
In order to run jpl_time locally on a Mac, you will need to install it with pip or pip3, and then add the path to the bin directory where the executable was installed to your path. You will also need to create a chronos setup file.

After installing with pip3, you will see a message similar to this:
```
Successfully built jpl-time
Installing collected packages: jpl-time
  WARNING: The script jpl_time is installed in '/Users/<user>/Library/Python/3.7/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

To add to your path, add the following line to your `~/.bash_profile` file:
```
export PATH="<path listed in pip/pip3 installation>:${PATH}"
```

Next, create a chronos setup file somewhere on your computer. The name of the file does not matter.

Next, add the CHRONOS_SETUP environment variable to your .bash_profile file:
```
export CHRONOS_SETUP="<path to chronos setup file created>"
```

Next, either open a new terminal or source your .bash_profile file:
```
source ~/.bash_profile
```

You should now be able to run jpl_time anywhere on your laptop from the terminal by typing:
```
jpl_time
```

# Loading SPICE Kernels

## Downloading the latest NAIF kernels from the CLI
This feature is currently only available for InSight, MSL and M2020. Running `jpl_time -f <mission>` will grab the latest kernels from NAIF and then print the command needed to set the CHRONOS_SETUP environment variable. For example:
```
jpl_time -f msl
Progress: |██████████████████████████████████████████████████| 100.0%
Run the following command or add to your .cshrc/.bash_profile to automatically find the kernels:
shell: setenv CHRONOS_SETUP "/Users/forrestr/Documents/m2020/git_repos/surface/jpl_time/MSL/setup/chronos.msl"
bash:  export CHRONOS_SETUP="/Users/forrestr/Documents/m2020/git_repos/surface/jpl_time/MSL/setup/chronos.msl"
```

## Checking if latest kernels are being used from the CLI
This feature is currently only available for InSight, MSL and M2020. In order to check if you are using the latest kernels, you can run the following:
```
jpl_time -l
```

## Checking and downloading the latest kernels from a Python script
If you are importing jpl_time into a script then you can still check for the latest kernels and download new ones if needed. For example:
```
from jpl_time import Time, Duration, load_chronos_config, download_latest_kernels, check_for_latest_kernels
if check_for_latest_kernels(): # this returns a list of missing kernels, empty is good
    chronos_setup_path = download_latest_kernels('m2020')
    load_chronos_config(chronos_setup_path)
```

## Loading a CHRONOS config file
You can import the method called by jpl_time.py to locate and parse CHRONOS config files in your scripts. This is done by first importing the function:
```
from jpl_time import load_chronos_config
```
Next, call this method by either passing the path to a CHRONOS config file or without any arguments. If no arguments are given then it will look for a CHRONOS config file using environment variables. It looks for any environment variables which include CHRONOS_SETUP in their name.
```
load_chronos_config()
```

## Loading SPICE kernels directly
You can load SPICE kernels in your script by first importing the Time class and then calling the following method:
```
Time.load_kernels(kernel_list)
```
where the kernel_list is a list of paths to SPICE kernels. You can alternatively load an individual kernel by calling
```
Time.load_kernel(kernel)
```
There is also a method which will unload all current SPICE kernels and load new kernels:
```
Time.reload_kernels(kernel_list)
```
However, note that this will unload all kernels, which is not always desired.

## Creating a Chronos config file
A Chronos config file is a meta kernel which has a specific format. The important pieces of information are the kernel locations and the spacecraft NAIF ID. An example of this is below:
```
\begindata

   PATH_VALUES       = ('/Users/forrestr/Documents/m2020/git_repos/surface/jpl_time/test/inputs/')
   PATH_SYMBOLS      = ('KERNELS')
   KERNELS_TO_LOAD   = ('$KERNELS/nsyt_kernels_07112019/de430s.bsp',
                       '$KERNELS/nsyt_kernels_07112019/insight.tls',
                       '$KERNELS/nsyt_kernels_07112019/insight.tsc',
                       '$KERNELS/nsyt_kernels_07112019/insight_atls_ops181206_v1.bsp',
                       '$KERNELS/nsyt_kernels_07112019/insight_lmst_ops181206_v1.tsc',
                       '$KERNELS/nsyt_kernels_07112019/insight_ls_ops181206_iau2000_v1.bsp',
                       '$KERNELS/nsyt_kernels_07112019/insight_nom_2016e09o_cruise_v1.bsp',
                       '$KERNELS/nsyt_kernels_07112019/insight_nom_2016e09o_edl_v1.bsp',
                       '$KERNELS/nsyt_kernels_07112019/insight_surf_ops_v1.bc',
                       '$KERNELS/nsyt_kernels_07112019/insight_tp_ops181206_iau2000_v1.tf',
                       '$KERNELS/nsyt_kernels_07112019/insight_v05.tf',
                       '$KERNELS/common_kernels/mar097.bsp',
                       '$KERNELS/common_kernels/pck00010.tpc'
                       )

   SPACECRAFT_ID    = -189
\begintext
```

# Configuring for a Spacecraft

jpl_time.py supports multiple spacecraft by allowing users to specify through multiple methods the NAIF ID of their spacecraft. This can either be done by updating the default value or by passing it to each method.

## Default spacecraft ID
As mentioned in the importing SPICE page, jpl_time will automatically try to find the CHRONOS_SETUP file to import. The values in that file can be overridden by using the methods below, but it should default to the correct spacecraft if the CHRONOS_SETUP environment variables are set correctly.

## Updating the default values
### Surface missions
To update the default values of the spacecraft ID and LMST SCLK ID (Mars surface missions only), call the following method:
```
Time.set_spacecraft_id_and_lmst_id(-168)
```
Note that the NAIF spacecraft ID is always negative, and the LMST SCLK ID for Mars surface missions is the spacecraft ID followed by 900.

### Other missions
The LMST SCLK ID is not needed for orbiter missions, so you only need to call the following method:
```
Time.set_spacecraft_id(-168)
```

## Getting the spacecraft ID from a CHRONOS config file
The spacecraft ID can be obtained automatically from a CHRONOS config file

## Passing a Spacecraft ID to Time methods
If multiple spacecraft are being considered in a single script then updating the default value is not useful. However, only a few methods currently take the spacecraft ID as an argument, although this will be updated in the future. The conversion to ERT/ETT for multiple spacecraft currently needs to be done by using the downleg and upleg methods, which do have spacecraft ID as an argument. For use cases with only a single spacecraft you will be able to call to_ert(), to_ett(), etc. instead of using downleg and upleg.

# Time Class
# Creating Time objects
The jpl_time Time class is used to represent times as object. Time objects can be created by passing in a string, datetime.date object, datetime.datetime object, or by calling static methods which return a time object. The strptime method can be used to parse any format of time objects.

## Using the Time constructor
The most common way of creating Time objects is to use the constructor, which is done like this:
```
t1 = Time('2019-150T00:00:00')
t2 = Time('09/15/2019 12:34:56')
t3 = Time('Sol-250M00:00:00')

dt = datetime(2019, 9, 15)
t6 = Time(dt)
```
Under the hood, all of these times will be converted to a number of ephemeris seconds since the SPICE ET epoch representing the SCET time.

## Using static Time methods to create Time objects
For time formats other than UTC or LMST, such as SCLK, SCLKD, PT, etc., static methods of the Time class must be used to create time objects.
```
t1 = Time.from_sclk('1/0694267269-12059')
t2 = Time.from_sclkd(694267269.1840057)
t3 = Time.from_pt('2019-150T00:00:00')
t4 = Time.from_gps('2019-150T00:00:00')
t4 = Time.from_ert('2019-150T00:00:00')
t4 = Time.from_ett('2019-150T00:00:00')
t5 = Time.from_gps_seconds(1293494418)
t6 = Time.from_timezone('Asia/Kolkata')
t7 = Time.from_ltst('Sol-150T00:00:00')
t8 = Time.from_iso_week_day(2019, 30, 4)
```

## Creating time objects using strptime
The Time.strptime method can be used to parse custom formats of strings representing utc times. This wraps datetime.strptime, so the same format options apply. This can be used for even weird requirements, such as converting 2019wk43-1 to the date representing the monday of week 43 in year 2019. See this guide for all syntax options: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

# Conversions
Time objects can be converted to different formats by calling instance methods. Note that most to_x methods return either strings or floats.

## Basic Earth time conversions
```
t = Time('2020-002T00:00:00')

t.to_string() == '2020-002T00:00:00.000'
t.to_scet() == '2020-002T00:00:00.000'
t.to_utc() == '2020-002T00:00:00.000'
t.to_isoc() == '2020-01-02T00:00:00.000'
t.to_julian() == 'JD 2458850.500'
t.to_calendar() == '2020 JAN 02 00:00:00.000'

t.to_pt() == '2020-001T16:00:00.000'
t.to_indian_std_time() == '2020-002T05:30:00.000'
t.to_timezone('America/Adak') == '2020-001T14:00:00.000'

t.to_utc_strftime('%m/%d/%Y, %H:%M:%S') == '01/02/2020, 00:00:00'
```

## OWLT conversions
```
ert_time = Time.from_ert('2021-150T00:00:00')
ett_time = Time.from_ett('2021-150T00:00:00')

ert_time.to_scet() == '2021-149T23:41:23.208'
ert_time.to_ert() == '2021-150T00:00:00.000'

ett_time.to_scet() == '2021-150T00:18:36.728'
ett_time.to_ett() == '2021-150T00:00:00.000'

t = Time('2020-001T00:00:00')
owlt_earth_to_spacecraft = Time.upleg(t)
owlt_spacecraft_to_earth = Time.downleg(t)
```

## Mars time conversions
```
t = Time('2022-001T00:00:00')
t.to_lmst() == 'Sol-0308M02:59:38.698'
t.to_ltst() == 'Sol-0308T03:32:42'

format_string1 = 'Sol-{0:04d}M{1:02d}:{2:02d}:{3:06.3f}'
format_string2 = 'SOL {0:04d} {1:02d}:{2:02d}:{3:09.6f}'
t.to_lmst_strftime(format_string1) == 'Sol-0308M02:59:38.698'
t.to_lmst_strftime(format_string2) == 'SOL 0308 02:59:38.698040'
```
There are also additional convenience methods:
```
Time('Sol-150M11:55:00').to_lmst_am_pm() == 'AM'
Time('Sol-150M00:00:00').to_lmst_am_pm() == 'AM'
Time('Sol-150M11:59:59.999').to_lmst_am_pm() == 'AM'
Time('Sol-150M05:00:00.123').to_lmst_am_pm() == 'AM'

Time('Sol-150M23:55:00').to_lmst_am_pm() == 'PM'
Time('Sol-150M12:00:00').to_lmst_am_pm() == 'PM'
Time('Sol-150M23:59:59.999').to_lmst_am_pm() == 'PM'
Time('Sol-150M17:00:00.123').to_lmst_am_pm() == 'PM'
```

# Specifying number of decimal places to output
There are two ways to specify the number of decimals when outputting a string, updating the default value or by passing it as an argument to the to_x() methods.

## Updating the default decimal output
To update the default output for your script, call the set_output_decimal_precision method and pass a number of decimal places. A negative number can be passed to output only seconds, hours, etc. This value is used for most to_x methods, such as to_pt, to_utc, to_lmst, etc. Note that the times are rounded and not truncated. To truncate, you can call the floor method.
```
t = Time('Sol-0308M02:59:38.698')

# the default is 3
t.to_lmst() == 'Sol-0308M02:59:38.698'

Time.set_output_decimal_precision(-1)
t.to_lmst() == 'Sol-0308M02:59:40'

Time.set_output_decimal_precision(0)
t.to_lmst() == 'Sol-0308M02:59:39'

Time.set_output_decimal_precision(3)
t.to_lmst() == 'Sol-0308M02:59:38.698'

Time.set_output_decimal_precision(6)
t.to_lmst() == 'Sol-0308M02:59:38.698000'
```

## Passing the decimal places as an argument
```
t = Time('2022-001T00:00:00')
t.to_lmst() == 'Sol-0308M02:59:38.698'
t.to_lmst(0) == 'Sol-0308M02:59:39'
t.to_lmst(1) == 'Sol-0308M02:59:38.7'
t.to_lmst(2) == 'Sol-0308M02:59:38.70'
t.to_lmst(3) == 'Sol-0308M02:59:38.698'
```

# Rounding Time objects
There are instance methods which allow users to create a new time object which is rounded to an input duration. These methods are round, ceil, and floor. For example:
```
t1 = Time('2020-365T12:26:49.972')
t2 = Time('2020-366T12:30:00')
d1 = Duration('1T00:00:00')
d2 = Duration('01:00:00')
d3 = Duration('00:01:00')
d4 = Duration('00:00:01')

t1.round(d1) == Time('2020-366T00:00:00')
t1.round(d2) == Time('2020-365T12:00:00')
t1.round(d3) == Time('2020-365T12:27:00')
t1.round(d4) == Time('2020-365T12:26:50')
t2.round(d1) == Time('2021-001T00:00:00')
```

You can also round/ceil/floor LMST times. Note that the M in the duration string represents a mars duration.
```
lmst = Time('Sol-1234M12:34:56.123')
d1 = Duration('1M00:00:00')
d2 = Duration('M01:00:00')
d3 = Duration('M00:01:00')
d4 = Duration('M00:00:01')

lmst.round_lmst(d1) == Time('Sol-1235M00:00:00')
lmst.round_lmst(d2) == Time('Sol-1234M13:00:00')
lmst.floor_lmst(d3) == Time('Sol-1234M12:34:00')
lmst.ceil_lmst(d4) == Time('Sol-1234M12:34:57')
```

# Min and Max methods
The Python min and max methods return the minimum or maximum time in a list of times, based on the current default comparison precision. For example:
```
time_list = [
    Time('2022-001T00:00:00'),
    Time('2022-001T00:00:01'),
    Time('2022-002T00:00:00')
]

min(time_list) == Time('2022-001T00:00:00')
max(time_list) == Time('2022-002T00:00:00')
```

# Converting to/from hours since epoch
## Mars hours to/from Sol 0
```
Time('Sol-0010M00:00:00').to_fractional_sols() * 24 == 240.0
Time.from_fractional_sols(240 / 24) == Time('Sol-0010M00:00:00')
```

## Earth durations to/from Sol 0
```
(Time('Sol-0010M00:00:00') - Time('Sol-0000M00:00:00)).to_hours() == 246.598
Time('Sol-0000M00:00:00') + Duration(246.598 * 3600) == Time('Sol-0010M00:00:00')
```

## Earth duration from any epoch
```
t1 = Time('2020-001T00:00:00')
t2 = Time(2019-001T00:00:00')
d = t1 - t2
d.to_seconds() == 31536000.0
d.to_minutes() == 525600.0
d.to_hours() == 8760.0
d.to_days() == 365.0
```

# Duration Class
# Creating Duration objects

The jpl_time Duration class is used to represent durations as object. Duration objects can be created by passing in a string, float, int, or timedelta object, or by calling static methods which return a Duration object.

## Using the Duration constructor
All of the following are equivalent ways to make a duration object which represents 2 hours
```
d = Duration('02:00:00')
d = Duration('00:120:00')
d = Duration('00:00:7200')
d = Duration(7200)
d = Duration(datetime.timedelta(hours=2))
```
You can also create objects presenting mars durations by putting an M in front of the duration.
```
d = Duration('M02:00:00')
d = Duration('5M00:00:00')
```

## Conversions and string outputs
Durations can be converted to mars durations, timedeltas, seconds, or a string.
```
Duration(5.5).to_string() == '00:00:05.500'
Duration(-1).to_string() == '-00:00:01.000'
Duration(0).to_string() == '00:00:00.000'
Duration('0:1:0').to_string() == '00:01:00.000'
Duration('00:01:00').to_string() == '00:01:00.000'
Duration('0:1:0.0000').to_string() == '00:01:00.000'
Duration('5T00:00:01').to_string() == '5T00:00:01.000'
Duration('-01:00:00').to_string() == '-01:00:00.000'
Duration('50:00:00').to_string() == '2T02:00:00.000'

Duration(1).to_seconds() == 1
Duration('00:00:01').to_seconds() == 1
Duration('M00:00:01').to_seconds() == 1.0274912517

Duration('01:00:00').to_minutes() == 60
Duration('01:00:00').to_hours() == 1
Duration('01:00:00').to_days() == 1/24

Duration('1M00:00:00').to_mars_dur() == '1M00:00:00.000'
```

## Custom Formats
There are strfdelta and mars_strfdelta methods for custom duration formats. They use the following formatting:
```
strfdelta:
Input format string should match the standard python {} .format, with
        {0} = sign
        {1} = days
        {2} = hours
        {3} = minutes
        {4} = seconds (float)
d.strfdelta('{1:02d}T{2:02d}:{3:02d}:{4:06.3f}') = 03T04:05:06.789
d.strfdelta('{0}{1} days,{2} hours, :{3} minutes, :{4} seconds') = -3 days, 4 hours, 5 minutes, 6.789 seconds
```
```
mars_strfdelta:
Input format string should match the standard python {} .format, with
        {0} = sign
        {1} = sols
        {2} = mars hours
        {3} = mars minutes
        {4} = mars seconds (float)
Example:
d.mars_strfdelta('{0}{1:04d}M{2:02d}:{3:02d}:{4:06.3f}') = -003M04:05:06.789
d.mars_strfdelta('{0}{1} sols,{2} hours,{3} minutes,{4} seconds') = -3 sols, 4 hours, 5 minutes, 6.789 seconds
```

## Rounding Durations
Durations can be rounded in the same way as Time objects, by passing in a Duration object as a precision.
```
d = Duration('06:03:59.972')
ONE_HOUR = Duration('01:00:00')
ONE_MINUTE = Duration('00:01:00')
ONE_SECOND = Duration('00:00:01')

d.round(ONE_HOUR) == Duration('06:00:00')
d.round(ONE_MINUTE) == Duration('06:04:00')
d.round(ONE_SECOND) == Duration('06:04:00')

d.ceil(ONE_HOUR) == Duration('07:00:00')
d.ceil(ONE_MINUTE) == Duration('06:04:00')
d.ceil(ONE_SECOND) == Duration('06:04:00')

d.floor(ONE_HOUR) == Duration('06:00:00')
d.floor(ONE_MINUTE) == Duration('06:03:00')
d.floor(ONE_SECOND) == Duration('06:03:59')
```

## Min/max methods
The Python min and max methods return the minimum or maximum Duration in a list of Durations, based on the current default comparison precision. For example:
```
duration_list = [
    Duration('00:00:00'),
    Duration('00:00:01'),
    Duration('1T00:00:00')
]

min(duration_list) == Duration('00:00:00')
max(duration_list) == Duration('1T00:00:00')
```

# Math with Time and Duration objects
Times and Durations can be used together with several math methods: adding, subtracting, multiplying, and dividing. Multiplying and dividing are exclusive to Durations.

## Adding Times and Durations
```
t = Time('2019-150T00:00:00')
d = Duration('1T12:00:00')
(t + d).to_string() == '2019-151T12:00:00'
(d + d).to_string() == '3T00:00:00'
```

## Subtracting Times and Durations
```
t = Time('2019-150T00:00:00')
d = Duration('1T12:00:00')
(t - d).to_string() == '2019-148T12:00:00'
(d + d).to_string() == '00:00:00'
(d - d - d).to_string() = '-1T12:00:00'
```

## Multiplying Durations
Durations can only be multiplied by ints or floats, not durations.
```
Duration(1) * 5 == Duration('00:00:05')
Duration('00:00:01') * -10 == Duration('-00:00:10')
```

## Dividing Durations
Durations can be divided by Durations, ints, or floats.

### Dividing Durations by Durations
If a Duration is divided by a Duration then it returns a float.
```
Duration('01:00:00') / Duration('00:01:00') == 60.0
```

### Dividing Durations by floats or ints
If a Duration is divided by a float or int then it returns a Duration.
```
Duration('01:00:00') / 60.0 == Duration('00:01:00')
Duration('01:00:00') / 3600 == Duration('00:00:01')
```

# Comparing Times and Durations
Times and Durations can be compared by using ==, !=, <, >, <=, or >=.

## Comparison Precision
Times and Durations have the concept of a "comparison precision" because both are stored as floats (doubles) under the hood. The Time comparison precision is specified as a Duration object, while the Duration comparison precision is specified as a number of seconds. The default for both duration and time comparisons is 1 millisecond.
```
# one ms comparison precision
Time.set_comparison_precision(Duration("00:00:00.001"))
Duration.set_comparison_precision(0.001)
```

The comparison precision works by using that value whenever comparing two Times or Durations. For example:
```
t = Time('2022-001T00:00:00')
t2 = Time('2022-001T00:00:01')
t3 = Time('2022-001T00:00:00.1')
t4 = Time('2022-001T00:00:00.01')
t5 = Time('2022-001T00:00:00.001')
t6 = Time('2022-001T00:00:00.0001')

Time('2022-001T00:00:00') != Time('2022-001T00:00:00.001')
Time('2022-001T00:00:00') == Time('2022-001T00:00:00.0001')

Time.set_comparison_precision(Duration(10))
Time('2022-001T00:00:00') == Time('2022-001T00:00:01')

Time.set_comparison_precision(Duration(1))
Time('2022-001T00:00:00') != Time('2022-001T00:00:01')
Time('2022-001T00:00:00') == Time('2022-001T00:00:00.1')

Time.set_comparison_precision(Duration(.1))
Time('2022-001T00:00:00') != Time('2022-001T00:00:00.01')
Time('2022-001T00:00:00') == Time('2022-001T00:00:00.001')
```

The other operators also use the precision for all comparisons.

## Comparison operator examples
```
Time('2020-001T00:00:00') < Time('2020-003T00:00:00')
Time('2020-001T00:00:00') <= Time('2020-001T00:00:00')

Time('2020-004T00:00:00') > Time('2020-003T00:00:00')
Time('2020-001T00:00:00') >= Time('2020-001T00:00:00')

Time('2020-001T00:00:00') == Time('2020-001T00:00:00')
Time('2020-001T00:00:00') != Time('2020-001T00:00:01')

Duration(1) < Duration('00:00:01')
Duration(2) <= Duration('00:00:02')

Duration(3) > Duration('00:00:02')
Duration(4) >= Duration('00:00:04')

Duration(1) == Duration(1)
Duration(1) != Duration('00:00:02')
```

## Check if two times are within X duration of each other
```
t1 = Time('2020-001T00:00:00')
t2 = Time('2020-002T00:00:00')
Duration.abs(t1 - t2) <= Duration('1T00:00:00')
```