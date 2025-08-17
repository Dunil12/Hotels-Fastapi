import io

from jinja2 import Template
from openpyxl.workbook import Workbook


def render_html(path: str, data: dict):
    with open(path) as f:
        template = Template(f.read())
    html_body = template.render(**data)
    return html_body


def generate_excel(data: dict):
    wb = Workbook()
    ws = wb.active
    ws.title = "Booking Details"
    ws.append(["Параметр", "Значение"])
    ws.append(["ID брони", data["booking_id"]])
    ws.append(["Отель", data["hotel_name"]])
    ws.append(["Номер", data["room_name"]])
    ws.append(["Дата заезда", data["date_from"]])
    ws.append(["Дата выезда", data["date_to"]])
    ws.append(["Стоимость", f"{data['price']} руб."])
    ws.append(["Email", data["user_email"]])

    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    return excel_file