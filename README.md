![Alt text](pics/wiki.png)

You will make a 90s style wiki - where anyone from anywhere in the world can edit and create pages.

The URL schemes of this wiki are as follows:

/ will redirect to /HomePage - HomePage is just a regular page. See below.
/<page_name> will render the contents of the specified page_name. We will call this the "view page". If the page doesn't exist, it will display the place holder page, giving users a link to create that page. For example: If a web user went to the URL http://myawesomewiki.com/Python, one of two things could happen:
If someone had previously created a "Python" page, that page would display.
Otherwise, a placeholder page would display, saying: "This page doesn't exist. Click here to create it!"
/<page_name>/edit will display a form for the user to edit or create the specified page. We will call this the "edit page".
/<page_name>/save is the URL where the edit form will send a POST request to save the new version of the page.
Setup

Create a new directory and initialize it as a Flask application.
Create a static subdirectory.
Create a templates subdirectory.
Create a layout.html in the templates subdirectory.
Create a server.py program that starts up the web server and servers up a basic hello world page.
Database Setup

You'll need to create a Wiki database in PostgreSQL. Create the database schema. To start, you need only one table: page. A page has the following:

title - titles must be unique
page content
last modified date
name of the author that last modified the page
Placeholder Pages

Create a route with the page name as a route parameter: /<page_name>, and render a default place holder page for the matching URLs. You might call the view template placeholder.html - put that in the templates folder. In side placeholder.html, put in text that says: this page has not been created yet.
In the placeholder.html, add an "Edit this page" link that goes to /<page_name>/edit so the user can click on that and navigate to the edit page.
At this point, you can write any page name in the URL such as /Python, /WebFrameworks, /HockeySticks, /MusicMajors, and you will get a place holder page.

Home Page

Create a route for / - it should simply redirect to /HomePage, which is just a regular page and will initialize be non-existent.

Creating Pages

Step 1 is to create a form for the edit page. Create the edit page for the /<page_name>/edit route. The edit page will have a form. The form's action attribute will be set to /{{page_name}}/save, where you'll make a form submission handler in a next step, the method attribute will be POST. In the form there will be a textarea and a submit button (make sure the button's type is "submit"). The data that the user enters in the textarea will become the new contents of the page.
Step 2 is to write a form submission handler for the edit page form. Create the handler for the POST /<page_name>/save route. The handler will
Take the content from the form.
Save it into the Wiki database.
Redirect back to the page view at /<page_name>.
Step 3 is to allow the saved page to be displayed on the view page. Back in the /<page_name> route, rewrite the handler to
Render the user submitted contents of the page for the given the page name if it exists in the database, or
Render the place holder page if it doesn't.
Wiki Links

Many wikis have the convention that any CamelCasedWord in the user-entered content automatically become links. As in, the word CamelCasedWord should be rendered as: <a href="/CamelCasedWord">CamelCasedWord</a> in the view page. I have provided a module that will convert the text for you as a download: wiki_linkify.py.zip. Download and unzip that file and put that file into your project next to your server.py. Now you can

from wiki_linkify import wiki_linkify
And then use the wiki_linkify function to convert user content text that has CamelCasedWords in it to become links. Example:

>>> from wiki_linkify import wiki_linkify
>>> wiki_linkify('I DigitalCrafts!'
Utilize this module to make all your CamelCasedWords links when viewing a page. The Jinja template disallows HTML code to be rendered within the {{ }} by default for security reasons, therefore your links won't show up correctly. The way to make this work is by using the "safe" filter like so {{ content | safe }}. See how to render html content with jinja

Edit Existing Pages

Make existing pages editable. To do this you will need to add an "Edit this page" link to each /<page_name> page, and allow the /<page_name>/edit page to retrieve the existing content and populate the textarea with it.

Modify the handler for the edit page to read in the contents of the page of the given name from the database, and use it to pre-populate the textarea in the edit page.
If the page does not exist in the database, do not pre-populate the textarea.
Bonus 1: Supporting Markdown Format

Research using a Python module to parse and convert markdown to HTML format. You will interpret the user entered content as markdown, and you will convert markdown to HTML before rendering the content on the view page for viewing. For example, if the user entered the following in the text area:

This is a *really* cool [wiki](https://en.wikipedia.org/wiki/Wiki).
The HTML that should be displayed in the view page should be:

This is a really cool wiki.

Bonus 2: Create a special AllPages page

Create a special page at the URL /AllPages. This page will list all user-created pages on this wiki, and will contain a link to each one.



. Add a user table to your wiki database. This table will include a username and password.

2. Initially, until we add signup functionality, add a user manually to your database.

3. Add a route that will handle the login portion of the wiki. You will need a form for the username and password. Take the information from your form and check it against the username password combo in your database. Refer to the keynote for use of sessions.

4. When a user is logged in display the username at the top right corner.

5. Now you will implement signing up. This will be another route and form that will insert a new user into your user table.

6. After the sign-up was successful, the user will be sent to login.

Bonus

Access restriction: only users who are logged in will be able to edit pages.
