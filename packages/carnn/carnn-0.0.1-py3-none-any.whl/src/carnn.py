"""
Developer Name: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu

Description: carnn package for converting calcium imaging data into recurrent neural networks
"""
import torch
import torch.nn as nn
import torch.optim as optim
import time


#%% Continuous time recurrent neural networks

class CTRNN(nn.Module):
    """A continuous-time RNN implementation from https://colab.research.google.com/github/gyyang/nn-brain/blob/master/RNN_tutorial.ipynb#scrollTo=yellow-jason.


    Parameters:
        input_size: Number of input neurons
        hidden_size: Number of hidden neurons
        dt: discretization time step in ms.
            If None, dt equals time constant tau

    Inputs:
        input: tensor of shape (seq_len, batch, input_size)
        hidden: tensor of shape (batch, hidden_size), initial hidden activity
            if None, hidden is initialized through self.init_hidden()

    Outputs:
        output: tensor of shape (seq_len, batch, hidden_size)
        hidden: tensor of shape (batch, hidden_size), final hidden activity
    """

    def __init__(self, input_size, hidden_size, dt=None, **kwargs):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.tau = 100
        if dt is None:
            alpha = 1
        else:
            alpha = dt / self.tau
        self.alpha = alpha

        self.input2h = nn.Linear(input_size, hidden_size)
        self.h2h = nn.Linear(hidden_size, hidden_size)

    def init_hidden(self, input_shape):
        batch_size = input_shape[1]
        return torch.zeros(batch_size, self.hidden_size)

    def recurrence(self, input, hidden):
        """Run network for one time step.

        Inputs:
            input: tensor of shape (batch, input_size)
            hidden: tensor of shape (batch, hidden_size)

        Outputs:
            h_new: tensor of shape (batch, hidden_size),
                network activity at the next time step
        """
        h_new = torch.relu(self.input2h(input) + self.h2h(hidden))
        h_new = hidden * (1 - self.alpha) + h_new * self.alpha
        return h_new

    def forward(self, input, hidden=None):
        """Propogates the input through the network."""

        # If hidden activity is not provided, initialize it
        if hidden is None:
            hidden = self.init_hidden(input.shape).to(input.device)

        # Loop through time
        output = []
        steps = range(input.size(0))
        for i in steps:
            hidden = self.recurrence(input[i], hidden)
            output.append(hidden)

        # Stack together output from all time steps
        output = torch.stack(output, dim=0)  # (seq_len, batch, hidden_size)
        return output, hidden


class RNNNet(nn.Module):
    """Recurrent network model from https://colab.research.google.com/github/gyyang/nn-brain/blob/master/RNN_tutorial.ipynb#scrollTo=yellow-jason.

    Parameters:
        input_size: int, input size
        hidden_size: int, hidden size
        output_size: int, output size

    Inputs:
        x: tensor of shape (Seq Len, Batch, Input size)

    Outputs:
        out: tensor of shape (Seq Len, Batch, Output size)
        rnn_output: tensor of shape (Seq Len, Batch, Hidden size)
    """

    def __init__(self, input_size, hidden_size, output_size, **kwargs):
        super().__init__()

        # Continuous time RNN
        self.rnn = CTRNN(input_size, hidden_size, **kwargs)

        # Add an output layer
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        rnn_output, _ = self.rnn(x)
        out = self.fc(rnn_output)
        return out, rnn_output


