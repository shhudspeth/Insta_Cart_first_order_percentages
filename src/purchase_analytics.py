#purchase_analytics.py

import csv
import create_dictions
import sys

input_prod= sys.argv[1]
input_file_dept = sys.argv[2]
output_file = sys.argv[3]

#reads cvs file and skips header
reader_prod = csv.reader(open(input_prod, 'r'))
reader_prod.next()

#makes a list of products, counts the number of times they were ordered
# and counts if it was a first time order
dict_product_orders = create_dictions.product_count(reader_prod)

#makes a dictionary of department ids from products.csv and skips header
reader_dept = csv.reader(open(input_file_dept, 'r'))
reader_dept.next()

#makes a dictionary of the department ids and connected product ids
dict_depart_id = create_dictions.department(reader_dept)

#makes a dictionary organized by department of order counts, first orders,
#and makes the percentage of the two
dict_of_totals = create_dictions.orders_from_department(dict_depart_id,dict_product_orders)

#takes the dictionary of totals and finds those with order, writes to reportfile
create_dictions.write_csv(dict_of_totals, output_file)
