from flask import render_template
from soft.constant import avio_json
from soft.func.date_func import today_date, convert_date_to_string_for_nbr, number_of_day, \
    convert_date_string_to_isoformat
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
        total_list[0].append('{} €'.format(str(total_net - ((total_net * 20)/100))))
        total_list[0].append('{} €'.format(str((total_net * 20)/100)))

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

    total_net_7A = total_invoices_out_7A - total_invoices_in_7A
    aparts_list[0].append('7A (Katianne)')
    aparts_list[0].append('{} €'.format(str(total_invoices_out_7A)))
    aparts_list[0].append('{} €'.format(str(total_invoices_in_7A)))
    aparts_list[0].append('{} €'.format(str(total_net_7A)))
    aparts_list[0].append('{} €'.format(str(total_net_7A - ((total_net_7A * 20)/100))))
    aparts_list[0].append('{} €'.format(str((total_net_7A * 20)/100)))

    # append data in aparts_list for other
    total_net_other = total_invoices_out_other - total_invoices_in_other
    aparts_list.append(['Autres (Georges)'])
    aparts_list[1].append('{} €'.format(str(total_invoices_out_other)))
    aparts_list[1].append('{} €'.format(str(total_invoices_in_other)))
    aparts_list[1].append('{} €'.format(str(total_net_other)))
    aparts_list[1].append('{} €'.format(str(total_net_other - ((total_net_other * 20)/100))))
    aparts_list[1].append('{} €'.format(str((total_net_other * 20)/100)))

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

        total_net = total_invoices_out - total_invoices_in
        aparts_list[n].append('{} €'.format(str(total_invoices_out)))
        aparts_list[n].append('{} €'.format(str(total_invoices_in)))
        aparts_list[n].append('{} €'.format(str(total_net)))
        aparts_list[n].append('{} €'.format(str(total_net - ((total_net * 20)/100))))
        aparts_list[n].append('{} €'.format(str((total_net * 20)/100)))

        n += 1

    return aparts_list

def total_by_benefits(y: int):
    total_price_out = 0

    # Calculate total gross of apartment 7A
    total_gross_7A = 0
    day_nbr = 0
    n_invoice_out = 0
    invoice_req = InvoicesOut.query.filter_by(apartment_name='7A').filter_by(year=y)
    for i in invoice_req:
        total_price_out = 0
        day_nbr += calculate_day_nbr(str(i.date_in), str(i.date_out))
        total_price_out += i.price
        n_invoice_out +=1
    total_gross_7A += (day_nbr * total_price_out) * n_invoice_out

    # Calculate total net of apartment 7A
    total_net_7A = 0
    n_invoice_in = 0
    total_price_in = 0
    invoice_req = InvoicesIn.query.filter_by(apartment_name='7A').filter_by(year=y)
    for i in invoice_req:
        total_price_in += i.price
        n_invoice_in +=1

    total_net_7A += (total_gross_7A - total_price_in)
    total_net_7A = total_net_7A - ((total_net_7A * 20)/100)
    total_held_on_account_7A = (total_net_7A * 20)/100
    # TODO 20% create a setting variable to change value

    aparts_list = []
    aparts_req = Apartments.query.all()
    n = 0
    total_out_gross_other = 0
    total_invoice_in= 0
    for i in aparts_req:
        if i.apartment_name == '7A':
            aparts_list.append(['7A (Katianne)'])
            aparts_list[n].append('{} €'.format(str(total_net_7A)))
            aparts_list[n].append('{} €'.format(str(total_held_on_account_7A)))
            n += 1
        else:
            invoice_out_req = InvoicesOut.query.filter_by(apartment_name=i.apartment_name).filter_by(year=y)
            for item_out in invoice_out_req:
                price = item_out.price
                d_nbr = (calculate_day_nbr(str(item_out.date_in), str(item_out.date_out)))
                total_out_gross_other += price * d_nbr

            invoice_in_req = InvoicesIn.query.filter_by(apartment_name=i.apartment_name).filter_by(year=y)
            n_invoice = 0
            total_in_other = 0
            for item_in in invoice_in_req:
                price = item_in.price
                n_invoice += 1
                total_in_other += price

            total_invoice_in += (total_in_other * n_invoice)

    total_net_other = (total_out_gross_other - total_invoice_in)
    total_net_other = total_net_other - ((total_net_other * 20)/100)
    total_held_on_account_other = (total_net_other * 20)/100
    aparts_list.append(['Autres (Georges)'])
    aparts_list[1].append('{} €'.format(str(total_net_other)))
    aparts_list[1].append('{} €'.format(str(total_held_on_account_other)))

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

        total_gross += (total_out * n_invoice_out)

        total_net_list[n].append("{} €".format(str(total_gross - total_in)))
        n += 1

    return total_net_list

def invoice_in_table_list(y: int):
    aparts_list = []
    aparts_req = Apartments.query.all()

    # Get aparts name list
    n = 0
    for i in aparts_req:
        aparts_list.append([i.apartment_name])
        n_invoice = 0
        total = 0
        invoice_req = InvoicesIn.query.filter_by(apartment_name=i.apartment_name).filter_by(year=y)
        for item in invoice_req:
            n_invoice += 1
            total += item.price
        aparts_list[n].append(str(n_invoice))
        aparts_list[n].append("{} €".format(str(total)))
        n += 1

    return aparts_list

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
        total_gross_ += (total * n_invoice)
        aparts_list[n].append(str(n_invoice))
        aparts_list[n].append("{} €".format(str(total * n_invoice)))
        n += 1

    return aparts_list

def create_invoice_nbr(n, apart_name, date_, id_customer=''):
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
        return 'F-{}-{}-{}'.format(apart_name, convert_date_to_string_for_nbr(date_), nbr)
    else:
        nbr = id_customer
        return 'F-{}-{}-{}'.format(apart_name, convert_date_to_string_for_nbr(date_), nbr)

def create_contract_nbr(apart_name, id_customer=''):
    """
    :param apart_name:
    :param id_customer:
    :return:
    """
    nbr = id_customer
    return 'C-{}-{}-{}'.format(apart_name, today_date(), nbr)

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
    return [apart_req.address, str(apart_req.zipcode), apart_req.city]

def get_apartment_name(id_):
    apart_req = Apartments.query.get_or_404(id_)
    return str(apart_req.apartment_name)

def calculate_day_nbr(d_in, d_out):
    nbr = str(number_of_day(convert_date_string_to_isoformat(d_in), convert_date_string_to_isoformat(d_out)))
    return int(nbr)