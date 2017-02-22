## Denver Open Street Map Munging  
### Map Area

Denver, CO, United States  
* http://www.openstreetmap.org/relation/253750 

I currently live and work in Denver but am new to the area so I thought I'd explore the OSM  
data and see what it contains

### Problems found in data set
I first downloaded a much smaller sample set of Denver to start invesigating any problems. Below is what  
I found and how I addressed the issues:

Most of the user entered data simply had inconsistent abbreviations which I decided to clean up:

*  Ave changed to Avenue
*  Dr changed to Drive
*  Pky to Parkway
*  ct to Court, as well as Ct to Court
*  Rd and Rd. as well as Ave., these small changes were more difficult to catch

I kept some the entered data the same like North State Highway 83 and Park Avenue West even though they at first appeared to need cleaning.  The vast majority of problems were fixed by auditing the data and then changing them to the updated names mapping that I continue updating as I saw more and more of my data set.

The sample that I used, being so small, didn't fully prepare me for the errors that existed in the truly OSM file.  After loading that and beginning to clean it, I had to circle back and look at additional problems created like the abbreviations with a '.' at the end.

### Overview of the data

#### Size of the file:     

```python
denver-boulder_colorado.osm.....850mb  
sample.osm....4mb  
nodes.csv...325mb  
nodes_tags.csv...11mb  
ways.csv...26mb  
ways_tags.csv...108mb  
way_nodes.csv...62mb
```
