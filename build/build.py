# Собирает index.html из шаблона и базы знаний: python3 build/build.py <версия>
import sys,re,json,subprocess,os
D=os.path.dirname(os.path.abspath(__file__));R=os.path.dirname(D);V=sys.argv[1]
subprocess.run([sys.executable,os.path.join(D,'kb_from_xlsx.py'),os.path.join(D,'kb.xlsx'),os.path.join(D,'kb.json')],check=True)
t=open(os.path.join(D,'app.html'),encoding='utf-8').read()
brand=re.sub(r'Спортивная · v\d+','Спортивная · v'+V,open(os.path.join(D,'brand.html'),encoding='utf-8').read())
kb=open(os.path.join(D,'kb.json'),encoding='utf-8').read().replace('</','<\\/')
t=t.replace('{{CSS}}',open(os.path.join(D,'base.css'),encoding='utf-8').read()).replace('{{BRAND}}',brand).replace('{{V}}',V).replace('{{KB}}',kb)
open(os.path.join(R,'index.html'),'w',encoding='utf-8').write(t)
open(os.path.join(R,'version.txt'),'w').write(V+'\n')
sw=open(os.path.join(R,'sw.js'),encoding='utf-8').read();sw=re.sub(r"const C='forum-v\d+'","const C='forum-v"+V+"'",sw)
sw=sw.replace("const SAME=['./','./index.html','./mermaid.min.js'];","const SAME=['./','./index.html'];")
open(os.path.join(R,'sw.js'),'w',encoding='utf-8').write(sw)
print('built v'+V,len(t))
