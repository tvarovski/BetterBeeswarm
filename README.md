# BetterBeeswarm

This repository contains a modified `Beeswarm` class (swarmplot or swarm) from `seaborn`, which will automatically decrease the spacing of scatter datapoints untill no points fall into the `Beeswarm` "gutters".

## Installation

It is the easiest to install the `BetterBeeswarm` package through pip:
```bash
pip install --upgrade betterbeeswarm
```

## Usage

To use BetterBeeswarm instead of the standard Seaborn Beeswarm, type the following each time you import the `seaborn` library:

```python
import seaborn as sns
import betterbeeswarm
```

When using swarmplot, you can now add additional `overflow` argument which can be set to `overflow='gutters'` (default), `overflow='shrink'`, or `overflow='random'`.

## Examples
### Default
When Seaborn's native Beeswarm class runs out of place it will put points that don't fit into gutters as in the example below:

```python
import seaborn as sns
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", alpha=0.7, palette='viridis')
```
<p align="center">
    <img src="https://raw.githubusercontent.com/tvarovski/BetterBeeswarm/main/examples/native_beeswarm.png" width="500" height="500">
</p>

### Example 1
Default behaviour of native `Seaborn` can be modifies with `BetterBeeswarm` by passing `overflow='shrink'`:

```python
import seaborn as sns
import betterbeeswarm
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", alpha=0.7, palette='viridis', overflow="shrink")
```
<p align="center">
    <img src="https://raw.githubusercontent.com/tvarovski/BetterBeeswarm/main/examples/betterbeeswarm_shrink.png" width="500" height="500">
</p>

### Example 2
`BetterBeeswarm` can also be used to randomly place points that don't fit into the gutters by passing `overflow='random'`:

```python
import seaborn as sns
import betterbeeswarm
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", alpha=0.7, palette='viridis', overflow="random")
```
<p align="center">
    <img src="https://raw.githubusercontent.com/tvarovski/BetterBeeswarm/main/examples/betterbeeswarm_random.png" width="500" height="500">
</p>

### Example 3
`BetterBeeswarm` also works for categorical plots and any time Seaborn's `Beeswarm` class is used:

```python
from betterbeeswarm import Beeswarm
import seaborn as sns
sns.categorical.Beeswarm = Beeswarm
tips = sns.load_dataset("tips")

sns.catplot(
    data=tips, kind="swarm",
    x="time", y="total_bill", hue="sex", col="day",
    aspect=0.6, height=2.5, alpha=0.7, size=5, overflow="shrink"
)
```
<p align="center">
<img src="https://raw.githubusercontent.com/tvarovski/BetterBeeswarm/main/examples/betterbeeswarm_cat.png">
</p>

### Example 4
`BetterBeeswarm` can be used with `matplotlib` as well to customize the plot even further, for example by removing the fill color of the points acheaving a more minimalistic, wireframe look:

```python
import seaborn as sns
import betterbeeswarm
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", size=5, overflow='shrink')
plt.setp(plt.gca().collections, edgecolor="black", linewidth=.5)
for collection in plt.gca().collections:
    collection.set_edgecolor((0, 0, 0, 1))  # RGBA tuple where A is the alpha channel
    collection.set_facecolor((1, 1, 1, 0))  # RGBA tuple where A is the alpha channel
```
<p align="center">
    <img src="https://raw.githubusercontent.com/tvarovski/BetterBeeswarm/main/examples/betterbeeswarm_shrink_wireframe.png" width="500" height="500">
</p>