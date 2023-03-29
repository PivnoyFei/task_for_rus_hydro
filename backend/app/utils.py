import uuid
from decimal import Decimal
from typing import Any

import pandas as pd
from django.conf import settings


def generate_uuid() -> str:
    return str(uuid.uuid4().hex)


def decimal_converter(value: Any) -> Decimal | None:
    try:
        if value:
            return Decimal(str(value))
        return None
    except ValueError:
        return None


def report_parser(file: Any) -> tuple[list, list, list, list]:
    file = pd.read_excel(
        file,
        converters={
            "Налоговая база": decimal_converter,
            "Налог": decimal_converter,
        },
        index_col=None,
        skiprows=[1, 2],
    )
    base_items = file["Налоговая база"]
    tax_items = file["Налог"]
    deviation_items = []
    tax_base_items = []

    for base, tax in zip(base_items, tax_items):
        if base:
            tax_base = 13 if base < 5000000 else 15
        else:
            tax_base = None

        if isinstance(base, Decimal):
            deviation_items.append(float(int(tax) - base / 100 * tax_base))
        else:
            deviation_items.append(None)
        tax_base_items.append(tax_base)

    return (
        list(file["Филиал"]),
        list(file["Сотрудник"]),
        list(file["Налоговая база"]),
        list(file["Налог"]),
        tax_base_items,
        deviation_items,
    )


def report_analysis(file):
    items = report_parser(file)
    filename = f"{generate_uuid()}.xlsx"
    path_filename = settings.MEDIA_ROOT / filename
    zipped = zip(*items)
    zipped = sorted(zipped, key=lambda x: x[-1] if x[-1] else 0, reverse=True)

    df = pd.DataFrame({i: [i] for i in range(7)})
    with pd.ExcelWriter(path_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Страница 1', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Страница 1']

        merge_format = workbook.add_format({'align': 'center', 'border': 1, 'text_wrap': True})
        row_format = workbook.add_format({'border': 1})
        row_format_red = workbook.add_format({'border': 1, 'bg_color': 'red'})
        row_format_green = workbook.add_format({'border': 1, 'bg_color': 'green'})

        worksheet.set_column('A:B', 41)
        worksheet.set_column('C:D', 11)
        worksheet.set_column('E:E', 16)
        worksheet.set_column('F:G', 11)
        worksheet.merge_range('A1:A2', 'Филиал', merge_format)
        worksheet.merge_range('B1:B2', 'Сотрудник', merge_format)
        worksheet.merge_range('C1:C2', 'Налоговая база', merge_format)
        worksheet.merge_range('D1:E1', 'Налог', merge_format)
        worksheet.merge_range('F1:G2', 'Отклонения', merge_format)
        worksheet.write('D2:D2', 'Исчисленно всего', merge_format)
        worksheet.write('E2:E2', 'Исчисленно всего по формуле', merge_format)

        count = 3
        for branch, coworker, base, tax, tax_base, deviation in zipped:
            if isinstance(coworker, str):
                worksheet.write_row(
                    f"A{count}",
                    (branch, coworker, base, tax, tax_base),
                    row_format
                )
                if isinstance(base, Decimal):
                    if deviation == 0:
                        worksheet.merge_range(f"F{count}:G{count}", deviation, row_format_green)
                    else:
                        worksheet.merge_range(f"F{count}:G{count}", deviation, row_format_red)
                count += 1

        return path_filename, filename, writer
