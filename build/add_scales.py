# Добавляет в таблицу шкалы зрелости, ошибки, связки, главные вопросы (пример: ремонты, производство, бюджет)
import sys
from openpyxl import load_workbook
from openpyxl.styles import Font,Alignment,PatternFill,Border,Side
from openpyxl.utils import get_column_letter
P=sys.argv[1];wb=load_workbook(P)
F=Font(name='Arial',size=10);FH=Font(name='Arial',size=10,bold=True,color='FFFFFF');HF=PatternFill('solid',fgColor='112434');ED=PatternFill('solid',fgColor='FFF7D6')
W=Alignment(wrap_text=True,vertical='top');B=Border(bottom=Side(style='thin',color='DDE3E7'))
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from scales_data import IMPACT,MAIN,SCALES,ERRORS,LINKS
ws=wb['Вопросы']
if ws.cell(1,12).value!='Влияние на шкалу':
  for c,h in ((12,'Влияние на шкалу'),(13,'Главный вопрос')):
    x=ws.cell(1,c,h);x.font=FH;x.fill=HF;x.alignment=W
  ws.column_dimensions['L'].width=18;ws.column_dimensions['M'].width=10
for r in range(2,ws.max_row+1):
  t,q,a=ws.cell(r,1).value,ws.cell(r,3).value,ws.cell(r,7).value
  v=IMPACT.get((t,q),{}).get(a,'')
  for c,val in ((12,v),(13,'да' if (t,q) in MAIN else '')):
    x=ws.cell(r,c,val or None);x.font=F;x.alignment=W;x.border=B;x.fill=ED
# убрать общий вопрос «что полезно после форума» — его заменяет выбор демо в итоге
for r in range(ws.max_row,1,-1):
  if ws.cell(r,1).value=='common' and ws.cell(r,3).value=='t2':ws.delete_rows(r)
ws.auto_filter.ref=f"A1:M{ws.max_row}"
def sheet(name,head,widths,rows,edit):
  if name in wb.sheetnames:del wb[name]
  s=wb.create_sheet(name);s.append(head)
  for c in range(1,len(head)+1):x=s.cell(1,c);x.font=FH;x.fill=HF;x.alignment=W
  for row in rows:
    s.append(row);i=s.max_row
    for c in range(1,len(head)+1):x=s.cell(i,c);x.font=F;x.alignment=W;x.border=B;x.fill=ED if c-1 in edit else PatternFill()
  for i,w in enumerate(widths,1):s.column_dimensions[get_column_letter(i)].width=w
  s.freeze_panes='A2'
sheet('Шкалы',['Код темы','Код направления','Направление','Следующий уровень: как это выглядит в системе','Демо под это направление'],[10,12,26,80,50],SCALES,edit=(2,3,4))
sheet('Ошибки',['Код темы','Частая ошибка','Показать, если'],[10,90,18],ERRORS,edit=(1,2))
sheet('Связки',['Тема 1','Тема 2','Как темы связаны','Связанный сценарий на демо'],[10,10,80,60],LINKS,edit=(2,3))
# легенда
lg=wb['Как заполнять']
have={str(c.value) for c in lg['A']}
for t in ['','Шкала зрелости (пока заполнена для ремонтов, производства и бюджета):',
 '«Шкалы» — направления темы, как выглядит следующий уровень и что показать на демо под это направление.',
 '«Влияние на шкалу» на листе «Вопросы» — какой балл от 1 до 4 ставит ответ. Пример: «plan:1; cost:2». Если направление задели несколько ответов, берётся самый низкий балл.',
 '«Главный вопрос» — «да», если вопрос задаётся, даже когда клиент выбрал несколько тем. Остальные вопросы задаются, только когда тема одна.',
 '«Ошибки» — частые ошибки. «Показать, если»: например, «pf<=2» — если направление pf оценено на 2 и ниже. Пусто — показывать всегда.',
 '«Связки» — что сказать, если клиент выбрал обе темы, и какой связанный сценарий предложить на демо.']:
  if t and t in have:continue
  lg.append([t]);lg.cell(lg.max_row,1).font=Font(name='Arial',size=10,bold=t.endswith(':'));lg.cell(lg.max_row,1).alignment=W
wb.save(P);print('ok')
