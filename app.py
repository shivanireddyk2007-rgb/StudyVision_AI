import streamlit as st
from PIL import Image

from database import (
    initialize_database,
    add_subject,
    get_subjects,
    save_history,
    get_history,
    save_quiz_result,
    get_quiz_results,
    save_document,
    get_documents
)

from utils.auth import (
    show_login,
    logout
)

from utils.ai import (
    ask_ai,
    analyze_image,
    answer_from_document,
    summarize,
    generate_exam_answer,
    generate_quiz
)

from utils.pdf_utils import (
    extract_pdf_text,
    split_text
)

from utils.rag import (
    build_context
)


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudyVision AI",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

initialize_database()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = []


if "pdf_chunks" not in st.session_state:

    st.session_state.pdf_chunks = []


if "pdf_name" not in st.session_state:

    st.session_state.pdf_name = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 45px;
        font-weight: 800;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
    }

    .big-number {
        font-size: 32px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    show_login()

    st.stop()


# =========================================================
# USER INFORMATION
# =========================================================

user_id = st.session_state.user_id
user_name = st.session_state.user_name


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 StudyVision AI")

    st.write(
        f"Welcome, **{user_name}**"
    )

    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💬 AI Study Assistant",
            "🖼️ Image Solver",
            "📄 PDF RAG Assistant",
            "📝 Summarizer",
            "❓ Quiz Generator",
            "🎯 Exam Answer Generator",
            "📚 Subjects",
            "📊 Progress",
            "🕘 Study History"
        ]
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">'
        '🎓 StudyVision AI'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your intelligent AI-powered study companion'
        '</div>',
        unsafe_allow_html=True
    )

    history = get_history(user_id)

    results = get_quiz_results(user_id)

    documents = get_documents(user_id)

    subjects = get_subjects(user_id)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Subjects",
            len(subjects)
        )

    with col2:

        st.metric(
            "💬 Questions",
            len(history)
        )

    with col3:

        st.metric(
            "📄 Documents",
            len(documents)
        )

    with col4:

        st.metric(
            "❓ Quizzes",
            len(results)
        )

    st.divider()

    st.subheader(
        "🚀 StudyVision AI Features"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="card">

            ### 💬 AI Study Assistant

            Ask academic questions and receive
            easy-to-understand explanations.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="card">

            ### 🖼️ Multimodal AI

            Upload textbook images,
            handwritten questions,
            diagrams and screenshots.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="card">

            ### 📄 RAG PDF Assistant

            Upload notes and ask questions
            based on your study material.

            </div>
            """,
            unsafe_allow_html=True
        )

    c4, c5, c6 = st.columns(3)

    with c4:

        st.markdown(
            """
            <div class="card">

            ### ❓ AI Quiz

            Generate quizzes and track
            your performance.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c5:

        st.markdown(
            """
            <div class="card">

            ### 🎯 Exam Preparation

            Generate structured 5, 10
            and 15-mark answers.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c6:

        st.markdown(
            """
            <div class="card">

            ### 📊 Progress Tracking

            Monitor your quizzes,
            questions and study activity.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# AI STUDY ASSISTANT
# =========================================================

elif menu == "💬 AI Study Assistant":

    st.title("💬 AI Study Assistant")

    st.write(
        "Ask any academic question."
    )

    subject = st.selectbox(
        "Select subject",
        [
            "General",
            "Java",
            "Python",
            "Computer Organization",
            "Mathematics",
            "Accounting",
            "Other"
        ]
    )

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask your study question..."
    )

    if question:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "StudyVision AI is thinking..."
            ):

                try:

                    answer = ask_ai(
                        f"""
                        Subject: {subject}

                        Student Question:
                        {question}
                        """
                    )

                    st.markdown(answer)

                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                    save_history(
                        user_id,
                        subject,
                        question,
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"AI error: {e}"
                    )


# =========================================================
# IMAGE SOLVER
# =========================================================

elif menu == "🖼️ Image Solver":

    st.title(
        "🖼️ Multimodal AI Image Solver"
    )

    st.write(
        "Upload a question, diagram, textbook page "
        "or programming screenshot."
    )

    uploaded_image = st.file_uploader(
        "Upload image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]
    )

    if uploaded_image:

        image = Image.open(
            uploaded_image
        )

        st.image(
            image,
            caption="Uploaded Study Image",
            use_container_width=True
        )

        task = st.selectbox(
            "What should AI do?",
            [
                "Explain the question",
                "Solve the question",
                "Explain step by step",
                "Convert into exam answer",
                "Explain the diagram",
                "Extract text"
            ]
        )

        custom_question = st.text_area(
            "Additional instructions",
            placeholder="Optional..."
        )

        if st.button(
            "🔍 Analyze Image",
            use_container_width=True
        ):

            prompt = f"""
            Analyze the uploaded image.

            Task:
            {task}

            Additional instructions:
            {custom_question}

            Give a clear student-friendly answer.
            """

            with st.spinner(
                "Analyzing image..."
            ):

                try:

                    answer = analyze_image(
                        prompt,
                        uploaded_image.getvalue(),
                        uploaded_image.type
                    )

                    st.subheader(
                        "🤖 AI Result"
                    )

                    st.markdown(answer)

                    save_history(
                        user_id,
                        "Image Analysis",
                        task,
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"Image analysis failed: {e}"
                    )


