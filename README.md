# BookMarker

Simple CLI to add a bookmark from anywhere in your terminal. 

## Useage
install: 
```
./install.sh
```
then after installation is complete, you can use the following examples, from anywhere in your terminal to add a bookmark to your documents folder. 

```
bookmark http://example.com 
```
or
```
bk http://example.com 
```
Additional optional args can be passed: 
```
bk http://example.com -d "This is a description" -f "This is a Folder Name" -t " tag1, tag2, tag3"
```
Creates a md file and bookmarks.html that looks like this: 

bookmarks.md:
```

- Example Folder
	- [This is an example](https://linktest.com) - Tags: tag1, tag2, tag4
	- [This is an example](https://linktest.com) - Tags: tag1, tag2, tag4
```

bookmarks.html:

```
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DT><H3>Example Folder</H3>
<DL>
<DT><A HREF="https://linktest.com" TAGS="tag1, tag2, tag4">This is an example</A>
<DT><A HREF="https://linktest.com" TAGS="tag1, tag2, tag4">This is an example</A>
</DL>

```


## Additional Args
Create Subfolders (passed with link)
```
bk -f "folder/subfolder/subfolder of a subfolder/etc"
```
List all "Folders":
```
bk --folders
```
List all Links: 
```
bk --list --all
```
List All Links Within A "Folder":
```
bk --list --f "Folder/Subfolder/etc"
```
List All By Tag
```
bk --list --t "Tag"
```
Export to bookmarks.html
```
bk --export
```
Import Existing bookmarks.html from browser
```
bk --import "path/to/your/bookmarks.html"
```





## TO-DO
- ~~Folder Heirachies ~~
- ~~List All Within A Folder~~
- ~~List All By Tag~~
- add date added field so it doesnt interfere with the html file
- add syntax handling so mispelled words dont auto get added to link list