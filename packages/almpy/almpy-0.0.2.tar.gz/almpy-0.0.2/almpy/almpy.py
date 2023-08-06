import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math


def generate_base(N=200, NLayer=3, NY=15, NZ=((1, 1.5), (2, 2.2), (2.5, 3))):
    """
    Function that generates a DataFrame model
    ===
    - N - number of columns 
    - Nlayer - number of layers
    - NY - number of rows in each layer
    - NZ - bounds of the value of each layer
    """
    b = []

    def gen_layer(layerNumber):
        a = []
        for i in range(N):
            a.append(np.random.uniform(NZ[layerNumber][0], NZ[layerNumber][1]))
        return a
    for i in range(NLayer):
        for j in range(NY):
            b.append(gen_layer(i))
    return pd.DataFrame(b)

# df = pd.read_csv('LAYER.txt', header = None, nrows=100, sep="   ")
# df = df.transpose()


def gen_slice(df, Y = random.randint(75, 125), L = random.random() * 45, type = 1, side = 1, shiftForce = 10):
    """
    Function that generate geological shift
    ===
    - df - your DataFrame
    - Y - column number at which the geological shift begins
    - L - angle of geological shift
    - type - 0 = down ; 1 = up
    - side - 0 = left ; 1 = right
    - shiftForce - force of the geological shift
    """

    temp = math.tan(math.radians(90-L))
    columns = df.shape[1]
    rows = df.shape[0]
    topLayerValue = np.median(df.values[:1])
    bottomLayerValue = np.median(df.values[rows-1:rows])

    for i in (range(columns) if type else reversed(range(columns))):
        de2 = temp * (i - Y) * (rows/columns)
        for j in (range(rows) if type else reversed(range(rows))):
            if (de2 >= j if side else de2 <= j):
                try:
                    df[i][j] = df[i][j + shiftForce if type else j - shiftForce]
                except:
                    df[i][j] = bottomLayerValue if type else topLayerValue
    return df


def show(df):
    """
    Function that show model
    ===
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(df)
    plt.show()