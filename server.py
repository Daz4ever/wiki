from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, render_template, redirect, request, session, flash
import pg
from wiki_linkify import wiki_linkify
import markdown, os

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask('Wiki', template_folder=tmp_dir)

app.secret_key = 'whatever'

db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

@app.route('/login')
def login():


    return render_template(
    'login.html'
    )

@app.route('/submit_login', methods = ['POST'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    query= db.query('select * from users where username = $1', username)
    query_list = query.namedresult()
    print 'HERE : ', query_list

    if len(query_list) > 0:
        user = query_list[0]
        if password == user.password:
            session['username'] = username
            return redirect('/')
        else:
            return redirect('/login')
    else:
        flash('username or password was incorrect')
        return redirect('/login')

@app.route('/sign_up')
def signup():

    return render_template(
    'signup.html'
    )

@app.route('/submit_sign_up', methods = ['POST'])
def submit_sign_up():

    username = request.form.get('username')
    password = request.form.get('password')

    query = db.query("select * from users where username = $1", username)
    query_list = query.namedresult()
    #if a specific username is already taken redirect back to the sign up page with a flash note saying its already been taken else insert the users input into the database
    if len(query_list) > 0:
        flash('%s has already been taken' % username)
        return redirect('/sign_up')

    else:
        db.insert(
        'users',
        username=username,
        password=password
        )
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']

    return redirect('/login')


@app.route('/')
def wikihome():

    return render_template(
    'homepage.html'
    )


@app.route('/all_pages')

def all_pages():
    query=db.query('''select title from title''')
    query_list = query.namedresult()

    return render_template('allpages.html',
    title='All Pages',
    query_list= query_list
    )
@app.route('/<page_name>')
def wiki(page_name):
    # id = int(request.form.get('id'))

#since there are multipule content pages you have to select from page_id in descending order to get the newest one
    query = db.query("select title.id as title_id, page.id as page_id, title.title, page.page_content from page inner join title on page.title_id = title.id where title = $1 order by page_id desc", page_name)
    result_list = query.namedresult()
    if len(result_list) > 0:
        wiki_page = result_list[0]
        wiki_linkify_content = markdown.markdown(wiki_linkify(wiki_page.page_content))
        return render_template(
            'view.html',
            title= page_name,
            page_name = page_name,
            wiki_page = wiki_page,
            wiki_linkify_content = wiki_linkify_content
            )
    else:
        return render_template(
            'placeholder.html',
            title= page_name,
            page_name=page_name)


@app.route('/<page_name>/edit')
def wikiedit(page_name):
    query = db.query("select title.id as title_id, page.id as page_id, title.title, page.page_content from page inner join title on page.title_id = title.id where title = $1 order by page_id desc", page_name)

    if 'username' in session:
        # page_name = page_name
        result_list = query.namedresult()
        print result_list
        if len(result_list) > 0:
            wiki_page = result_list[0]

            return render_template ('edit.html',
            title=page_name,
            page_name =page_name,
            wiki_page = wiki_page
            )



        else:
            return render_template(
            'edit.html',
            page_name = page_name
            )
    else:
        return redirect('/login')

@app.route('/<page_name>/save', methods= ['POST'])
def newpage(page_name):

    query = db.query("select title.id as id from page inner join title on page.title_id = title.id where title.title = $1", page_name)

    result_list = query.namedresult()

    page_content = request.form.get('page_content')
    title = page_name
    # id = request.form.get('id')

    print "THe length is $1", len(result_list)
    if len(result_list) < 1:
        db.insert(
            'title', {
                'title': page_name,

            }
        )
        query = db.query("select id from title where title.title = $1", page_name)
        result_list = query.namedresult()
    else:
        pass
    db.insert(
        'page', {
            'page_content': page_content,
            'last_modified_date': "",
            'title_id': result_list[0].id
        }
    )


    return redirect('/' + page_name)




if __name__ == '__main__':
    app.run(debug=True)
