import os
from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "uploads"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

ALLOWED_EXTENSIONS = {
    "txt", "pdf", "png", "jpg", "jpeg", "gif",
    "doc", "docx", "xls", "xlsx", "csv", "zip",
}

db = SQLAlchemy(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    files = db.relationship("File", backref="owner", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    original_name = db.Column(db.String(256), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<File {self.original_name}>"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    user_count = User.query.count()
    file_count = File.query.count()
    return render_template("index.html", user_count=user_count, file_count=file_count)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        flash(f"User '{username}' registered successfully!", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    users = User.query.order_by(User.username).all()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        file = request.files.get("file")

        if not user_id:
            flash("Please select a user.", "danger")
            return redirect(url_for("upload"))

        if not file or file.filename == "":
            flash("No file selected.", "danger")
            return redirect(url_for("upload"))

        if not allowed_file(file.filename):
            flash("File type not allowed.", "danger")
            return redirect(url_for("upload"))

        original_name = file.filename
        filename = secure_filename(file.filename)
        # Add timestamp prefix to avoid collisions
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{filename}"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)

        db_file = File(
            filename=filename,
            original_name=original_name,
            file_size=file_size,
            user_id=int(user_id),
        )
        db.session.add(db_file)
        db.session.commit()
        flash(f"File '{original_name}' uploaded successfully!", "success")
        return redirect(url_for("upload"))

    return render_template("upload.html", users=users)


@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/admin")
def admin():
    users = User.query.order_by(User.created_at.desc()).all()
    files = File.query.order_by(File.uploaded_at.desc()).all()
    return render_template("admin.html", users=users, files=files)


@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Delete associated files from disk
    for f in user.files:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    # Delete user (cascades to files via session)
    File.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' and associated files deleted.", "warning")
    return redirect(url_for("admin"))


@app.route("/admin/delete_file/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    f = File.query.get_or_404(file_id)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(f)
    db.session.commit()
    flash(f"File '{f.original_name}' deleted.", "warning")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
