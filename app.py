import streamlit as st
from aiutils import add_boxes_to_image, generate_prompt, generate_response, extract_list

def main():
    st.title("Detect and Count Objects in an Image using Gemini AI")
    st.write("Upload an image and choose a task for analysis.")

    uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    selected_objects = None
    

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        select_prompt = """Enumerate all the objects found in the image. Some objects might
    appear multiple times. Only mention each object once. Output as a comma 
    separated list. Do not add any other information."""

        selected_objects = generate_response(select_prompt)

        st.write("Customize the list of objects to detect:")    
        selected_objects = st.text_input("Found Objects: ", selected_objects)
    else:
        st.warning("Please upload an image.")

    if st.button("Analyze Image"):
        with st.spinner("Processing..."):
            if selected_objects:
                object_list = [obj.strip() for obj in selected_objects if obj.strip()]
                prompt = generate_prompt(object_list)
                response, object_counts = add_boxes_to_image(uploaded_image, prompt)

                if response is not None:
                    st.image(response, caption="Image Analysis:", use_container_width=True)

                    st.subheader("Detected Objects:")
                    for obj, count in object_counts.items():
                        st.write(f"{obj}: {count}")
                        
                else:
                    st.write("Error: Could not display image.")
            else:
                st.warning("Mo objects were selected.")


if __name__ == "__main__":
    main()
