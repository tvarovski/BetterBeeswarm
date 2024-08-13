# Default
import seaborn as sns
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", alpha=0.7, palette='viridis')
plt.savefig('native_beeswarm.png', dpi=200)

# Example 1
import seaborn as sns
import betterbeeswarm
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", palette='viridis', size=5, alpha=0.7, overflow='shrink')

# #modify marks to have black border
# plt.setp(plt.gca().collections, edgecolor="black", linewidth=.5)
# for collection in plt.gca().collections:
#     collection.set_edgecolor((0, 0, 0, 1))  # RGBA tuple where A is the alpha channel
#     collection.set_facecolor((1, 1, 1, 0))  # RGBA tuple where A is the alpha channel

plt.savefig('betterbeeswarm_shrink.png', dpi=200)

# Example 2
import seaborn as sns
import betterbeeswarm
import matplotlib.pyplot as plt
tips = sns.load_dataset("tips")

plt.figure(figsize=(4, 4)) # set figure size
sns.swarmplot(data=tips, x="size", y="total_bill", hue="size", palette='viridis', size=5, alpha=0.7, overflow='random')
plt.savefig('betterbeeswarm_random.png', dpi=200)

# Example 3
import seaborn as sns
import betterbeeswarm
tips = sns.load_dataset("tips")

sns.catplot(
    data=tips, kind="swarm", x="time", y="total_bill", hue="sex", 
    col="day", aspect=0.6, height=2.5, alpha=0.7, size=5, overflow='shrink')
plt.savefig('betterbeeswarm_cat.png', dpi=200)
