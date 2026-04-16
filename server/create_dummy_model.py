import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

model = Sequential([
    Flatten(input_shape=(224, 224, 3)),
    Dense(64, activation='relu'),
    Dense(8, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy')

model.save("model.h5")

print("✅ Dummy model created successfully")