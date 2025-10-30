import torch
print(torch.version.hip)   # should not be None
print(torch.cuda.is_available())  # may return False, but HIP backend is active
print(torch.backends.mps.is_available())  # ignore if False