# =========================================================
# PDF RAG ASSISTANT
# =========================================================

elif menu == "📄 PDF RAG Assistant":

    st.title(
        "📄 PDF RAG Study Assistant"
    )

    st.write(
        "Upload your notes and ask questions "
        "from the document."
    )

    col1, col2 = st.columns(2)

    with col1:

        subject = st.text_input(
            "Document subject",
            placeholder="Example: Java"
        )

    with col2:

        uploaded_pdf = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

    if uploaded_pdf:

        if (
            st.session_state.pdf_name
            != uploaded_pdf.name
        ):

            with st.spinner(
                "Processing PDF..."
            ):

                try:

                    text = extract_pdf_text(
                        uploaded_pdf
                    )

                    chunks = split_text(
                        text
                    )

                    st.session_state.pdf_chunks = chunks

                    st.session_state.pdf_name = (
                        uploaded_pdf.name
                    )

                    save_document(
                        user_id,
                        uploaded_pdf.name,
                        subject,
                        text
                    )

                    st.success(
                        f"PDF processed successfully. "
                        f"{len(chunks)} chunks created."
                    )

                except Exception as e:

                    st.error(
                        f"PDF processing failed: {e}"
                    )

    if st.session_state.pdf_chunks:

        st.divider()

        st.success(
            f"Active document: "
            f"{st.session_state.pdf_name}"
        )

        question = st.text_area(
            "Ask something about this PDF",
            placeholder=(
                "Example: Explain inheritance "
                "from these notes."
            )
        )

        if st.button(
            "🔎 Search & Answer",
            use_container_width=True
        ):

            if not question:

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Searching document..."
                ):

                    context = build_context(
                        question,
                        st.session_state.pdf_chunks,
                        top_k=5
                    )

                with st.spinner(
                    "Generating answer..."
                ):

                    try:

                        answer = answer_from_document(
                            question,
                            context
                        )

                        st.subheader(
                            "🤖 Answer"
                        )

                        st.markdown(answer)

                        with st.expander(
                            "🔎 Retrieved Context"
                        ):

                            st.write(
                                context
                            )

                        save_history(
                            user_id,
                            subject or "PDF",
                            question,
                            answer
                        )

                    except Exception as e:

                        st.error(
                            f"Error: {e}"
                        )


# =========================================================
# SUMMARIZER
# =========================================================

