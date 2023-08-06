import torch
import torch.nn.functional as F


def kl_divergence(z_mean, z_stddev):
    
    mean_sq = z_mean * z_mean
    stddev_sq = z_stddev * z_stddev
    
    return 0.5 * torch.mean(mean_sq + stddev_sq - torch.log(stddev_sq) - 1)


def binary_cross_entropy(recon_x, x):
    return F.binary_cross_entropy(recon_x, x) # 'sum'


def mse_loss(recon_x,x):
    return F.mse_loss(recon_x, x)


def cross_entropy(recon_x, x):
    return F.cross_entropy(recon_x, x)


def compute_kernel(x, y):
    x_size = x.size(0)
    y_size = y.size(0)
    dim = x.size(1)
    x = x.unsqueeze(1) # (x_size, 1, dim)
    y = y.unsqueeze(0) # (1, y_size, dim)
    tiled_x = x.expand(x_size, y_size, dim)
    tiled_y = y.expand(x_size, y_size, dim)
    kernel_input = (tiled_x - tiled_y).pow(2).mean(2) / float(dim)
    
    return torch.exp(-kernel_input) # (x_size, y_size)

def compute_mmd(x, y):
    x_kernel = compute_kernel(x, x)
    y_kernel = compute_kernel(y, y)
    xy_kernel = compute_kernel(x, y)
    mmd = x_kernel.mean() + y_kernel.mean() - 2 * xy_kernel.mean()
    
    return mmd