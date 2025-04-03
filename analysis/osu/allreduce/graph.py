import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([4, 8, 16, 32])
bm = [22.604, 20.83, 29.922, 37.638]
user = [20.818, 21.452, 36.92, 72.812]

# Generate error margins
max_bm = [34.20, 24.81, 34.89, 46.16]
min_bm = [15.14, 19.11, 26.91, 33.94]

max_user = [34.58, 22.74, 54.88, 102.33]
min_user = [15.27, 20.41, 30.30, 53.65]


# Create line plot with error margins
sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.lineplot(x=x, y=bm, label='Bare metal')
sns.lineplot(x=x, y=user, label='Usernetes')
plt.fill_between(x, min_bm, max_bm, alpha=0.2)
plt.fill_between(x, min_user, max_user, alpha=0.2)

# Set plot title and labels
plt.title('osu_allreduce, 96 tasks per node, UCX_TLS=rc,sm, size 64')
plt.xlabel('Number of nodes')
plt.ylabel('Latency (microseconds)')
plt.xticks(x,x)

# Display the plot
plt.legend()
plt.savefig("allreduce.png")

