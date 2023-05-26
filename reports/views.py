from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import xlwt
from item.models import *
from store.models import *
from grn.models import *

class ReportView(View):
    template_name = 'reports/reports.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        from_date = request.POST.get("fromDate")
        to_date = request.POST.get("toDate")
        report_type = request.POST.get("reportType")
        print(from_date, to_date, report_type)
        if int(report_type) == 1:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="items_reports.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('items')
            ws.write_merge(0, 7, 0, 9,
                           'Copotron Inventory Management' + '\n' + 'Items report',
                           xlwt.easyxf(
                               'font: height 250, name Arial, colour_index black, bold on, italic on; align: wrap on, vert centre, horiz center;'))
            row_num = 10
            font_style = xlwt.XFStyle()
            columns = ['No', 'Item Name', 'Item Code ', 'Item Type', 'Description', 'Unit of measurement', 'Created At']
            for col_num in range(len(columns)):
                ws.row(row_num).height_mismatch = True
                ws.row(row_num).height = 20 * 20
                ws.write(row_num, col_num, columns[col_num], font_style)
            # font_style = xlwt.XFStyle()
            date_font = xlwt.XFStyle()
            font_style.font.height = 180
            date_font.font.height = 180
            font_style.borders.left = 1
            date_font.borders.left = 1
            font_style.borders.right = 1
            date_font.borders.right = 1
            font_style.borders.top = 1
            date_font.borders.top = 1
            font_style.borders.bottom = 1
            date_font.borders.bottom = 1
            date_font.num_format_str = 'yyyy-mm-dd'
            ws.col(0).width = int(27 * 260)
            ws.col(1).width = int(30 * 260)
            ws.col(2).width = int(27 * 260)
            rows = Item.objects.filter(created_at__range=[from_date, to_date])
            rows = list(rows)
            for i, row in enumerate(rows):
                row_num += 1
                ws.write(row_num, 0, i+1, font_style)
                ws.write(row_num, 1, row.name, date_font)
                ws.write(row_num, 2, row.item_code, font_style)
                ws.write(row_num, 3, row.item_type.name, font_style)
                ws.write(row_num, 4, row.description, font_style)
                ws.write(row_num, 5, row.uom.name, font_style)
                ws.write(row_num, 6, str(row.created_at), font_style)

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.font.height = 210
            font_style.borders.left = 1
            font_style.borders.right = 1
            font_style.borders.top = 1
            font_style.borders.bottom = 1
            wb.save(response)
            return response
        if int(report_type) == 2:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="store_reports.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('stores')
            ws.write_merge(0, 7, 0, 9,
                           'Copotron Inventory Management' + '\n' + 'Store report',
                           xlwt.easyxf(
                               'font: height 250, name Arial, colour_index black, bold on, italic on; align: wrap on, vert centre, horiz center;'))
            row_num = 10
            font_style = xlwt.XFStyle()
            columns = ['No', 'Store Name', 'Created At']
            for col_num in range(len(columns)):
                ws.row(row_num).height_mismatch = True
                ws.row(row_num).height = 20 * 20
                ws.write(row_num, col_num, columns[col_num], font_style)
            # font_style = xlwt.XFStyle()
            date_font = xlwt.XFStyle()
            font_style.font.height = 180
            date_font.font.height = 180
            font_style.borders.left = 1
            date_font.borders.left = 1
            font_style.borders.right = 1
            date_font.borders.right = 1
            font_style.borders.top = 1
            date_font.borders.top = 1
            font_style.borders.bottom = 1
            date_font.borders.bottom = 1
            date_font.num_format_str = 'yyyy-mm-dd'
            ws.col(0).width = int(27 * 260)
            ws.col(1).width = int(30 * 260)
            ws.col(2).width = int(27 * 260)
            rows = Store.objects.filter(created_at__range=[from_date, to_date])
            rows = list(rows)
            for i, row in enumerate(rows):
                row_num += 1
                ws.write(row_num, 0, i+1, font_style)
                ws.write(row_num, 1, row.name, date_font)
                ws.write(row_num, 2, str(row.created_at), font_style)

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.font.height = 210
            font_style.borders.left = 1
            font_style.borders.right = 1
            font_style.borders.top = 1
            font_style.borders.bottom = 1
            wb.save(response)
            return response
        if int(report_type) == 3:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="good_receive_reports.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('good_receive')
            ws.write_merge(0, 7, 0, 9,
                           'Copotron Inventory Management' + '\n' + 'Good Receive details report',
                           xlwt.easyxf(
                               'font: height 250, name Arial, colour_index black, bold on, italic on; align: wrap on, vert centre, horiz center;'))
            row_num = 10
            font_style = xlwt.XFStyle()
            columns = ['No', 'Good Receive Code', 'Total Price', 'Store', 'Item', 'Quantity', 'Unit Price', 'Created At']
            for col_num in range(len(columns)):
                ws.row(row_num).height_mismatch = True
                ws.row(row_num).height = 20 * 20
                ws.write(row_num, col_num, columns[col_num], font_style)
            # font_style = xlwt.XFStyle()
            date_font = xlwt.XFStyle()
            font_style.font.height = 180
            date_font.font.height = 180
            font_style.borders.left = 1
            date_font.borders.left = 1
            font_style.borders.right = 1
            date_font.borders.right = 1
            font_style.borders.top = 1
            date_font.borders.top = 1
            font_style.borders.bottom = 1
            date_font.borders.bottom = 1
            date_font.num_format_str = 'yyyy-mm-dd'
            ws.col(0).width = int(27 * 260)
            ws.col(1).width = int(30 * 260)
            ws.col(2).width = int(27 * 260)
            rows = GrnDetails.objects.filter(created_at__range=[from_date, to_date])
            rows = list(rows)
            for i, row in enumerate(rows):
                row_num += 1
                ws.write(row_num, 0, i+1, font_style)
                ws.write(row_num, 1, row.grn.code, date_font)
                ws.write(row_num, 2, row.grn.total_price, font_style)
                ws.write(row_num, 3, row.grn.store.name, font_style)
                ws.write(row_num, 4, row.item.name, font_style)
                ws.write(row_num, 5, row.quantity, font_style)
                ws.write(row_num, 6, row.unit_price, font_style)
                ws.write(row_num, 7, str(row.created_at), font_style)

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.font.height = 210
            font_style.borders.left = 1
            font_style.borders.right = 1
            font_style.borders.top = 1
            font_style.borders.bottom = 1
            wb.save(response)
            return response
        if int(report_type) == 4:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="stock_reports.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('stock')
            ws.write_merge(0, 7, 0, 9,
                           'Copotron Inventory Management' + '\n' + 'Stock Report',
                           xlwt.easyxf(
                               'font: height 250, name Arial, colour_index black, bold on, italic on; align: wrap on, vert centre, horiz center;'))
            row_num = 10
            font_style = xlwt.XFStyle()
            columns = ['No', 'Item', 'Quantity', 'Store', 'Created At']
            for col_num in range(len(columns)):
                ws.row(row_num).height_mismatch = True
                ws.row(row_num).height = 20 * 20
                ws.write(row_num, col_num, columns[col_num], font_style)
            # font_style = xlwt.XFStyle()
            date_font = xlwt.XFStyle()
            font_style.font.height = 180
            date_font.font.height = 180
            font_style.borders.left = 1
            date_font.borders.left = 1
            font_style.borders.right = 1
            date_font.borders.right = 1
            font_style.borders.top = 1
            date_font.borders.top = 1
            font_style.borders.bottom = 1
            date_font.borders.bottom = 1
            date_font.num_format_str = 'yyyy-mm-dd'
            ws.col(0).width = int(27 * 260)
            ws.col(1).width = int(30 * 260)
            ws.col(2).width = int(27 * 260)
            rows = Stock.objects.filter(created_at__range=[from_date, to_date])
            rows = list(rows)
            for i, row in enumerate(rows):
                row_num += 1
                ws.write(row_num, 0, i+1, font_style)
                ws.write(row_num, 1, row.item.name, date_font)
                ws.write(row_num, 2, row.quantity, font_style)
                ws.write(row_num, 3, row.store.name, font_style)
                ws.write(row_num, 4, str(row.created_at), font_style)

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.font.height = 210
            font_style.borders.left = 1
            font_style.borders.right = 1
            font_style.borders.top = 1
            font_style.borders.bottom = 1
            wb.save(response)
            return response
        if int(report_type) == 5:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="stock_out_reports.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('stock_out')
            ws.write_merge(0, 7, 0, 9,
                           'Copotron Inventory Management' + '\n' + 'Stock Out Report',
                           xlwt.easyxf(
                               'font: height 250, name Arial, colour_index black, bold on, italic on; align: wrap on, vert centre, horiz center;'))
            row_num = 10
            font_style = xlwt.XFStyle()
            columns = ['No', 'Item', 'Description', 'Stock Out Quantity', 'Remarks', 'Created At']
            for col_num in range(len(columns)):
                ws.row(row_num).height_mismatch = True
                ws.row(row_num).height = 20 * 20
                ws.write(row_num, col_num, columns[col_num], font_style)
            # font_style = xlwt.XFStyle()
            date_font = xlwt.XFStyle()
            font_style.font.height = 180
            date_font.font.height = 180
            font_style.borders.left = 1
            date_font.borders.left = 1
            font_style.borders.right = 1
            date_font.borders.right = 1
            font_style.borders.top = 1
            date_font.borders.top = 1
            font_style.borders.bottom = 1
            date_font.borders.bottom = 1
            date_font.num_format_str = 'yyyy-mm-dd'
            ws.col(0).width = int(27 * 260)
            ws.col(1).width = int(30 * 260)
            ws.col(2).width = int(27 * 260)
            rows = StockOut.objects.filter(created_at__range=[from_date, to_date])
            rows = list(rows)
            for i, row in enumerate(rows):
                row_num += 1
                ws.write(row_num, 0, i+1, font_style)
                ws.write(row_num, 1, row.stock.item.name, date_font)
                ws.write(row_num, 2, row.stock.item.description, date_font)
                ws.write(row_num, 3, row.quantity, font_style)
                ws.write(row_num, 4, row.remarks, font_style)
                ws.write(row_num, 5, str(row.created_at), font_style)

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.font.height = 210
            font_style.borders.left = 1
            font_style.borders.right = 1
            font_style.borders.top = 1
            font_style.borders.bottom = 1
            wb.save(response)
            return response
        return render("stocks")