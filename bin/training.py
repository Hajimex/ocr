# coding: utf-8
import argparse
import sys
from keras.models import Sequential
from keras.layers import Dense, Activation

# as the first layer in a Sequential model
model = Sequential()
model.add(LSTM(32, input_shape=(10, 64)))