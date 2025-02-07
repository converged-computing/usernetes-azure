# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0
# https://github.com/google/learn-oss-with-google/tree/main/kubernetes/job-examples/ml_training_pytorch

import os, sys, logging
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.distributed as dist
from torchvision import datasets
from torchvision import transforms

# Set up logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
)
handler.setFormatter(formatter)
root.handlers.clear()
root.addHandler(handler)

NUM_EPOCHS = 8  # number of training passes over the training dataset

# dataset batch size; each batch gets evenly distributed across hosts and local devices per host
# This needs to fail if we get a non integer
BATCH_SIZE = int(os.environ.get("BATCH_SIZE") or 128)


# Similar to resnet?
# https://github.com/pytorch/vision/blob/fab1188094f7763920b000196589f18891f46db1/torchvision/models/resnet.py#L166
class MLP(nn.Module):
    def __init__(self, num_classes):
        super(MLP, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


# Load dataset and create dataloader
def load_dataset(rank, world_size):
    dataset = datasets.MNIST(
        f"./data_{rank}",
        train=True,
        download=True,
        transform=transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        ),
    )
    num_classes = len(set(dataset.targets.numpy()))
    sampler = torch.utils.data.distributed.DistributedSampler(
        dataset, num_replicas=world_size, rank=rank
    )
    # IMPORTANT: this might need to be adjusted to account for the world size
    # e.g., the batch size should be the world size // the number of processes the worker has?
    dataloader = torch.utils.data.DataLoader(
        dataset, batch_size=BATCH_SIZE, sampler=sampler
    )
    return dataloader, num_classes


# Average gradients across all ranks
def average_gradients(model):
    world_size = float(dist.get_world_size())
    for param in model.parameters():
        dist.all_reduce(param.grad.data, op=dist.ReduceOp.SUM)
        param.grad.data /= world_size


# Average loss across all ranks
def average_loss(train_loss, device):
    train_loss_tensor = torch.tensor(train_loss).to(device)
    dist.all_reduce(train_loss_tensor, op=dist.ReduceOp.SUM)
    return train_loss_tensor.item() / dist.get_world_size()


# Main training loop
def run():
    local_rank = int(os.environ["LOCAL_RANK"])
    rank = dist.get_rank()
    size = dist.get_world_size()
    logging.info(f"Rank {rank}: starting, world size={size}")
    torch.manual_seed(1234)

    train_set, num_classes = load_dataset(rank, size)
    logging.info(f"Rank {rank}: num_classes: {num_classes}")

    # Set up device and model
    if torch.cuda.is_available():
        device = torch.device(f"cuda:{local_rank}")
        torch.cuda.set_device(local_rank)
        model = MLP(num_classes).to(device)
        model = nn.parallel.DistributedDataParallel(
            model, device_ids=[local_rank], output_device=local_rank
        )
    else:
        device = torch.device(f"cpu")
        model = MLP(num_classes).to(device)
        model = nn.parallel.DistributedDataParallel(model)

    # Initialize the optimizer
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

    print(f"batch size: {BATCH_SIZE}")
    print(f"epochs: {NUM_EPOCHS}")
    print(f"world size: {dist.get_world_size()}")

    # Train the model
    for epoch in range(NUM_EPOCHS):
        logging.info(f"Rank {rank}, epoch={epoch+1}/{NUM_EPOCHS}: starting")

        epoch_loss = 0.0
        for train_batch_num, (data, target) in enumerate(train_set):
            data, target = data.to(device), target.to(device)
            mini_batch_size = len(data)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss_item = loss.item()
            epoch_loss += loss_item
            loss.backward()
            average_gradients(model)
            optimizer.step()
            # logging.debug(f"Rank {rank}: epoch: {epoch+1}/{NUM_EPOCHS}, batch: {train_batch_num+1}/{len(train_set)}, mini-batch size: {mini_batch_size}")
        avg_epoch_loss = average_loss(epoch_loss / len(train_set), device)
        logging.info(
            f"Rank {rank}: epoch {epoch+1}/{NUM_EPOCHS}, average epoch loss={avg_epoch_loss:.4f}"
        )
    logging.info(f"Rank {rank}: training completed.")


def _get_backend():
    if torch.cuda.is_available() and torch.cuda.nccl.is_available(
        [torch.rand(2, 2, device="cuda")]
    ):
        return "nccl"
    return "gloo"


if __name__ == "__main__":
    for key in [
        "LOCAL_RANK",
        "RANK",
        "GROUP_RANK",
        "ROLE_RANK",
        "LOCAL_WORLD_SIZE",
        "WORLD_SIZE",
        "ROLE_WORLD_SIZE",
        "MASTER_ADDR",
        "MASTER_PORT",
    ]:
        value = os.environ[key]
        logging.info(f"env: {key}={value}")
    dist.init_process_group(backend=_get_backend())
    run()
