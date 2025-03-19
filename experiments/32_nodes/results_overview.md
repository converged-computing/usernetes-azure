# Overview of the results 

## AMG

### bare

```
azureuser@flux-user000000:/opt/bare$ cat results/amg/amg-4-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.427991e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.430436e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.435640e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.431590e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.417077e+08
azureuser@flux-user000000:/opt/bare$ cat results/amg/amg-8-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.320222e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.322809e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.281775e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.184277e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.274396e+08
azureuser@flux-user000000:/opt/bare$ cat results/amg/amg-16-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 3.959597e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 3.948444e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 3.953941e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 3.940536e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 3.936824e+08
azureuser@flux-user000000:/opt/bare$ cat results/amg/amg-32-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.629086e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.532505e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.519769e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.723532e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 6.729249e+08
```

### usernetes

```
azureuser@flux-user000000:/opt/usernetes$ cat results/amg/amg-4-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.409862e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.426569e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.426341e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.424412e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 1.417130e+08
azureuser@flux-user000000:/opt/usernetes$ cat results/amg/amg-8-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.299533e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.332136e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.316331e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.320925e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 2.306368e+08
azureuser@flux-user000000:/opt/usernetes$ cat results/amg/amg-16-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 4.009945e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 4.043023e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 4.072271e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 4.051204e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 4.073286e+08
azureuser@flux-user000000:/opt/usernetes$ cat results/amg/amg-32-iter-* | grep "Figure of Merit"
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.782941e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.845763e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.776316e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 6.507061e+08
Figure of Merit (FOM): nnz_AP / (Setup Phase Time + 3 * Solve Phase Time) 7.882129e+08
```


## Minife

### bare
```
azureuser@flux-user000000:/opt/bare$ cat results/minife/miniFE.230x230x230.P384.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 452019
    Total CG Mflops: 439910
    Total CG Mflops: 441899
    Total CG Mflops: 434009
    Total CG Mflops: 449334
azureuser@flux-user000000:/opt/bare$ cat results/minife/miniFE.230x230x230.P768.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 8843.7
    Total CG Mflops: 528664
    Total CG Mflops: 518428
    Total CG Mflops: 498028
    Total CG Mflops: 511877
azureuser@flux-user000000:/opt/bare$ cat results/minife/miniFE.230x230x230.P3072.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 922104
    Total CG Mflops: 2.16317e+06
    Total CG Mflops: 840116
    Total CG Mflops: 967811
    Total CG Mflops: 934402
azureuser@flux-user000000:/opt/bare$ cat results/minife/miniFE.230x230x230.P1536.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 710337
    Total CG Mflops: 607166
    Total CG Mflops: 605018
    Total CG Mflops: 613522
    Total CG Mflops: 714919
```
### usernetes
```
azureuser@flux-user000000:/opt/usernetes$ cat results/minife/miniFE.230x230x230.P384.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 678044
    Total CG Mflops: 599986
    Total CG Mflops: 638880
    Total CG Mflops: 499932
    Total CG Mflops: 647131
azureuser@flux-user000000:/opt/usernetes$ cat results/minife/miniFE.230x230x230.P768.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 754884
    Total CG Mflops: 973688
    Total CG Mflops: 632443
    Total CG Mflops: 742125
    Total CG Mflops: 724252
azureuser@flux-user000000:/opt/usernetes$ cat results/minife/miniFE.230x230x230.P3072.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 846983
    Total CG Mflops: 970525
    Total CG Mflops: 1.67427e+06
    Total CG Mflops: 1.31912e+06
    Total CG Mflops: 1.13066e+06
azureuser@flux-user000000:/opt/usernetes$ cat results/minife/miniFE.230x230x230.P1536.T1.2025* | grep "Total CG Mflops"
    Total CG Mflops: 1.27191e+06
    Total CG Mflops: 1.16234e+06
    Total CG Mflops: 1.32609e+06
    Total CG Mflops: 1.27713e+06
    Total CG Mflops: 1.44286e+06
```

## Lammps

