from python.publications import publications
from python.talks import talks
from python.qiita import qiita
import os

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
    qiita(dirname, html_escape)


if __name__ == "__main__":
    main()
