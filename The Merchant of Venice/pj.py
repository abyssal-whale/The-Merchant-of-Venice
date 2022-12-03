# this is a project executing an HTML file into markdown format and find three top-used labels
# a brief introduction of this project is in README.md 
import os
import re

act=0   # indicate which action is at present

def get_list_scene(home_path):    # return the path of child scenes
    # print(str)
    scene_list=[]
    with open(home_path,'r') as f:
        for line in f:
            reg = re.compile(r'"\.(/m.*?)"')
            child_scene=re.findall(reg,line)
            # print(child_scene)
            if len(child_scene)!=0:
                scene_list.append(child_scene[0])
    # print(scene_list)
    return scene_list 

def manage_scene(scene_path):   # manage each scene into particular format
    new_script=""
    with open(scene_path,'r') as file:
        current_act=0
        current_scene=""
        global act
        for line in file:
            # print(line)
            # this part is used to extract the number and name of scene from html
            reg_for_scene=re.compile('<title>(.*)')
            find_scene=re.findall(reg_for_scene,line)
            if len(find_scene)!=0:
                current_scene+=find_scene[0]

            # this part is used to judge whether we shall print the current act
            reg_for_act=re.compile('\\bAct (\d)')
            find_act=re.findall(reg_for_act,line)
            if len(find_act)!=0:
                current_act=int(find_act[0])
                # print(current_act)
                break
        if current_act!=act:
            act=current_act
            new_script+="\n"+"## ACT "+str(current_act)+"\n"
        new_script+="\n### "+current_scene+"\n"

        # this part is used to manage the content of script
        for line in file:
            # whether it's an instruction line
            reg_for_instruction=re.compile('<i>(.*)</i>')
            find_instruction=re.findall(reg_for_instruction,line)
            if len(find_instruction)!=0:
                new_script+="\n*"+find_instruction[0]+"*\n"
                
            # whether it's a name line
            reg_for_name=re.compile('<b>(.*)</b>')
            find_name=re.findall(reg_for_name,line)
            if len(find_name)!=0:
                new_script+="\n**"+find_name[0]+"**\n\n"
                
            # whether it's a text line
            reg_for_text=re.compile('>(.*)</A><br>')
            find_text=re.findall(reg_for_text,line)
            if len(find_text)!=0:
                # delete the empty space in the front of text
                empty=0
                while empty==0:
                    if find_text[0][0]==' ':
                        find_text[0]=find_text[0][1:]
                    else:
                        empty=1
                # using escape characters
                find_text[0].replace("<","/&lt;").replace(">","/&gt;")
                new_script+=find_text[0]+"\n"
    # print(new_script)
    return new_script

def change_string_to_md(str,write_path):    # write string into .md file
    file=open(write_path,'w')
    file.write(str)
    file.close()

def get_list_tags(path):    # return a dictionary of tags and their numbers
    dict={'<!doctype>':0,'<meta>':0}
    with open(path,'r') as file:
        for line in file:
            """
            if line[0]=='<' and line[len(line)-2]!='>':
                line=line[:len(line)-2]+'>'+line[len(line)-2:]
                line.replace('/','')
                print(line)
            """
            # handle two irregular situation
            if line.find('<!')!=-1:
                dict['<!doctype>']+=1
            elif line.find('<meta')!=-1:
                dict['<meta>']+=1

            # handle regular situation, just focus on <***> tags with ignorance on </***> tags
            reg_for_tag=re.compile('<[^/].*?>')
            find_tag=re.findall(reg_for_tag,line)
            # print(find_tag)
            for i in range(0,len(find_tag)):
                find_tag[i]=find_tag[i].split(" ")[0].lower()   # change all tags to lower case
                if find_tag[i][-1]!='>':
                    find_tag[i]+='>'
                flag=0  # determine whether a key is already in the dictionary
                for key in dict.keys():
                    if find_tag[i]==key:
                        flag=1
                        break
                if flag==0: # did not match
                    dict[find_tag[i]]=1
                else:   # match
                    dict[find_tag[i]]+=1
    # print(dict)
    return dict

def merge_dict(dict_old:dict,dict_new:dict):    # merge two dictionaries
    for key_new in dict_new.keys():
        flag=0  # determine whether a key is already in the dictionary
        for key_old in dict_old.keys():
            if key_old==key_new:
                flag=1 
                break
        if flag==0: #did not match
            dict_old[key_new]=dict_new[key_new]
        else:   # match
            dict_old[key_new]+=dict_new[key_new]
    return dict_old

def get_key(my_dict,val):   # get key by its value
    for key, value in my_dict.items():
         if val == value:
             return key

if __name__ == '__main__':
    current_path = os.getcwd()
    scenes=get_list_scene(current_path+"/data/Merchant of Venice_ List of Scenes.html")
    main_dict=get_list_tags(current_path+"/data/Merchant of Venice_ List of Scenes.html")
    # print(main_dict)
    script=""
    for i in range(0,len(scenes)):
        script+=manage_scene(current_path+"/data"+scenes[i])
        new_dict=get_list_tags(current_path+"/data"+scenes[i])
        main_dict=merge_dict(main_dict,new_dict)
    # print(main_dict)
    value_lst=[]
    for key in main_dict.keys():
        value_lst.append(main_dict[key])
    value_lst.sort()
    for i in range(1,4):
        value=value_lst[-i]
        key=get_key(main_dict,value)
        print("第{}大的值数量为{}，其对应标签为{}\n".format(i,value,key))
    change_string_to_md(script,current_path+"/document/The Merchant of Venice.md")
