# CunitPy
#### This is a universal conversor. It has methods to convert measurment units and world's most popular currency.

#
## Installation
```
pip install cunitpy
```

#
## How to use
```
from cunitpy import *
```
#### Now, use the pattern bellow to asign a variable the converted value: 
##### *Quantity.your_measurement_unit2new_measurement_unit(value)*
### Examples:
```py
# 38° Celsius to Kelvin
tempKel = Temperature.celsius2kelvin(38)
```
```py
# 250 pounds to kilograms
kg = Mass.pound2kilogram(250)
```
```py
# 2000 Japanese Ienes to Dollars
dol = Currency.JPY2USD(2000)
```