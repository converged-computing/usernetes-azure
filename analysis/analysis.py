import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = 'data'

platforms = ['bare', 'usernetes']

applications = ['osu_allreduce', 'lammps', 'lammps_time', 'amg', 'minife', 'osu_latency', 'osu_bw']

osu_latency_pattern = re.compile(r'osu_latency-(\d+)-iter-(\d+)-.*\.out')
osu_bandwidth_pattern = re.compile(r'osu_bw-(\d+)-iter-(\d+)-.*\.out')
osu_pattern = re.compile(r'osu_allreduce-(\d+)-iter-(\d+)-.*\.out')
lammps_pattern = re.compile(r'lammps-(\d+)-iter-(\d+)-.*\.out')
amg_pattern = re.compile(r'amg-(\d+)-iter-(\d+)-.*\.out')
minife_pattern = re.compile(r'miniFE.230x230x230.P(\d+).*\.yaml')

sns.set(font_scale=2)

def extract_osu_bandwidth_value(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts and parts[0] == '4194304':
                try:
                    return float(parts[1])
                except (IndexError, ValueError):
                    return None
    return None


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

def extract_lammps_time(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('Total wall time:'):
                try:
                    match = re.search(r"(\d+):(\d+):(\d+)", line)
                    if match:
                        hours, minutes, seconds = map(int, match.groups())
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                        return total_seconds
                    else:
                        print("No time found.")
                        return None
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
for platform in platforms:
    i=0
    for app in applications:
       directory = os.path.join(BASE_DIR, platform, app)
       if app == 'osu_latency' or app == 'osu_bw':
           directory = os.path.join(BASE_DIR, platform, 'osu_pt2pt')
       if app == 'lammps_time':
           directory = os.path.join(BASE_DIR, platform, 'lammps')
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
                       print(f"Warning: No value found in {filepath}")
           if app == 'osu_bw':
               match = osu_bandwidth_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_osu_bandwidth_value(filepath)
                   if value is not None:
                       records.append((platform, app, size, iteration, value))
                   else:
                       print(f"Warning: No value found in {filepath}")
           if app == 'osu_latency':
               match = osu_latency_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_osu_value(filepath)
                   if value is not None:
                       records.append((platform, app, size, iteration, value))
                   else:
                       print(f"Warning: No value found in {filepath}")
           elif app == 'lammps':
               match = lammps_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_lammps_value(filepath)
                   if value is not None:
                       records.append((platform, app, size, iteration, value))
                   else:
                       print(f"Warning: No value found in {filepath}")
           elif app == 'lammps_time':
               match = lammps_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_lammps_time(filepath)
                   if value is not None:
                       records.append((platform, app, size, iteration, value))
                   else:
                       print(f"Warning: No value found in {filepath}")
           elif app == 'amg':
               match = amg_pattern.match(filename)
               if match:
                   size = int(match.group(1))
                   iteration = int(match.group(2))
                   value = extract_amg_value(filepath)
                   if value is not None:
                        records.append((platform, app, size, iteration, value))
                   else:
                        print(f"Warning: No value found in {filepath}")
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
                        print(f"Warning: No value found in {filepath}")

df = pd.DataFrame(records, columns=['Platform','Application', 'Size', 'Iteration', 'Value'])
df_mean = df.groupby(['Platform','Application','Size']).agg({'Value': 'mean'}).reset_index()
df.to_csv('summary_results.csv', index=False)
print(f"Saved summary results to 'summary_results.csv'")

sns.set(style="whitegrid")
for app in applications:
    plt.figure(figsize=(10, 6))
    coordinates="default"
    if app == 'lammps':
        coordinates="Matom-step/s"
    if app == 'lammps_time':
        coordinates="wall time (seconds)"
    elif app == 'osu_allreduce':
        coordinates="latency (us)"
    elif app == 'osu_latency':
        coordinates="latency (us)"
    elif app == 'osu_bw':
        coordinates="bandwidth (MB/s)"
    elif app == 'amg':
        coordinates="Figure of Merit"
    elif app == 'minife':
        coordinates="Total CG Mflops"

    subset = df[df['Application'] == app]
    df["Size"] = df["Size"].astype(int)
    if app == 'osu_latency' or app == 'osu_bw':
        ax=sns.boxplot(
            data=subset,
            x='Size',
            y='Value',
            hue='Platform',
            showfliers=True
        )
        ax.set(xticklabels=[])
        plt.xlabel(None)
    #elif app in ['lammps', 'lammps_time']:
    #    sns.barplot(
    #        data=subset,
    #        x='Size',
    #        y='Value',
    #        hue='Platform',
    #        order=sorted(subset.Size.unique())
    #    )
    else:
        ax=sns.barplot(
            data=subset,
            x='Size',
            y='Value',
            hue='Platform',
            order=sorted(subset.Size.unique())
        )
        plt.xlabel('Nodes')
        ax.tick_params(labelsize=15)
        if app in ['minife', 'amg']:
            ax.set(yscale='log')
        #sns.lineplot(
        #    data=subset,
        #    x='Size',
        #    y='Value',
        #    hue='Platform',
        #    style='Platform',
        #    markers=True,
        #    dashes=False,
        #    err_style='bars'
        #)

    plt.xlabel('Nodes', fontsize=15)
    plt.ylabel(coordinates, fontsize=15)
    plt.legend(title='Platform', fontsize=11)
    plt.tight_layout()
    plot_filename = f'plot_{app}.png'
    plt.savefig(plot_filename)
    print(f"Saved plot for {app} as '{plot_filename}'")
