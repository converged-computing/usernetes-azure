"""run.py:"""
#!/usr/bin/env python
import os
import sys
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run():
    """ Distributed function to be implemented later. """
    rank = dist.get_rank()
    size = dist.get_world_size()
    print(f"Hello friend I am rank {rank} with size {size}")

def init_process(rank, size, fn, backend='mpi'):
    """ Initialize the distributed environment. """
    os.environ['MASTER_ADDR'] = '127.0.0.1'
    os.environ['MASTER_PORT'] = '29500'
    dist.init_process_group(backend)
    fn()

if __name__ == "__main__":
    init_process(0, 0, run, backend='mpi')
