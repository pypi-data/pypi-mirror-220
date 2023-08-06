# ResponseCurve.py

ResponseCurve.py is a Python library for detecting response curves in time series data. It uses a combination of statistical and machine learning techniques to identify patterns in the data that correspond to changes in the underlying system.

## Installation

You can install ResponseCurve.py using pip install responsecurve


ResponseCurve.py requires several external dependencies, including pandas, numpy, scipy, matplotlib, and scikit-learn, which will be installed automatically when you install the library.

## Usage

To use ResponseCurve.py, simply import the functions or classes you need into your Python code. Here's an example of how to use the `detect_response_curves` function:

```python
from responsecurve import detect_response_curves

# Load time series data from a file
data = load_data('data.csv')

# Detect response curves in the data
response_curves = detect_response_curves(data)

# Print the start and end points of each response curve
for curve in response_curves:
    print('Start:', curve[0], 'End:', curve[1])
```

ResponseCurve.py also includes a ResponseCurveDetector class that provides a higher-level interface for detecting response curves. Below is an example of how to use the ResponseCurveDetector class:

```python
from responsecurve import ResponseCurveDetector

# Create a detector object with default parameters
detector = ResponseCurveDetector()

# Load time series data from a file
data = load_data('data.csv')

# Detect response curves in the data
detector.detect(data)

# Visualize the data and the detected response curves
detector.plot()
```

For more information on how to use ResponseCurve.py, please refer to the documentation.

## Contributing

If you find a bug or have a feature request, please open an issue on GitHub. If you would like to contribute to the development of ResponseCurve.py, please submit a pull request.

## License

ResponseCurve.py is licensed under the MIT License. See LICENSE for more information.