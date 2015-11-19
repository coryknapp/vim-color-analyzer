import sys
import os

fh = open( sys.argv[1] )

highlight_list= []

#whole_scheme_map
whole_scheme_map = {}

#color_map maps colors to what highlight groups that use it.
#each element is a dictionary of ctermfg, ctermbg, cterm, guifg, guibg, gui
color_map = {}

for line in fh.readlines():
    if line[0:2] == 'hi':  #we found a highlight group
        #split the line, cut off the head
        hi_line_split = line.split()[1:]
        group_name = hi_line_split[0]
        re_joined = " ".join( hi_line_split[1:])
        highlight_list.append( [group_name, re_joined] )
        if re_joined in whole_scheme_map:
            whole_scheme_map[ re_joined ].append( group_name )
        else:
            whole_scheme_map[ re_joined ] = [ group_name ]

        for color_def in hi_line_split[1:]:
            color_def_split = color_def.split('=')
            #each color is going to have a list that looks something like this
            #['Number', 'guifg'], ['Operator', 'guifg']...
            if color_def_split[1] in color_map:
                color_map[color_def_split[1]].append( [group_name, color_def_split[0] ] )
            else:
                #we have to add color group
                color_map[color_def_split[1]] = [ [group_name, color_def_split[0] ] ]
    else: #not a highlight line
        highlight_list.append( None )

for color in color_map:
#gonna
    single_color_map = {"ctermfg":[], "ctermbg":[], "cterm":[], "guifg":[], "guibg":[], "gui":[] }
    for entry in color_map[color]:
        single_color_map[ entry[1] ].append( entry[0] )
    print_line = color+" "
    for part in single_color_map:
        if len( single_color_map[ part ] ) > 0:
            print_line += part +': ' + str( single_color_map[ part ] )
    #print "\t"+print_line

highlighting_to_name_map = {}
for color in whole_scheme_map:
    print "\" the following highlighting is used by :"
    for hl in whole_scheme_map[color]:
        print "\"\t" + hl
    highlighting_to_name_map[color] = whole_scheme_map[color][0]
    print "let s:cs_"+highlighting_to_name_map[color]+" = \""+color+"\"\n\n"

print """


" Start of highlight groups...
"""

for group in highlight_list:
    if group is None:
        print "\n"
    else:
        print "exec \"hl "+group[0]+" \".s:cs_"+highlighting_to_name_map[group[1]]
