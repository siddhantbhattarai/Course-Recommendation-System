# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import shap

# Initialize Flask app
app = Flask(__name__)

# Load the saved model, label encoder, and feature columns
model_path = "Model-Development/best_course_recommendation_model_Logistic Regression.joblib"
model = joblib.load(model_path)
label_encoder = joblib.load('Model-Development/label_encoder.joblib')
feature_columns = joblib.load('Model-Development/feature_columns.joblib')

# Course metadata for immersive course previews
course_metadata = {
    "Cybersecurity": {
        "description": "Master cybersecurity strategies and skills in a realistic virtual simulation.",
        "vr_link": "https://example-vr-platform.com/cybersecurity-course",
        "preview_video": "https://example-platform.com/preview/cybersecurity-intro.mp4"
    },
    "E-Commerce Development": {
        "description": "Learn to build scalable and secure e-commerce platforms using modern frameworks.",
        "vr_link": "https://example-vr-platform.com/ecommerce-course",
        "preview_video": "https://example-platform.com/preview/ecommerce-intro.mp4"
    },
    "DevOps": {
        "description": "Explore the full DevOps lifecycle and implement CI/CD pipelines in a virtual lab.",
        "vr_link": "https://example-vr-platform.com/devops-course",
        "preview_video": "https://example-platform.com/preview/devops-intro.mp4"
    },
    "Computer Vision": {
        "description": "Understand computer vision algorithms and apply them in immersive AR/VR environments.",
        "vr_link": "https://example-vr-platform.com/computer-vision-course",
        "preview_video": "https://example-platform.com/preview/computer-vision-intro.mp4"
    },
    "Cloud Computing": {
        "description": "Learn cloud infrastructure and services through hands-on virtual labs.",
        "vr_link": "https://example-vr-platform.com/cloud-computing-course",
        "preview_video": "https://example-platform.com/preview/cloud-computing-intro.mp4"
    },
    "Quantum Computing": {
        "description": "Gain a practical understanding of quantum algorithms in a simulated metaverse lab.",
        "vr_link": "https://example-vr-platform.com/quantum-computing-course",
        "preview_video": "https://example-platform.com/preview/quantum-computing-intro.mp4"
    },
    "App Development": {
        "description": "Create mobile and web applications with collaborative design in virtual environments.",
        "vr_link": "https://example-vr-platform.com/app-development-course",
        "preview_video": "https://example-platform.com/preview/app-development-intro.mp4"
    },
    "Data Engineering": {
        "description": "Master data pipelines and big data processing with virtual hands-on exercises.",
        "vr_link": "https://example-vr-platform.com/data-engineering-course",
        "preview_video": "https://example-platform.com/preview/data-engineering-intro.mp4"
    },
    "Data Science": {
        "description": "Learn to analyze and visualize data with Python in an immersive VR platform.",
        "vr_link": "https://example-vr-platform.com/data-science-course",
        "preview_video": "https://example-platform.com/preview/data-science-intro.mp4"
    },
    "Artificial Intelligence": {
        "description": "Explore AI concepts, from neural networks to reinforcement learning, in a virtual metaverse lab.",
        "vr_link": "https://example-vr-platform.com/ai-course",
        "preview_video": "https://example-platform.com/preview/ai-intro.mp4"
    },
    "Big Data Analytics": {
        "description": "Analyze massive datasets with advanced tools and virtual collaboration features.",
        "vr_link": "https://example-vr-platform.com/big-data-analytics-course",
        "preview_video": "https://example-platform.com/preview/big-data-intro.mp4"
    },
    "Game Development": {
        "description": "Build immersive game worlds and learn real-time graphics programming in VR labs.",
        "vr_link": "https://example-vr-platform.com/game-development-course",
        "preview_video": "https://example-platform.com/preview/game-dev-intro.mp4"
    },
    "Natural Language Processing": {
        "description": "Design and train language models with interactive virtual projects.",
        "vr_link": "https://example-vr-platform.com/nlp-course",
        "preview_video": "https://example-platform.com/preview/nlp-intro.mp4"
    },
    "Full-Stack Development": {
        "description": "Learn end-to-end web and app development with virtual team collaboration environments.",
        "vr_link": "https://example-vr-platform.com/full-stack-course",
        "preview_video": "https://example-platform.com/preview/full-stack-intro.mp4"
    },
    "Machine Learning": {
        "description": "Master machine learning techniques with hands-on AR/VR-supported data experiments.",
        "vr_link": "https://example-vr-platform.com/ml-course",
        "preview_video": "https://example-platform.com/preview/ml-intro.mp4"
    },
    "IoT Development": {
        "description": "Design IoT systems and simulations using virtual smart devices in the metaverse.",
        "vr_link": "https://example-vr-platform.com/iot-course",
        "preview_video": "https://example-platform.com/preview/iot-intro.mp4"
    },
    "Networking": {
        "description": "Build and troubleshoot networks in a virtual environment with real-time collaboration.",
        "vr_link": "https://example-vr-platform.com/networking-course",
        "preview_video": "https://example-platform.com/preview/networking-intro.mp4"
    },
    "Blockchain": {
        "description": "Understand blockchain technology and build decentralized applications in virtual labs.",
        "vr_link": "https://example-vr-platform.com/blockchain-course",
        "preview_video": "https://example-platform.com/preview/blockchain-intro.mp4"
    },
    "UI/UX Design": {
        "description": "Design user interfaces and experiences using 3D modeling and interactive prototypes.",
        "vr_link": "https://example-vr-platform.com/ui-ux-course",
        "preview_video": "https://example-platform.com/preview/ui-ux-intro.mp4"
    },
    "Embedded Systems": {
        "description": "Simulate embedded hardware and software design with AR-based debugging tools.",
        "vr_link": "https://example-vr-platform.com/embedded-systems-course",
        "preview_video": "https://example-platform.com/preview/embedded-systems-intro.mp4"
    },
    "AR/VR Development": {
        "description": "Create interactive AR/VR experiences and optimize them for immersive learning environments.",
        "vr_link": "https://example-vr-platform.com/ar-vr-development-course",
        "preview_video": "https://example-platform.com/preview/ar-vr-intro.mp4"
    },
    "Business Intelligence": {
        "description": "Explore BI dashboards, reports, and data-driven decisions using immersive 3D data visualizations.",
        "vr_link": "https://example-vr-platform.com/bi-course",
        "preview_video": "https://example-platform.com/preview/bi-intro.mp4"
    },
    "Web Development": {
        "description": "Learn web development and test designs in real-time within a collaborative virtual workspace.",
        "vr_link": "https://example-vr-platform.com/web-dev-course",
        "preview_video": "https://example-platform.com/preview/web-dev-intro.mp4"
    },
    "Software Testing": {
        "description": "Master software testing techniques using simulated test cases in virtual environments.",
        "vr_link": "https://example-vr-platform.com/software-testing-course",
        "preview_video": "https://example-platform.com/preview/software-testing-intro.mp4"
    },
    "Digital Marketing": {
        "description": "Learn digital marketing strategies with real-time campaign simulations in AR environments.",
        "vr_link": "https://example-vr-platform.com/digital-marketing-course",
        "preview_video": "https://example-platform.com/preview/digital-marketing-intro.mp4"
    },
    "Python Programming, Linear Algebra, Statistics": {
    	"description": "Master Python programming and foundational math for machine learning.",
    	"vr_link": "https://example-vr-platform.com/python-course",
    	"preview_video": "https://example-platform.com/preview/python-intro.mp4"
    },
    "Machine Learning Basics": {
        "description": "Learn the fundamentals of machine learning in a collaborative virtual environment.",
        "vr_link": "https://example-vr-platform.com/ml-course",
        "preview_video": "https://example-platform.com/preview/ml-intro.mp4"
    },
}


# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to recommend courses based on user input
@app.route('/recommend-course', methods=['POST'])
def recommend_course():
    data = request.json
    print("Received Data: ", data)  # Debug input

    user_input = pd.DataFrame({
        'Area of Interest': [data.get('interest', '') if isinstance(data.get('interest', ''), str) else 'Unknown'],
        'Career Goal': [data.get('goal', '') if isinstance(data.get('goal', ''), str) else 'Unknown'],
        'Preferred Learning Style': [data.get('learning_style', '') if isinstance(data.get('learning_style', ''), str) else 'Unknown']
    })

    # One-hot encode the user input
    user_input_encoded = pd.get_dummies(user_input, columns=['Area of Interest', 'Career Goal', 'Preferred Learning Style'])
    user_input_encoded = user_input_encoded.reindex(columns=feature_columns, fill_value=0)

    try:
        course_encoded = model.predict(user_input_encoded)[0]
        recommended_course = label_encoder.inverse_transform([course_encoded])[0]
        message = "Based on your inputs, this course is recommended."
        immersive_data = course_metadata.get(recommended_course, {
            "description": "No immersive preview available for this course.",
            "vr_link": "",
            "preview_video": ""
        })
    except Exception as e:
        recommended_course = "N/A"
        message = f"Error during prediction: {str(e)}"
        immersive_data = {}

    return jsonify({
        "recommended_course": recommended_course,
        "message": message,
        "immersive_details": immersive_data
    })

# Route to log user feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_data = request.json
    with open("feedback_log.csv", "a") as f:
        f.write(f"{feedback_data['user_id']},{feedback_data['recommended_course']},{feedback_data['relevance']}\n")
    return jsonify({"message": "Feedback recorded. Thank you!"})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

