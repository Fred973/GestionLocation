from fpdf import FPDF
from soft.constant import george_json, avio_json, receipts_path, receipt_text
from soft.constant import invoices_out_path
from soft.func.date_func import convert_date_to_string, today_date_str, number_of_day, convert_date_string_to_isoformat
from soft.func.various_func import create_invoice_out_nbr, get_apartment_data, get_apartment_name, calculate_day_nbr, \
    create_receipt_nbr
from soft.gestion_loc.apartments.model import Apartments
from soft.gestion_loc.tenants.model import Tenants


def create_invoice_out_pdf(id_apart, date_in, date_out, due_date, price, ref_customer):
    """
    Create pdf for invoice_out

    :param id_apart:
    :param date_in:
    :param date_out:
    :param due_date:
    :param price:
    :param ref_customer:
    :return pdf file:
    """

    # Get invoice nbr
    invoice_nbr = create_invoice_out_nbr(
        n=0,
        apart_name=get_apartment_name(id_apart),
        date_=date_in
    )

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
    pdf.text(x_text_1, y, '{} {}'.format(george_json[0]['name'], george_json[0]['first_name']))
    pdf.text(x_text_1, y + 7, '{}'.format(george_json[0]['address']))
    pdf.text(x_text_1, y + 14, '{} {}'.format(george_json[0]['zipcode'], george_json[0]['city']))
    pdf.text(x_text_2, y, '{}'.format(george_json[0]['phone']))
    pdf.text(x_text_2, y + 7, '{}'.format(george_json[0]['email']))

    y += 19
    pdf.line(10, y, 200, y)

    y += 13
    pdf.set_font('arial', '', 16)
    pdf.text(40, y, 'Période du {} au {}'.format(convert_date_to_string(date_in), convert_date_to_string(date_out)))

    y += 9
    pdf.line(10, y, 200, y)

    x = 40
    pdf.set_font('arial', 'B', 12)
    pdf.cell(w=0, h=43, ln=1)
    pdf.cell(x, 0, 'N° Facture :', align='R')
    pdf.cell(x + 30, 0, 'Facturé à :', align='R')
    pdf.cell(w=0, h=7, ln=1)
    pdf.cell(x, 0, 'Date :', align='R')
    pdf.cell(w=0, h=7, ln=1)
    pdf.cell(x, 0, 'Réservation client :', align='R')

    x_text_3 = 50
    y += 9
    pdf.set_font('arial', '', 12)
    pdf.text(x_text_3, y, '{}'.format(invoice_nbr))
    pdf.text(x_text_3, y + 7, '{}'.format(today_date_str()))
    pdf.text(x_text_3, y + 14, 'du {}'.format(convert_date_to_string(date_in)))
    pdf.text(x_text_3, y + 21, 'au {}'.format(convert_date_to_string(date_out)))
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
    pdf.cell(42.5, 5, '{}'.format(convert_date_to_string(date_in)), align='C')
    pdf.cell(42.5, 5, '{}'.format(convert_date_to_string(date_out)), align='C')
    pdf.cell(35, 5, '{} {}'.format(price, chr(128)), align='C')

    sub_total = str(int(calculate_day_nbr(date_in, date_out)) * int(price))
    pdf.cell(35, 5, '{}'.format(str(calculate_day_nbr(date_in, date_out))), align='C')
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
    pdf.cell(50, 0, '{}'.format(convert_date_to_string(due_date)), align='L')

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
    pdf.cell(140, 10, 'du {} au {}'.format(convert_date_to_string(date_in), convert_date_to_string(date_out)), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'N° Facture', align='C', border=1)
    pdf.cell(140, 10, '{}'.format(invoice_nbr), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Date', align='C', border=1)
    pdf.cell(140, 10, '{}'.format(today_date_str()), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'Montant dû', align='C', border=1)
    pdf.cell(140, 10, '{} {}'.format(sub_total, chr(128)), align='L', border=1)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(50, 10, 'RIB', align='C', border=1)
    pdf.cell(140, 10, '{}   BIC : {}'.format(george_json[0]['RIB']['account_nbr'], george_json[0]['RIB']['BIC']), align='L', border=1)

    pdf.output(invoices_out_path + '/{}'.format('{}.pdf'.format(invoice_nbr)))

    return '{}.pdf'.format(invoice_nbr)


def create_receipt_pdf(date_in, date_out, apartment, id_tenant):
    pdf = FPDF(
        orientation='P',
        unit='mm',
        format='A4'
    )

    pdf.add_page()

    # Header
    pdf.set_font('arial', 'B', 16)
    pdf.cell(w=0, h=0, ln=1)
    pdf.set_fill_color(95, 95, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 10, 'QUITTANCE DE LOYER', align='C', fill=True)
    pdf.set_text_color(0, 0, 0)
    # pdf.set_font('arial', 'B', 12)
    pdf.cell(w=0, h=20, ln=1)

    x_cell_1= 95
    x_cell_2 = 95
    pdf.set_font('arial', 'B', 12)
    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(x_cell_1, 0, 'Bailleur :', align='L')
    pdf.cell(x_cell_2, 0, 'Locataire :', align='L')
    pdf.set_font('arial', '', 12)

    # Lessor
    y_lessor = 41.4
    x_lessor = 30
    pdf.text(x_lessor, y_lessor, '{} {}'.format(george_json[0]['name'], george_json[0]['first_name']))
    pdf.text(x_lessor, y_lessor + 7, '{}'.format(george_json[0]['address']))
    pdf.text(x_lessor, y_lessor + 14, '{} {}'.format(george_json[0]['zipcode'], george_json[0]['city']))
    pdf.text(x_lessor, y_lessor + 21, '{}'.format(george_json[0]['phone']))
    pdf.text(x_lessor, y_lessor + 28, '{}'.format(george_json[0]['email']))

    # Tenant
    # Get tenant data from DB
    tenant_req = Tenants.query.get_or_404(id_tenant)
    # Get tenant's apartment address
    apart_req = Apartments.query.get_or_404(tenant_req.fk_apartment)
    y_tenant = 41.4
    x_tenant = 128
    pdf.text(x_tenant, y_tenant, '{} {}'.format(tenant_req.name, tenant_req.first_name))
    pdf.text(x_tenant, y_tenant + 7, '{}'.format(apart_req.address))
    pdf.text(x_tenant, y_tenant + 14, '{} {}'.format(apart_req.zipcode, apart_req.city))
    pdf.text(x_tenant, y_tenant + 21, '{}'.format(tenant_req.phone))
    pdf.text(x_tenant, y_tenant + 28, '{}'.format(tenant_req.email))

    pdf.cell(w=0, h=40, ln=1)
    pdf.cell(190, 10, 'Appartements : {}'.format(apartment), align='C')

    # Table
    pdf.cell(w=0, h=20, ln=1)
    pdf.set_fill_color(150, 150, 150)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('arial', 'I', 12)
    pdf.cell(110, 10, 'Quittance', align='C', fill=True, border=1)
    pdf.cell(80, 10, 'Montants', align='C', fill=True, border=1)

    pdf.set_text_color(0, 0, 0)

    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(5, 10, '', border='L')
    pdf.set_font('arial', 'I', 12)
    pdf.cell(105, 10, 'Période du {} au {}'.format(date_in, date_out), border='R', align='L')
    pdf.cell(80, 10, '', border='R')

    pdf.set_font('arial', '', 12)
    pdf.cell(w=0, h=10, ln=1)
    pdf.set_font('arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(5, 10, '', border='L')
    pdf.cell(105, 10, 'Loyer', border='R')
    pdf.cell(70, 10, '1550.00', align='R')
    # TODO add price calculation or not, function of per month/per day
    pdf.cell(10, 10, '{}'.format(chr(128)), border='R')

    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(5, 10, '', border='L')
    pdf.cell(105, 10, 'Charges', border='R')
    pdf.cell(70, 10, '0.00', align='R')
    pdf.cell(10, 10, '{}'.format(chr(128)), border='R')

    pdf.cell(w=0, h=10, ln=1)
    pdf.cell(110, 30, '', border='L, R')
    pdf.cell(80, 30, '', border='R')

    pdf.cell(w=0, h=20, ln=1)
    pdf.cell(100, 10, 'Total', align='R', border='L, B, T')
    pdf.cell(10, 10, '', border='R, B, T')
    pdf.cell(70, 10, '1550.00', align='R', border='B, T')
    pdf.cell(10, 10, '{}'.format(chr(128)), border='B, R, T')

    pdf.cell(w=0, h=30, ln=1)
    pdf.multi_cell(190, 7, '{}'.format(receipt_text), align='C')

    pdf.output(
        receipts_path + '/' + '{}.pdf'.format
            (create_receipt_nbr(
                apart_name=apart_req.apartment_name,
                id_customer=tenant_req.id
            )
        )
    )

    return '{}.pdf'.format(
        create_receipt_nbr(
            apart_name=apart_req.apartment_name,
            id_customer=tenant_req.id
        )
    )