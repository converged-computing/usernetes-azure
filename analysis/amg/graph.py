import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([4, 8, 16, 32])
bm = [142854680, 227669580, 394786840, 742682820]
user = [142086280, 231505860, 404994580, 755884200]

# Generate error margins
max_bm = [1.435640e+08, 2.322809e+08, 3.959597e+08, 7.723532e+08]
min_bm = [1.417077e+08, 2.184277e+08, 3.936824e+08, 6.729249e+08]

max_user = [1.426569e+08, 2.332136e+08, 4.073286e+08, 7.882129e+08]
min_user = [1.409862e+08, 2.299533e+08, 4.009945e+08, 6.507061e+08]


# Create line plot with error margins
sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.lineplot(x=x, y=bm, label='Bare metal')
sns.lineplot(x=x, y=user, label='Usernetes')
plt.fill_between(x, min_bm, max_bm, alpha=0.2)
plt.fill_between(x, min_user, max_user, alpha=0.2)

# Set plot title and labels
plt.title('AMG, 32 tasks per node, OMP_NUM_THREADS=3, 3 cores per task, 256x256x128')
plt.xlabel('Number of nodes')
plt.ylabel('Figure of Merit')
plt.xticks(x,x)

# Display the plot
plt.legend()
plt.savefig("amg.png")

