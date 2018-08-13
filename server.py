from flask import Flask, render_template, request
import boto3
import os
import colorgram
import webcolors
import numpy as np
import cv2
import statistics
import pandas as pd
from json2table import convert
from werkzeug import secure_filename

os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'

def is_nan(x):
    return (x is np.nan or x != x)

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')

def color(file):
    colors = colorgram.extract(file, 2)
    first_color = colors[1]
    rgb = first_color.rgb
    return (rgb)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

@app.route('/my-link/', methods = ['GET', 'POST'])
def main():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        file = str(f.filename)

    s3 = boto3.client('s3')
    bucket = 'avadakadaba'
    photo = file
    s3.upload_file(photo, bucket, photo)
    client = boto3.client('rekognition')
    response = client.detect_text(Image={'S3Object': {'Bucket': 'avadakadaba', 'Name': photo}})
    textDetections = response['TextDetections']
    text2 = ""
    for text in textDetections:
        if text['DetectedText'] not in text2:
            text2 = text2 + text['DetectedText']
    text2 = ''.join(text2.split())

    # Getting color
    requested_colour = color(photo)
    actual_name, closest_name = get_colour_name(requested_colour)
    if "grey" in closest_name:
        closest_name = "WHITE"
    if "rose" in closest_name:
        closest_name = "PINK"
    if "red" in closest_name:
        closest_name = "RED"
    if "yellow" in closest_name:
        closest_name = "YELLOW"
    if "blue" in closest_name:
        closest_name = "BLUE"

    # Getting shape
    shape=""
    img = cv2.imread(photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(np.asarray(gray), 50, 250)

    _,contours, h = cv2.findContours(gray, 1, 2)

    avgArray = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        avgArray.append(len(approx))

    # print((avgArray))
    edges = statistics.median(avgArray)
    # print(edges)

    if edges < 15:
        shape = "OVAL"
        # cv2.drawContours(photo, [cnt], 0, 255, -1)
    # elif edges == 3:
    #     print("triangle")
    #     cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
    # elif edges == 4:
    #     print("square")
    #     cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
    # elif edges == 9:
    #     print("half-circle")
    #     cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
    elif edges > 15:

        shape = "CIRCLE"

    data = {"uploadName":photo,"text":text2,"color":closest_name,"shape":shape}
    print(data)
    # print(data)

    dataframe = pd.read_csv("out.csv")

    for index, row in dataframe.iterrows():
        name = str(row["Imprint"]).replace(";","")
        if not is_nan(row["Name"]):
            if name == text2 and row["Color"] == color and row["Shape"] == shape:
                return '''<style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 5px;
                    text-align: left;
                }
                b{
                    margin-left: 43%;
                    font-size: 20px;
                }
                </style><b>Pill Details</b><br><table style="width:100%; height: 80%; padding: 1px; margin: 1px"><br />
                  <tr><th>Author</th><td>'''+str(row["Author"])+'''</td></tr>
                    <tr><th>Name</th><td>'''+str(row["Name"])+'''</td></tr>
                    <tr><th>Color</th><td>'''+str(row["Color"])+'''</td></tr>
                    <tr><th>Imprint</th><td>'''+str(row["Imprint"])+'''</td>
                    <tr><th>Size</th><td>'''+str(row["Size"])+'''</td></tr>
                    <tr><th>Shape</th><td>'''+str(row["Shape"])+'''</td></tr>
                    <tr><th>Ingredients</th><td>'''+str(row["Ingredients"])+'''</td></tr>
                </table>'''



    for index, row in dataframe.iterrows():
        name = str(row["Imprint"]).replace(";","")
        if not is_nan(row["Name"]):
            if name == text2 and row["Color"] == color:
                return '''<style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 5px;
                    text-align: left;
                }
                b{
                    margin-left: 43%;
                    font-size: 20px;
                }
                </style><b>Pill Details</b><br><table style="width:100%; height: 80%; padding: 1px; margin: 1px"><br />
                  <tr><th>Author</th><td>'''+str(row["Author"])+'''</td></tr>
                    <tr><th>Name</th><td>'''+str(row["Name"])+'''</td></tr>
                    <tr><th>Color</th><td>'''+str(row["Color"])+'''</td></tr>
                    <tr><th>Imprint</th><td>'''+str(row["Imprint"])+'''</td>
                    <tr><th>Size</th><td>'''+str(row["Size"])+'''</td></tr>
                    <tr><th>Shape</th><td>'''+str(row["Shape"])+'''</td></tr>
                    <tr><th>Ingredients</th><td>'''+str(row["Ingredients"])+'''</td></tr>
                </table>'''

    for index, row in dataframe.iterrows():
        name = str(row["Imprint"]).replace(";","")
        if not is_nan(row["Name"]):
            if name == text2:
                return '''<style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 5px;
                    text-align: left;
                }
                b{
                    margin-left: 43%;
                    font-size: 20px;
                }
                </style><b>Pill Details</b><br><table style="width:100%; height: 80%; padding: 1px; margin: 1px"><br />
                  <tr><th>Author</th><td>'''+str(row["Author"])+'''</td></tr>
                    <tr><th>Name</th><td>'''+str(row["Name"])+'''</td></tr>
                    <tr><th>Color</th><td>'''+str(row["Color"])+'''</td></tr>
                    <tr><th>Imprint</th><td>'''+str(row["Imprint"])+'''</td>
                    <tr><th>Size</th><td>'''+str(row["Size"])+'''</td></tr>
                    <tr><th>Shape</th><td>'''+str(row["Shape"])+'''</td></tr>
                    <tr><th>Ingredients</th><td>'''+str(row["Ingredients"])+'''</td></tr>
                </table>'''

if __name__ == "__main__":
    app.run(debug=True)
