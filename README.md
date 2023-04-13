# Book Master Python Scraper

## Project overview

In this project we created a web scraper using python, various API endpoints, and a website displaying the data. This repository contains code for the Python web scraper.

## Tech stack

We used the BeautifulSoup library in Python to build our web scraper. And we used Supabase to store all our data.

## How did we build it

Web scraping is the process of extracting data from websites by using automated software or tools. Web scraping typically involves sending an HTTP request to a website, parsing the HTML or XML code of the response, and extracting relevant information from the code.

HTML, or Hypertext Markup Language, is the standard markup language used to create web pages. HTML consists of a series of tags that define the structure and content of a web page. Each tag is surrounded by angle brackets, and most tags have an opening tag and a closing tag. For example, the `<p>` tag is used to define a paragraph of text, and the opening tag is `<p>` and the closing tag is `</p>`.

HTML tags can also contain attributes, which provide additional information about the element. For example, the `<a>` tag is used to define a hyperlink, and it includes an `href` attribute that specifies the URL of the link. Attributes are included in the opening tag and are specified using the attribute name and value, separated by an equals sign. For example, `<a href="https://www.example.com">Example Website</a>`.

We used BeautifulSoup Library to parse the HTML of the page we are scraping. The parser library reads the HTML code and creates a parse tree, which is a hierarchical representation of the HTML structure. This allows the we to navigate the HTML code and extract specific data elements.

After scraping the data layer by layer, we generated a dictionary that contains all the info of a book and checked if it's in the database already, if it's not, we insert the book into the database.

## Deploy your own Book Master Python Scraper

Clone this GitHub repo, go into the folder.

Create a Supabase project with a table of the same structure as `@/utils/types/supabase.ts` in the Book Master repo.

Then, add SUPABASE_URL and SUPABASE_KEY into your session's environment variable by running:

```bash
export SUPABASE_URL=<your supabase url>
export SUPABASE_KEY=<your supabase service key>
```

Finally, run the `scraper.py` with your Python install.
