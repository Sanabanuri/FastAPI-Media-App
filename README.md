# 📸 FastAPI Media App

Welcome to the **FastAPI Media App**! This is a simple social media application where you can sign up, log in, and share your favorite moments with others.

## 🚀 What This Project Does
This project creates a web application that acts like a mini social media platform.
- **Users can create accounts** and log in securely.
- **Users can upload photos and videos** to a shared feed.
- **Everyone can view the feed**, seeing what others have posted.
- **You can delete your own posts** if you change your mind.

It connects a modern backend (the logic) with a simple frontend (what you see) to make everything work smoothly.

## ✨ Main Features
- **User Accounts**: Sign up and log in securely (using email and password).
- **Media Upload**: Upload both **Images** (JPEG, PNG) and **Videos** (MP4, AVI).
- **Live Feed**: A scrollable feed showing everyone's posts with captions.
- **Smart Image Handling**: Images and videos are automatically optimized and served quickly.
- **Security**: Passwords are encrypted, and only you can delete your own posts.

## 🛠️ Technologies Used
We used modern and popular tools to build this:
- **[FastAPI](https://fastapi.tiangolo.com/)**: The "brain" of the application. It handles all the logic, security, and data communication.
- **[Streamlit](https://streamlit.io/)**: The "face" of the application. It creates the website you see and interact with.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: The tool that talks to the database to save users and posts.
- **[ImageKit](https://imagekit.io/)**: A cloud service that stores and optimizes your uploaded images and videos (so they load fast!).
- **[SQLite](https://www.sqlite.org/)**: A simple database file to store user info and post details locally.

## ⚙️ How It Works (Simply)
1.  **The Backend (FastAPI)**: This is running in the background. It waits for commands (like "log me in" or "upload this file"). When it gets a command, it checks if it's allowed and then does the work.
2.  **The Frontend (Streamlit)**: This is the website you open in your browser. When you click "Login" or "Upload", it sends a message to the Backend.
3.  **The Database**: When you sign up or post, the Backend saves that information into the Database so it's there when you come back.
4.  **The Cloud (ImageKit)**: When you upload a photo, the Backend sends it to ImageKit for safe keeping. ImageKit gives back a link, which we save in the Database to show the picture later.

## 📝 Usage
To run this project, you typically need two terminal windows:
1.  **Run the Backend**:
    ```bash
    uv run uvicorn app.app:app
    ```
2.  **Run the Frontend**:
    ```bash
    uv run streamlit run app/frontend.py
    ```
Then open your browser to the URL shown by Streamlit (usually `http://localhost:8501`).
