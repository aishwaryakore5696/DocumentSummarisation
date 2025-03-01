
import pydot
import sys
import os

# Configuration variables
ranksep = '2 equally' # distance between nodes (suggested values: 1-3) => (graphviz varialbe)
overlap='false' # whether the nodes overlap each other (true or false) => (graphviz varialbe)
splines='true' # whether the lines are straight or curved (true or false) => (graphviz varialbe)
gen_dot = False # whether the dot file should be generated => (python varialbe)

# the list can be managed by a manually defined array of colors

def GenerateColors():
	colors_nodes = InitArrayOfcolors('black', ['grey', '#bfe8f5', '#a1f1b3', '#d7301f', '#b00300', '#700f00'])
	colors_font = InitArrayOfcolors('white', ['black', 'black', 'black'])
	return (colors_nodes, colors_font)

def getAttributes(node, level):
	# provides access to colors
	colors_nodes, colors_font = GenerateColors()
	# investigates edge
	# default edge
	if type(node) is tuple:
		return {
		'penwidth':'1',
		'color':'black'}
	# root node
	if level is 0:
		return {'shape':'box, filled',
		'fillcolor':'gray',
		'style':'"filled"',
		'penwidth':'1',
		'color':colors_nodes[level + 1],
		'fontcolor':'black',
		'fontsize':'20'
	}
	
	# investigates node
	# remove whitespaces
	node = node.strip()
	# __underlined__
	if node.startswith("__") and node.endswith("__"):
		return {'shape':'box',
		'style':'"rounded,filled"',
		'penwidth':'1',
		'label':node[2:-2],
		'fillcolor':'yellow',
		'color':colors_nodes[level],
		'fontcolor':'black',
		'fontsize':'15'}
	# **bold**
	if node.startswith("**") and node.endswith("**"):
		return {'shape':'box',
		'style':'"rounded, filled"',
		'penwidth':'1',
		'label':node[2:-2],
		'color':'black',
		'fillcolor':'red',
		'fontcolor':'black',
		'fontsize':'15'}
	# //italic//
	if node.startswith("//") and node.endswith("//"):
		return {'shape':'box',
		'style':'"rounded, filled"',
		'penwidth':'1',
		'label':node[2:-2],
		'color':'black',
		'fillcolor':'green',
		'fontcolor':'black', 
		'fontsize':'15'}
	# standard node
	else:
		return {'shape':'box',
		'fixedsize': 'false',
		'style':'filled',
		'penwidth':'1',
		#'fillcolor':'#bfe8f5',
		'fillcolor':colors_nodes[level],
		'color':colors_nodes[level + 1],
		'fontcolor':colors_font[level],
		'fontsize':'15'}

def InitArrayOfcolors(default, colors):
	# generates an array of 12 colors
	colors_nodes = [default for x in range(12)]
	return colors + colors_nodes[len(colors):]

def ReadFile(filename):
	fh = open(filename)
	return [x.rstrip() for x in fh.readlines()]

def CreateEdges(lines):
	edge_list = ['' for x in range(50)]
	mindmaps = []
	edges = []
	for line in lines:
		if (line is "" and len(edges) > 0):
			print ("mindmap name: %s" % edges[0][0])
			mindmaps.append(edges)
			edges = []
			continue
		# identify right indent (tabs excluding tabs in the text)
		tabs_all = line.count('\t')
		line = line.strip()
		pos = tabs_all - line.count('\t')
		# removes comments (tabbed text)
		index = line.find("\t")
		if index is not -1: line = line[:index]
		# assign extracted text from a line
		edge_list[pos] = line
		if pos:
			edges.append((edge_list[pos - 1], edge_list[pos], pos - 1))
	if (len(edges) > 0):
		print ("mindmap name: %s" % edges[0][0])
		mindmaps.append(edges)
	return mindmaps

def CreateGraphFromEdges(mindmaps, path):
	for edges in mindmaps:
		# defines graph (according to configuration variables)
		g = pydot.Dot(splines=splines, overlap=overlap, ranksep=ranksep, root="%s" % edges[0][0])
		# iterates through edges
		for edge in edges:
			g.add_node(pydot.Node(edge[0], **getAttributes(edge[0], edge[2])))
			g.add_node(pydot.Node(edge[1], **getAttributes(edge[1], edge[2] + 1)))
			g.add_edge(pydot.Edge(edge[0], edge[1], **getAttributes((edge[0], edge[0]), edge[2])))
		# in a case that there is only one mindmap on a page there is no reason for extension of a mm_title to a mm_title_rootnode
		if len(mindmaps) == 1:
			output = "%s" % (path)
		else:
			# extending a file name in a case of multiple mindmaps per file
			output = "%s_%s" % (path, edges[0][0])
		# creates dot file according to prog parameter
		if gen_dot:
			g.write('%s.dot' % str(output), prog='twopi')
		# creates image file according to prog parameter
		g.write_png('%s.png' % str(output), prog='twopi')

def main(argv):
	# extract path to an attachment directory (remove *.txt extension)
	path = argv[1][:-4]
	# extract page name from a path
	page = str(path.split("/")[-1:][0])
	print(path)
	# construct output directory (deprecated)
	path = "%s" % (path)
	print(path)
	CreateGraphFromEdges(CreateEdges(ReadFile(argv[1])), path)

if __name__ == "__main__":
	main(sys.argv)