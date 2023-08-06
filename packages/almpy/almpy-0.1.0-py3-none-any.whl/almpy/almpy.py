import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math


def generate_base(NLayer=random.randint(3,6), NY=60, NX=60, smoothness=False, NZ=[]):
    """
    Function that generates a DataFrame model
    ===
    - Nlayer - number of layers
    - NY - number of rows
    - NX - number of columns
    - smoothness - sets single value in layer
    - NZ - bounds of the value of each layer if not smooth or value of each layer if smooth
    """
    NYlayer = round(NY/NLayer)

    if (len(NZ) < NLayer):
        NZ = []
        if smoothness:
            for i in range(NLayer):
                NZ.append(random.randint(50,600))
        else:
            for i in range(NLayer):
                temp = random.randint(50,600)
                percentage = 10
                NZ.append([temp - (temp/100) * percentage, temp + (temp/100) * percentage])


    def gen_layer(layerNumber):
        a = []
        for i in range(NX):
            if (smoothness):
                a.append(np.random.uniform(NZ[layerNumber], NZ[layerNumber]))
            else:
                a.append(np.random.uniform(NZ[layerNumber][0], NZ[layerNumber][1]))
        return a
    
    b = []
    for i in range(NLayer):
        for j in range(NYlayer):
            b.append(gen_layer(i))
    return pd.DataFrame(b)


def gen_slice(df, Y=None, L = random.randint(-45, 45), shiftType = 1, side = 1, shiftForce = 10):
    """
    Function that generate geological shift
    ===
    - df - your DataFrame
    - Y - column number of center geological shift (default = +-20% from center)
    - L - angle of geological shift
    - shiftType - 0 = down ; 1 = up
    - side - 0 = left ; 1 = right
    - shiftForce - force of the geological shift
    """
    columns = df.shape[1]
    rows = df.shape[0]

    if not Y:
        Y = random.randint((columns/2) - (columns/100)*20, (columns/2) + (columns/100)*20)

    temp = math.tan(math.radians(90-L))
    topLayerValue = np.median(df.values[:1])
    bottomLayerValue = np.median(df.values[rows-1:rows])

    Ystart = -((math.tan(math.radians(L)) * rows/2) - Y)

    for i in (range(columns) if shiftType else reversed(range(columns))):
        de2 = temp * (i - Ystart)
        for j in (range(rows) if shiftType else reversed(range(rows))):
            if (de2 >= j if side else de2 <= j):
                
                try:
                    df[i][j] = df[i][j + shiftForce if shiftType else j - shiftForce]
                except:
                    df[i][j] = bottomLayerValue if shiftType else topLayerValue

    return df


def gen_models(N, NY=60, NX=60, smoothness=False, shiftType=None, side=None, shiftForce=None):
    """
    Function that generate N models
    ===
    - N - number of models
    - NY - number of rows
    - NX - number of columns
    - smoothness - sets single value in layer

    - shiftType - 0 = down ; 1 = up (default = random)
    - side - 0 = left ; 1 = right (default = random)
    - shiftForce - force of the geological shift (default = 4-12)
    """

    models = []

    isDefault = [True if shiftType else False, True if side else False, shiftForce if type(shiftForce)==list else 1 if type(shiftForce)==int else 0] 

    for o in range(N):
        shiftType = shiftType if isDefault[0] else random.randint(0, 1)
        side = side if isDefault[1] else random.randint(0, 1)
        shiftForce = random.randint(isDefault[2][0], isDefault[2][1]) if type(isDefault[2])==list else shiftForce if isDefault[2] == 1 else random.randint(4,12)

        df = generate_base(NLayer=random.randint(3,6), NY=NY, NX=NX, smoothness=smoothness)
        df = gen_slice(df, L = random.randint(-45, 45), shiftType=shiftType, side=side, shiftForce=shiftForce)
        models.append(df)
    return models


def show(models, cmap='viridis'):
    """
    Function that show models or dataframe
    ===
    - models - your models
    - cmap - Colormap
    """

    if len(models) == 1 or isinstance(models, pd.DataFrame):
        plt.figure(figsize=(10, 6))
        plt.imshow(models, cmap)
        plt.show()
        return
    elif len(models) == 2:
        figure, axis = plt.subplots(1, 2)
        axis[0].imshow(models[0], cmap)
        axis[1].imshow(models[1], cmap)
        plt.show()
        return
    
    up =  math.ceil(len(models)**0.5)
    low =  round(len(models)**0.5)

    figure, axis = plt.subplots(low, up)
    
    for i in range(len(models)):
        axis[i//up, i%up].imshow(models[i], cmap)

    plt.show()