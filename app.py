from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from ImageScrapper import ImageScrapper
from Utils import util
app = Flask(__name__)


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/searchImages', methods=['GET', 'POST'])
@cross_origin()
def search_images():

    if request.method == 'POST':
        search_keyword = request.form['search_keyword']
        images_limit = int(request.form['images_limit'])
        image_urls = ImageScrapper.scrape(search_keyword, images_limit)

        return render_template("showImages.html", images=image_urls)

    return jsonify(message="No image searchedx"), 404


@app.route('/showImages', methods=['GET'])
@cross_origin()
def show_keywords():

    keywords = util.getKeywords()
    return render_template('showImages.html', keywords=keywords)


@app.route('/showImages/<string:keyword>')
@cross_origin()
def show_images(keyword: str):
    images = util.getImages(keyword)
    return render_template('showImages.html', images=images, keyword=keyword)


if __name__ == '__main__':
    app.run(debug=True)
