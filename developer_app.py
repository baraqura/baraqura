# ================================
# 🧠 BaraQura AI Developer Panel
# ================================

import streamlit as st  # 🔹 Streamlit UI
import os               # 🔹 File system access

# 🔹 Page config
st.set_page_config(page_title="BaraQura AI Developer Panel", layout="wide")

st.title("🧠 BaraQura AI Developer Panel")

# ================================
# 📁 Project Path
# ================================
BASE_PATH = "."

# ================================
# 📂 Get All Python Files
# ================================
def get_all_files(base_path):
    file_list = []

    # ❌ unwanted folder exclude
    exclude = {'.venv', 'venv', '__pycache__', '.git'}

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in exclude]

        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                file_list.append(full_path)

    return file_list


# ================================
# 📂 File Dropdown
# ================================
files = get_all_files(BASE_PATH)

if not files:
    st.warning("⚠️ কোনো Python file পাওয়া যায়নি!")
    st.stop()

selected_file = st.selectbox("📂 কোন ফাইলে কাজ করবেন?", files)


# ================================
# 📄 Show Existing Code
# ================================
if selected_file:
    try:
        with open(selected_file, "r", encoding="utf-8") as f:
            existing_code = f.read()

        st.subheader(f"📄 Current Code: {selected_file}")
        st.code(existing_code, language="python")

    except Exception as e:
        st.error(f"❌ File read error: {e}")


# ================================
# ✏️ Code Input Section
# ================================
st.subheader("✏️ নতুন কোড যোগ করুন")

new_code = st.text_area(
    "এখানে কোড পেস্ট করুন",
    height=250,
    placeholder="Example:\nprint('Hello World')"
)


# ================================
# 🧪 Basic Syntax Check
# ================================
def check_syntax(code):
    try:
        compile(code, "<string>", "exec")  # 🔹 syntax check
        return True, None
    except Exception as e:
        return False, str(e)


# ================================
# 🚀 Add Code Button
# ================================
if st.button("🚀 কোড যুক্ত করুন"):

    # ❌ empty code check
    if not new_code.strip():
        st.warning("⚠️ কিছু কোড লিখুন!")
        st.stop()

    # 🧪 syntax check
    is_valid, error = check_syntax(new_code)

    if not is_valid:
        st.error(f"❌ Syntax Error:\n{error}")
        st.stop()

    # ✅ write code
    try:
        with open(selected_file, "a", encoding="utf-8") as f:
            f.write("\n\n# ===== New Code Added =====\n")
            f.write(new_code)

        st.success(f"✅ Code successfully added to {selected_file}")
        st.balloons()  # 🎈 success animation

        # 🔄 auto refresh
        st.rerun()

    except Exception as e:
        st.error(f"❌ Write Error: {e}")
