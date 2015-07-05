#! /usr/bin/env python3

import os
import os.path
import subprocess
import shutil
import sys

names = []
titles = {}
htmlroot = "/vs-bonn/"
convert_command = "sed -e 's/^(/\\\\(/' -e 's/\\(date:\\s*[0-9]\\+\\)\\./\\1\\\\./' {0}.md | pandoc --from=markdown --to=paragraphs_single.lua -o {1}.html"

htmltemplate = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>  
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
<link rel="stylesheet" href="{path_to_top}style.css">
</head>
<body>
<div class="container">
{content}
</div>
</body>
</html>
'''

htmltemplatefile = "res/template_sp.html"
with open(htmltemplatefile, "r") as f:
	htmltemplate = f.read()


def path_to_top(level):
	if(level == 0):
		return "./"
	else:
		return "../" * (level)

def generate_navtree(names, titles, filterprefix, level):
	order = {}
	for name in names:
		prefix = name[0]
		fname = name[1]
		title = titles[name]
		if(prefix.startswith(filterprefix)):
			if prefix not in order:
				order[prefix] = []
			order[prefix].append((fname,title))
		
	navtree = ""
	for key in sorted(order):
		navtree += "<b><a href='{0}{1}/index.html'>{1}</a></b>\n<ul>".format(path_to_top(level),key)
		for fname, title in order[key]:
			navtree += "<li><a href='{0}{1}/{2}.html'>{3}</a></li>\n".format(path_to_top(level), key, fname, title)
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
			breadcrumbs += '<li><a href="{0}index.html">{1}</a></li>\n'.format(current_path, label)
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


#	convert all files ending on .md to the respective html output in the html folder
for name in names:
	mdpath = os.path.join("./md", name[0], name[1])
	htmlpath = os.path.join("./html", name[0], name[1])
	level = name[2]
	
	title = ''
	short = ''
	
	with open("{0}.md".format(mdpath), "r") as f:
		for line in f:
			if(line.startswith("title:")):
				title = line[6:].strip()
			if(line.startswith("short:")):
				short = line[6:].strip()
	print("Title: {0}".format(title))
	print("Short: {0}".format(short))
	if short == '':
		short = title
	titles[name] = short
	print("Converting {0}.md	to {1}.html".format(mdpath, htmlpath))
	print(convert_command.format(mdpath, htmlpath))
	subprocess.call(convert_command.format(mdpath, htmlpath), shell=True)
	
	htmlcontent = ''
	with open("{0}.html".format(htmlpath), "r") as f:
		htmlcontent = f.read()
	
	with open("{0}.html".format(htmlpath), "w") as f:
		f.write(htmltemplate.format(content=htmlcontent, navigation='', path_to_top=path_to_top(level), title=name[1]))

folders = []
for(prefix, name, lvl) in names:
	if prefix not in folders:
		folders.append(prefix)
		navtree = generate_navtree(names, titles, prefix, lvl)
		breadcrumbs = generate_breadcrumbs(prefix, "", lvl)
		f = open(os.path.join("./html", prefix, "index.html"), "w")
		print(htmltemplate.format(content=breadcrumbs + navtree, path_to_top=path_to_top(lvl), title=prefix), file=f)
		f.close()


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
			navitems += '<li><a href="{0}.html" class="active">{1}</a></li>\n'.format(urlpath, titles[filename])
		else:
			navitems += '<li><a href="{0}.html">{1}</a></li>\n'.format(urlpath, titles[filename])
	
	breadcrumbs = generate_breadcrumbs(name[0], name[1], level)
	
	f = open("{0}.html".format(htmlpath), "w")
	f.write(content.format(navigation=breadcrumbs, path_to_top=path_to_top(level)))
	f.close()


# create an index file referencing those files in the html folder
htmllist = ''
for name in names:
	urlpath = os.path.join("./", name[0], name[1])
	htmllist += '<li><a href="{0}.html">{1}</a></li>'.format(urlpath, name[1])

breadcrumbs = generate_breadcrumbs("", "TOP", 0, toplevel=True)

f = open('html/index.html', 'w')
print(htmltemplate.format(content=breadcrumbs + generate_navtree(names, titles, "", 0), path_to_top=path_to_top(0), title="Index"), file=f)
f.close()