### bare
```
azureuser@flux-user000000:/opt/bare$ cat results/lammps/lammps-4-iter-* | grep "Performance:"
Performance: 0.001 ns/day, 25561.425 hours/ns, 0.109 timesteps/s, 4.330 Matom-step/s
Performance: 0.001 ns/day, 26120.178 hours/ns, 0.106 timesteps/s, 4.237 Matom-step/s
Performance: 0.001 ns/day, 26160.587 hours/ns, 0.106 timesteps/s, 4.231 Matom-step/s
Performance: 0.001 ns/day, 25619.636 hours/ns, 0.108 timesteps/s, 4.320 Matom-step/s
Performance: 0.001 ns/day, 25492.750 hours/ns, 0.109 timesteps/s, 4.342 Matom-step/s
azureuser@flux-user000000:/opt/bare$ cat results/lammps/lammps-8-iter-* | grep "Performance:"
Performance: 0.002 ns/day, 13155.827 hours/ns, 0.211 timesteps/s, 8.413 Matom-step/s
Performance: 0.002 ns/day, 13116.242 hours/ns, 0.212 timesteps/s, 8.439 Matom-step/s
Performance: 0.002 ns/day, 13407.890 hours/ns, 0.207 timesteps/s, 8.255 Matom-step/s
Performance: 0.002 ns/day, 14350.354 hours/ns, 0.194 timesteps/s, 7.713 Matom-step/s
Performance: 0.002 ns/day, 13292.669 hours/ns, 0.209 timesteps/s, 8.327 Matom-step/s
azureuser@flux-user000000:/opt/bare$ cat results/lammps/lammps-16-iter-* | grep "Performance:"
Performance: 0.003 ns/day, 8215.185 hours/ns, 0.338 timesteps/s, 13.473 Matom-step/s
Performance: 0.003 ns/day, 7376.635 hours/ns, 0.377 timesteps/s, 15.005 Matom-step/s
Performance: 0.003 ns/day, 7422.791 hours/ns, 0.374 timesteps/s, 14.911 Matom-step/s
Performance: 0.003 ns/day, 7416.895 hours/ns, 0.375 timesteps/s, 14.923 Matom-step/s
Performance: 0.003 ns/day, 7158.521 hours/ns, 0.388 timesteps/s, 15.462 Matom-step/s
azureuser@flux-user000000:/opt/bare$ cat results/lammps/lammps-32-iter-* | grep "Performance:"
Performance: 0.007 ns/day, 3684.189 hours/ns, 0.754 timesteps/s, 30.043 Matom-step/s
Performance: 0.006 ns/day, 3743.506 hours/ns, 0.742 timesteps/s, 29.567 Matom-step/s
Performance: 0.006 ns/day, 3720.345 hours/ns, 0.747 timesteps/s, 29.751 Matom-step/s
Performance: 0.007 ns/day, 3684.348 hours/ns, 0.754 timesteps/s, 30.041 Matom-step/s
Performance: 0.006 ns/day, 3751.318 hours/ns, 0.740 timesteps/s, 29.505 Matom-step/s
```

### usernetes
```
azureuser@flux-user000000:/opt/usernetes$ cat results/lammps/lammps-4-iter-* | grep "Performance:"
Performance: 0.001 ns/day, 25865.429 hours/ns, 0.107 timesteps/s, 4.279 Matom-step/s
Performance: 0.001 ns/day, 25682.701 hours/ns, 0.108 timesteps/s, 4.310 Matom-step/s
Performance: 0.001 ns/day, 25939.025 hours/ns, 0.107 timesteps/s, 4.267 Matom-step/s
Performance: 0.001 ns/day, 25564.593 hours/ns, 0.109 timesteps/s, 4.330 Matom-step/s
Performance: 0.001 ns/day, 26376.145 hours/ns, 0.105 timesteps/s, 4.196 Matom-step/s
azureuser@flux-user000000:/opt/usernetes$ cat results/lammps/lammps-8-iter-* | grep "Performance:"
Performance: 0.002 ns/day, 13480.097 hours/ns, 0.206 timesteps/s, 8.211 Matom-step/s
Performance: 0.002 ns/day, 13648.687 hours/ns, 0.204 timesteps/s, 8.109 Matom-step/s
Performance: 0.002 ns/day, 13444.057 hours/ns, 0.207 timesteps/s, 8.233 Matom-step/s
Performance: 0.002 ns/day, 14194.227 hours/ns, 0.196 timesteps/s, 7.798 Matom-step/s
Performance: 0.002 ns/day, 13180.095 hours/ns, 0.211 timesteps/s, 8.398 Matom-step/s
azureuser@flux-user000000:/opt/usernetes$ cat results/lammps/lammps-16-iter-* | grep "Performance:"
Performance: 0.003 ns/day, 7256.500 hours/ns, 0.383 timesteps/s, 15.253 Matom-step/s
Performance: 0.003 ns/day, 9121.412 hours/ns, 0.305 timesteps/s, 12.134 Matom-step/s
Performance: 0.003 ns/day, 7366.753 hours/ns, 0.377 timesteps/s, 15.025 Matom-step/s
Performance: 0.003 ns/day, 8202.919 hours/ns, 0.339 timesteps/s, 13.493 Matom-step/s
Performance: 0.003 ns/day, 7416.584 hours/ns, 0.375 timesteps/s, 14.924 Matom-step/s
azureuser@flux-user000000:/opt/usernetes$ cat results/lammps/lammps-32-iter-* | grep "Performance:"
Performance: 0.006 ns/day, 3926.306 hours/ns, 0.707 timesteps/s, 28.190 Matom-step/s
Performance: 0.006 ns/day, 3980.938 hours/ns, 0.698 timesteps/s, 27.803 Matom-step/s
Performance: 0.006 ns/day, 3923.140 hours/ns, 0.708 timesteps/s, 28.213 Matom-step/s
Performance: 0.006 ns/day, 3991.018 hours/ns, 0.696 timesteps/s, 27.733 Matom-step/s
Performance: 0.006 ns/day, 3956.392 hours/ns, 0.702 timesteps/s, 27.976 Matom-step/s
```

## OSU allreduce

### bare
```
azureuser@flux-user000000:/opt/bare$ cat results/osu_allreduce/osu_allreduce-4-iter-* | grep "^64"64                     31.90
64                     34.20
64                     15.80
64                     15.14
64                     15.98
azureuser@flux-user000000:/opt/bare$ cat results/osu_allreduce/osu_allreduce-8-iter-* | grep "^64"64                     24.81
64                     20.26
64                     19.11
64                     19.46
64                     20.51
azureuser@flux-user000000:/opt/bare$ cat results/osu_allreduce/osu_allreduce-16-iter-* | grep "^64"
64                     34.89
64                     27.72
64                     31.95
64                     28.14
64                     26.91
azureuser@flux-user000000:/opt/bare$ cat results/osu_allreduce/osu_allreduce-32-iter-* | grep "^64"
64                     46.16
64                     36.39
64                     37.43
64                     33.94
64                     34.27
```

### usernetes
```
azureuser@flux-user000000:/opt/usernetes$ cat results/osu_allreduce/osu_allreduce-4-iter-* | grep "^64"
64                     15.27
64                     20.48
64                     17.12
64                     34.58
64                     16.64
azureuser@flux-user000000:/opt/usernetes$ cat results/osu_allreduce/osu_allreduce-8-iter-* | grep "^64"
64                     20.54
64                     21.84
64                     21.73
64                     22.74
64                     20.41
azureuser@flux-user000000:/opt/usernetes$ cat results/osu_allreduce/osu_allreduce-16-iter-* | grep "^64"
64                     31.48
64                     54.88
64                     37.48
64                     30.30
64                     30.46
azureuser@flux-user000000:/opt/usernetes$ cat results/osu_allreduce/osu_allreduce-32-iter-* | grep "^64"
64                     60.69
64                     74.53
64                     72.86
64                    102.33
64                     53.65
```
