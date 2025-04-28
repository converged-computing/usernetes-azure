import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = 'data'

platforms = ['bare', 'usernetes']

applications = ['osu_allreduce', 'lammps', 'amg', 'minife']

osu_pattern = re.compile(r'osu_allreduce-(\d+)-iter-(\d+)-.*\.out')
lammps_pattern = re.compile(r'lammps-(\d+)-iter-(\d+)-.*\.out')
amg_pattern = re.compile(r'amg-(\d+)-iter-(\d+)-.*\.out')
minife_pattern = re.compile(r'miniFE.230x230x230.P(\d+).*\.yaml')

def extract_osu_value(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts and parts[0] == '64':
                try:
                    return float(parts[1])
                except (IndexError, ValueError):
                    return None
    return None

def extract_lammps_value(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('Performance:'):
                try:
                    parts = line.strip().split(',')
                    last_part = parts[-1].strip()
                    last_value = float(last_part.split()[0])
                    return last_value
                except (IndexError, ValueError):
                    return None
    return None

def extract_amg_value(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('Figure of Merit'):
                try:
                    parts = line.strip().split(' ')
                    last_value = float(parts[-1].strip())
                    return last_value
                except (IndexError, ValueError):
                    return None
    return None

def extract_minife_value(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("    Total CG Mflops:"):
                try:
                    parts = line.strip().split(':')
                    last_value = float(parts[1].strip())
                    return last_value
                except (IndexError, ValueError):
                    return None
    return None

records = []
i=0
for platform in platforms:
    for app in applications:
       directory = os.path.join(BASE_DIR, platform, app)
       if not os.path.exists(directory):
           print(f"Directory not found: {directory}")
           continue

       for filename in os.listdir(directory):
           filepath = os.path.join(directory, filename)
           if app == 'osu_allreduce':
               match = osu_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_osu_value(filepath)
                   if value is not None:
                       records.append((platform, app, size, iteration, value))
                   else:
                       print(f"No value found in {filepath}")

           elif app == 'lammps':
               match = lammps_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_lammps_value(filepath)
                   if value is not None:
                       records.append((platform, app, size, iteration, value))
                   else:
                       print(f"No value found in {filepath}")
           elif app == 'amg':
               match = amg_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_amg_value(filepath)
                   if value is not None:
                        records.append((platform, app, size, iteration, value))
                   else:
                        print(f"No value found in {filepath}")
           elif app == 'minife':
               i+=1
               match = minife_pattern.match(filename)
               if match:
                   size = int(match.group(1))/96
                   iteration = i
                   value = extract_minife_value(filepath)
                   if value is not None:
                        records.append((platform, app, size, iteration, value))
                   else:
                        print(f"No value found in {filepath}")

df = pd.DataFrame(records, columns=['Platform','Application', 'Size', 'Iteration', 'Value'])

df_mean = df.groupby(['Platform','Application','Size']).agg({'Value': 'mean'}).reset_index()
df_mean.to_csv('summary_results.csv', index=False)

sns.set(style="whitegrid")
for app in applications:
    plt.figure(figsize=(10, 6))
    subset = df_mean[df_mean['Application'] == app]
    coordinates="default"
    if app == 'lammps':
        coordinates="Matom-step/s"
    elif app == 'osu':
        coordinates="latency (us)"
    elif app == 'osu':
        coordinates="Figure of Merit"
    elif app == 'minife':
        coordinates="Total CG Mflops"

    sns.lineplot(
        data=subset,
        x='Size',
        y='Value',
        hue='Platform',
        style='Platform',
        markers=True,
        dashes=False,
        err_style='bars'
    )

    plt.title(f'{app}')
    plt.xticks(sorted(subset['Size'].unique()))
    plt.xlabel('Nodes')
    plt.ylabel(coordinates)
    plt.legend(title='Platform')
    plt.tight_layout()
    plot_filename = f'plot_{app}.png'
    plt.savefig(plot_filename)
    print(f"Saved plot for {app} as '{plot_filename}'")
