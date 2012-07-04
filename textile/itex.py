#!/bin/env python

from textile import textile
from pyquery import PyQuery as pq

def wrap_page(wrapper, mid=None, mclass=[], step=0, line=0):
    if mid:
        wrapper.attr('id', mid)
    wrapper.attr('data-x', str(1000 * step))
    y = 1500 * step / line if line else 0
    wrapper.attr('data-y', str(y))
    wrapper.addClass('step')
    wrapper.addClass('slide')
    map(wrapper.addClass, mclass)
    return wrapper

def get_element(filename):
    def new_query(e):
        q = pq('<div></div>')
        q.append(e)
        return q
    with open(filename) as f:
        html = textile(f.read())
        query = pq(html.strip())
        elements = query.children()
        r_q = None
        for e in elements:
            if e.tag == 'h1':
                r_q = new_query(e) 
            if e.tag == 'h2':
                yield r_q
                r_q = new_query(e)
            else:
                r_q.append(e)
        yield r_q

def make_cloth(func):
    def wrapper(filename):
        cloth1 = '''
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=1024" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <title>impress.js | presentation tool based on the power of CSS3 transforms and transitions in modern browsers | by Bartek Szopka @bartaz</title>
    <meta name="description" content="impress.js is a presentation tool based on the power of CSS3 transforms and transitions in modern browsers and inspired by the idea behind prezi.com." />
    <meta name="author" content="Bartek Szopka" />
    <link href="http://fonts.googleapis.com/css?family=Open+Sans:regular,semibold,italic,italicsemibold|PT+Sans:400,700,400italic,700italic|PT+Serif:400,700,400italic,700italic" rel="stylesheet" />
    <link href="css/impress-demo.css" rel="stylesheet" />

    <link rel="shortcut icon" href="favicon.png" />
    <link rel="apple-touch-icon" href="apple-touch-icon.png" />
</head>
<body class="impress-not-supported">
<div class="fallback-message">
    <p>Your browser <b>doesn't support the features required</b> by impress.js, so you are presented with a simplified version of this presentation.</p>
    <p>For the best experience please use the latest <b>Chrome</b>, <b>Safari</b> or <b>Firefox</b> browser.</p>
</div>'''
        cloth2 = '''
<script src="js/impress.js"></script>
<script>impress().init();</script>
</body>
</html>'''
        body = func(filename)
        cloth = ''.join([cloth1, str(body), cloth2])
        return cloth
    return wrapper
   
@make_cloth                
def make_body(filename):
    query = pq('<div id="impress"></div>')
    for i, qe in enumerate(get_element(filename)):
        p = wrap_page(qe, step=i)
        query.append(p)
    return query


if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    print make_body(fname)
