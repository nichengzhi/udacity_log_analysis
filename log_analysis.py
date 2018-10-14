#! /usr/bin/env python3
import psycopg2
database_name = "news"

#get query result
def get_queryresult(query_string):
    conn = psycopg2.connect(database=database_name)
    cur = conn.cursor()
    cur.execute(query_string)
    results = cur.fetchall()
    conn.close()
    return results

#1.What are the most popular three articles of all time? 
query1 = "select title, count(*) as views from articles \
            inner join log on log.path like concat('%',articles.slug) \
            where log.status like '%200%' \
            group by title order by views desc limit 3"
#2. Who are the most popular article authors of all time?
query2 = "select name, count(*) as views from articles \
            inner join log on log.path like concat('%',articles.slug) \
            inner join authors on articles.author = authors.id \
            where log.status like '%200%' \
            group by name order by views desc limit 1"
#On which days did more than 1% of requests lead to errors? 
query3 =  "select day, perc from ( \
    select day, round((sum(requests)/(select count(*) from log where \
    substring(cast(log.time as text), 0, 11) = day) * 100), 2) as \
    perc from (select substring(cast(log.time as text), 0, 11) as day, \
    count(*) as requests from log where status like '%404%' group by day) \
    as log_percentage group by day order by perc desc) as final_query \
    where perc >= 1"
#3. On which days did more than 1% of requests lead to errors? 
result1 = get_queryresult(query1)
result2 = get_queryresult(query2)
result3 = get_queryresult(query3)
print("1.What are the most popular three articles of all time? ")
for result in result1:
    print("{} -> {} views".format(result[0],result[1]))
print("Who are the most popular article authors of all time?")
for result in result2:
    print("{} -> {} views".format(result[0],result[1]))
print("On which days did more than 1% of requests lead to errors? ")
for result in result3:
    print("{} -> {} %".format(result[0],result[1]))