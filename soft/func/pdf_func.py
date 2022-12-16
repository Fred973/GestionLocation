from fpdf import FPDF
from soft.constant import george_json, avio_json
from soft.constant import invoices_out_path
from soft.func.date_func import convert_date, today_date_str, number_of_day, convert_date_string_to_isoformat
from soft.func.various_func import create_invoice_nbr, get_apartment_data, get_apartment_name


def create_invoice_out_pdf(id_apart, date_in, date_out, due_date, price, ref_customer):

    pdf = FPDF(
        orientation='P',
        unit='mm',
        format='A4'
    )

    pdf.add_page()

    # Get data for pdf
    address_apart = get_apartment_data(id_apart)

    w=10
    pdf.set_font('arial', 'B', 16)
    pdf.cell(w=0, h=0, ln=1)
    pdf.cell(
        180,
        w,
        'LOCATION {} {} {}'.format(address_apart[0].upper(), address_apart[1].upper(), address_apart[2].upper()),
        align='C'
    )

    pdf.line(10, 27, 200, 27)

    x_cell_1 = 30
    x_cell_2 = 110
    pdf.set_font('arial', 'B', 12)
    pdf.cell(w=0, h=23, ln=1)
    pdf.cell(x_cell_1, 0, 'Propriétaire :', align='R')
    pdf.cell(x_cell_2, 0, 'Téléphone :', align='R')
    pdf.cell(w=0, h=7, ln=1)
    pdf.cell(x_cell_1, 0, 'Adresse :', align='R')
    pdf.cell(x_cell_2, 0, 'E-mail :', align='R')

    y = 34.3
    x_text_1 = 40
    x_text_2 = 150
    pdf.set_font('arial', '', 12)
    pdf.text(x_text_1, y, '{} {}'.format(george_json['name'], george_json['first_name']))
    pdf.text(x_text_1, y + 7, '{}'.format(george_json['address']))
    pdf.text(x_text_1, y + 14, '{} {}'.format(george_json['zipcode'], george_json['city']))
    pdf.text(x_text_2, y, '{}'.format(george_json['phone']))
    pdf.text(x_text_2, y + 7, '{}'.format(george_json['email']))

    y += 19
    pdf.line(10, y, 200, y)

    y += 13
    pdf.set_font('arial', '', 16)
    pdf.text(40, y, 'Période du {} au {}'.format(convert_date(date_in), convert_date(date_out)))

    y += 9
    pdf.line(10, y, 200, y)

    x = 40
    pdf.set_font('arial', 'B', 12)
    pdf.cell(w=0, h=43, ln=1)
    pdf.cell(x, 0, 'Ref. Client :', align='R')
    pdf.cell(x + 30, 0, 'Facturé à :', align='R')
    pdf.cell(w=0, h=7, ln=1)
    pdf.cell(x, 0, 'Date :', align='R')
    pdf.cell(w=0, h=7, ln=1)
    pdf.cell(x, 0, 'Réservation client :', align='R')

    x_text_3 = 50
    y += 9
    pdf.set_font('arial', '', 12)
    pdf.text(x_text_3, y, '{}'.format(ref_customer))
    pdf.text(x_text_3, y + 7, '{}'.format(today_date_str()))
    pdf.text(x_text_3, y + 14, 'du {}'.format(convert_date(date_in)))
    pdf.text(x_text_3, y + 21, 'au {}'.format(convert_date(date_out)))
    pdf.text(x_text_3 + 70, y, '{}'.format(avio_json['name']))
    pdf.text(x_text_3 + 70, y + 7, '{}'.format(avio_json['address']))
    pdf.text(x_text_3 + 70, y + 14, '{} {}'.format(avio_json['zipcode'], avio_json['city']))

    y += 26
    pdf.line(10, y, 200, y)

    pdf.set_fill_color(95, 95, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w=0, h=20, ln=1)
    pdf.cell(42.5, 5, 'Date de début', align='C', fill=True)
    pdf.cell(42.5, 5, 'Date de fin', align='C', fill=True)
    pdf.cell(35, 5, 'Prix', align='C', fill=True)
    pdf.cell(35, 5, 'Nbr de jour', align='C', fill=True)
    pdf.cell(35, 5, 'Sous Total', align='C', fill=True)

    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(42.5, 5, '{}'.format(convert_date(date_in)), align='C')
    pdf.cell(42.5, 5, '{}'.format(convert_date(date_out)), align='C')
    pdf.cell(35, 5, '{} {}'.format(price, chr(128)), align='C')
    day_nbr = str(number_of_day(convert_date_string_to_isoformat(date_in), convert_date_string_to_isoformat(date_out)))
    sub_total = str(int(day_nbr) * int(price))
    pdf.cell(35, 5, '{}'.format(day_nbr), align='C')
    pdf.cell(35, 5, '{} {}'.format(sub_total, chr(128)), align='C')

    pdf.set_font('arial', 'B', 12)
    pdf.cell(w=0, h=45, ln=1)
    pdf.cell(167, 0, 'Total :', align='R')
    pdf.set_font('arial', '', 12)
    pdf.cell(25, 0, '{} {}'.format(sub_total, chr(128)), align='L')

    pdf.cell(w=0, h=15, ln=1)
    pdf.set_font('arial', 'B', 12)
    pdf.cell(52, 0, 'Somme à payer avant le :', align='R')
    pdf.set_font('arial', '', 12)
    pdf.cell(50, 0, '{}'.format(convert_date(due_date)), align='L')

    y += 82
    pdf.line(10, y, 200, y)

    pdf.set_fill_color(95, 95, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(190, 10, 'VERSEMENT', align='C', border=1, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Nom du client', align='C', border=1)
    pdf.cell(140, 10, 'Société AVIO S.P.A.', align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Réservation client', align='C', border=1)
    pdf.cell(140, 10, 'du {} au {}'.format(convert_date(date_in), convert_date(date_out)), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Référence client', align='C', border=1)
    pdf.cell(140, 10, '{}'.format(ref_customer), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Date', align='C', border=1)
    pdf.cell(140, 10, '{}'.format(today_date_str()), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Montant dû', align='C', border=1)
    pdf.cell(140, 10, '{} {}'.format(sub_total, chr(128)), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'RIB', align='C', border=1)
    pdf.cell(140, 10, '{}   BIC : {}'.format(george_json['RIB']['account_nbr'], george_json['RIB']['BIC']), align='L', border=1)

    pdf.output(invoices_out_path + '/{}'.format('{}.pdf'.format(create_invoice_nbr(n=0, apart_name=get_apartment_name(id_apart)))))

    return '{}.pdf'.format(create_invoice_nbr(n=0, apart_name=get_apartment_name(id_apart)))