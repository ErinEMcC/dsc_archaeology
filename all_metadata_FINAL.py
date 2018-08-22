import requests
from bs4 import BeautifulSoup
import json
import pprint

articles_metadata = []
article_metadata = {}

issues_tocs = json.loads(open("LatinAmericanAntiquity_TOC_URLs.json").read())

# looping through each issue url in the issues_toc file to soup-ify/parse individual issue toc pages
for a_issue in issues_tocs[:]:
    r = requests.get(a_issue)
    if r.status_code != 200:
        print("There was an error with", url)

    object_html = r.content
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, "html.parser", from_encoding=encoding)

    metadata = soup.find_all("ul", attrs={"class": "details"})

    for article in metadata:
        title = article.find("a", attrs={"class": "part-link"}).string
        doi = article.find("a", attrs={"class": "url doi"}).string
        pub_date = article.find("span", attrs={"class": "date"}).string
        pages = article.find("span", attrs={"class": "pages"}).string
        art_url = article.find("a", attrs={'data-hasqtip': 'Download PDF'})
        pdf_url = ('https://www.cambridge.org{0}'.format(str(art_url.get('href'))))

        authors = []
        author_elem = article.find("li", attrs={"class": "author"})
        if author_elem.find("a", attrs={"class": "more-by-this-author"}):
            all_authors = author_elem.find_all("a", attrs={"class": "more-by-this-author"})
            for a_author in all_authors:
                # author_frame = a_author.find("a", {"class": "more-by-this-author"})
                if a_author:
                    for a in a_author:
                        if a not in authors:
                            authors.append(a)
            if not authors:
                authors_string = "N/A"
            else:
                authors_string = ", ".join(authors)

        # defining the metadata dictionary for earch article's metadata
        article_metadata = dict(title=title, author=authors_string, doi=doi, pub_date=pub_date, page=pages,
                                pdf_url=pdf_url)

        articles_metadata.append(article_metadata)

    with open('articles_metadata.json', 'w') as f:
        f.write(json.dumps(articles_metadata, indent=4))

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(articles_metadata)