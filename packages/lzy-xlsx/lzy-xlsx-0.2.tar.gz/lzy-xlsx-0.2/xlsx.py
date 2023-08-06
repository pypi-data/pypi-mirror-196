import win32com.client as win32


def xlsx(old, new):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(old)
    wb.SaveAs(new, FileFormat=51)
    wb.Close()
    excel.Application.Quit()
    return new