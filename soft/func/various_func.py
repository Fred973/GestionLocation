import decimal
import os
from flask import render_template
from soft.constant import avio_json, amount_held_on_account, tmp_path, tasks_files_path
from soft.func.date_func import today_date, convert_date_to_string_for_nbr, number_of_day, \
    convert_date_string_to_isoformat, today_datetime_sec, convert_date_format_to_date_string
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.invoices.model import InvoicesOut, InvoicesIn


def total_year_forecast(y: int):
    try:
        total_list = [[]]
        total_invoices_out = 0
        total_invoices_in = 0

        # Calculate total gross invoice out
        invoice_out_req = Apartments.query.all()
        for data in invoice_out_req:
            if data.month:
                total_invoices_out += data.rent_price * 12
            else:
                total_invoices_out += (data.rent_price * 31 * 7)
                total_invoices_out += (data.rent_price * 30 * 4)
                total_invoices_out += (data.rent_price * 28)

        # Calculate total invoice in
        invoices_in_req = InvoicesIn.query.filter_by(year=y)
        for data in invoices_in_req:
            total_invoices_in += data.price

        total_net = total_invoices_out - total_invoices_in
        total_list[0].append('{} €'.format(str(total_invoices_out)))
        total_list[0].append('{} €'.format(str(total_invoices_in)))
        total_list[0].append('{} €'.format(str(total_net)))
        total_list[0].append('{} €'.format(str(total_net - ((total_invoices_out * amount_held_on_account)/100))))
        total_list[0].append('{} €'.format(str((total_invoices_out * amount_held_on_account)/100)))

        return total_list
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )

def total_year_forecast_by_benefits(y: int):
    aparts_list = [[]]

    # Calculate total gross for 7A for year = y
    total_invoices_out_7A = 0
    invoices_out_7A_req = Apartments.query.filter_by(apartment_name='7A')
    for data_out_7A in invoices_out_7A_req:
        if data_out_7A.month:
            total_invoices_out_7A += data_out_7A * 12
        else:
            total_invoices_out_7A += (data_out_7A.rent_price * 31 * 7)
            total_invoices_out_7A += (data_out_7A.rent_price * 30 * 4)
            total_invoices_out_7A += (data_out_7A.rent_price * 28)

    # Calculate total gross for other for year = y
    total_invoices_out_other = 0
    invoices_out_other_req = Apartments.query.filter(Apartments.apartment_name != '7A')
    for data_out_other in invoices_out_other_req:
        if data_out_other.month:
            total_invoices_out_other += (data_out_other.rent_price * 12)
        else:
            total_invoices_out_other += (data_out_other.rent_price * 31 * 7)
            total_invoices_out_other += (data_out_other.rent_price * 30 * 4)
            total_invoices_out_other += (data_out_other.rent_price * 28)

    # Calculate total invoices in for 7A for year = y
    total_invoices_in_7A = 0
    invoices_in_7A_req = InvoicesIn.query.filter_by(apartment_name='7A').filter_by(year=y)
    for data_in_7A in invoices_in_7A_req:
        total_invoices_in_7A += data_in_7A.price

    # Calculate total invoices in for other for year = y
    total_invoices_in_other = 0
    invoices_in_other_req = InvoicesIn.query.filter(InvoicesIn.apartment_name != '7A').filter_by(year=y)
    for data_in_other in invoices_in_other_req:
        total_invoices_in_other += data_in_other.price

    total_invoices_out_7A = decimal.Decimal(total_invoices_out_7A)
    total_net_7A = total_invoices_out_7A - total_invoices_in_7A
    aparts_list[0].append('7A (Katianne)')
    aparts_list[0].append('{} €'.format(str(total_invoices_out_7A)))
    aparts_list[0].append('{} €'.format(str(total_invoices_in_7A)))
    aparts_list[0].append('{} €'.format(str(total_net_7A)))
    aparts_list[0].append('{} €'.format(str(total_net_7A - ((total_invoices_out_7A * amount_held_on_account)/100))))
    aparts_list[0].append('{} €'.format(str((total_invoices_out_7A * amount_held_on_account)/100)))

    # append data in aparts_list for other
    total_net_other = decimal.Decimal(total_invoices_out_other) - decimal.Decimal(total_invoices_in_other)
    aparts_list.append(['Autres (Georges)'])
    aparts_list[1].append('{} €'.format(str(total_invoices_out_other)))
    aparts_list[1].append('{} €'.format(str(total_invoices_in_other)))
    aparts_list[1].append('{} €'.format(str(total_net_other)))
    aparts_list[1].append('{} €'.format(str(total_net_other - decimal.Decimal((total_invoices_out_other * amount_held_on_account)/100))))
    aparts_list[1].append('{} €'.format(str((total_invoices_out_other * amount_held_on_account)/100)))

    return aparts_list