elif menu == "📝 Summarizer":

    st.title(
        "📝 AI Study Material Summarizer"
    )

    text = st.text_area(
        "Paste your study material",
        height=350
    )

    if st.button(
        "📝 Generate Summary",
        use_container_width=True
    ):

        if not text:

            st.warning(
                "Please enter study material."
            )

        else:

            with st.spinner(
                "Creating summary..."
            ):

                try:

                    result = summarize(
                        text
                    )

                    st.subheader(
                        "📚 Summary"
                    )

                    st.markdown(result)

                    save_history(
                        user_id,
                        "Summarizer",
                        "Summarize study material",
                        result
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


# =========================================================
# QUIZ GENERATOR
# =========================================================

elif menu == "❓ Quiz Generator":

    st.title(
        "❓ AI Quiz Generator"
    )

    topic = st.text_input(
        "Quiz topic",
        placeholder="Example: Java OOP"
    )

    number = st.slider(
        "Number of questions",
        3,
        10,
        5
    )

    if st.button(
        "🎯 Generate Quiz",
        use_container_width=True
    ):

        if not topic:

            st.warning(
                "Please enter a topic."
            )

        else:

            with st.spinner(
                "Generating quiz..."
            ):

                try:

                    quiz = generate_quiz(
                        topic,
                        number
                    )

                    st.session_state.current_quiz = quiz
                    st.session_state.quiz_topic = topic

                except Exception as e:

                    st.error(
                        f"Quiz generation failed: {e}"
                    )

    if "current_quiz" in st.session_state:

        quiz = st.session_state.current_quiz

        st.divider()

        st.subheader(
            "🧠 Answer the questions"
        )

        answers = []

        for i, item in enumerate(quiz):

            st.markdown(
                f"### Question {i + 1}"
            )

            st.write(
                item["question"]
            )

            selected = st.radio(
                "Choose an answer",
                item["options"],
                key=f"quiz_{i}",
                index=None
            )

            answers.append(
                selected
            )

        if st.button(
            "🏆 Submit Quiz",
            use_container_width=True
        ):

            score = 0

            for i, item in enumerate(quiz):

                correct_index = item[
                    "answer"
                ]

                if (
                    answers[i]
                    is not None
                    and
                    answers[i]
                    ==
                    item["options"][
                        correct_index
                    ]
                ):

                    score += 1

            total = len(quiz)

            percentage = (
                score / total
            ) * 100

            st.success(
                f"🎉 Score: {score}/{total} "
                f"({percentage:.1f}%)"
            )

            save_quiz_result(
                user_id,
                st.session_state.quiz_topic,
                score,
                total
            )

            st.subheader(
                "📖 Answer Review"
            )

            for i, item in enumerate(quiz):

                st.markdown(
                    f"**Question {i + 1}:** "
                    f"{item['question']}"
                )

                correct = item[
                    "options"
                ][item["answer"]]

                st.write(
                    f"✅ Correct answer: {correct}"
                )

                st.write(
                    item["explanation"]
                )


# =========================================================
# EXAM ANSWER
# =========================================================

elif menu == "🎯 Exam Answer Generator":

    st.title(
        "🎯 Exam Answer Generator"
    )

    topic = st.text_area(
        "Enter your exam question",
        placeholder=(
            "Example: Explain inheritance "
            "in Java."
        )
    )

    marks = st.selectbox(
        "Marks",
        [2, 5, 10, 15]
    )

    if st.button(
        "✍️ Generate Exam Answer",
        use_container_width=True
    ):

        if not topic:

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Preparing exam answer..."
            ):

                try:

                    answer = generate_exam_answer(
                        topic,
                        marks
                    )

                    st.markdown(answer)

                    save_history(
                        user_id,
                        "Exam Preparation",
                        topic,
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


# =========================================================
# SUBJECTS
# =========================================================

elif menu == "📚 Subjects":

    st.title(
        "📚 My Subjects"
    )

    new_subject = st.text_input(
        "Add a subject",
        placeholder="Example: Java"
    )

    if st.button(
        "➕ Add Subject"
    ):

        if new_subject:

            add_subject(
                user_id,
                new_subject
            )

            st.success(
                "Subject added!"
            )

            st.rerun()

        else:

            st.warning(
                "Enter a subject name."
            )

    st.divider()

    subjects = get_subjects(
        user_id
    )

    if subjects:

        for subject in subjects:

            st.write(
                f"📚 {subject[1]}"
            )

    else:

        st.info(
            "No subjects added yet."
        )


# =========================================================
# PROGRESS
# =========================================================

elif menu == "📊 Progress":

    st.title(
        "📊 My Learning Progress"
    )

    results = get_quiz_results(
        user_id
    )

    history = get_history(
        user_id
    )

    if results:

        total_quizzes = len(results)

        total_score = sum(
            row[1]
            for row in results
        )

        total_questions = sum(
            row[2]
            for row in results
        )

        average = (
            total_score /
            total_questions *
            100
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Quizzes",
                total_quizzes
            )

        with c2:

            st.metric(
                "Questions",
                total_questions
            )

        with c3:

            st.metric(
                "Average Score",
                f"{average:.1f}%"
            )

        st.divider()

        st.subheader(
            "🏆 Quiz Results"
        )

        for result in results:

            topic = result[0]
            score = result[1]
            total = result[2]
            date = result[3]

            percentage = (
                score / total
            ) * 100

            st.write(
                f"**{topic}** — "
                f"{score}/{total} "
                f"({percentage:.1f}%)"
            )

            st.caption(
                date
            )

            st.progress(
                percentage / 100
            )

    else:

        st.info(
            "Complete a quiz to see your progress."
        )

    st.divider()

    st.subheader(
        "📈 Study Activity"
    )

    st.write(
        f"You have completed "
        f"**{len(history)} study activities**."
    )


# =========================================================
# STUDY HISTORY
# =========================================================

elif menu == "🕘 Study History":

    st.title(
        "🕘 Study History"
    )

    history = get_history(
        user_id
    )

    if history:

        for item in history:

            subject = item[0]
            question = item[1]
            answer = item[2]
            date = item[3]

            with st.expander(
                f"{subject} — {question[:70]}"
            ):

                st.caption(date)

                st.markdown(
                    f"### Question\n{question}"
                )

                st.markdown(
                    f"### Answer\n{answer}"
                )

    else:

        st.info(
            "Your study history will appear here."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 StudyVision AI | "
    "Multimodal AI Study Assistant | "
    "Built with Python + Streamlit"
)