from flask import Flask, render_template, redirect, request
import pg
import wiki_linkify

app = Flask("Wiki")

db = pg.DB(dbname='wiki')

@app.route('/')
def wikihome():
    return redirect('/Homepage')

@app.route('/<page_name>')
def wiki(page_name):
    # id = int(request.form.get('id'))


    query = db.query("select * from page where title = '%s'" % page_name)
    result_list = query.namedresult()
    if len(result_list) == 0:
        return render_template(
            'placeholder.html',
            title= page_name,
            page_name = page_name
            )
    else:
        wiki_page = result_list[0]
        has_content = False

    # if id == True:
    #     query = db.query('''
    #     select * from wiki
    #     where id = %d''' % id)
    #     entry = query.namedresults()[0]
    #
    #
    # else:
    if len(wiki_page.page_content) > 0:
        has_content = True
    else:
        pass
    return render_template(
        'placeholder.html',
        title= page_name,
        wiki_page = wiki_page,
        has_content = has_content,
        page_name = page_name
    )

@app.route('/<page_name>/edit')
def wikiedit(page_name):
    query = db.query("select * from page where title = '%s'" % page_name)



    page_name = page_name
    result_list = query.namedresult()

    if len(result_list) == 0:
        wiki_page = result_list[0]
        title=page_name
        return render_template(
        'edit.html'
        )


    else:

        return redirect('/' + page_name)


@app.route('/<page_name>/save', methods= ['POST'])
def newpage(page_name):

    query = db.query("select * from page where title = '%s'" % page_name)
    result_list = query.namedresult(),
    wiki_page = result_list[0]

    page_content = request.form.get('page_content')
    title = page_name
    id = request.form.get('id')

    if len(wiki_page) == 0:
        db.insert(
        'page',
        page_content = wiki_linkify(page_content),
        title = title)
        return redirect('/' + page_name)

    else:
        db.update('page', {
        'id': id,
        'page_content': page_content

        })
        return redirect('/' + page_name)
    # db.update('page'), {
    # 'page_content': page_content
    # })



if __name__ == '__main__':
    app.run(debug=True)
