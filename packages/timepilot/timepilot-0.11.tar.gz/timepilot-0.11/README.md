

# TimePilot Lib 311x-011

TimePilot is a simple Python 3.11 library that helps you work with timezones and format them in different ways. With TimePilot, you can display the current time in a specific timezone or format a range of dates and times to appear in a particular way.

## Installation

You can easily install TimePilot using pip. Simply run the following command:

```python
pip install timepilot
```

## How to Use

Here's an example of how you can use TimePilot to display the current time in the Eastern Timezone:

```python
import timepilot

# Specify the timezone and formatting option you want to use
time_zone = "US/Eastern"
time_format = "hour_minute"

# Get the current time in the specified timezone and format
current_time = timepilot.get_current_time(time_zone, time_format)

# Print out the current time
print(f"The current time in {time_zone} is {current_time}")
```

We should get an output of something like this:

    The current time in US/Eastern is 3:30 PM

## Available Formatting Options
TimePilot provides several formatting options for displaying timezones, including:
- `hour_minute`: displays the hour and minute (e.g. 3:30 PM)
- `hour_minute_second`: displays the hour, minute, and second (e.g. 3:30:45 PM)
- `minute_second`: displays the minute and second (e.g. 30:45)
- `hour`: displays the hour (e.g. 3 PM)
- `second`: displays the second (e.g. 45)

You can specify the formatting option when calling get_current_time or format_datetime.

## Version

The current version of TimePilot is 311x-01, indicating that it is compatible with Python 3.11 and all sub-versions and the library version is 0.1.

# License
TimePilot is released under the MIT License. You can find the license information in the LICENSE file.