def total_year_forecast_by_aparts(y: int):
    aparts_list = []

    n = 0
    invoice_our_req = Apartments.query.all()
    for data_invoice_out in invoice_our_req:
        total_invoices_in = 0
        total_invoices_out = 0
        aparts_list.append([data_invoice_out.apartment_name])
        if data_invoice_out.month:
            total_invoices_out += data_invoice_out.rent_price * 12
        else:
            total_invoices_out += data_invoice_out.rent_price * 31 * 7
            total_invoices_out += data_invoice_out.rent_price * 30 * 4
            total_invoices_out += data_invoice_out.rent_price * 28

        invoices_in_req = InvoicesIn.query.filter_by(apartment_name=data_invoice_out.apartment_name).filter_by(year=y)
        for i in invoices_in_req:
            total_invoices_in += i.price

        total_invoices_out = decimal.Decimal(total_invoices_out)
        total_net = total_invoices_out - total_invoices_in
        aparts_list[n].append('{} €'.format(str(total_invoices_out)))
        aparts_list[n].append('{} €'.format(str(total_invoices_in)))
        aparts_list[n].append('{} €'.format(str(total_net)))
        aparts_list[n].append('{} €'.format(str(total_net - ((total_invoices_out * amount_held_on_account)/100))))
        aparts_list[n].append('{} €'.format(str((total_invoices_out * amount_held_on_account)/100)))

        n += 1

    return aparts_list

def total_by_benefits(y: int):
    aparts_list = [[]]

    """ Calculate total 7A """
    total_gross_out_7A = 0
    total_invoice_in_7A = 0

    # Get and Calculate common invoice apartment 7
    invoice_in_common_req = InvoicesIn.query.filter_by(common_invoice=True).filter_by(year=y)
    for i in invoice_in_common_req:
        pass

    # Calculate total gross 7A
    invoice_out_7A_req = InvoicesOut.query.filter_by(apartment_name='7A').filter_by(year=y)
    for i in invoice_out_7A_req:
        d_nbr = 0
        d_nbr += calculate_day_nbr(str(i.date_in), str(i.date_out))
        total_gross_out_7A += i.price * d_nbr

    # Calculate invoice in total 7A
    invoice_in_7A_req = InvoicesIn.query.filter_by(apartment_name='7A').filter_by(year=y)
    for i in invoice_in_7A_req:
        total_invoice_in_7A += i.price

    # Calculate total net 7A
    (total_net_7A) = decimal.Decimal(total_gross_out_7A - total_invoice_in_7A)

    """ Calculate total 7B """
    total_gross_out_7B = 0
    total_in_7B = 0
    # Calculate total gross 7B
    invoices_out_7B_req = InvoicesOut.query.filter_by(apartment_name='7B').filter_by(year=y)
    for i in invoices_out_7B_req:
        d_nbr = 0
        d_nbr += calculate_day_nbr(str(i.date_in), str(i.date_out))
        total_gross_out_7B += i.price * d_nbr

    # Calculate total invoices in 7B
    invoices_in_7B_req = InvoicesIn.query.filter_by(apartment_name='7B').filter_by(year=y)
    for i in invoices_in_7B_req:
        total_in_7B += i.price

    # Calculate total net 7B
    total_net_7B = decimal.Decimal(total_gross_out_7B - total_in_7B)

    # Convert to decimal
    total_gross_out_7A = decimal.Decimal(total_gross_out_7A)
    total_gross_out_7B = decimal.Decimal(total_gross_out_7B)

    # Made aparts_list
    aparts_list[0].append('7A (Katianne)')
    aparts_list[0].append(str(total_net_7A - ((total_gross_out_7A * amount_held_on_account)/100)) + ' €')
    aparts_list[0].append(str((total_gross_out_7A * amount_held_on_account)/100) + ' €')
    aparts_list.append(["7B (Georges)"])
    aparts_list[1].append(str(total_net_7B - ((total_gross_out_7B * amount_held_on_account)/100)) + ' €')
    aparts_list[1].append(str((total_gross_out_7B * amount_held_on_account)/100) + ' €')

    return aparts_list

def total_apart(y: int):
    total_net_list = []
    aparts_req = Apartments.query.all()

    # Get aparts name list
    n = 0
    for i in aparts_req:
        total_net_list.append([i.apartment_name])
        n_invoice_out = 0
        total_out = 0
        total_gross = 0
        invoice_req = InvoicesOut.query.filter_by(apartment_name=i.apartment_name).filter_by(year=y)
        for item in invoice_req:
            n_invoice_out += 1
            if i.month:
                total_out += item.price
            else:
                day_nbr = calculate_day_nbr(str(item.date_in), str(item.date_out))
                total_out += item.price * day_nbr

        n_invoice_in = 0
        total_in = 0
        invoice_req = InvoicesIn.query.filter_by(apartment_name=i.apartment_name).filter_by(year=y)
        for item in invoice_req:
            n_invoice_in += 1
            total_in += item.price

        total_gross += total_out

        total_net_list[n].append("{} €".format(str(total_gross - total_in)))
        n += 1

    return total_net_list

