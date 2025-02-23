import streamlit as st
import requests
from PIL import Image
import io

def main():
    st.title("Object Detection App")
    
    # Sidebar
    st.sidebar.header("Settings")
    threshold = st.sidebar.slider("Detection Threshold", 0.0, 1.0, 0.9, 0.1)
    endpoint = st.sidebar.selectbox(
        "Select Endpoint",
        ["object-count", "predict"]
    )

    # File uploader
    st.write("Upload an image for object detection")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Process button
        if st.button('Detect Objects'):
            with st.spinner('Processing...'):
                # API call
                files = {'file': uploaded_file}
                data = {'threshold': threshold}
                
                try:
                    response = requests.post(
                        f'http://localhost:5000/{endpoint}',
                        files=files,
                        data=data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if endpoint == "object-count":
                            st.subheader("Results:")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("Current Objects:")
                                for obj in result['current_objects']:
                                    st.write(f"- {obj['object_class']}: {obj['count']}")
                            
                            with col2:
                                st.write("Total Objects:")
                                for obj in result['total_objects']:
                                    st.write(f"- {obj['object_class']}: {obj['count']}")
                        else:
                            st.subheader("Predictions:")
                            for pred in result['predictions']:
                                st.write(f"Class: {pred['class_name']}")
                                st.write(f"Confidence: {pred['score']:.2%}")
                                
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

if __name__ == '__main__':
    main()