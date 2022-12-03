
## README.md

本pj要实现两个功能：格式转换、标签统计

### 一些全局函数

***get_list_scene***

get_list_scene函数用来返回主菜单的子scene链接路径
入参为主菜单路径home_path，以只读模式打开home路径上的文件，
通过*re.compile(r'"\.(/m.*?)"')*匹配子幕路径，
html中展示的子scene路径为./xxxxxxx，而我们更想要的是直接将子路径append到current_path上，故匹配'.'后面的部分

### 格式转换

***manage_scene***

manage_scene函数用来将每一scene的html格式的剧本变为string格式
以只读方式打开一个scene的html文件，以*for line in file*的方法按行读取（在本porject中按行读取易于后续操作）

（1）处理大标题act
一共有20个scene，但是只有五个act，因此不是每一个新打开的scene文件都会输出出当前的act
这里我们引入一个全局变量*global act*，每次新打开scene文件时用*re.compile('\\bAct (\d)')*匹配当前act
将*current_act*与全局*act*比较，若相同则说明还在同一个act之下，不用输出；
若不相同则说明已经到了新的act，需用*new_script+="\n"+"## ACT "+str(current_act)+"\n"*输出act，并更新全局变量*act*的值

（2）处理次级标题scene
scene比较好处理，用正则表达式*re.compile('&lt;title>(.*)')*匹配scene
用*new_script+="\n### "+current_scene+"\n"*输出scene
这里有一点需要注意：不需要担心scene和act被匹配多次，因为每个html都会在首部按顺序出现title和act，故findall找到act之后break即可

（3）处理小标题instrution、name
对于每一行，用*re.compile('<i&gt;(.*)</i&gt;')*匹配instruction
对于每一行，用re.compile('<b&gt;(.*)</b&gt;')*匹配name

（4）处理文本text
用*re.compile('>(.*)</A&gt;<br&gt;')*匹配text
需要注意的一点是：仔细观察生成的markdown文件会发现有些行首出现了一些blank
我们用一个while语句循环删除blank
另外需要注意的是：我们自己写markdown时会遇到一些“烦人”的处境，需要我们用escape characters（转义字符）
虽然正则匹配到的text部分看起来没有需要转义的地方，但是我们还是写一句转义（至少看起来考虑过hhhhh）

***change_string_to_md***

change_string_to_md函数用来将string型的script写入markdown文件
一个open，一个write，一个close就已经结束嘞

### 标签统计

***get_list_tags***

get_list_tags函数用来返回一个字典，存储一个scene内的所有标签及其数量
以只读方式打开一个scene的html文件，以*for line in file*的方法按行读取

（1）处理两个特殊的标签（向命运屈服了）
有两个标签比较特殊:<!DOCTYPE>和&lt;meta>,它们的标签不在同一行闭合，并且内容中有'/'
如果看一看被注释掉的那一段，您可能不明白我的尝试，我想给这两个标签在所在行手动闭合，加上'>',然后删除'/'
后续即可和其他标签一同匹配，但是很遗憾失败了
所以我们手动添加两种标签到dict中，其数量通过*line.find('<!')*和*line.find('<meta')*匹配递增

（2）用一个方法处理剩余所有标签
由于一个正常的标签</***>一定有与之对应的<***>，而<***>不一定有与其对应的</***>，因此我们考虑过滤掉形如</***>的标签
使用*re.compile('<[^/].*?>')*匹配所有非</***>标签
这时我们注意到有一些标签如<A name=>和<A href=>，需要将其变成标签&lt;a>
因此我们使用*find_tag[i]=find_tag[i].split(" ")[0].lower()*取空格前的字符串并转换成小写
这样即可匹配出<A,<br等半成品标签
手动加上'>'后即可获得所有标签
下面时计数相关说明：
第一次匹配到某个标签的时候，将其加入dict并设置数量为1；后面再匹配到的时候直接将value++

***merge_dict***

merge_dict函数用来合并两个字典
分别遍历新字典和老字典，如果老字典中找不到新字典的某个key，就将此key加入老字典并置value为1
如果找到key，就将相同的key对应value++

***get_key***

get_key函数用来返回字典中某个value对应的key
遍历字典的key，如果其值为value就break掉，返回key就ok了

### main

调用*get_list_scene*获得子scene路径
遍历*get_list_scene*，对于每一个scene做*manage_scene*和*get_list_tags*操作
对于每次返回的新字典，将其与原字典merge一下，最终形成一个总字典
对总字典中的value进行sort，取最大的三个get_key找其key
最终打印






