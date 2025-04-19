import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([4, 8, 16, 32])
bm = [443434, 413168, 650192, 1165520]
user = [612795, 765478, 1296066, 1188310]

# Generate error margins
max_bm = [452019, 528664, 714919, 2163170]
min_bm = [434009, 8843.7, 605018, 840116]

max_user = [678044, 973688, 1442860, 1674270]
min_user = [499932, 632443, 1162340, 846983]


# Create line plot with error margins
sns.set(style="darkgrid")
plt.figure(figsize=(8, 6))
sns.lineplot(x=x, y=bm, label='Singularity')
sns.lineplot(x=x, y=user, label='Usernetes')
plt.fill_between(x, min_bm, max_bm, alpha=0.2)
plt.fill_between(x, min_user, max_user, alpha=0.2)

# Set plot title and labels
# 96 tasks per node, nx=230 ny=230 nz=230
plt.title('MiniFE')
plt.xlabel('Nodes')
plt.ylabel('Total CG Mflops')
plt.xticks(x,x)

# Display the plot
plt.legend()
plt.savefig("minife.png")

