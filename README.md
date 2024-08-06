# BetterBeeswarm

This repository contains a modified Beeswarm class from Seaborn, which will automatically decrease the spacing of scatter datapoints untill no points fall into the Beeswarm "gutters".

## Installation

It is the easiest to install the BetterBeeswarm package through pip:
```bash
pip install --upgrade betterbeeswarm
```

## Usage

To use BetterBeeswarm instead of the standard seaborn Beeswarm, type the following each time you import the seaborn library:

```python
from betterbeeswarm import Beeswarm
import seaborn as sns
sns.categorical.Beeswarm = Beeswarm
```

