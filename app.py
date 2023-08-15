from flask import Flask,render_template,request
import pickle
import numpy as np


books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(books['Title'].values),
                           book_author = list(books['Author'].values),
                           book_genre = list(books['Genre'].values),
                           book_height = list(books['Height'].values),
                           book_publisher = list(books['Publisher'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[0])),key=lambda x:x[1],reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Title')['Title'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Author'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Genre'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Height'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Publisher'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)
