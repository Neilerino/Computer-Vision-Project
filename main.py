import os
import cv2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from scipy.stats import itemfreq
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization, \
    GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from matplotlib.image import imread
import os
import numpy as np

def matrix_Bin(labels):
    labels_bin=np.array([])

    labels_name, labels0 = np.unique(labels, return_inverse=True)
    labels0
    
    for _, i in enumerate(itemfreq(labels0)[:,0].astype(int)):
        labels_bin0 = np.where(labels0 == itemfreq(labels0)[:,0][i], 1., 0.)
        labels_bin0 = labels_bin0.reshape(1,labels_bin0.shape[0])

        if (labels_bin.shape[0] == 0):
            labels_bin = labels_bin0
        else:
            labels_bin = np.concatenate((labels_bin,labels_bin0 ),axis=0)

    print("Nber SubVariables {0}".format(itemfreq(labels0)[:,0].shape[0]))
    labels_bin = labels_bin.transpose()
    print("Shape : {0}".format(labels_bin.shape))
    
    return labels_name, labels_bin


os.chdir('stanford-dogs-dataset/images/Images')
d = '.'
training_names = [os.path.join(d, o) for o in os.listdir(d)
                  if os.path.isdir(os.path.join(d, o))]

images = []
names = []
path = os.getcwd()
image_size = 128

for image_folder in training_names:
    for file_name in os.listdir(image_folder):
        if 'n02' in file_name :
            image = cv2.imread(path + '/' + image_folder[2:] + '/' + file_name)
            if image is None:
                print(file_name)
            images.append(cv2.resize(image, (image_size, image_size)))
            names.append(image_folder)

# y_train_raw = np.array(names, np.uint8)
x_train_raw = np.array(images, np.float32) / 255.
num_class = 120 #y_train_raw.shape[1]

labels_name, labels_bin = matrix_Bin(names)

train_x, test_x, train_y, test_y = train_test_split(x_train_raw, labels_bin, test_size=0.2)

batch_size = 128
epochs = 20
learning_rate = 0.001

model = Sequential()
model.add(BatchNormalization(input_shape=(image_size, image_size, 3)))
model.add(Conv2D(filters=16, kernel_size=3, kernel_initializer='he_normal', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())
model.add(Conv2D(filters=32, kernel_size=3, kernel_initializer='he_normal', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())
model.add(Conv2D(filters=64, kernel_size=3, kernel_initializer='he_normal', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())
model.add(Conv2D(filters=128, kernel_size=3, kernel_initializer='he_normal', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())
model.add(Conv2D(filters=256, kernel_size=3, kernel_initializer='he_normal', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())
model.add(GlobalAveragePooling2D())
model.add(Dense(num_class, activation='softmax'))
model.summary()

# opt = optimizers.Adam(lr = learning_rate)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

two_up = os.path.abspath(os.path.join(__file__ ,"../.."))
os.chdir(two_up)

checkpoint = ModelCheckpoint(filepath='checkpoints.hdf5', verbose=1, save_best_only=True)

history = model.fit(train_x, train_y, validation_data=(test_x, test_y), batch_size=batch_size,verbose=2, epochs=epochs, shuffle = True)

model.save('saved_model/my_model')
# save the model to disk
filename = 'finalized_model.sav'
# pickle.dump(model, open(filename, 'wb'))

# some time later...

# load the model from disk
#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)
