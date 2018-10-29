from flask import Flask
from flask import render_template
from flask import jsonify
from flask_cors import CORS
import csv
import phonetics
from fuzzywuzzy import fuzz




app = Flask(__name__, static_folder="../static", template_folder="../static/src")
CORS(app)


def parse():
    # open file and read
    csvfile = open('../Data/normal.csv', 'r')
    csv_reader = csv.reader(csvfile, delimiter=',')

    # data structures
    dataArray = []
    dataIds= []
    duplicates = set()
    nearDuplicates = set()
    data = {'duplicates': [], 'nearDuplicates': []}
    first_line = True


    for row in csv_reader:
        if first_line:
            first_line = False
        else:
            # add all data to dataDict and dataId
            id = row[0]
            row = row[1:]
            s = " ".join(row)
            print(s)
            dataArray.append(s)
            dataIds.append(id)

    # for every item in dataDict, compare to every other item
    for i in range(len(dataArray)):
        for j in range(len(dataArray)):
            # don't compare same item
            if i == j:
                break
            # if they are equal, they are exact duplicates
            if dataArray[i] == dataArray[j]:
                if (i,j) not in duplicates and (j,i) not in duplicates:
                    duplicates.add((i, j))
                    break

            # check levenshtein distance and metaphone for near duplicates
            a = fuzz.token_set_ratio(dataArray[i], dataArray[j])
            metaphone1 = phonetics.metaphone(dataArray[i])
            metaphone2 = phonetics.metaphone(dataArray[j])
            if a > 80 or metaphone1 == metaphone2:
                if (i, j) not in nearDuplicates and (j,i) not in nearDuplicates:
                    nearDuplicates.add((i, j))

    # add to final 'data' dictionary to post
    for item in duplicates:
        data['duplicates'].append([dataIds[item[0]] + " " + dataArray[item[0]], dataIds[item[1]] + " " + dataArray[item[1]]])

    for item in nearDuplicates:
        data['nearDuplicates'].append([dataIds[item[0]] + " " + dataArray[item[0]], dataIds[item[1]] + " " + dataArray[item[1]]])
    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/duplicates")
def duplicates():
    data = parse()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)