import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Truck Diagnostic & Knowledge Base", page_icon="🚛"
)
st.title("🚛 نظام تشخيص أعطال أسطول الشاحنات")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

    st.subheader("🔍 البحث الشامل في الكتالوجات والمخططات")

    truck_type = st.selectbox(
        "اختر نوع الشاحنة / النظام:",
        [
            "Mercedes Actros MP3",
            "Mercedes Actros MP4",
            "Volvo FM / FH (D13A / D13C)",
            "Mercedes Atego",
            "أنظمة هيدروليك وكهرباء عامة",
        ],
    )

    user_query = st.text_area(
        "أدخل كود العطل أو الوصف الفني أو اسم المكون المطلوب:",
        placeholder="مثال: GS 10، أو عطل P0335، أو سبب تأخير التشغيل، أو مخطط دائرة التبريد...",
    )

    if st.button("🔍 بحث وتشخيص من قاعدة بيانات الكتالوجات"):
        if not user_query:
            st.warning("يرجى كتابة كود العطل أو الاستفسار الفني.")
        else:
            with st.spinner(
                "جاري استعلام الكتالوجات وتحليل العطل بواسطة الذكاء الاصطناعي..."
            ):
                prompt = f"""
                أنت مهندس صيانة أسطول نقل ثقيل خبير متخصص في شاحنات المرسيدس والفولفو والمعدات.
                
                النظام / الشاحنة المطلوب فحصها: {truck_type}
                استفسار المهندس / الفني: {user_query}
                
                يرجى تقديم تقرير فني متكامل يشمل:
                1. اسم القطعة / المكون (الاسم الفني بالإنجليزية + الاسم المتداول في الورشة).
                2. التوصيف الفني للعطل والأسباب المحتملة مرتبة من الأكثر احتمالاً وأسهل فحصاً.
                3. خطوات الفحص والإصلاح التشخيصية (Troubleshooting Steps).
                4. القيم القياسية (Sensors values/Voltage) وملاحظات السلامة أثناء الصيانة.
                """

                try:
                    # الاعتماد المباشر على الموديل المستقر
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as err:
                    st.error(
                        f"حدث خطأ أثناء الاتصال: {err}\nيرجى التأكد من صحة الـ API Key وإعادة إدخاله."
                    )
else:
    st.warning("يرجى إدخال Gemini API Key في القائمة الجانبية للبدء.")
