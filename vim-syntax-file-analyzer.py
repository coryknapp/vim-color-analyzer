import os
import sys

#global options
syntax_directory = "/usr/local/Cellar/macvim/7.4-77/MacVim.app/Contents/Resources/vim/runtime/syntax"

#global variables
parent_child_list = []
keyword_map = {}

cascade_map = {}

def main():
    """Reads all `.vim` files in the syntax directory and outputs a summery

    :syntax_directory: TODO
    :returns: TODO

    """

    file_to_syn_command_list = {}

    for filename in os.listdir(syntax_directory):
        file_to_syn_command_list[filename] = analyze_file(syntax_directory+"/"+filename)

    #find parents in parent_child_list who are not listed as the child in any
    #other p/c group; these children will be roots of the tree of
    #`hi def link` groups
    for pc_group in parent_child_list:
        parent = pc_group[0]
        child = pc_group[1]
        success_flag = False
        for pc_parent_check_group in parent_child_list:
                # pc_group's parent is a child of another group, and we can
                # and we can ignore it
                if pc_group[0] == pc_parent_check_group[1]:
                    success_flag = True
                    break
        if success_flag:
            break
        cascade_map[ pc_group[0] ] = {}
    
    #now we have a list of parents
    

    for filename in sorted(file_to_syn_command_list):
        
        print "\" " + filename + " {{{\n"
        for command in file_to_syn_command_list[filename]:
            print "\" " + print_path_for_syn_command( command )
            print "\" hi " + command + " \n\"\t\\ ctermfg=1 ctermbg=0 cterm=NONE " \
			+ "\n\"\t\\ guifg=#ffffff" \
			+ "\n\"\t\\ guibg=#000000" \
                        + "\n\"\t\\ gui=NONE\n"
        print "\" }}}"

def print_path_for_syn_command( syn_command ):
    for pc_group in parent_child_list:
        if pc_group[1] == syn_command:
            return syn_command + ">" + print_path_for_syn_command( pc_group[0] )
    return syn_command

def analyze_file( file_name ):
    """find syn commands in file_name and print results

    :file_name: TODO
    :returns list of syn names

    """

    match_keywords = [ "match", "region", "keyword" ]

    list_of_syn = []
    with open(file_name) as f:
        for line in f.readlines():
            split_line = line.split()
            #check for `syn` commands
            if len( split_line ) > 0 and split_line[0] == "syn" and \
                    split_line[1] in match_keywords:
                #we found one!
                if split_line[2] not in list_of_syn:
                    list_of_syn.append( split_line[2] )
                #if it's a keyword, record it's matches
                if split_line[1] == "keyword":
                    keyword_map[ split_line[2] ] = split_line[3:]
                    #TODO check for coalitions in keyword_map
            #check for `hi def link`
            if "".join(split_line[0:3]) == "hideflink":
                child = split_line[3]
                parent = split_line[4]
                parent_child_list.append( [parent, child] )
    return list_of_syn

main()
