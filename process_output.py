from openpyxl import load_workbook
import pdb


class Writer:
    def __init__(self, data):
        self.data = data

    def write(self, region, commune, rol_first, rol_second):
        wb = load_workbook("data/output.xlsx")
        ws = wb.worksheets[0]
        do_format = True
        if self.data is None:
            ws.append([commune, '{}-{}'.format(rol_first, rol_second), 'SIN INFORMACION'])
        else:
            if do_format:
                try:
                    ws.append(self.format_output(self.data))
                except:
                    ws.append([self.data[0], self.data[1], 'ERROR ESCRITURA'])
            else:
                for item in self.data:
                    ws.append(item)
        wb.save("data/output.xlsx")

    def format_output(self, data):
        total_debt = 0
        installments_debt = ''
        vigentes_installments = ''
        overall_state = ''
        # Data should come as [['ANTOFAGASTA', '15330-00023', '3-2019', '30-09-2019', '$ 188.292', '$ 231.227']] Look the array
        commune = data[0][0]
        rol = data[0][1]
        for register in data:
            try:
                _, _, installment, _, _, final_amount = register

                if final_amount == 'VIGENTE':
                    _, _, installment, _, final_amount, state = register
                    overall_state = state
                    vigentes_installments += '{}, '.format(final_amount)
                
                total_debt += int(final_amount.replace('$', '').replace('.', '').strip())
                installments_debt += '{}, '.format(installment)
            except:
                return register

        if overall_state == 'VIGENTE':
            return [commune, rol, rol.split('-')[0], rol.split('-')[1], overall_state, installments_debt, vigentes_installments, str(total_debt)]
        else:
            return [commune, rol, rol.split('-')[0], rol.split('-')[1], installments_debt, str(total_debt)]
