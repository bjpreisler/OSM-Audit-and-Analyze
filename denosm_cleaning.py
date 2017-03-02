
# coding: utf-8

# ## Denver Open Street Map Munging  
# ### Map Area
# 
# Denver, CO, United States  
# * http://www.openstreetmap.org/relation/253750 
# 
# I currently live and work in Denver but am new to the area so I thought I'd explore the OSM  
# data and see what it contains
# 
# ### Problems contained in data set
# I first downloaded a much smaller sample set to start invesigating any problems. Below is what  
# I found and how I addressed the issues:
# 

# In[23]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

OSMFILE = "denver-boulder_colorado.osm"


# In[24]:

def count_tags(filename):
    """
    Counts unique tags within an osm file
    
    Parameters
    ---------
    arg1: str
    
    
    Returns
    --------
    dict
        Key is the name of the tag and value is the count
    
    """
    dct = {}
    lst = []
    for event, element in ET.iterparse(filename):
        unique_tag = element.tag
        lst.append(unique_tag)
    for i in lst:
        if i in dct.keys():
            dct[i] += 1
        else:
            dct[i] = 1
    return dct

count_tags(OSMFILE)


# In[25]:

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Circle", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave":"Avenue",
           "Ave.":"Avenue",
            "Rd.":"Road",
           "Rd":"Road",
           "Dr":"Drive",
           "Pky":"Parkway",
           "Pkwy":"Parkway",
           "ct":"Court",
           "Ct":"Court",
           "Cir":"Circle",
           "Pl":"Place"
            }


def audit_street_type(street_types, street_name):
    """
    Creates unique dict of street names that need to be cleaned
    
    Paramenters
    ----------
    arg1: dict
    
    arg2:str
    
    Returns
    ---------
    Dict with street names that match regex
        If the str is characters followed by a '.', it is added
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """
    Provides attribute of element tag
    
    Parameter
    --------
    arg1: osm element
    
    Returns
    --------
    str
        The str attribute of the element tag
    """ 
    
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    Examines file and extracts street types that need cleaning
    
    Parameters
    ----------
    arg1: str
    
    Returns
    ---------
    dict
        Containing street types as key and names as values   
    
    """
    
    
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    
    """
    Cleans a str that matches with a dictionary key
    
    Parameters
    ---------
    arg1: str
    
    arg2: dict
    
    Returns
    --------
    str
        This is the value of the dictionary, the cleaned str  
    """
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
    if street_type in mapping.keys():
        name = re.sub(street_type, mapping[street_type], name)
    return name


# In[26]:

def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name


# In[27]:

test()


# In[28]:

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    """
    Counts how many of specific regexes an element's tag matches with
    
    Parameters
    ---------
    arg1: osm element
    
    arg2: dict
    
    Returns:
    dict
        Updated with counts of matches    
    """
    if element.tag == "tag":
        # YOUR CODE HERE
        for tag in element.iter("tag"):
            #print tag.attrib['k']
            if re.search(lower, tag.attrib['k']):
                keys["lower"]+= 1
            elif re.search(lower_colon, tag.attrib['k']):
                keys["lower_colon"]+=1
            elif re.search(problemchars, tag.attrib['k']):
                keys["problemchars"]+= 1
            else:
                keys["other"]+=1
            
        pass
        
    return keys



def process_map(filename):
    """
    Puts osm file through key_type function
    
    Parameters
    ---------
    arg1: str
    
    Returns
    ---------
    dict
        With counts of regex matches
    
    """
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


# In[29]:

def test():
    keys = process_map(OSMFILE)
    pprint.pprint(keys)
    
test()


# In[30]:

def process_map(filename):
    """
    Produces unique list of uids from file
    
    Parameter
    --------
    arg1: str
    
    Returns
    -------
    lst
        Of uids obtained from parsing input str
    """
    
    users = set()
    for _, element in ET.iterparse(filename):
        if element.get("uid"):
            users.add(element.attrib["uid"])
    return users


def test():
    users = process_map(OSMFILE)
    pprint.pprint(users)
    
test()


# In[31]:

# %load 'schema.py'
schema.py


# In[32]:

import csv
import codecs
import cerberus
import schema
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re


OSM_PATH = "sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type','phone', 'street']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    if element.tag == 'node':
        node_attribs = {}    
        tags = []
        
        for item in NODE_FIELDS:
            if item == 'lat':
                node_attribs[item] = element.attrib[item].strip()
            else:
                node_attribs[item] = element.attrib[item]

        for tag in element.iter("tag"):  
 
            match_prob = PROBLEMCHARS.search(tag.attrib['k'])
            
            if not match_prob:
                node_tag_dict = {} 
                node_tag_dict['id'] = element.attrib['id'] 
                node_tag_dict['value'] = tag.attrib['v']  

                m = LOWER_COLON.search(tag.attrib['k'])
                if not m:
                    node_tag_dict['type'] = 'regular'
                    node_tag_dict['key'] = tag.attrib['k']
                    if tag.attrib['k'] == 'phone':
                        #node_tag_dict['phone'] = PC.search(tag.attrib['v']).group(0)
                        #clean_postcode = re.findall(r'^(\d{5})-\d{4}$', postcode)[0]
                        pn = re.findall(r'^(.*)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$',tag.attrib['v'])
                        if pn:
                            pnh = pn[0][1] + '-' + pn[0][2] + '-' + pn[0][3]
                            node_tag_dict['phone'] = pnh
                elif tag.attrib['k'] == 'addr:street':
                    node_tag_dict['street'] = update_name(tag.attrib['v'],mapping)
                else:
                    chars_before_colon = re.findall('^(.+?):', tag.attrib['k'])
                    chars_after_colon = re.findall('^[a-z_]+:(.+)', tag.attrib['k'])
                    
                    node_tag_dict['type'] = chars_before_colon[0]
                    node_tag_dict['key'] = chars_after_colon[0]

            tags.append(node_tag_dict)
        
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        way_attribs = {}
        way_nodes = []
        tags = []  
    
        for item in WAY_FIELDS:
            way_attribs[item] = element.attrib[item]
    
        for tag in element.iter("tag"):  
 
            match_prob = PROBLEMCHARS.search(tag.attrib['k'])
            if not match_prob:
                way_tag_dict = {}
                way_tag_dict['id'] = element.attrib['id'] 
                way_tag_dict['value'] = tag.attrib['v']  

                m = LOWER_COLON.search(tag.attrib['k'])
                if not m:
                    way_tag_dict['type'] = 'regular'
                    way_tag_dict['key'] = tag.attrib['k']
                else:
                    chars_before_colon = re.findall('^(.+?):', tag.attrib['k'])
                    chars_after_colon = re.findall('^[a-z_]+:(.+)', tag.attrib['k'])

                    way_tag_dict['type'] = chars_before_colon[0]
                    way_tag_dict['key'] = chars_after_colon[0]

            tags.append(way_tag_dict)
        
        
        count = 0
        for tag in element.iter("nd"):  
            way_nd_dict = {} 
            way_nd_dict['id'] = element.attrib['id'] 
            way_nd_dict['node_id'] = tag.attrib['ref'] 
            way_nd_dict['position'] = count  
            count += 1
            
            way_nodes.append(way_nd_dict)
    
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

                    


# In[33]:

process_map(OSM_PATH, validate=False)


# In[ ]:



