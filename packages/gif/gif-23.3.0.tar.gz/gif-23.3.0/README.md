<div align="center">
  <img alt="gif" src="https://raw.githubusercontent.com/maxhumber/gif/master/images/logo.png" height="200px">
</div>
<div align="center">
  <a href="https://calver.org/"><img src="https://img.shields.io/badge/calver-YY.MM.MICRO-22bfda.svg"></a>
  <a href="https://pypi.org/project/gif/"><img src="https://img.shields.io/pypi/v/gif.svg"></a>
  <a href="https://pepy.tech/project/gif"><img alt="Downloads" src="https://pepy.tech/badge/gif/month"></a>
</div>

### About

The [matplotlib](https://matplotlib.org/) Animation Extension

### Install & Import

```sh
pip install gif
```

```python
import gif
```

### Quickstart

```python
import gif
from random import randint
from matplotlib import pyplot as plt

x = [randint(0, 100) for _ in range(100)]
y = [randint(0, 100) for _ in range(100)]

# (Optional) Set the dots per inch resolution to 300
gif.options.matplotlib["dpi"] = 300

# Decorate a plot function with @gif.frame
@gif.frame
def plot(i):
    xi = x[i*10:(i+1)*10]
    yi = y[i*10:(i+1)*10]
    plt.scatter(xi, yi)
    plt.xlim((0, 100))
    plt.ylim((0, 100))

# Construct "frames"
frames = [plot(i) for i in range(10)]

# Save "frames" to gif with a specified duration (milliseconds) between each frame
gif.save(frames, 'example.gif', duration=50)
```


### Examples

| [![arrival.gif](images/arrival.gif)](examples/arrival.py)    | [![hop.gif](images/hop.gif)](examples/hop.py)          | [![phone.gif](images/phone.gif)](examples/phone.py) |
| ------------------------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------- |
| [![seinfeld.gif](images/seinfeld.gif)](examples/seinfeld.py) | [![spiral.gif](images/spiral.gif)](examples/spiral.py) | [![heart.gif](images/heart.gif)](heart.py)          |


### Warning

Altair and Plotly are no longer supported in `22.5.0`+

Please use `pip install gif==3.0.0` if you still need to interface with these libraries
