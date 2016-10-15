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


    query = db.query("select title.title, page.page_content from page inner join title on page.title_id = title.id where title = '%s'" % page_name)
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
    query = db.query("select title.title, page.page_content from page inner join title on page.title_id = title.id where title = '%s'" % page_name)

    page_name = page_name
    result_list = query.namedresult()

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

    query = db.query("select title.title, page.page_content, title.id as title_id from page inner join title on page.title_id = title.id where title.title = '%s'" % page_name)
    result_list = query.namedresult()

    page_content = request.form.get('page_content')
    title = page_name
    id = request.form.get('id')

    if len(result_list) == 0:
        db.insert(
            'title', {
                'title': page_name
            }
        )
    else:
        pass
    db.insert(
        'page', {
            'page_content': page_content,
            'last_modified_date': "",
            'title_id': id
        }
    )

    return redirect('/' + page_name)


if __name__ == '__main__':
    app.run(debug=True)
