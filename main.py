import smtplib
import os
from flask import Flask, render_template, request
import requests


app = Flask(__name__)
response = requests.get("https://api.npoint.io/8752b8a1c56cdbde6142")
all_posts = response.json()

EMAIL = "yukimetochianaki@gmail.com"
PASSWORD = os.environ.get("PASSWORD")


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(name)
        print(email)
        print(phone)
        print(message)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject:New Message\n\nName:{name}\nEmail:{email}\nPhone:{phone}\nMessage:{message}")
        return render_template("contact.html", h1="Successfully sent your message.")
    else:
        return render_template("contact.html", h1="Contact Me")


@app.route("/post/<int:index>")
def post(index):
    requested_post = None
    for blog_post in all_posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
