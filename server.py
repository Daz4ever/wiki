from flask import Flask, render_template, redirect, request
import pg
from wiki_linkify import wiki_linkify
import markdown

app = Flask("Wiki")

db = pg.DB(dbname='wiki')

@app.route('/')
def wikihome():
    return redirect('/Homepage')

@app.route('/<page_name>')
def wiki(page_name):
    # id = int(request.form.get('id'))

#since there are multipule content pages you have to select from page_id in descending order to get the newest one
    query = db.query("select title.id as title_id, page.id as page_id, title.title, page.page_content from page inner join title on page.title_id = title.id where title = '%s' order by page_id desc" % page_name)
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



    # if len(wiki_linkify_content) > 0:
    #     has_content = True
    # else:
    #     pass
    # return render_template(
    #     'placeholder.html',
    #     title= page_name,
    #     wiki_page = wiki_page,
    #
    #     page_name = page_name
    # )

@app.route('/<page_name>/edit')
def wikiedit(page_name):
    query = db.query("select title.id as title_id, page.id as page_id, title.title, page.page_content from page inner join title on page.title_id = title.id where title = '%s' order by page_id desc" % page_name)

    page_name = page_name
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


@app.route('/<page_name>/save', methods= ['POST'])
def newpage(page_name):

    query = db.query("select title.id as id from page inner join title on page.title_id = title.id where title.title = '%s'" % page_name)

    result_list = query.namedresult()

    page_content = request.form.get('page_content')
    title = page_name
    # id = request.form.get('id')

    print "THe length is %s" % len(result_list)
    if len(result_list) < 1:
        db.insert(
            'title', {
                'title': page_name,

            }
        )
        query = db.query("select id from title where title.title = '%s'" % page_name)
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
