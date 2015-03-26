#! /usr/bin/env python3

import os
import os.path
import subprocess

names = []
pandocargs = "pandoc --from=markdown --to=paragraphs.lua -o html/{0}.html {0}/{0}.md"

htmltemplate = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>vs-bonn directory</title>
</head>
<body>
<h1>vs-bonn</h1>
{0}
</body>
</html>
'''

#for all folders not named html:
for name in os.listdir('.'):
	if(os.path.isfile("{0}/{0}.md".format(name))):
		names.append(name)
		
#	convert all files ending on .md to the respective html output in the html folder
for name in names:
	subprocess.call(pandocargs.format(name), shell=True)


# create an index file referencing those files in the html folder
htmllist = '<ul>'
for name in names:
	htmllist += '<li><a href="{0}.html">{0}</a></li>'.format(name)
htmllist += '</ul>'

f = open('html/index.html', 'w')
print(htmltemplate.format(htmllist), file=f)
f.close()