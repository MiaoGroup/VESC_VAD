import torch

torch.set_printoptions(precision=20)

# Load the state dictionary from the model.pth file
state_dict = torch.load('./model/model.pth')

# Print all parameters with values
for param_tensor in state_dict:
    print(f'Parameter Name: {param_tensor}')
    print(f'Size: {state_dict[param_tensor].size()}')
    print(f'Values: {state_dict[param_tensor]}\n')
