# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import string
import re
import random
import spacy
import json
import numpy as np

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_token = 0
EOS_token = 1

nlp = spacy.load('en_core_web_lg')

def read_data(numbers=200):
    file_name = '/Users/vedmathai/Documents/python/initial_data.json'
    with open(file_name, 'rt') as f:
        fjson = json.load(f)
    vectors = []
    answers = []
    for i in range(numbers):
        event1 = np.random.choice(fjson)
        if np.random.randint(2) == 0:
            event2 = np.random.choice(fjson)
            ans = 0
        else:
            event2 = event1
            ans = 1
        mention1 = np.random.choice(event1)
        mention2 = np.random.choice(event2)

        keys = ['sentences', 'sentence', 'clause', 'tokens']
        vectors1 = [sentence2vecs(mention1[key]) for key in keys]
        vectors2 = [sentence2vecs(mention2[key]) for key in keys]
        vectors += [vectors1 + vectors2]
        answers += [ans]
    return vectors, answers

def sentence2vecs(sentence):
    tokens = nlp(sentence)
    vec = []
    for word in tokens:
        vec += [word.vector]
    return vec

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.gru = nn.GRU(input_size, hidden_size)

    def forward(self, input, hidden):
        output, hidden = self.gru(input, hidden)
        return hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)

class ConvNet(nn.Module):

    def __init__(self):
        super(ConvNet, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(1512, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        # x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.sigmoid(self.fc3(x))
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


teacher_forcing_ratio = 0.5


def train(inputs, target, encoders, conv_net, optimizers, criterion):
    for encoder in encoders:
        encoder.zero_grad()
    conv_net.zero_grad()

    target_length = target.size(0)

    loss = 0
    conv_input = []
    for input_vectorsi, inp_vectors in enumerate(inputs):
        encoder = encoders[input_vectorsi]
        encoder_hidden = encoder.initHidden()
        input_length = len(inp_vectors)
        for ei in range(input_length):
            encoder_hidden = encoder(torch.tensor([inp_vectors[ei]]).unsqueeze(0), encoder_hidden)
        conv_input += [encoder_hidden]

    conv_input = torch.stack(conv_input).permute(2, 1, 0, 3)
    conv_output = conv_net(conv_input)

    loss += criterion(conv_output, target)
    loss.backward()

    for optimizer in optimizers:
        optimizer.step()

    return loss.item() / target_length


######################################################################
# This is a helper function to print time elapsed and estimated time
# remaining given the current time and progress %.
#

import time
import math


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))


######################################################################
# The whole training process looks like this:
#
# -  Start a timer
# -  Initialize optimizers and criterion
# -  Create set of training pairs
# -  Start empty losses array for plotting
#
# Then we call ``train`` many times and occasionally print the progress (%
# of examples, time so far, estimated time) and average loss.
#

def trainIters(encoders, conv_net, n_iters, print_every=100, plot_every=100, learning_rate=0.01):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    optimizers = []
    for i in range(8):
        optimizers += [optim.SGD(encoders[i].parameters(), lr=learning_rate)]
    optimizers += [optim.SGD(conv_net.parameters(), lr=learning_rate)]
    batch_size = 100
    input_set, target_set = read_data(batch_size+10)
    criterion = nn.CrossEntropyLoss()

    for iter in range(1, n_iters + 1):
        if iter % batch_size == 0:
            input_set, target_set = read_data(batch_size+10)
        input_tensors = input_set[(iter-1) % batch_size]

        target_tensor = torch.tensor(target_set[(iter-1) % batch_size]).unsqueeze(0)

        loss = train(input_tensors, target_tensor, encoders,
                     conv_net, optimizers, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                         iter, iter / n_iters * 100, print_loss_avg))

        """
        if iter % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0
        """
    # showPlot(plot_losses)


######################################################################
# Plotting results
# ----------------
#
# Plotting is done with matplotlib, using the array of loss values
# ``plot_losses`` saved while training.
#

#import matplotlib.pyplot as plt
#plt.switch_backend('agg')
#import matplotlib.ticker as ticker
#import numpy as np


#def showPlot(points):
#    plt.figure()
#    fig, ax = plt.subplots()
#    # this locator puts ticks at regular intervals
#    loc = ticker.MultipleLocator(base=0.2)
#    ax.yaxis.set_major_locator(loc)
#    plt.plot(points)


######################################################################
# Evaluation
# ==========
#
# Evaluation is mostly the same as training, but there are no targets so
# we simply feed the decoder's predictions back to itself for each step.
# Every time it predicts a word we add it to the output string, and if it
# predicts the EOS token we stop there. We also store the decoder's
# attention outputs for display later.
#

def evaluate(encoder, decoder, sentence):
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1]


######################################################################
# We can evaluate random sentences from the training set and print out the
# input, target, and output to make some subjective quality judgements:
#

def evaluateRandomly(encoder, decoder, n=10):
    for i in range(n):
        pair = random.choice(pairs)
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions = evaluate(encoder, decoder, pair[0])
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')


######################################################################
# Training and Evaluating
# =======================
#
# With all these helper functions in place (it looks like extra work, but
# it makes it easier to run multiple experiments) we can actually
# initialize a network and start training.
#
# Remember that the input sentences were heavily filtered. For this small
# dataset we can use relatively small networks of 256 hidden nodes and a
# single GRU layer. After about 40 minutes on a MacBook CPU we'll get some
# reasonable results.
#
# .. Note::
#    If you run this notebook you can train, interrupt the kernel,
#    evaluate, and continue training later. Comment out the lines where the
#    encoder and decoder are initialized and run ``trainIters`` again.
#

hidden_size = 256
encoders = []
for i in range(8):
    encoders += [EncoderRNN(300, hidden_size).to(device)]
conv_net = ConvNet().to(device)

trainIters(encoders, conv_net, 75000, print_every=100)

######################################################################
#

#evaluateRandomly(encoder1, attn_decoder1)


######################################################################
# Visualizing Attention
# ---------------------
#
# A useful property of the attention mechanism is its highly interpretable
# outputs. Because it is used to weight specific encoder outputs of the
# input sequence, we can imagine looking where the network is focused most
# at each time step.
#
# You could simply run ``plt.matshow(attentions)`` to see attention output
# displayed as a matrix, with the columns being input steps and rows being
# output steps:
#

#output_words, attentions = evaluate(
#    encoder1, attn_decoder1, "je suis trop froid .")
#plt.matshow(attentions.numpy())
