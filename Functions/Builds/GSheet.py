import lib

gc = lib.gspread.service_account(filename='gitignore/client_secret.json')

def getData(mode, workbook, sheet, range): #FromGSheet
    sh = gc.open_by_key(workbook)
    worksheet = sh.worksheet(sheet)
    if mode == "Meta" or mode == "Trials":
        res = worksheet.get(range, value_render_option='FORMULA')
    else:
        res = worksheet.get(range)
    return res

def pushData(data, workbook, sheet, start_letter, end_letter, start_row):

    for row in data:
        if row[len(row)-1] == "X" or row[len(row)-1] == "V":
            row = row.pop()

    sh = gc.open_by_key(workbook)
    worksheet = sh.worksheet(sheet)
    end_row = start_row + len(data) - 1
    range = "%s%d:%s%d" % (start_letter, start_row, end_letter, end_row)
    cell_list = worksheet.range(range)

    try:
        idx = 0
        for (start_row, rowlist) in enumerate(data):
            for (colnum, value) in enumerate(rowlist):
                cell_list[idx].value = value
                idx += 1
                if idx >= len(cell_list):
                    break
        
        # Update the whole sheet
        worksheet.update_cells(cell_list)
        return "Done"
    except:
        return "Not Done"

def reset_trialdata(workbook, sheet, range):
    sh = gc.open_by_key(workbook)   
    sh.values_clear(f"{sheet}!{range}")

def get_trialsheetlist(workbook):
    sh = gc.open_by_key(workbook)
    worksheets_list = sh.worksheets()
    list = []
    for worksheet in worksheets_list:
        if worksheet.title != "Summary":
            list.append(worksheet.title)

    
    return list

