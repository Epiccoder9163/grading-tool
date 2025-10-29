import torch

# Is HIP available
print(torch.version.hip)

# Is CUDA available
# note that cuda does apply to AMD graphics cards as well as Nvidia ones
print(torch.cuda.is_available())

# Are there any real devices available to accelerate on
print(torch.cuda.get_device_name(0))
