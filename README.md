# 🌾 Meteor Madness

**Meteor Madness** is an interactive web experience that blends a traditional frontend website (HTML, CSS, JS) with a dynamic **Streamlit** backend built in Python.

---

## 🚀 Overview

Meteor Madness brings together creativity and data visualization.  
It allows users to explore meteor activity in real-time through a beautiful web interface and a powerful Streamlit dashboard.

---

## ✨ Features

- 🖥️ **Interactive Frontend:** Built with HTML, CSS, and JavaScript.  
- 🧠 **Data-Driven Backend:** Streamlit handles analytics and visualization.  
- 🔗 **Seamless Integration:** Frontend and Streamlit run together in one place.  
- 🌍 **Free Hosting:** Designed to work smoothly on Replit’s free tier.

---

## 🗂️ Project Structure

.
├── app.py # Main Streamlit app
├── index.html # Landing page
├── requirements.txt # Python dependencies
├── static/ # CSS, JS, images, etc.
│ ├── style.css
│ └── script.js
└── README.md # Project documentation


---

## 🛠️ Setup & Deployment (Replit)

### 1️⃣ Clone or Upload
Upload your files to [Replit](https://replit.com)  
Create a new **Python Repl**.

### 2️⃣ Install Dependencies
In the Replit Shell:
```bash
pip install -r requirements.txt
```
Make sure requirements.txt includes:
```bash
streamlit
flask
```
3️⃣ Run the App

Start both Flask (for HTML site) and Streamlit (for data app) from app.py:
```bash
streamlit run app.py --server.port=8080 --server.address=0.0.0.0
```

Replit will give you a live URL — your project is now online!


---

## 🧭 Navigation
Section	Description
/	Opens your HTML homepage
/streamlit	Opens your Streamlit dashboard

You can add a “Get Started” button in your HTML that redirects to the Streamlit link.


---

## 🧩 Technologies Used

Frontend: HTML, CSS, JavaScript

Backend: Python (Streamlit, Flask)

Hosting: Replit (Free Cloud)


---

## 🎯 Our Goal

To make space data visualization fun and accessible, blending education and interactivity through modern web technologies.


---

## 🙏 Thank You

Thanks for checking out Meteor Madness!
Feel free to fork, modify, or contribute — every idea helps us improve the cosmic experience 🚀
