from flask import Flask, render_template, session
from flask_session import Session

app = Flask(__name__)

# Cấu hình session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    # Kiểm tra người dùng đã đăng nhập chưa
    user_session_id = session.get("userId", "userIsNotLoggedIn")

    # Đếm số lần người dùng truy cập trang
    session["viewsNumber"] = session.get("viewsNumber", 0) + 1
    view_number = session["viewsNumber"]

    return render_template("index.html", user_session_id=user_session_id, view_number=view_number)

if __name__ == "__main__":
    app.run(debug=True)
