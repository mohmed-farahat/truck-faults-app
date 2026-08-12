import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Troubleshooting Assistant", page_icon="🚛")
st.title("🚛 Truck Maintenance & Faults Finder")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    truck_type = st.selectbox(
        "اختر نوع الشاحنة",
        ["Mercedes Actros MP3", "Volvo FM", "Mercedes Atego", "Other"],
    )
    user_query = st.text_input(
        "أدخل كود العطل أو الوصف (مثال: P0335 أو تأخير تشغيل):"
    )

    if st.button("بحث عن العطل"):
        prompt = f"""
        You are an expert heavy transport fleet engineer.
        Analyze this issue for {truck_type}: {user_query}.
        Provide output in BOTH English and Workshop Arabic:
        1. Component / القطعة (Keep English technical name + Arabic workshop term)
        2. Description / الوصف الفني
        3. Causes / الأسباب المحتملة
        4. Fix / خطوات الإصلاح
        5. Manual Reference / رقم الصفحة أو المخطط التقديري
        """
        with st.spinner("جاري التحليل..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
else:
    st.warning("يرجى إدخال Gemini API Key في القائمة الجانبية للبدء.")
