import os

from python.publications import publications
from python.qiita import qiita
from python.talkmap import talkmap
from python.talks import talks
from python.view import print_view

html_escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;"}


def html_escape(text):
    if type(text) is str:
        return "".join(html_escape_table.get(c, c) for c in text)
    else:
        raise TypeError("Argument must be a string")


def main():
    dirname = os.path.dirname(__file__)
    publications(dirname, html_escape)
    talks(dirname, html_escape)
    talkmap(os.path.join(dirname, "../"))
    qiita(dirname, html_escape)
    print_view(dirname)


if __name__ == "__main__":
    main()
