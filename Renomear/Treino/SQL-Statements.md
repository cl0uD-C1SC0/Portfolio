# TASK 5: ULTIMA QUERY:
```sql
    SELECT DISTINCT _garbage_file_extract FROM customers c
    JOIN rentals r ON r.customerid = c.id
    JOIN unicorns u on u.id = r.unicornid
    JOIN reviews rw ON rw.rentalid = r.id
    WHERE c.name like 'Michael Bolton'
```

# Possíveis:
```sql
    SELECT AVG( column_name ) FROM table_name
    SELECT AVG(id) FROM customers
```
# ORDER BY:
```sql
    SELECT column_name FROM table_name ORDER BY nome;
```
# WHERE CONDITION:
```sql
    SELECT age,condition FROM "databaet"."unicorns" WHERE condition = 'dangerously bad'
    AND age > 9000;
```

# CLOUDWATCH SQL STATEMENT 1:
# sort packetsTransnffered
```sql
    filter action="Inbound REJECT, Inbound ACCEPT, outbound REJECT: NACL" |
    stats sum(packets) as packetsTransferred by srcAddr, dstAddr
    | sort packetsTransffered desc
    | limit 15

```
# ORDER BY TWO TABLES:
```sql
    SELECT nome, data_nascimento FROM pessoa ORDER BY nome, data_nascimento;
```
#
#
# QUERY EXAMPLE DATABASE (aws_service_logs) TABLE (cf_access_optimized):
```sql
    SELECT * FROM aws_service_logs.cf_access_optimized LIMIT 10
                ou
    SELECT * FROM "aws_service_logs"."cf_access_optimized" LIMIT 10
```
# QUERY WITH DESC:
```sql
    SELECT * FROM aws_service_logs.cf_access_optimized ORDER BY time DESC LIMIT 10
```
# QUERY WITH ASC:
```sql
    SELECT * FROM aws_service_logs.cf_access_optimized ORDER BY time ASC LIMIT 10
```

# QUERY WITH SUM AND WHERE AND BETWEEN:
```sql
    SELECT SUM(bytes) AS total_bytes FROM aws_service_logs.cf_access_optimized WHERE time BETWEEN TIMESTAMP '2018-11-02' AND TIMESTAMP '2018-11-03'
```