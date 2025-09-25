# app.py
import streamlit as st

# Conversion constants
LB_TO_KG = 0.45359237
IN_TO_M = 0.0254
FT_TO_IN = 12.0

def bmi_category(bmi: float):
    if bmi < 18.5:
        return "Underweight", "BMI < 18.5 — underweight. Consider healthy diet & guidance."
    elif bmi < 25:
        return "Normal weight", "BMI 18.5–24.9 — healthy range for many adults."
    elif bmi < 30:
        return "Overweight", "BMI 25–29.9 — overweight. Consider lifestyle review."
    elif bmi < 35:
        return "Obesity (Class I)", "BMI 30–34.9 — obesity class I. Medical advice may help."
    elif bmi < 40:
        return "Obesity (Class II)", "BMI 35–39.9 — obesity class II. Consult professional help."
    else:
        return "Obesity (Class III)", "BMI ≥ 40 — obesity class III. Seek medical guidance."

def calculate_bmi_from_inputs(units, weight_kg, height_cm, weight_lb, height_ft, height_in):
    # Returns (success: bool, display_text: str, downloadable_text: str)
    try:
        if units == "Metric":
            wkg = float(weight_kg)
            h_m = float(height_cm) / 100.0
            if wkg <= 0 or h_m <= 0:
                return False, "❗ Please enter positive values for weight and height.", ""
            bmi = wkg / (h_m ** 2)
            steps = (
                f"Weight = {wkg} kg\n"
                f"Height = {height_cm} cm = {h_m:.3f} m\n"
                f"BMI = {wkg} / ({h_m:.3f}^2) = {bmi:.1f} kg/m²"
            )
        else:
            wlb = float(weight_lb)
            hft = float(height_ft)
            hin = float(height_in)
            total_in = hft * FT_TO_IN + hin
            if wlb <= 0 or total_in <= 0:
                return False, "❗ Please enter positive values for weight and height.", ""
            wkg = wlb * LB_TO_KG
            h_m = total_in * IN_TO_M
            bmi = wkg / (h_m ** 2)
            steps = (
                f"Weight = {wlb} lb × {LB_TO_KG:.6f} = {wkg:.3f} kg\n"
                f"Height = {hft} ft + {hin} in = {total_in:.2f} in × {IN_TO_M:.6f} = {h_m:.3f} m\n"
                f"BMI = {wkg:.3f} / ({h_m:.3f}^2) = {bmi:.1f} kg/m²"
            )
    except ValueError:
        return False, "❗ Please enter valid numeric values.", ""

    category, note = bmi_category(bmi)
    result_display = (
        f"**BMI:** {bmi:.1f} kg/m²  \n"
        f"**Category:** {category}  \n\n"
        f"**Note:** {note}\n\n"
        f"---\n**Steps & conversions:**\n{steps}\n\n"
        f"**Disclaimer:** This tool is for educational purposes only, not medical advice."
    )

    downloadable = (
        f"BMI Result\n"
        f"==========\n"
        f"BMI: {bmi:.1f} kg/m^2\n"
        f"Category: {category}\n\n"
        f"Steps & conversions:\n{steps}\n\n"
        f"Disclaimer: Educational only.\n"
    )

    return True, result_display, downloadable

# --- Streamlit UI ---
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")
st.title("🧮 Simple BMI Calculator")
st.write("Enter your weight and height. Choose Metric (kg, cm) or Imperial (lb, ft+in).")

units = st.radio("Unit system", ("Metric", "Imperial"))

if units == "Metric":
    weight_kg = st.number_input("Weight (kg)", min_value=0.0, value=70.0, format="%.2f")
    height_cm = st.number_input("Height (cm)", min_value=0.0, value=170.0, format="%.1f")
    weight_lb = height_ft = height_in = None
else:
    weight_lb = st.number_input("Weight (lb)", min_value=0.0, value=154.0, format="%.2f")
    height_ft = st.number_input("Height (ft)", min_value=0.0, value=5.0, format="%.0f")
    height_in = st.number_input("Height (in)", min_value=0.0, value=7.0, format="%.1f")
    weight_kg = height_cm = None

if st.button("Calculate BMI"):
    ok, display_text, downloadable = calculate_bmi_from_inputs(
        units, weight_kg, height_cm, weight_lb, height_ft, height_in
    )
    if not ok:
        st.error(display_text)
    else:
        st.markdown(display_text)
        st.download_button(
            "Download result as text",
            data=downloadable,
            file_name="bmi_result.txt",
            mime="text/plain"
        )

st.markdown("---")
st.caption("BMI = weight (kg) ÷ (height (m))². This is a simple screening tool; consult a health professional for personalized advice.")
