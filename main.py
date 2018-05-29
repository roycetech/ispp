import re
import sys
from os.path import basename


SQL_INSERT = "INSERT INTO `retail_inventory` (`card_record_id`," \
 "`transaction_id`, `fkitemid`, `fkstoreid`, `orderDate`, `shippedDate`, " \
 "`invoice_number`, `serial_number`, `item_number`, `item_name`, " \
 "`myob_item_id`) \nVALUES "


CONSTANTS = {
    'transaction_id': 168960,
    'myob_item_id': 970,
    'invoice_number': 21369,
    'fkitemid': 'null'
}

INDEX = {
    'Product Code': 0,
    'ICCID': 1,
    'Control Number': 2
}


def main():
    '''
    main routine.  We expect to read 10k records from the passed file.
    '''
    if len(sys.argv) < 4:
        print('Usage: main.py <filename.csv> <store_id> <card_record_id>')
        sys.exit(1)

    store_id = sys.argv[2]
    card_record_id = sys.argv[3]
    filename = sys.argv[1]

    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]

    lines.pop(0)
    assert len(lines) == 10000

    base_filename = basename(filename)
    filename_date = get_date(base_filename)
    item_name = get_item_name(base_filename)

    print(SQL_INSERT)
    for line in lines:
        data = line.split(',')
        print("({}, {}, {}, {}, '{}', '{}', {}, {}, '{}', '{}', {})".format(
            card_record_id,
            CONSTANTS['transaction_id'],
            CONSTANTS['fkitemid'],
            store_id,
            filename_date,
            filename_date,
            CONSTANTS['invoice_number'],
            data[INDEX['ICCID']],
            data[INDEX['Product Code']],
            item_name,
            CONSTANTS['myob_item_id']), end='')

        if lines[-1] != line:
            print(',')
        else:
            print(';')


def get_item_name(file_basename):
    '''
    '''
    m = re.search(r'(?<=amaysim\sPOSA\s)(\$\d+)', file_basename)
    return '{} Starter Kit'.format(m.group(0))


def get_date(file_basename):
    '''
    Extracts the order/ship date from base filename.
    '''
    m = re.search(r'(\d{4})(\d{2})(\d{2})(?=\sx\s)', file_basename)
    date_year = m.group(1)
    date_month = m.group(2)
    date_day = m.group(3)
    return '{}-{}-{} 00:00:00'.format(date_year, date_month, date_day)


main()
