import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([4, 8, 16, 32])
bm = [13.162, 15.514, 212.536, 871.648]
user = [13.116, 15.832, 117.434, 69.1]

# Generate error margins
max_bm = [14.20, 18.35, 966.20, 3119.43]
min_bm = [12.47, 14.04, 22.18, 34.79]

max_user = [14.58, 16.67, 322.26, 113.15]
min_user = [12.64, 15.03, 29.97, 39.73]


# Create line plot with error margins
sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.lineplot(x=x, y=bm, label='Bare metal')
sns.lineplot(x=x, y=user, label='Usernetes')
plt.fill_between(x, min_bm, max_bm, alpha=0.2)
plt.fill_between(x, min_user, max_user, alpha=0.2)

# Set plot title and labels
plt.title('osu_barrier, 96 tasks per node, UCX_TLS=rc,sm')
plt.xlabel('Number of nodes')
plt.ylabel('Latency (microseconds)')
plt.xticks(x,x)

# Display the plot
plt.legend()
plt.savefig("barrier.png")

