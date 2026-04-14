# 🔐 Secure File Vault with Diary System

A **Flask-based secure file storage and personal diary web application** that allows users to store, view, edit, and manage encrypted files with authentication.

---

## 🚀 Features

### 🔐 Authentication

* User Registration & Login
* Password verification before accessing files

---

### 📂 Secure File Vault

* Upload files (text, images, PDF, etc.)
* Files are **encrypted before storage**
* Decryption only after password verification
* Secure download system (no direct access)

---

### 📄 File Management

* View files (text, images, PDF preview)
* Edit text files (with authentication)
* Delete files
* Organized dashboard with file type icons

---

### 📔 Personal Diary System (NEW ✨)

* Rich text editor (bold, lists, formatting)
* Mood tracking (😊 😢 😡)
* Daily diary entries
* HTML-rendered diary view (clean UI)
* Secure storage using encryption

---

### 🎨 UI Improvements

* Bootstrap-based responsive design
* Professional dashboard with cards
* Action dropdown for each file
* Clean editor interface

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, Bootstrap
* **Editor:** Quill.js (Rich Text Editor)
* **Encryption:** Custom Encryption Manager
* **Storage:** Local file system + metadata JSON

---

## 📁 Project Structure

```
project/
│
├── app.py
├── data/                  # Encrypted user files
├── templates/             # HTML files
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── editor.html
│   ├── diary.html
│   ├── view_file.html
│   └── pdf_view.html
│
├── src/
│   ├── services/
│   │   ├── auth.py
│   │   ├── vault.py
│   │   ├── storage.py
│   │   └── logger.py
│   │
│   ├── security/
│   │   ├── encryption.py
│   │   └── access_control.py
│   │
│   └── models/
│       └── file.py
```

---

## ⚙️ How to Run

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd project
```

### 2️⃣ Install dependencies

```bash
pip install flask
```

### 3️⃣ Run the application

```bash
python app.py
```

### 4️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 🔐 Security Features

* Files are **encrypted before saving**
* Password required for:

  * Viewing files
  * Downloading files
  * Editing files
* No direct file access without verification
* Session-based secure actions

---

## 📸 Supported File Types

| Type        | Behavior        |
| ----------- | --------------- |
| `.txt`      | View + Edit     |
| `.png/.jpg` | Image preview   |
| `.pdf`      | Embedded viewer |
| Others      | Download only   |

---

## 📔 Diary System Details

* Stored as encrypted `.txt` files
* Format:

  ```
  mood|||<html content>
  ```
* Rendered using HTML (`safe` filter)
* Supports rich text formatting

---

## 🚧 Future Improvements

* 📅 Calendar view for diary entries
* 🔍 Search files & diary entries
* ⭐ Favorite / Pin files
* 🔑 Stronger encryption (AES)
* ☁️ Cloud storage integration
* 📱 Mobile responsive UI improvements

---

## 👩‍💻 Author

**Rashi Bharti**

Final Year BS (EECS)
IISER Bhopal

---

## 💡 Notes

* This project is built for **learning + academic purposes**
* Not recommended for production without advanced security upgrades

---



## Documentation

All diagrams and architecture designs are available in the `documentation/` folder.
