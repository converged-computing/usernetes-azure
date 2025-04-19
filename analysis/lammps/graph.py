import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([4, 8, 16, 32])
bm = [4.292, 8.2294, 14.7548, 29.7814]
user = [4.2764, 8.1498, 14.1658, 27.983]

# Generate error margins
max_bm = [4.342, 8.439, 15.462, 30.043]
min_bm = [4.231, 7.713, 13.473, 29.505]

max_user = [4.330, 8.398, 15.253, 28.213]
min_user = [4.196, 7.798, 12.134, 27.733]


# Create line plot with error margins
sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.lineplot(x=x, y=bm, label='Singularity')
sns.lineplot(x=x, y=user, label='Usernetes')
plt.fill_between(x, min_bm, max_bm, alpha=0.2)
plt.fill_between(x, min_user, max_user, alpha=0.2)

# Set plot title and labels
# 96 nodes per task, 64x64x32
plt.title('LAMMPS')
plt.xlabel('Nodes')
plt.ylabel('Matom-step/s')
plt.xticks(x,x)

# Display the plot
plt.legend()
plt.savefig("lammps.png")

