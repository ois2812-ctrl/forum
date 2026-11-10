# Читает таблицу базы знаний и пишет kb.json для формы
import sys,json,re
from openpyxl import load_workbook
src,out=sys.argv[1],sys.argv[2]
wb=load_workbook(src,data_only=True)
def rows(name):
  ws=wb[name];it=ws.iter_rows(values_only=True);head=[str(h or '').strip() for h in next(it)]
  return [dict(zip(head,[('' if v is None else str(v).strip()) for v in r])) for r in it if any(v not in (None,'') for v in r)]
T=[];TI={}
for r in rows('Темы'):
  t={'id':r['Код темы'],'n':r['Тема (как видит клиент)'],'deep':r['Глубина']=='полная','kw':[k.strip().lower().replace('ё','е') for k in re.split(r'[,;\n]',r['Слова для распознавания']) if k.strip()],'demo':r['Что покажем на демо'],'q':[]}
  T.append(t);TI[t['id']]=t
TI['common']={'id':'common','n':'Общие вопросы','q':[]}
for r in rows('Итоги по темам'):
  t=TI.get(r['Код темы'])
  if t:t['intro']=r['Вступление к итогу'];t['base']=[x.strip() for x in r['Чек-лист: всегда'].split('\n') if x.strip()]
Q={}
for r in rows('Вопросы'):
  tid,qid=r['Код темы'],r['№ вопроса'];t=TI.get(tid)
  if not t:continue
  k=(tid,qid)
  if k not in Q:
    cond=None;c=r['Показать, если'].replace(' ','')
    if c and ':' in c:a,b=c.split(':',1);cond={'q':a,'a':[x for x in b.split(',') if x]}
    Q[k]={'id':qid,'t':r['Вопрос'],'cond':cond,'multi':r['Несколько ответов'].lower() in ('да','yes','1'),'main':r.get('Главный вопрос','').lower() in ('да','yes','1'),'o':[]};t['q'].append(Q[k])
  imp={}
  for part in re.split(r'[;,]',r.get('Влияние на шкалу','')):
    if ':' in part:
      d,v=part.split(':',1)
      try:imp[d.strip()]=int(float(v))
      except ValueError:pass
  Q[k]['o'].append({'c':r['Код ответа'],'t':r['Ответ'],'see':r['Что мы видим (вывод)'],'rec':r['Рекомендация'],'chk':r['Пункт чек-листа'],'imp':imp})
def cond(c):
  out=[]
  for part in re.split(r'[;,]',c or ''):
    m=re.match(r'\s*(\w+)\s*<=\s*(\d)',part)
    if m:out.append({'d':m.group(1),'max':int(m.group(2))})
  return out
if 'Шкалы' in wb.sheetnames:
  for r in rows('Шкалы'):
    t=TI.get(r['Код темы'])
    if t:t.setdefault('dims',[]).append({'id':r['Код направления'],'n':r['Направление'],'next':r['Следующий уровень: как это выглядит в системе'],'demo':r['Демо под это направление']})
if 'Ошибки' in wb.sheetnames:
  for r in rows('Ошибки'):
    t=TI.get(r['Код темы'])
    if t:t.setdefault('err',[]).append({'t':r['Частая ошибка'],'cond':cond(r['Показать, если'])})
links=[]
if 'Связки' in wb.sheetnames:
  links=[{'a':r['Тема 1'],'b':r['Тема 2'],'t':r['Как темы связаны'],'demo':r['Связанный сценарий на демо']} for r in rows('Связки')]
kb={'topics':T,'common':TI['common']['q'],'links':links}
json.dump(kb,open(out,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('topics',len(T),'questions',len(Q))
