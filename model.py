import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from util import fir, read_wav, sample_rate_to_8K
from vad_dataset import VAD_Dataset
from pathlib import Path


class CNN(nn.Module):
    def __init__(
        self,
        input_channel=1,
        n_channel=2,
        kernel_size=2,
        stride=2,
        dilation=1,
        padding="valid",
    ) -> None:
        super(CNN, self).__init__()

        self.fc_size = 120 * 2
        model = nn.Sequential(
            nn.Conv2d(
                in_channels=input_channel,
                out_channels=n_channel,
                kernel_size=(1, kernel_size),
                stride=stride,
                dilation=dilation,
                padding=padding,
                bias=False,
            ),
            nn.BatchNorm2d(num_features=n_channel),
            nn.Flatten(),
            nn.LeakyReLU(inplace=True),
            nn.Linear(in_features=self.fc_size, out_features=2),
            nn.Softmax(dim=1)
        )
        self.model = model

    def forward(self, x):
        # x = fir(x)
        x = self.model(x)
        return x


if __name__ == "__main__":
    # signal,signal_len,sample_rate = read_wav(str('data_1.wav'))
    # # print(file_dir,sample_rate)
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )
    # signal,signal_len = sample_rate_to_8K(signal,sample_rate)
    datasets = VAD_Dataset()

    train_dataloader = DataLoader(datasets, batch_size=32, shuffle=True)
    test_dataloader = DataLoader(datasets, batch_size=32, shuffle=True)

    for X, y in test_dataloader:
        print(f"Shape of X: {X.shape}")
        print(f"Shape of y: {y.shape} {y.dtype}")
        break

    model = CNN().to(device)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4)

    def train(dataloader, model, loss_fn, optimizer):
        size = len(dataloader.dataset)
        model.train()
        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(device), y.to(device)

            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)

            # Backpropagation
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            if batch % 100 == 0:
                loss, current = loss.item(), (batch + 1) * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

    def test(dataloader, model, loss_fn):
        size = len(dataloader.dataset)
        num_batches = len(dataloader)
        model.eval()
        test_loss, correct = 0, 0
        with torch.no_grad():
            for X, y in dataloader:
                X, y = X.to(device), y.to(device)
                pred = model(X)
                test_loss += loss_fn(pred, y).item()
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        test_loss /= num_batches
        correct /= size
        print(
            f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
        )

    epochs = 10
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train(train_dataloader, model, loss_fn, optimizer)
        test(test_dataloader, model, loss_fn)
    print("Done!")

    dir_path = Path(__file__).parent
    torch.save(model.state_dict(), f"{dir_path}/model/model.pth")
