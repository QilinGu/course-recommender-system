from flask import Flask, render_template, request, url_for, g, flash, redirect
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from  sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
course_names = {}
data_source = pd.read_csv("indexed_courses.csv", header=None, names=['id', 'title', 'description'])
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0,
                         stop_words='english')
tfidf_matrix = tf.fit_transform(data_source['description'])

@app.route("/")
@app.route("/hello")
def collect_data():
    # print(data_source)
    return render_template('index.html')


@app.route("/analyze", methods=['POST'])
def analyze_data():
    course1 = request.form['course1']
    course2 = request.form['course2']
    course3 = request.form['course3']
    course4 = request.form['course4']
    #print(course1)
    course1_description = data_source[data_source.title == course1].description
    course2_description = data_source[data_source.title == course2].description
    course3_description = data_source[data_source.title == course3].description
    course4_description = data_source[data_source.title == course4].description
    print("course 1 description: " + str(course1_description))

    sim1 = cosine_similarity(tfidf_matrix[data_source[data_source.title == course1].id], tfidf_matrix)
    dsim1 = sim1[0]
    course1_top_three = similarity(dsim1)
    sim2 = cosine_similarity(tfidf_matrix[data_source[data_source.title == course2].id], tfidf_matrix)
    dsim2 = sim2[0]
    course2_top_three = similarity(dsim2)
    sim3 = cosine_similarity(tfidf_matrix[data_source[data_source.title == course3].id], tfidf_matrix)
    dsim3 = sim3[0]
    course3_top_three = similarity(dsim3)
    sim4 = cosine_similarity(tfidf_matrix[data_source[data_source.title == course4].id],tfidf_matrix)
    dsim4 = sim4[0]
    course4_top_three = similarity(dsim4)
    course_list = [course1, course2, course3, course4]
    return render_template('result.html', first_course = course1_top_three, ls_kurs = course_list,
                           second_course = course2_top_three, third_course = course3_top_three,
                           fourth_course = course4_top_three)
    #return redirect(url_for('success'))


@app.route('/success/')
def success():
    return 'Welcome sai'

def similarity(dsim):
    subject = {}
    for i in range(len(dsim)):
        title = str(data_source['title'][i])
        subject[title] = float(dsim[i])
        #print(title)
    descending = sorted(subject.items(), key=lambda x: x[1], reverse=True)
    # get top_5
    # First will always be the highest, the course it self
    top3 = descending[1:4]
    with_description = []
    for title, val in top3:
        exact_series = data_source[data_source.title == title]
        description = "".join(exact_series['description'].tail(1))
        new_top3 = (title, val, description)
        with_description.append(new_top3)
        print(title + ": " + description + "\n")
    return with_description

if __name__ == "__main__":
    app.run(debug=True)
