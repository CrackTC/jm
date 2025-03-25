import jmcomic
import os
import subprocess
from flask import Flask, request, send_from_directory

option = jmcomic.create_option_by_file("./option.yml")
client = option.new_jm_client()


def count(id):
    album: jmcomic.JmAlbumDetail = client.get_album_detail(id)
    return len(album.episode_list)


def write_img_to_pdf(images_dir, pdf_path):
    if not os.path.exists(os.path.dirname(pdf_path)):
        os.makedirs(os.path.dirname(pdf_path))

    subprocess.run(
        [
            "convert",
            "-compress",
            "jpeg",
            "-quality",
            "75",
            f"{images_dir}/*.webp",
            pdf_path,
        ]
    )


def download(id, index):
    images_dir = f"./downloads/{id}/{index}"
    if not os.path.exists(images_dir):
        album: jmcomic.JmAlbumDetail = client.get_album_detail(id)
        photo = album.create_photo_detail(index)

        # redirect
        id = album.album_id
        index = photo.album_index
        images_dir = f"./downloads/{id}/{index}"
        if not os.path.exists(images_dir):
            jmcomic.download_photo(photo.id, option=option)

    pdf_path = f"./result/jm_{id}_{index}.pdf"
    if not os.path.exists(pdf_path):
        write_img_to_pdf(images_dir, pdf_path)

    return f"/result/jm_{id}_{index}.pdf"


app = Flask(__name__)


@app.get("/count")
def count_route():
    id = request.args.get("id")
    if not id:
        return "id is required", 400
    return str(count(int(id)))


@app.get("/download")
def download_route():
    id = request.args.get("id")
    index = request.args.get("index")
    if not id or not index:
        return "id and index are required", 400
    filepath = download(int(id), int(index))
    return filepath


@app.get("/result/<path:filename>")
def result_route(filename):
    return send_from_directory("./result", filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="::", port=port)
