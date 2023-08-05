# Chromify - Python Library Documentation

Chromify is a Python library that provides functionalities for color manipulation and conversion. It allows you to convert between different color representations such as RGB, HEX, HSL, CMYK, and HSV, and perform various color operations.

![BANNER](https://github.com/plaraje/chromify/assets/61209614/e4906631-4315-4923-83de-df161fcc1bae)

![GitHub all releases](https://img.shields.io/github/downloads/plaraje/chromify/total?style=plastic&logo=GitHub&label=Downloads&color=%2300FF00)   ![Static Badge](https://img.shields.io/badge/License-MIT-green?style=plastic&logo=MIT&label=License&color=%2300FF00)   ![GitHub release (with filter)](https://img.shields.io/github/v/release/plaraje/chromify?style=plastic&logo=GitHub&label=Relase&color=%23ff0000)   ![GitHub Repo stars](https://img.shields.io/github/stars/plaraje/chromify?style=plastic&logo=GitHub&label=Stars&color=%23ffff00)





# Table of Contents
- [Chromify - Python Library Documentation](#chromify---python-library-documentation)
  * [Table of Contents](#table-of-contents)
  * [Installation](#installation)
  * [Usage](#usage)
    + [`Color` Class](#color-class)
    + [Creating a `Color` Object](#creating-a-color-object)
  * [Color Conversion](#color-conversion)
  * [Color Manipulation](#color-manipulation)
  * [`Converter` Class](#converter-class)
    + [Creating a `Converter` Object](#creating-a-converter-object)
  * [Color Conversion](#color-conversion-1)
  * [License](#license)

## Installation

You can install Chromify using pip: `pip install chromify`


## Usage

### `Color` Class

The `Color` class represents a color and provides methods for color conversion and manipulation.

### Creating a `Color` Object

You can create a `Color` object in the following ways:

```python
from chromify import Color

# Create a Color object from a CSS representation
color1 = Color("#FF0000")
color2 = Color("rgb(255, 0, 0)")
color3 = Color("hsl(0, 100%, 50%)")

# Create a Color object from RGB values
color4 = Color(255, 0, 0)

# Create a Color object from another Color object
color5 = Color(color1)
```

# Color Conversion

You can convert a Color object to different representations using the following methods:

```python
# Convert to HEX representation
hex_value = color1.to_hex()  # Returns "#FF0000"

# Convert to HSL representation
hsl_value = color1.to_hsl()  # Returns "hsl(0, 100%, 50%)"

# Convert to CMYK representation
cmyk_value = color1.to_cmyk()  # Returns "cmyk(0%, 100%, 100%, 0%)"

# Convert to HSV representation
hsv_value = color1.to_hsv()  # Returns "hsv(0, 100%, 100%)"

# Convert to CSS representation (RGB)
css_value = color1.to_css()  # Returns "rgb(255, 0, 0)"
```

# Color Manipulation

The Color class also provides methods for color manipulation, such as inverting the color, calculating brightness, generating a color palette, among others.

```python
# Invert the color
inverted_color = color1.invert()

# Calculate the brightness of the color
brightness = color1.brightness()

# Generate a color palette
palette = color1.generate_palette(5)
```

# `Converter` Class

The `Converter` class is a subclass of Color and adds additional functionalities for converting color values between different representations.

### Creating a `Converter` Object

You can create a `Converter` object in the same ways as a Color object:

```python
from chromify import Converter

# Create a Converter object from a CSS representation
converter1 = Converter("#FF0000")
converter2 = Converter("rgb(255, 0, 0)")
converter3 = Converter("hsl(0, 100%, 50%)")

# Create a Converter object from RGB values
converter4 = Converter(255, 0, 0)

# Create a Converter object from another Color object
converter5 = Converter(color1)
```

# Color Conversion

The `Converter` class provides additional methods to convert color values between different representations. You can use the following methods:

```python
# Convert to HEX representation
hex_value = converter1.to_hex()  # Returns "#FF0000"

# Convert to HSL representation
hsl_value = converter1.to_hsl()  # Returns "hsl(0, 100%, 50%)"

# Convert to CMYK representation
cmyk_value = converter1.to_cmyk()  # Returns "cmyk(0%, 100%, 100%, 0%)"

# Convert to HSV representation
hsv_value = converter1.to_hsv()  # Returns "hsv(0, 100%, 100%)"

# Convert to CSS representation (RGB)
css_value = converter1.to_css()  # Returns "rgb(255, 0, 0)"
```

# License
MIT License, to view the license details, click [here](LICENSE)