def invoice_in_table_list(y: int):
    total_invoices_in_list = []

    # Calculate total common invoices
    total_invoice_common_in = 0
    nbr_invoice_common_in = 0
    invoices_in_req = InvoicesIn.query.filter_by(year=y)
    for i in invoices_in_req:
        if i.common_invoice:
            total_invoice_common_in += i.price
            nbr_invoice_common_in += 1

    # Made the [aparts_list]
    n = 0
    aparts_list_req = Apartments.query.all()
    for apart in aparts_list_req:
        total_invoices_in_list.append([apart.apartment_name])
        invoice_in_req = InvoicesIn.query.filter_by(apartment_name=apart.apartment_name).filter_by(year=y)
        nbr_invoice_in = 0
        total_invoices_in = 0
        for i in invoice_in_req:
            if i.common_invoice is not True:  # Not a common invoice
                nbr_invoice_in += 1
                total_invoices_in += i.price

        if apart.apartment_name == '7A':  # Common invoice
            total_invoices_in += total_invoice_common_in / 2
            nbr_invoice_in += nbr_invoice_common_in
        elif apart.apartment_name == '7B':
            total_invoices_in += total_invoice_common_in / 2
            nbr_invoice_in += nbr_invoice_common_in

        total_invoices_in_list[n].append(str(nbr_invoice_in))
        # if total_invoices_in < 0:
        #     total_invoices_in_list[n].append(str(0) + ' €')
        # else:
        total_invoices_in_list[n].append(str(total_invoices_in) + ' €')
        n += 1

    return total_invoices_in_list

def invoice_out_table_list(y: int):
    aparts_list = []
    aparts_req = Apartments.query.all()

    # Get aparts name list
    n = 0
    total_gross_ = 0
    for i in aparts_req:
        aparts_list.append([i.apartment_name])
        n_invoice = 0
        total = 0
        invoice_req = InvoicesOut.query.filter_by(apartment_name=i.apartment_name).filter_by(year=y)
        for item in invoice_req:
            n_invoice += 1
            if i.month:
                total += item.price
            else:
                day_nbr = calculate_day_nbr(str(item.date_in), str(item.date_out))
                total += item.price * day_nbr

        total_gross_ += total
        aparts_list[n].append(str(n_invoice))
        aparts_list[n].append("{} €".format(str(total)))
        n += 1

    return aparts_list

def create_invoice_out_nbr(n, apart_name, date_, id_customer=''):
    """
    n = 0 -> Avio customer
    n > 0 -> other (tenants)
    :param date_:
    :param apart_name:
    :param id_customer:
    :param n:
    :return:
    """
    if n == 0:
        nbr = avio_json['id_customer']
        return 'FS-{}-{}-{}'.format(apart_name, convert_date_to_string_for_nbr(date_), nbr)
    else:
        nbr = id_customer
        return 'FS-{}-{}-{}'.format(apart_name, convert_date_to_string_for_nbr(date_), nbr)

def create_invoice_in_nbr(apart_name, id_user, id_invoice_in):
    """
    :param id_invoice_in:
    :param id_user:
    :param apart_name:
    :return:
    """
    return 'FE-{}-{}-{}-{}'.format(apart_name, today_datetime_sec(), id_user, id_invoice_in)

def create_contract_nbr(apart_name):
    """
    :param apart_name:
    :return:
    """

    return 'C-{}-{}'.format(apart_name, today_datetime_sec())

def create_receipt_nbr(apart_name, id_customer=''):
    """
    n = 0 -> Avio customer
    n > 0 -> other (tenants)
    :param apart_name:
    :param id_customer:
    :return:
    """
    nbr = id_customer
    return 'Q-{}-{}-{}'.format(apart_name, today_date(), nbr)

def get_apartment_data(id_):
    apart_req = Apartments.query.get_or_404(id_)
    print(apart_req.address)
    return [apart_req.address, str(apart_req.zipcode), apart_req.city]

def get_apartment_name(id_):
    apart_req = Apartments.query.get_or_404(id_)
    return str(apart_req.apartment_name)

def calculate_day_nbr(d_in, d_out):
    nbr = str(number_of_day(convert_date_string_to_isoformat(d_in), convert_date_string_to_isoformat(d_out)))
    return int(nbr)

def get_apartment_name_list():
    aparts_name_list = []
    aparts_name_req_list = Apartments.query.all()
    for i in aparts_name_req_list:
        aparts_name_list.append(i.apartment_name)
    return aparts_name_list

def mager_dicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

def purge_tmp_path():
    try:
        for file in os.listdir(tmp_path):
            os.remove(tmp_path + file)
    except Exception as e:
        print(e)

def create_invoices_zip_name():
    zip_name = 'Factures_{}.zip'.format(today_datetime_sec())
    return str(zip_name)


def compare_list(l1: list, l2: list):
    """
    compare list and return a list without same values
    :return:
    """
    i = 0
    while i < len(l1):
        if l1[i] in l2:
            del l1[i]
            continue
        i += 1

    return l1

def create_task_files_folder(id_task: int, added_date):
    # Create folder name string
    folder_name = f'{convert_date_format_to_date_string(added_date)}-ID{str(id_task)}'
    # Create folder
    try:
        os.mkdir(os.path.join(tasks_files_path, folder_name))
    except FileExistsError:
        pass
    return folder_name