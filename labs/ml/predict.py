import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('number_recognition_model.h5')


def predict_image(img_path):
    img = image.load_img(img_path, target_size=(28, 28), color_mode='grayscale')
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    predictions = model.predict(img_array)
    predicted_label = np.argmax(predictions, axis=1)
    return predicted_label[0]


# Example usage
img_path = 'path_to_your_image.png'  # Replace with your image path
predicted_number = predict_image(img_path)
print(f'The predicted number is: {predicted_number}')
