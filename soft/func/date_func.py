from datetime import datetime
import locale


def convert_date_string_to_isoformat(date_: str):
    return datetime.strptime(date_, '%Y-%m-%d')


def convert_date_string_to_isoformat_for_db(date_: str):
    return datetime.strptime(date_, '%d%m%Y')


def convert_date(date_):
    locale.setlocale(locale.LC_TIME,'')
    d_in = datetime.strptime(date_, '%Y-%m-%d')
    return str(datetime.strftime(d_in, '%d %B %Y'))


def today_date():
    date_ = datetime.now()
    return str(datetime.strftime(date_, '%d%m%Y'))


def today_date_str():
    date_ = datetime.now()
    return str(datetime.strftime(date_, '%d %B %Y'))


def number_of_day(d1, d2):
    delta = d2 - d1
    return delta.days + 1