#! /usr/bin/env python3

import os
import os.path
import subprocess

names = []
pandocargs = "pandoc --from=markdown --to=paragraphs.lua -o html/{0}.html md/{0}.md"

htmltemplate = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>vs-bonn directory</title>  
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
{0}
</div>
</body>
</html>
'''

navitemplate = '''
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="index.html">vs-bonn</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
	{0}
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
'''

#for all folders not named html:
for name in os.listdir('./md'):
	if(os.path.isfile("./md/{0}".format(name)) and name[-3:] == '.md'):
		names.append(name[:-3])

names.sort()
#	convert all files ending on .md to the respective html output in the html folder
for name in names:
	print("Converting ./md/{0}.md	to ./html/{0}.html".format(name))
	subprocess.call(pandocargs.format(name), shell=True)
	
for name in names:
	f = open("html/{0}.html".format(name), "r")
	content = f.read()
	f.close()
	
	navitems = ''
	for filename in names:
		if(name == filename):
			navitems += '<li><a href="{0}.html" class="active">{0}</a></li>\n'.format(filename)
		else:
			navitems += '<li><a href="{0}.html">{0}</a></li>\n'.format(filename)
	
	f = open("html/{0}.html".format(name), "w")
	f.write(content.replace('<!-- Navigation -->',navitemplate.format(navitems)))
	f.close()


# create an index file referencing those files in the html folder
htmllist = ''
for name in names:
	htmllist += '<li><a href="{0}.html">{0}</a></li>'.format(name)

f = open('html/index.html', 'w')
print(htmltemplate.format(navitemplate.format(htmllist)), file=f)
f.close()