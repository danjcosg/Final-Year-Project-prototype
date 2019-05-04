import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
rng = np.arange(50)

x = np.random.randint(low=1, high=11, size=50)
y = x + np.random.randint(1, 5, size=x.size)
data = np.column_stack((x, y))

ax.hist(data, bins=np.arange(data.min(), data.max()), label=('Channing Tatum', 'Brie Larson'))
ax.legend(loc=(0.65, 0.8))
ax.set_title('Frequencies of $x$ and $y$')
ax.yaxis.tick_right()

input("continue?")