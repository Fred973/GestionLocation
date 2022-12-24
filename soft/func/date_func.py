from datetime import datetime
import locale


def convert_date_string_to_isoformat(date_: str):
    return datetime.strptime(date_, '%Y-%m-%d')


def convert_date_string_to_isoformat_for_db(date_: str):
    return datetime.strptime(date_, '%d%m%Y')

def convert_date_str_to_date_to_string(date_: str):
    d = convert_date_string_to_isoformat_for_db(date_)
    return str(datetime.strftime(d, '%d %B %Y'))


def convert_date_to_string_for_nbr(date_):
    d= datetime.strptime(date_, '%Y-%m-%d')
    return str(datetime.strftime(d, '%Y%m%d'))


def convert_date_to_string(date_):
    locale.setlocale(locale.LC_TIME,'')
    d_in = datetime.strptime(date_, '%Y-%m-%d')
    return str(datetime.strftime(d_in, '%d %B %Y'))


def today_date():
    date_ = datetime.now()
    return str(datetime.strftime(date_, '%d%m%Y'))


def today_datetime():
    date_ = datetime.now()
    return str(datetime.strftime(date_, '%d%m%Y-%H%M'))


def today_date_str():
    date_ = datetime.now()
    return str(datetime.strftime(date_, '%d %B %Y'))


def number_of_day(d1, d2):
    delta = d2 - d1
    return delta.days + 1

def convert_to_month(date_):
    locale.setlocale(locale.LC_TIME,'')
    d_in = datetime.strptime(date_, '%Y-%m-%d')
    return str(datetime.strftime(d_in, '%B/'))

def convert_to_year(date_):
    locale.setlocale(locale.LC_TIME,'')
    d_in = datetime.strptime(date_, '%Y-%m-%d')
    return str(datetime.strftime(d_in, '%Y'))