import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Gemini Pro
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image, prompt])
    return response.text

# Streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor", layout="wide")
st.header("Multilanguage Invoice Extractor")

# Input prompt and image upload
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Image...", type=['jpg', 'png', 'jpeg', 'webp'])

# Layout split into two columns
col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

if uploaded_file is not None:
    # Open the image using PIL
    image = Image.open(uploaded_file)
    with col1:  # Image on the left
        st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Process")

# Prompt for the model
prompt = (
    "You are an expert in document understanding, specializing in parsing and replicating invoice structures. "
    "Your task is to replicate the entire document sequentially in markdown format, maintaining the original structure "
    "of the document from top to bottom. This includes:\n\n"
    "- Extracting and replicating all text content as plain text in the markdown output.\n"
    "- Detecting and reproducing all tables in markdown table format exactly as they appear in the original document, "
    "with rows and columns maintained accurately.\n"
    "- Preserving any headings, subheadings, labels, and other text placement as close as possible to the original layout.\n"
    "- Ensuring the final markdown representation is an accurate, sequential reconstruction of the document without omitting any parts.\n\n"
    "Important notes:\n"
    "- Do not add any extra commentary or interpretation to the output.\n"
    "- The output should only contain the replicated content of the document in markdown format, structured as described.\n"
    "- For tables, ensure the alignment and data integrity are preserved while converting them to markdown table syntax.\n"
    "- Maintain text placement, such as line breaks, paragraphs, and indentation, as close as possible to the original document.\n"
)


if submit and uploaded_file is not None:
    try:
        # Call the Gemini model
        response = get_gemini_response(input_text, image, prompt)
        with col2:  # Markdown response on the right
            st.markdown(response, unsafe_allow_html=False)
    except Exception as e:
        st.error(f"An error occurred: {e}")
