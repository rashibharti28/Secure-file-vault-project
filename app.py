from flask import Flask, render_template, request, redirect, session, send_file, url_for, jsonify
from src.services.auth import AuthService
from src.services.vault import VaultSystem
import base64
import io
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
import requests
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"

auth = AuthService()
vault = VaultSystem()


# Helpers
class TempUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def get_current_user():
    return TempUser(session["username"], session["password"])


# Template filters
@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        auth.register(request.form["username"], request.form["password"])
        return redirect("/login")
    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = auth.login(request.form["username"], request.form["password"])

        if user:
            session["username"] = user.username
            session["password"] = user.password
            return redirect("/dashboard")

        return "❌ Invalid credentials"

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    user_files = []

    for f in vault.files:
        if f.owner == session["username"]:
            user_files.append({
                "name": f.filename,
                "date": getattr(f, "upload_date", "N/A"),
                "type": f.filename.split(".")[-1].lower()
            })

    return render_template(
        "dashboard.html",
        username=session["username"],
        files=user_files
    )


# Upload
@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session:
        return redirect("/login")

    user = get_current_user()
    file = request.files.get("file")

    if file and file.filename:
        vault.upload_file(user, file.filename, file.read())

    return redirect("/dashboard")



@app.route("/upload_url", methods=["POST"])
def upload_url():
    if "username" not in session:
        return redirect("/login")

    user = get_current_user()
    file_url = request.form.get("file_url")

    if not file_url:
        return "❌ No URL provided"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        
        head = requests.head(file_url, headers=headers, allow_redirects=True, timeout=10)

        content_type = head.headers.get("Content-Type", "").lower()
        content_length = head.headers.get("Content-Length")

        print("HEAD type:", content_type)

       
        if "text/html" in content_type:
            return "❌ This is a webpage, not a file"

       
        response = requests.get(file_url, headers=headers, stream=True, timeout=30)

        if response.status_code != 200:
            return f"❌ Failed (Status: {response.status_code})"

        #  filename extraction
        filename = file_url.split("/")[-1].split("?")[0]

        if not filename:
            filename = "downloaded_file"

        #  ensure extension
        if "." not in filename:
            if "pdf" in content_type:
                filename += ".pdf"
            elif "image" in content_type:
                filename += ".jpg"

       
        file_bytes = io.BytesIO()

        for chunk in response.iter_content(8192):
            if chunk:
                file_bytes.write(chunk)

        file_bytes.seek(0)

      
        vault.upload_file(user, filename, file_bytes.read())

        return redirect("/dashboard")

    except requests.exceptions.Timeout:
        return "❌ Timeout: File took too long"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# create text file

@app.route("/create", methods=["POST"])
def create():
    if "username" not in session:
        return redirect("/login")

    filename = request.form["filename"]

    if not filename.endswith(".txt"):
        filename += ".txt"

    return redirect(f"/edit/{filename}")


# download
@app.route("/download/<path:filename>", methods=["GET", "POST"])
def download(filename):
    if "username" not in session:
        return redirect("/login")

    user = get_current_user()

    if request.method == "POST":
        password = request.form["password"]

        result = vault.download_file(user, filename, password)

        if "error" in result:
            return render_template("view_file.html",
                                   filename=filename,
                                   result=result)

        session["verified_file"] = filename
        data = result["data"]

        if filename.lower().endswith(".txt"):
            return render_template("view_file.html",
                                   filename=filename,
                                   filetype="text",
                                   content=data.decode(errors="ignore"))

        elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
            ext = filename.split(".")[-1]

            return render_template("view_file.html",
                                   filename=filename,
                                   filetype="image",
                                   image_data=data,
                                   ext=ext)

        elif filename.lower().endswith(".pdf"):
            return render_template("pdf_view.html", filename=filename)

        return send_file(io.BytesIO(data),
                         download_name=filename,
                         as_attachment=True)

    return render_template("download.html", filename=filename)


# secure downlaod
@app.route("/download_file/<path:filename>")
def download_file_direct(filename):
    if "username" not in session:
        return redirect("/login")

    if session.get("verified_file") != filename:
        return "❌ Unauthorized"

    user = get_current_user()
    result = vault.download_file(user, filename, user.password)

    if "error" in result:
        return "❌ Error downloading file"

    session.pop("verified_file", None)

    return send_file(
        io.BytesIO(result["data"]),
        download_name=filename,
        as_attachment=True
    )


# pdf view
@app.route("/view_file/<path:filename>")
def view_file_direct(filename):
    if "username" not in session:
        return redirect("/login")

    if session.get("verified_file") != filename:
        return "❌ Unauthorized"

    user = get_current_user()
    result = vault.download_file(user, filename, user.password)

    if "error" in result:
        return "❌ Cannot open file"

    return send_file(
        io.BytesIO(result["data"]),
        mimetype="application/pdf",
        as_attachment=False
    )


# diary
@app.route("/diary", methods=["GET", "POST"])
def diary():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        user = get_current_user()

        content = request.form["content"]
        mood = request.form["mood"]

        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"diary_{date_str}.txt"

        full_content = f"Mood: {mood}\n\n{content}"

        vault.upload_file(user, filename, full_content)

        return redirect("/dashboard")

    return render_template("diary.html")








# delete
@app.route("/delete/<path:filename>", methods=["POST"])
def delete_file(filename):
    if "username" not in session:
        return redirect("/login")

    user = get_current_user()

    success = vault.delete_file(user, filename)

    if not success:
        return "❌ File not found"

    return redirect("/dashboard")

#edit
@app.route("/edit/<path:filename>", methods=["GET", "POST"])
def edit(filename):
    if "username" not in session:
        return redirect("/login")

    # Only allow text files
    if not filename.endswith(".txt"):
        return "❌ Only text files allowed"

    user = get_current_user()

    
    if request.method == "POST" and "auth_password" in request.form:
        password = request.form["auth_password"]

        if password != user.password:
            # Show preview if wrong password
            for f in vault.files:
                if f.filename == filename and f.owner == user.username:
                    with open(f.encrypted_data, "rb") as file:
                        preview = file.read(32)

                    return render_template(
                        "edit_auth.html",
                        filename=filename,
                        error="❌ Wrong password",
                        preview=preview
                    )


        return redirect(url_for("edit", filename=filename, auth="true"))

    
    if request.args.get("auth") != "true":
        return render_template("edit_auth.html", filename=filename)

    
    if request.method == "POST":
        content = request.form["content"]   # HTML from Quill

        file_exists = any(
            f.filename == filename and f.owner == user.username
            for f in vault.files
        )

        if file_exists:
            vault.edit_file(user, filename, content)
        else:
            vault.upload_file(user, filename, content)

        return redirect("/dashboard")

    
    existing_content = vault.read_file_content(user, filename)

    return render_template(
        "editor.html",
        filename=filename,
        content=existing_content
    )


# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Run
if __name__ == "__main__":
    app.run(debug=True)