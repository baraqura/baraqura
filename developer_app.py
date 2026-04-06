
import streamlit as st
import os

st.set_page_config(page_title="BaraQura AI Developer Panel", layout="wide")

st.title("🧠 BaraQura AI Developer Panel")

# 📁 Project folder path
BASE_PATH = "."

# 📂 সব file collect করবে
def get_all_files(base_path):
    file_list = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                file_list.append(full_path)
    return file_list

# 📂 dropdown files
files = get_all_files(BASE_PATH)

selected_file = st.selectbox("📂 Select File", files)

# 📄 existing code দেখাবে
if selected_file:
    with open(selected_file, "r") as f:
        existing_code = f.read()

    st.subheader("📄 Existing Code")
    st.code(existing_code, language="python")

# ✏️ নতুন code input
st.subheader("✏️ Add New Code")
new_code = st.text_area("Paste your code here", height=200)

# 🚀 add button
if st.button("🚀 Add Code"):
    try:
        if selected_file and new_code:
            with open(selected_file, "a") as f:
                f.write("\n\n# ===== New Code Added =====\n")
                f.write(new_code)

            st.success("✅ Code added successfully!")

            # 🎈 Balloon effect
            st.balloons()

    except Exception as e:
        st.error(f"❌ Error: {e}")
