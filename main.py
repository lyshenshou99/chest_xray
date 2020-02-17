import os
from input_set import get_data

from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.callbacks import ReduceLROnPlateau , ModelCheckpoint
from keras.optimizers import RMSprop
from keras.utils.np_utils import to_categorical

from keras import backend as K
K.set_image_data_format('channels_first') 


def swish_activation(x):
    return (K.sigmoid(x) * x)


TRAIN_DIR = "./chest_xray/train/"
TEST_DIR = "./chest_xray/test/"

X_train, y_train = get_data(TRAIN_DIR)
X_test , y_test = get_data(TEST_DIR)

y_train = to_categorical(y_train, 2)
y_test = to_categorical(y_test, 2)

Pimages = os.listdir(TRAIN_DIR + "PNEUMONIA")
Nimages = os.listdir(TRAIN_DIR + "NORMAL")

lr_reduce = ReduceLROnPlateau(monitor='val_accuracy', factor=0.1, min_delta=0.0001, patience=1, verbose=1)

filepath="./weights.{epoch:02d}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, period=1)


X_train=X_train.reshape(5216,3,150,150)
X_test=X_test.reshape(624,3,150,150)



model = Sequential()
model.add(Conv2D(16, (3, 3), activation='relu', padding="same", input_shape=(3,150,150)))
model.add(Conv2D(16, (3, 3), padding="same", activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), activation='relu', padding="same", input_shape=(3,150,150)))
model.add(Conv2D(32, (3, 3), padding="same", activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu', padding="same"))
model.add(Conv2D(64, (3, 3), padding="same", activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(96, (3, 3), dilation_rate=(2, 2), activation='relu', padding="same"))
model.add(Conv2D(96, (3, 3), padding="valid", activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), dilation_rate=(2, 2), activation='relu', padding="same"))
model.add(Conv2D(128, (3, 3), padding="valid", activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(64, activation=swish_activation))
model.add(Dropout(0.4))
model.add(Dense(2 , activation='sigmoid'))

model.compile(loss='binary_crossentropy',
                  optimizer=RMSprop(lr=0.00005),
                  metrics=['accuracy'])

batch_size = 256
epochs = 6

model.fit(X_train, y_train, validation_data = (X_test , y_test) ,callbacks=[lr_reduce, checkpoint] ,epochs=epochs, verbose=2)

model.save(filepath)
