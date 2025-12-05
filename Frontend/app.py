import streamlit as st
import cv2
import numpy as np
from streamlit.runtime.uploaded_file_manager import UploadedFile
import io

def apply_filters(img, filters):
    """Apply selected filters to the image."""
    result = img.copy()
    
    if "Blur" in filters:
        result = cv2.GaussianBlur(result, (15, 15), 0)
    
    if "Sharpen" in filters:
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        result = cv2.filter2D(result, -1, kernel)
    
    if "Edge Detection" in filters:
        if len(result.shape) == 3:
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        else:
            result = cv2.Canny(result, 100, 200)
    
    if "Invert" in filters:
        result = cv2.bitwise_not(result)
    
    return result

def image_tuner(file: UploadedFile, image_type: str, width: int, height: int, 
                brightness: int, contrast: float, filters: list):
    """Processes an uploaded image file based on specified parameters."""
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    
    if image_type == "Grayscale":
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    elif image_type == "Binary":
        gray_img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        _, img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    elif image_type == "Color (BGR)":
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    elif image_type == "Color (RGB)":
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        st.error("Invalid image type selected.")
        return None, None
    
    original = img.copy()
    
    # Resize
    img = cv2.resize(img, (width, height))
    
    # Adjust brightness and contrast
    if len(img.shape) == 3:
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
    else:
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
    
    # Apply filters
    if filters:
        img = apply_filters(img, filters)
    
    return original, img

def show_image_info(img, label):
    """Display information about the image."""
    if img is not None:
        st.write(f"**{label} Info:**")
        if len(img.shape) == 3:
            st.write(f"- Shape: {img.shape[1]}x{img.shape[0]} pixels, {img.shape[2]} channels")
        else:
            st.write(f"- Shape: {img.shape[1]}x{img.shape[0]} pixels, 1 channel (grayscale)")
        st.write(f"- Data type: {img.dtype}")
        st.write(f"- Min/Max values: {img.min()} / {img.max()}")

def main():
    st.set_page_config(page_title="Image Processing Playground", layout="wide")
    
    st.title("🎨 Image Processing Playground")
    st.markdown("*Learn about image processing by experimenting with different parameters and filters*")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("📁 Upload Image")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            st.divider()
            st.header("🎛️ Image Controls")
            
            image_type = st.selectbox(
                "Color Mode",
                ["Color (RGB)", "Color (BGR)", "Grayscale", "Binary"],
                help="RGB is standard for display, BGR is OpenCV's default format"
            )
            
            st.subheader("Dimensions")
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Width", min_value=50, max_value=2000, value=400)
            with col2:
                height = st.number_input("Height", min_value=50, max_value=2000, value=400)
            
            st.subheader("Adjustments")
            brightness = st.slider("Brightness", -100, 100, 0, 
                                   help="Negative values darken, positive values brighten")
            contrast = st.slider("Contrast", 0.5, 3.0, 1.0, 0.1,
                                help="Values < 1 decrease contrast, > 1 increase contrast")
            
            st.subheader("Filters")
            filters = st.multiselect(
                "Apply Filters",
                ["Blur", "Sharpen", "Edge Detection", "Invert"],
                help="Select one or more filters to apply"
            )
            
            process_button = st.button("🚀 Process Image", type="primary", width='stretch')
    
    # Main content area
    if uploaded_file is None:
        st.info("👆 Please upload an image from the sidebar to get started!")
        
        # Educational content
        st.subheader("📚 What You'll Learn")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Color Modes**
            - RGB vs BGR formats
            - Grayscale conversion
            - Binary thresholding
            """)
        
        with col2:
            st.markdown("""
            **Image Properties**
            - Dimensions and channels
            - Pixel value ranges
            - Data types
            """)
        
        with col3:
            st.markdown("""
            **Transformations**
            - Resizing images
            - Brightness & contrast
            - Filters and effects
            """)
    
    else:
        if process_button:
            with st.spinner("Processing image..."):
                original, processed_img = image_tuner(
                    uploaded_file, image_type, width, height, 
                    brightness, contrast, filters
                )
                
                if processed_img is not None:
                    # Display images side by side
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📷 Original Image")
                        st.image(uploaded_file, width="stretch")
                        show_image_info(original, "Original")
                    
                    with col2:
                        st.subheader("✨ Processed Image")
                        st.image(processed_img, width="stretch")
                        show_image_info(processed_img, "Processed")
                    
                    # Show what was applied
                    st.divider()
                    st.subheader("🔧 Applied Transformations")
                    
                    transformations = []
                    if image_type != "Color (RGB)":
                        transformations.append(f"Color mode: {image_type}")
                    transformations.append(f"Resized to: {width}x{height}px")
                    if brightness != 0:
                        transformations.append(f"Brightness: {brightness:+d}")
                    if contrast != 1.0:
                        transformations.append(f"Contrast: {contrast}x")
                    if filters:
                        transformations.append(f"Filters: {', '.join(filters)}")
                    
                    for i, transform in enumerate(transformations, 1):
                        st.write(f"{i}. {transform}")
                    
                    # Educational tips
                    with st.expander("💡 Learn More"):
                        st.markdown("""
                        **Understanding Image Processing:**
                        
                        - **Brightness** adds or subtracts a constant value to all pixels
                        - **Contrast** multiplies pixel values, expanding or compressing the range
                        - **Blur** averages neighboring pixels for a smooth effect
                        - **Sharpen** enhances edges by emphasizing differences between pixels
                        - **Edge Detection** finds boundaries where pixel intensity changes rapidly
                        - **Binary** images have only two values (0 or 255), useful for masks and segmentation
                        """)
                    
                    st.divider()
                    # Add download button for the processed image
                    is_success, buffer = cv2.imencode(".png", processed_img)
                    if is_success:
                        st.download_button(
                            label="💾 Download Processed Image",
                            data=buffer.tobytes(),
                            file_name="processed_image.png",
                            mime="image/png",
                            type="primary"
                        )
                else:
                    st.error("Error processing the image. Please check the parameters.")

if __name__ == "__main__":
    main()