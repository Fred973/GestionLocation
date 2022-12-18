from soft.constant import avio_json
from soft.func.date_func import today_date, convert_date_str_to_date_to_string, convert_date_to_string_for_nbr
from soft.gestion_loc.apartments.model import Apartments


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
    n = 0 -> Avio customer
    n > 0 -> other (tenants)
    :param apart_name:
    :param id_customer:
    :param n:
    :return:
    """
    nbr = id_customer
    return 'C-{}-{}-{}'.format(apart_name, today_date(), nbr)

def get_apartment_data(id_):
    apart_req = Apartments.query.get_or_404(id_)
    return [apart_req.address, str(apart_req.zipcode), apart_req.city]

def get_apartment_name(id_):
    apart_req = Apartments.query.get_or_404(id_)
    return str(apart_req.apartment_name)

def get_date_from_db_save_name(d):
    date_ = d.replace('gestion_loc_', '')
    result = date_[:8]
    return convert_date_str_to_date_to_string(result)