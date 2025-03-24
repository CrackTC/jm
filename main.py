import jmcomic
import os
import subprocess
from urllib.parse import quote_plus, unquote_plus
from flask import Flask, request, send_from_directory

option = jmcomic.create_option_by_file("./option.yml")

if not os.path.exists("./result"):
    os.makedirs("./result")


def download(id):
    jmcomic.download_album(id, option=option)
    title = os.listdir(f"./downloads/{id}")[0]
    subprocess.run(
        [
            "convert",
            "-compress",
            "jpeg",
            "-quality",
            "75",
            f"./downloads/{id}/{title}/*.webp",
            f"./result/{title}.pdf",
        ]
    )
    return f"/result/{quote_plus(title)}.pdf"


app = Flask(__name__)


@app.get("/download")
def download_route():
    id = request.args.get("id")
    if id:
        filepath = download(int(id))
        return filepath
    return "missing id", 400


@app.get("/result/<path:filename>")
def result_route(filename):
    return send_from_directory("./result", unquote_plus(filename), as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="::", port=port)
