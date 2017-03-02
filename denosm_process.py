
# coding: utf-8

# In[4]:

import sqlite3

db = sqlite3.connect("den2")
c = db.cursor()
c2 = db.cursor()
QUERY = """SELECT n.lat, n.lon from nodes as n"""
q2 = """select nt.value, count(*) from nodes_tags as nt
        group by nt.value
        order by count(*) desc"""
c.execute(QUERY)
c2.execute(q2)
rows = c.fetchall()
rows2 = c2.fetchall()

db.close()


# In[5]:

hp = 39.75
vp = -105.010845

q1 = 0
q2 = 0
q3 = 0
q4 = 0

print len(rows)
for row in rows:
    try:
        lat = float(row[0].strip())
    except:
        continue
    try:
        lon = float(row[1])
    except:
        continue
    if lat > hp:
        if lon < vp:
            q1 += 1
        else:
            q2 += 1
    elif lat < hp:
        if lon < vp:
            q4 += 1
        else:
            q3 += 1
        
print q1, q2, q3, q4


# In[13]:

db = sqlite3.connect("den2")
c = db.cursor()
c2 = db.cursor()
QUERY = """select count(nt.key) from nodes_tags as nt
            where nt.key = 'brewery';"""
q2 = """select nt.value from nodes_tags as nt
            where nt.key = 'postcode'
        limit 10;"""
c.execute(QUERY)
c2.execute(q2)
rows = c.fetchall()
rows2 = c2.fetchall()

print rows

db.close()


# In[14]:

db = sqlite3.connect("den2")
c = db.cursor()
c2 = db.cursor()
QUERY = """select nt.key, count(distinct nt.key) from nodes_tags as nt
            group by nt.key order by count(nt.key) desc limit 100;"""

q2 = """select n.user, count(distinct n.id) from nodes_tags as nt
        join nodes as n on n.id = nt.id
        where nt.key = 'brewery'
        group by n.user
        order by count(n.id) desc;"""
c.execute(QUERY)
c2.execute(q2)
rows = c.fetchall()
rows2 = c2.fetchall()


db.close()


# In[15]:

from pprint import pprint
pprint (rows2)


# In[16]:

db = sqlite3.connect("den2")
c = db.cursor()
c2 = db.cursor()
QUERY = """SELECT COUNT(DISTINCT(b.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) as b;"""

c.execute(QUERY)
rows = c.fetchall()
db.close()

from pprint import pprint
pprint (rows)


# In[ ]:



