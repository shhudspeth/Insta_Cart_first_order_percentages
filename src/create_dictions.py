# create_dictions.py
import csv


def product_count(info):
    # initializes a dictionary
    d = {}

    

    # makes a dictionary that has a product_id as the key,
    # counts how many times that product has been order and
    # records the number of times it was a first order_id
    for ord, prod, add_o, re_or in info:
        # sets up some initial count values
        prod_count = 0
        reorder_count = 0
        
        if int(re_or) == 0:
            add_count = 1
        else:
            add_count = 0

        if prod in d.keys():
            prod_count = d[prod]['count']
            reorder_count = d[prod]['first_ordered_count']
            d[prod] = {"count": prod_count+1,
                       "first_ordered_count": reorder_count+add_count}
        else:
            d[prod] = {"count": prod_count+1,
                       "first_ordered_count": reorder_count+add_count}

    return(d)


# product_id,product_name,aisle_id,department_id
def department(reader):
    # creates a dictionary
    d = {}

    # cycles through the reader and makes a dictionary where
    # the product_id is the keys and stores the department id
    for id, prod, a_id, dept_id in reader:
        d.setdefault(dept_id, []).append(id)

    # returns product_ids and connected department
    return (d)


def orders_from_department(department_dict, product_dict):
    new_dict_totals = {}
    # from the dictionaries made above, counts product orders and firsts orders
    # also computes the percentage and formats it
    for k, val in department_dict.items():
        try:
            totals_prod = sum([product_dict[v]['count']
                               if v in product_dict.keys()
                               else 0 for v in department_dict[k]])
            totals_first = sum([product_dict[v]['first_ordered_count']
                                if v in product_dict.keys()
                                else 0 for v in department_dict[k]])

            if totals_prod == 0:
                new_dict_totals.setdefault(k, []).append({
                                            'number_of_orders': 0,
                                            'number_of_first_orders': 0,
                                            'percentage': 0})
            else:
                percentage = (float(totals_first)/float(totals_prod))
                new_dict_totals.setdefault(k, []).append(
                                   {'number_of_orders': totals_prod,
                                    'number_of_first_orders': totals_first,
                                    'percentage': format(percentage, '.2f')})
        except Exception:
            print("error at", k)

    return(new_dict_totals)


# takes the dictionary of orders and the file output name and writes
# a csv files if there is more than one order in the department
def write_csv(dict_of_dept_orders, output_name):

    final_dict = {}
    for key in dict_of_dept_orders.keys():
        if dict_of_dept_orders[key][0]['number_of_orders'] > 0:
            final_dict[key] = {'department_id': key,
                               'number_of_orders':
                              dict_of_dept_orders[key][0]['number_of_orders'],
                               'number_of_first_orders':
                         dict_of_dept_orders[key][0]['number_of_first_orders'],
                               'percentage':
                                dict_of_dept_orders[key][0]['percentage']}

    with open(output_name, 'w+') as report_file:
        fieldnames = ['department_id', 'number_of_orders',
                      'number_of_first_orders', 'percentage']
        writer = csv.DictWriter(report_file, fieldnames=fieldnames)
        writer.writerow({'department_id': 'department_id',
                         'number_of_orders': 'number_of_orders',
                         'number_of_first_orders': 'number_of_first_orders',
                         'percentage': 'percentage'})
        sorted_keys = sorted(final_dict.keys(), key=lambda x: int(x))

        for x in sorted_keys:
            writer.writerow(final_dict[x])
        report_file.close()

    return()
