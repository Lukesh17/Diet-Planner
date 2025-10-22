import streamlit as st
import requests

# --- Backend URL ---
# BACKEND_URL = ""  # change to your deployed API URL if hosted
BACKEND_URL = " http://localhost:8000"


# --- Page Setup ---
st.set_page_config(page_title="AI Health Management System", layout="wide", page_icon="🍎")
st.title("🍎 AI-Powered Health Management System")
st.markdown("### Personalized Nutrition & Fitness Recommendations using Gemini AI")

tab1, tab2, tab3 = st.tabs(["🏋️‍♂️ Health Profile", "🍽️ Food Analysis", "🧠 Health Insights"])

# --- Health Profile Tab ---
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
                if response.status_code == 200:
                    data = response.json()
                    if data.get("meal_plan"):
                        st.markdown("### 🥗 Your AI Meal Plan")
                        st.success(data["meal_plan"])
                    elif data.get("error"):
                        st.error(f"Backend error: {data['error']}")
                    else:
                        st.warning("No meal plan returned.")
                else:
                    st.error(f"Request failed: {response.status_code}")
                    st.write(response.text)
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Please start FastAPI on port 8000.")
            except Exception as e:
                st.error(f"Error fetching meal plan: {e}")

# --- Food Analysis Tab ---
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
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("food_analysis"):
                            st.markdown("### 🍛 Nutritional Analysis")
                            st.info(data["food_analysis"])
                        elif data.get("error"):
                            st.error(f"Backend error: {data['error']}")
                        else:
                            st.warning("No analysis returned.")
                    else:
                        st.error(f"Request failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")
                except Exception as e:
                    st.error(f"Error analyzing food: {e}")

# --- Health Query Tab ---
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
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("answer"):
                            st.markdown("### 🧬 Science-Backed Answer")
                            st.write(data["answer"])
                        elif data.get("error"):
                            st.error(f"Backend error: {data['error']}")
                        else:
                            st.warning("No answer returned.")
                    else:
                        st.error(f"Request failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")
                except Exception as e:
                    st.error(f"Error fetching answer: {e}")
