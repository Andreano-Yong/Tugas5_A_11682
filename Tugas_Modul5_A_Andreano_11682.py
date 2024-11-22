import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Definisikan jalur model

model_path = r'C:\Tugas5_A_11682\best_model_tf.h5'

# Muat model
if os.path.exists(model_path):
    try:
        tf.get_logger().setLevel('ERROR')
        model = tf.keras.models.load_model(model_path, compile=False)

        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
        'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

        def preprocess_image(image):
            image = image.resize((28, 28))
            image = image.convert('L')
            image_array = np.array(image) / 255.0
            image_array = image_array.reshape(1, 28, 28, 1)
            return image_array

        # UI Streamlit
        st.title("Fashion MNIST Image Classifier 1682") #
        st.write("Unggah satu atau lebih gambar item fashion (misalnya sepatu, tas, baju), dan model akan memprediksi kelasnya.")
        
        # File uploader untuk input beberapa gambar
        uploaded_files = st.file_uploader("Pilih gambar ... ", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        # Sidebar untuk tombol prediksi
        with st.sidebar:
            predict_button = st.button("Predict")

        # Tampilkan gambar yang diunggah
        if uploaded_files:
            images = [Image.open(file) for file in uploaded_files]
            st.image(images, caption=[file.name for file in uploaded_files], use_column_width=True)

        # Jika tombol prediksi di sidebar ditekan
        if predict_button:
            st.sidebar.write("### Hasil Prediksi")

            # Proses setiap gambar yang diunggah
            for file, image in zip(uploaded_files, images):
            # Proses gambar dan prediksi
                processed_image = preprocess_image(image)
                predictions = model.predict(processed_image)[0]

                # Mendapatkan kelas dan confidence dengan softmax
                predicted_class = np.argmax(predictions)
                confidence = predictions[predicted_class] * 100 # Confidence dalam persentase

                # Tampilkan hasil prediksi untuk setiap gambar di sidebar
                st.sidebar.write(f"#### {file.name}")
                st.sidebar.write(f"Kelas Prediksi: **{class_names[predicted_class]}**")
                st.sidebar.write(f"Confidence: **{confidence :.2f}%**")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.error("File model tidak ditemukan.")