class CaRNN():
    """
    A class used to convert calcium imaging data  to a recurrent neural network.

    """

    def __init__(self, data_path):
        self.input, self.neural_activity, self.time = self.prepare_data(data_path = data_path)
        self.net = RNNNet(input_size=self.input.shape[2], hidden_size=50, output_size=self.input.shape[2], dt=0.5)
        self.dataset = self.generate_dataset(seq=self.input,ws=1)
        self.predict_inputs, self.predict_labels = self.dataset

    def prepare_data(self, data_path):
        """
        Prepares input calcium imaging dataset for input into an RNN.

        Input data is returned as input and is a tensor.
        Neural activity is returned as neural_activity and is an numpy.ndarray
        The time vector is returned as time_data and is a numpy.ndarray.

        :param data_path:
        :return:
        """
        data = np.genfromtxt(data_path, delimiter=",")
        time_data = data[0, :] # only the time row
        neural_activity = data[1:, :] # all rows except the time row

        # Convert test_data to pytorch tensor object
        neural_activity = neural_activity.transpose()
        input = torch.from_numpy(neural_activity) # convert numpy array to a torch tensor
        input = input[:, None, :].to(torch.float32) # convert type to be consistent with the model datatype
        return input, neural_activity, time_data

    def train_model(self, epochs):
        """Helper function to train the model modified from https://colab.research.google.com/github/gyyang/nn-brain/blob/master/RNN_tutorial.ipynb#scrollTo=yellow-jason.

        Args:
            net: a pytorch nn.Module module
            dataset: a dataset object that when called produce a (input, target output) pair

        Returns:
            net: network object after training
        """

        # Use Adam optimizer
        optimizer = optim.Adam(self.net.parameters(), lr=0.01)
        # criterion = nn.CrossEntropyLoss() # does not support multi-target tensor
        criterion = nn.MSELoss()

        running_loss = 0
        running_acc = 0
        start_time = time.time()
        # Loop over training batches
        print('Training network...')
        for i in range(epochs):
            # # Generate input and target, convert to pytorch tensor
            inputs, labels = self.dataset
            for idx, input in enumerate(inputs):
                input = input.to(torch.float32)
                label = labels[idx].to(torch.float32)

                # standard pytorch training
                optimizer.zero_grad()  # zero the gradient buffers
                output, _ = self.net(input)
                output = output.flatten()

                loss = criterion(output, label)
                loss.backward()
                optimizer.step()  # Update is performed

            # Compute the running loss every 100 steps
            running_loss += loss.item()
            if i % 1 == 0:
                running_loss /= 100
                print('Step {}, Loss {:0.4f}, Time {:0.1f}s'.format(
                    i + 1, running_loss, time.time() - start_time))
                running_loss = 0
        return self.net

    def generate_dataset(self, seq, ws):
        """
        Generates the dataset consisting of windows and labels to be used for prediction.
        Each

        :param seq:
        :param ws:
        :return:
        """
        L = len(seq)
        windows = []
        labels = []
        for i in range(L - ws):
            window = seq[i:i + ws]
            label = seq[i + ws:i + ws + 1]
            windows.append(window)
            labels.append(label)

        return windows, labels

    def predict(self):
        """
        Predicts activity using network architecture and inputs.

        Will be adapted to accommodate different window sizes and to predict full sequences without updates.

        :param net:
        :param inputs:
        :return:
        """
        action_pred, rnn_activity = self.net(self.predict_inputs[0].to(torch.float32))
        activity_predicted = action_pred[0].detach().numpy().transpose()

        for i in range(len(self.predict_inputs[1:])):
            action_pred, rnn_activity = self.net(self.predict_inputs[i].to(torch.float32))
            activity_pred = action_pred[0].detach().numpy().transpose()
            activity_predicted = np.hstack((activity_predicted, activity_pred))

        return activity_predicted


#%% PCA functionality
# Import packages
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

def PCA_activity(activity: np.ndarray, num_components: int = 2):
    """
    Activity passed with shape (number of neurons, number of timepoints) is converted to a low-dimensional subspace
    size of num_components using PCA decomposition.

    :param activity:
    :param num_components:
    :return:
    """
    activity = activity.transpose() # activity (Time points, Neurons)
    pca = PCA(n_components=num_components)
    pca.fit(activity)  # activity (Time points, Neurons)
    activity_pc = pca.transform(activity)  # transform activity to low-dimension
    return activity_pc


def plot_PCA_activity(activity: np.ndarray, color='red'):
    """
    Activity passed with shape (number of neurons, number of timepoints) is converted to a low-dimensional subspace
    size of num_components using PCA decomposition and the activity is projected into the low-dimensional subspace
    to be plotted.

    :param activity:
    :return:
    """
    # Plot all trials in ax1, plot fewer trials in ax2
    fig = plt.plot(figsize=(6, 6))

    # Transform and plot each trial
    activity_pc = PCA_activity(activity, num_components=2)  # (Time points, PCs)
    plt.plot(activity_pc[:, 0], activity_pc[:, 1], '-', color=color, alpha=0.2)

    # Plot the beginning of a trial with a special symbol
    plt.plot(activity_pc[0, 0], activity_pc[0, 1], '^', color='black')

    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.show()