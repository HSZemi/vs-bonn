#! /usr/bin/env python3

import os
import os.path
import subprocess
import shutil
import sys

names = []
htmlroot = "/vs-bonn/"
convert_command = "sed -e 's/^(/\\\\(/' {0}.md | pandoc --from=markdown --to=paragraphs.lua -o {1}.html"

htmltemplate = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>vs-bonn directory</title>  
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
<link rel="stylesheet" href="{1}style.css">
</head>
<body>
<div class="container">
{0}
</div>
</body>
</html>
'''


def path_to_top(level):
	if(level == 0):
		return "./"
	else:
		return "../" * (level)

def generate_navtree(names, filterprefix, level):
	order = {}
	for(prefix, name, _) in names:
		if(prefix.startswith(filterprefix)):
			if prefix not in order:
				order[prefix] = []
			order[prefix].append(name)
		
	navtree = ""
	for key in sorted(order):
		navtree += "<b><a href='{0}{1}'>{1}</a></b>\n<ul>".format(path_to_top(level),key)
		for item in order[key]:
			navtree += "<li><a href='{0}{1}/{2}.html'>{2}</a></li>\n".format(path_to_top(level), key, item)
		navtree += "</ul>\n"
	return navtree

def generate_breadcrumbs(path, name, level, toplevel=False):
	breadcrumbs = '<ol class="breadcrumb">'
	
	current_path = path_to_top(level)
	breadcrumbs += '<li><a href="{0}">TOP</a></li>\n'.format(current_path)
	
	if(not toplevel):
		for item in path.split("/"):
			current_path += (item + "/")
			label = item
			breadcrumbs += '<li><a href="{0}">{1}</a></li>\n'.format(current_path, label)
		breadcrumbs += '<li class="active">{0}</li>\n'.format(name)
	breadcrumbs += '</ol>'
	return breadcrumbs


#for all folders not named html:
for item in ('toc.js', 'style.css'):
	shutil.copyfile('./res/{0}'.format(item), os.path.join("./html/", item))
for (dirpath, dirnames, filenames) in os.walk('./md'):
	level = dirpath.replace("./md", '').count(os.sep)
	for name in filenames:
		if(name[-3:] == '.md'):
			names.append((dirpath[5:], name[:-3], level))
	for directory in dirnames:
		if(not os.path.exists(os.path.join("./html", dirpath[5:], directory))):
			os.makedirs(os.path.join("./html", dirpath[5:], directory))
		


names.sort()
print(names)

folders = []
for(prefix, name, lvl) in names:
	if prefix not in folders:
		folders.append(prefix)
		navtree = generate_navtree(names, prefix, lvl)
		breadcrumbs = generate_breadcrumbs(prefix, "", lvl)
		f = open(os.path.join("./html", prefix, "index.html"), "w")
		print(htmltemplate.format(breadcrumbs + navtree, path_to_top(lvl)), file=f)
		f.close()



#	convert all files ending on .md to the respective html output in the html folder
for name in names:
	mdpath = os.path.join("./md", name[0], name[1])
	htmlpath = os.path.join("./html", name[0], name[1])
	level = name[2]
	print("Converting {0}.md	to {1}.html".format(mdpath, htmlpath))
	print(convert_command.format(mdpath, htmlpath))
	subprocess.call(convert_command.format(mdpath, htmlpath), shell=True)
	
for name in names:
	htmlpath = os.path.join("./html", name[0], name[1])
	level = name[2]
	f = open("{0}.html".format(htmlpath), "r")
	content = f.read()
	f.close()
	
	navitems = ''
	for filename in names:
		urlpath = os.path.join(path_to_top(level), filename[0], filename[1])
		if(name == filename):
			navitems += '<li><a href="{0}.html" class="active">{1}</a></li>\n'.format(urlpath, filename[1])
		else:
			navitems += '<li><a href="{0}.html">{1}</a></li>\n'.format(urlpath, filename[1])
	
	breadcrumbs = generate_breadcrumbs(name[0], name[1], level)
	
	f = open("{0}.html".format(htmlpath), "w")
	f.write(content.replace('<!-- Navigation -->',breadcrumbs).replace("<!-- PATH-TO-TOP -->", path_to_top(level)))
	f.close()


# create an index file referencing those files in the html folder
htmllist = ''
for name in names:
	urlpath = os.path.join("./", name[0], name[1])
	htmllist += '<li><a href="{0}.html">{1}</a></li>'.format(urlpath, name[1])

breadcrumbs = generate_breadcrumbs("", "TOP", 0, toplevel=True)

f = open('html/index.html', 'w')
print(htmltemplate.format(breadcrumbs + generate_navtree(names, "", 0), path_to_top(0)), file=f)
f.close()