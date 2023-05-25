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
            columns = ['No', 'Item Name', 'Created At']
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
        return render("stocks")