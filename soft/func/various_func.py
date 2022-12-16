from soft.constant import avio_json
from soft.func.date_func import today_date
from soft.gestion_loc.apartments.model import Apartments


def create_invoice_nbr(n, apart_name, id_customer=''):
    """
    n = 0 -> Avio customer
    n > 0 -> other (tenants)
    :param apart_name:
    :param id_customer:
    :param n:
    :return:
    """
    if n == 0:
        nbr = avio_json['id_customer']
        return '{}-{}-{}'.format(apart_name, today_date(), nbr)
    else:
        nbr = id_customer
        return '{}-{}-{}'.format(apart_name, today_date(), nbr)

def get_apartment_data(id_):
    apart_req = Apartments.query.get_or_404(id_)
    return [apart_req.address, str(apart_req.zipcode), apart_req.city]

def get_apartment_name(id_):
    apart_req = Apartments.query.get_or_404(id_)
    return str(apart_req.apartment_name)