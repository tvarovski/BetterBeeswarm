# Default
import seaborn as sns
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", alpha=0.7, palette='viridis')
plt.savefig('native_beeswarm.png', dpi=200)

# Example 1
from betterbeeswarm import Beeswarm
import seaborn as sns
sns.categorical.Beeswarm = Beeswarm
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", alpha=0.7, palette='viridis')
plt.savefig('betterbeeswarm.png', dpi=200)

# Example 2
from betterbeeswarm import Beeswarm
import seaborn as sns
sns.categorical.Beeswarm = Beeswarm
tips = sns.load_dataset("tips")

sns.catplot(
    data=tips, kind="swarm", x="time", y="total_bill", hue="sex", 
    col="day", aspect=0.6, height=2.5, alpha=0.7, size=5)
plt.savefig('betterbeeswarm_cat.png', dpi=200)