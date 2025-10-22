import streamlit as st
import requests

# --- Backend URL ---
BACKEND_URL = "https://ai-health-backend-vklb.onrender.com"  # Make sure no extra spaces

# --- Page Setup ---
st.set_page_config(
    page_title="AI Health Management System",
    layout="wide",
    page_icon="🍎"
)
st.title("🍎 AI-Powered Health Management System")
st.markdown("### Personalized Nutrition & Fitness Recommendations using Gemini AI")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([
    "🏋️‍♂️ Health Profile",
    "🍽️ Food Analysis",
    "🧠 Health Insights"
])

# --- Tab 1: Health Profile ---
with tab1:
    st.subheader("Upload Your Health Profile")

    with st.form("health_form"):
        age = st.number_input("Age", 1, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", 100, 250)
        weight = st.number_input("Weight (kg)", 30, 200)
        goal = st.text_input("Goal (e.g. Weight loss, Muscle gain)")
        allergies = st.text_input("Allergies (comma-separated)")
        fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
        submitted = st.form_submit_button("Generate Meal Plan")

    if submitted:
        profile = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "goal": goal,
            "allergies": allergies,
            "fitness_level": fitness_level,
        }
        with st.spinner("🔄 Generating personalized meal plan..."):
            try:
                response = requests.post(f"{BACKEND_URL}/generate_meal_plan/", json=profile)
                response.raise_for_status()
                data = response.json()
                if data.get("meal_plan"):
                    st.markdown("### 🥗 Your AI Meal Plan")
                    st.success(data["meal_plan"])
                else:
                    st.warning(data.get("error", "No meal plan returned."))
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Cannot connect to backend or request failed: {e}")

# --- Tab 2: Food Analysis ---
with tab2:
    st.subheader("Upload a Food Image for Nutrition Analysis")
    food_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

    if food_file:
        st.image(food_file, caption="Uploaded Image", use_container_width=True)
        if st.button("Analyze Food"):
            with st.spinner("🔍 Analyzing food..."):
                try:
                    files = {"file": (food_file.name, food_file, "image/jpeg")}
                    response = requests.post(f"{BACKEND_URL}/analyze_food/", files=files)
                    response.raise_for_status()
                    data = response.json()
                    if data.get("food_analysis"):
                        st.markdown("### 🍛 Nutritional Analysis")
                        st.info(data["food_analysis"])
                    else:
                        st.warning(data.get("error", "No analysis returned."))
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Cannot connect to backend or request failed: {e}")

# --- Tab 3: Health Queries ---
with tab3:
    st.subheader("Ask Health or Nutrition Questions")
    query = st.text_input("Enter your question")
    if st.button("Get Answer"):
        if not query.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("💡 Fetching scientific insights..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/health_query/", data={"query": query})
                    response.raise_for_status()
                    data = response.json()
                    if data.get("answer"):
                        st.markdown("### 🧬 Science-Backed Answer")
                        st.write(data["answer"])
                    else:
                        st.warning(data.get("error", "No answer returned."))
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Cannot connect to backend or request failed: {e}")
# --- End of File ---