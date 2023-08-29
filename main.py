import os

from flask import Flask, render_template, request, send_from_directory
import requests
from post import Post
import smtplib

MY_EMAIL = "testtheemail1122@gmail.com"
MY_PASSWORD = "iarsvhnedmhkzrbj"

app = Flask(__name__)

posts_content = requests.get("https://api.npoint.io/e09d1168b4eae7529e82").json()
all_posts = []
for post_content in posts_content:
    post_obj = Post(post_content["id"], post_content["title"], post_content["subtitle"], post_content["body"],
                    post_content["author"])
    all_posts.append(post_obj)


def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=email,
            to_addrs=MY_EMAIL,
            msg=f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
        )


@app.route('/')
def get_all_post():
    return render_template('index.html', blogs=all_posts)


@app.route('/index.html')
def home():
    print('Request for index page received')
    return render_template('index.html', blogs=all_posts)


@app.route('/about.html')
def about():
    return render_template('about.html')


# @app.route('/contact.html')
# def contact():
#     return render_template('contact.html')

@app.route("/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in all_posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", blogs=requested_post)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)
