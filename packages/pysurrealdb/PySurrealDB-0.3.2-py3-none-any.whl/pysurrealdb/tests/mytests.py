# add my own installation to path. It is 2 levels up from this file.
import sys, os

sys.path.insert(0, (os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
# sys.path.insert(0, 'C:/Users/Mike/Sync/code/mypysurreal/')


import pysurrealdb as surreal

# conn = surreal.connect(user='test', password='test', database='test', namespace='test')
conn = surreal.connect(host='localhost', port='8000', user='test', password='test', database='db', namespace='ns', client='ws')
# conn = surreal.connect(host='https://sparkling-cherry-9759.fly.dev', user='proth', password='passicus', database='main', namespace='main', client='ws')

name = 'Mike'
qry = f'''
        IF person:{name}.clocked_in = true THEN
            (UPDATE type::thing("dayst", time::floor(time::now(), 1d)) SET {name}[WHERE end = -1].end = time::floor(time::now(), 1m) RETURN DIFF)
        ELSE
            (UPDATE type::thing("dayst", time::floor(time::now(), 1d)) SET {name} += {{start: time::floor(time::now(), 1m), end: -1}} RETURN DIFF)
        END;
        UPDATE person:{name} SET clocked_in = (clocked_in != true) RETURN DIFF'''

q2 = f"UPDATE person:{name} SET clocked_in = (clocked_in != true) RETURN DIFF"
# conn.drop('person')
# conn.insert('test', {'id': 1 , 'name': 'test', 'age': 20.65, 'description': 'Test'})
# conn.query("insert into test {'id': 2 , 'name': 'test2', 'age': 20.65}")
# conn.insert('person', {'id': 2 , 'name': 'test', 'age': 2, 'description': '"This" is `a` test of strange encoding characters.'})
# conn.insert('test', {'id': 3 , 'name': 'test', 'age': 12, 'description': '"This" is `a` test of strange encoding characters.'})
# conn.insert('person', {'id':69 ,'name': "'test'", 'age': 42, 'description': "'This' is `a` test of strange encoding characters."})

# print(conn.query('select total from profiler'))
# print(conn.get("profiler"))
# conn.drop('profiler')
# conn.insert('documents', {'filename': '📜Writing Week 15 - Lesson 15📜.docx'})

conn.drop('person')
# create many records

conn.create('person:Mike', {'name': 'test1'})
# conn.insert('test', {'id': 'test', 'name': 'test1'})
# r = conn.upsert('test', {'id': 'test', 'name': 'test2'})
# r = conn.get('test')
# r = conn.get('test', 'testicles')
r = conn.query(qry)
# r = conn.query(q2)
# print(conn.query("SELECT id FROM test WHERE ((id = 'test:test2'))"))
# r = conn.table('test').insert([{ 'id': 'test', 'name': 'test' }, { 'id': 'test2', 'name': 'test2' }])
print(r)
# Sending b'{"filename": "\\ud83d\\udcdcWriting Week 15 - Lesson 15\\ud83d\\udcdc.docx"}' to http://localhost:8000/key/documents
# Sending b'select * from documents where filename = "\xf0\x9f\x93\x9cWriting Week 15 - Lesson 15\xf0\x9f\x93\x9c.docx"' to http://localhost:8000/sql