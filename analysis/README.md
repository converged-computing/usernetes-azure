## Get data
Exemple to fetch data from oras (same process for all benchmarks, this is for OSU):

```
app=XXX
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-bare-$app
mkdir results/$app/bare
mv results/$app/*.* results/$app/bare/
oras pull ghcr.io/converged-computing/usernetes-azure/performance:azure-usernetes-$app
mkdir results/$app/bare
mv results/$app/*.* results/$app/usernetes
```

```
Then for most benchmarks, run first:
./parse.sh
And then report the data to graph.py (by hand)
Current data in graph.py is up to date.
```

