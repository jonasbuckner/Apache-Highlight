#!/usr/bin/env python
# highlight.cgi: Syntax Highlight Python and Send it as HTML
# Copyright 2009-2010 Jonas Buckner
# Distributed under the GNU General Public License
# http://www.gnu.org/licenses/gpl.html
#
# 2009-05-13:   Initial Release
# 2010-05-12:   Added Documentation to README
#               Changed one of the styles to make the numbers a fixed-width font
# 
#
# To install, see README File
#
# WARNING: Be very sure that the directory to which you apply this contains the correct
#           files you want to highlight. This can be a major security flaw if you share
#           scripts and other files you don't intend to.

import os
import cgi

import pygments
import pygments.lexers as pyglexs
import pygments.formatters as pygforms
import pygments.styles as pygstyles

filename = cgi.os.environ["PATH_TRANSLATED"]

fh = open(filename, 'r')
lines = fh.readlines()
fh.close()

fullcode = "".join(lines)

for line in lines:
    uselexer = pyglexs.guess_lexer_for_filename(filename, line)

colorscheme = "vs"

form = cgi.FieldStorage()
if form.has_key("color") and form["color"].value != "":
    colorscheme = form["color"].value

usehtml = pygforms.HtmlFormatter(style=colorscheme, linenos='table')

print """Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>

  <title>%s</title>

<style type="text/css">
body {
    margin:             0;
    padding:            0;
}

#header {
    width:              %s;
    background-color:   #aab3a3;
    margin:             0;
    padding:            0;
    border-bottom:      3px double #000000;
}
#header h2 {
    font-family:        "Courier", "Courier New", monospace;
    color:              #ffffff;
    background-color:   #aab3a3;
    margin:             0;
    padding:            0;
    padding-top:        0em;
    padding-bottom:     0.2em;
    padding-left:       0.5em;
}

ul.navbar {
    position:           absolute;
    right:              0.0;
    top:                0.0;
    margin:             0;
    padding-left:       0.0;
    padding-right:      0.0;
    float:              right;
}

ul.navbar li {
    color:              #ffffff;
    list-style-type:    none;
    display:            inline;
    padding-right:      0;
    padding-left:       0;
    margin-left:        0;
    margin-right:       0;
    border-left:        1px solid #000000;
    border-right:       1px solid #000000;
    border-bottom:      1px solid #000000;
    font-size:          10pt;
}

ul.navbar li.navactive {
    background-color:   #a020f0;
}

ul.navbar li.navinactive {
    background-color:   #3a3f76;
}

ul.navbar li a {
    color:              #ffffff;
    text-decoration:    none;
    background-color:   transparent;
}

.highlighttable {
    padding:            0;
    margin:             0;
    width:              100%%;
    font-family:        "Courier", "Courier New", monospace;
    line-height:        auto;
}

.highlighttable .linenos {
    background-color:   #dddddd;
    padding-left:       0.0em;
    padding-right:      0.0em;
    margin:             0.0em;
    border-right:       3px double #000000;
}

/*** Begin Pygments Styles ***/
%s
</style>

</head>
<body class="highlight">
""" % (os.path.basename(filename), '100%', usehtml.get_style_defs(".highlight"))

print """
<div id="header">
  <h2>%s</h2>
""" % os.path.basename(filename)

print '  <ul class="navbar">'
colors = list(pygstyles.get_all_styles())

for color in colors:
    if (color == colorscheme):
        liclass = 'navactive'
    else:
        liclass = 'navinactive'

    print """    <li class="%s"><a href="%s?color=%s">%s</a></li>""" % (liclass, os.path.basename(filename), color, color)

print "  </ul>"
print "</div>\n"

print pygments.highlight(fullcode, uselexer, usehtml)

# for var in (cgi.os.environ.keys()):
#     print "<p>%s : %s</p>" % (var, cgi.os.environ[var])

print "</body>"
print "</html>"
