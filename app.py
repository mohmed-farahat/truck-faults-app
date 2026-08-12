import tempfile
import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Truck Diagnostic & Manuals Finder", page_icon="🚛"
)
st.title("🚛 مساعد أعطال وكتالوجات الشاحنات")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # استخدام موديل Gemini 1.5 Pro للتعامل مع ملفات الـ PDF والصور المعقدة
    model = genai.GenerativeModel("gemini-1.5-pro")

    st.sidebar.header("📁 رفع الكتالوجات والمخططات")
    uploaded_files = st.sidebar.file_uploader(
        "ارفع ملفات الـ PDF أو صور المخططات هنا:",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    truck_type = st.selectbox(
        "نوع الشاحنة / النظام:",
        ["Mercedes Actros MP3/MP4", "Volvo FM/FH", "ساعات عمل/هيدروليك", "عام"],
    )

    user_query = st.text_area(
        "أدخل كود العطل، الوصف الفني، أو السؤال عن القطعة:",
        placeholder="مثال: عطل P0335، أو سبب تأخير التشغيل والحرارة مرتفعة، أو استخراج صورة مخطط طلمبة الجاز...",
    )

    if st.button("🔍 بحث وتشخيص شامل"):
        if not user_query:
            st.warning("يرجى كتابة كود العطل أو استفسارك أولاً.")
        else:
            with st.spinner(
                "جاري فحص الكتالوجات والصور وتحليل العطل بواسطة الذكاء الاصطناعي..."
            ):
                content_payload = []

                # معالجة الملفات المرفقة (PDFs وصور)
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name

                        uploaded_gemini_file = genai.upload_file(tmp_path)
                        content_payload.append(uploaded_gemini_file)

                # صياغة الأمر الموجه للنموذج (Prompt)
                prompt = f"""
                أنت مهندس صيانة أسطول نقل ثقيل خبير (Fleet Maintenance Engineer).
                النظام / الشاحنة: {truck_type}
                استفسار المستخدم / كود العطل: {user_query}

                المطلوب:
                1. تحليل المشكلة بناءً على الكتالوجات والملفات المرفقة (إن وجدت) والخبرة الفنية.
                2. توضيح المكون الفني بالاسم الإنجليزي والاسم المتداول في الورش.
                3. الأسباب المحتملة للتأخير أو العطل بالترتيب من الأسهل للأصعب.
                4. خطوات الفحص والإصلاح الدقيقة (Troubleshooting Steps).
                5. الإشارة لرقم الصفحة أو اسم المخطط/الفيوز الموجود بالملفات المرفقة إن أمكن.
                """
                content_payload.append(prompt)

                response = model.generate_content(content_payload)
                st.markdown(response.text)
else:
    st.warning("يرجى إدخال Gemini API Key في القائمة الجانبية للبدء.")
