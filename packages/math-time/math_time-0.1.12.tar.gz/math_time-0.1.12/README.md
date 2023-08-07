# Math Time Python Module

Math Time is a Python module that facilitates time and date conversions and assists with converting between different time zones. Whether you need to calculate time differences, convert between various date formats, or determine the equivalent time in different regions, Math Time has got you covered.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install Math Time, you can use pip:

```bash
pip install math-time
```

## Usage

To use the Math Time module in your Python script, import it like this:

```python
from math_time import *
```

## Features

Math Time provides the following features:

- Timezone conversions: Convert dates and times between different time zones easily.
- Date arithmetic: Perform addition and subtraction operations on dates and times.
- Date formatting: Format dates and times in various styles according to your needs.

## Examples

1. Timezone Conversion:

```python
from math_time import timezone
# Convert a date and time from one timezone to another
result = timezone.timezone_converter("2023-07-19 12:00:00", "America/New_York", "Europe/London")
print(result)  # Output: "2023-07-19 17:00:00"
```

2. Date Arithmetic:

```python
from math_time import date_arithmentic
# Add 2 days to a given date
result = date_arithmentic.add_days("2023-07-19", 2)
print(result)  # Output: "2023-07-21"

# Subtract 1 month from a given date
result = date_arithmentic.subtract_months("2023-07-19", 1)
print(result)  # Output: "2023-06-19"

```

3. Date Formatting:

```python
from math_time import date_format
# Format a date in a user-friendly way
result = date_format.format_date("2023-07-19", "long")
print(result)  # Output: "July 19, 2023"

# Format a time in 24-hour format
result = date_format.format_time("12:30:00", "24h")
print(result)  # Output: "12:30"

```

## Contributing

Contributions are welcome! If you find any issues, have suggestions for improvements, or want to add new features, feel free to open an [issue](https://git.w3i.eu/Kilian/math_time/issues).

## License

[EUPL](https://eupl.eu/1.2/en/)
