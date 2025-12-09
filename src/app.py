import streamlit as st

st.title("🍱 Meal Analyzer")
st.write("Welcome! Enter your meal to get calorie estimation, nutrition balance & personalized feedback.")

# User input for meal text
meal_text = st.text_input("🍽 What did you eat? (ex: 'chicken breast 200g, rice 1 bowl, salad')")

# Analyze button
if st.button("🔍 Analyze Meal"):
    if not meal_text.strip():
        st.warning("⚠ Please enter your meal before analyzing.")
    else:
        st.write("📌 Meal Entered:", meal_text)
        st.write("⏳ Processing analysis... (features coming soon)")
        
        # Placeholder results
        st.subheader("Estimated Results")
        st.write("🔥 Estimated Calories: **~520 kcal**")
        st.write("🥗 Nutrient Breakdown:")
        st.write("- Protein: ~35g")
        st.write("- Carbs: ~50g")
        st.write("- Fat: ~15g")

        st.subheader("💡 Health Feedback")
        st.write("✔ Good protein source! Consider reducing carbs for better balance.")

        st.subheader("🌱 Recommended Alternatives")
        st.write("- Replace white rice with brown rice or quinoa")
        st.write("- Add a source of healthy fat (avocado or nuts)")

st.caption("⚠ Analysis results are placeholders. Real logic will be implemented soon.")
