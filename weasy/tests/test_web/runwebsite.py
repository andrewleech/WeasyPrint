#!/usr/bin/env python

import os.path
from flask import Flask, request, render_template, send_file
from weasy.document import PNGDocument, PDFDocument

app = Flask(__name__)


INPUT = os.path.join(app.root_path, 'input.html')
PNG_OUTPUT = os.path.join(app.root_path, 'output.png')
PDF_OUTPUT = os.path.join(app.root_path, 'output.pdf')

DEFAULT_CONTENT = """
<style>
body { margin: 1em 2em; }
h1 { text-decoration : underline; }
div { border: 10px solid; background: #ddd; }
</style>

<h1>Weasyprint testing</h1>

<div><ul><li>Hello, world!
"""


@app.route('/')
def index():
    if os.path.isfile(INPUT):
        with open(INPUT) as fd:
            content = fd.read()
    else:
        content = DEFAULT_CONTENT
    return render_template('index.html.jinja2', content=content)


@app.route('/render.png')
def render():
    html = request.args['html']
    assert html.strip()

    if html:
        assert 'fuu' not in html
        # Save the input HTML
        with open(INPUT, 'w') as fd:
            fd.write(html)

    PDFDocument.from_file(INPUT, encoding='utf8').write_to(PDF_OUTPUT)
    PNGDocument.from_file(INPUT, encoding='utf8').write_to(PNG_OUTPUT)

    return send_file(PNG_OUTPUT, cache_timeout=0)


if __name__ == '__main__':
    import logging

    logger = logging.getLogger('WEASYPRINT')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    app.run(port=12290, debug=True)