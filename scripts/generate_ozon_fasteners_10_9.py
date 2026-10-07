from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from pathlib import Path
import io, urllib.request, math

W,H=1440,720
OUT=Path('ozon/rich-content/fasteners-10-9-v3')
OUT.mkdir(parents=True, exist_ok=True)
BLUE=(20,88,177); RED=(239,35,42); NAVY=(20,28,38); MID=(95,105,118); WHITE=(255,255,255)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
BOLDOB='/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'

def f(path,size): return ImageFont.truetype(path,size)
def rr(draw,box,r,fill,outline=None,width=1): draw.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def txt(draw,xy,text,font,fill=NAVY,anchor=None,spacing=4,align='left'): draw.multiline_text(xy,text,font=font,fill=fill,anchor=anchor,spacing=spacing,align=align)
def logo(im,x,y,scale=1.0):
    d=ImageDraw.Draw(im); s=scale
    d.polygon([(x,y+88*s),(x+48*s,y),(x+98*s,y+88*s),(x+76*s,y+88*s),(x+49*s,y+39*s),(x+23*s,y+88*s)], fill=BLUE)
    d.polygon([(x+18*s,y+63*s),(x+115*s,y+42*s),(x+101*s,y+58*s),(x+36*s,y+72*s)], fill=RED)
    d.polygon([(x+61*s,y+83*s),(x+116*s,y+94*s),(x+91*s,y+104*s),(x+48*s,y+96*s)], fill=RED)
def ribbons(im):
    d=ImageDraw.Draw(im)
    d.polygon([(0,0),(W,0),(W,28),(520,46),(0,25)],fill=BLUE); d.polygon([(0,12),(W,7),(W,26),(820,47),(0,31)],fill=RED)
    d.polygon([(0,H-26),(W,H-45),(W,H),(0,H)],fill=BLUE); d.polygon([(0,H-12),(W,H-56),(W,H-29),(420,H),(0,H)],fill=RED)
def base(): im=Image.new('RGB',(W,H),WHITE); ribbons(im); return im
def pill(draw,x,y,text,w=None):
    font=f(BOLDOB,34); w=w or int(draw.textlength(text,font=font)+54)
    rr(draw,(x,y,x+w,y+54),18,BLUE); txt(draw,(x+24,y+9),text,font,WHITE); return w
def title(im,k,title1,accent=None,sub=None):
    d=ImageDraw.Draw(im); rr(d,(18,18,76,70),14,RED); txt(d,(47,44),str(k),f(BOLD,30),WHITE,anchor='mm')
    x=92; y=58; txt(d,(x,y),title1,f(BOLDOB,48),NAVY)
    if accent: txt(d,(x+d.textlength(title1,font=f(BOLDOB,48))+14,y),accent,f(BOLDOB,48),RED)
    if sub: pill(d,x,y+66,sub)
    logo(im,W-148,36,0.78)
def bullet(draw,x,y,head,body='',icon='■'):
    rr(draw,(x,y,x+56,y+56),12,RED); txt(draw,(x+28,y+28),icon,f(BOLD,26),WHITE,anchor='mm')
    txt(draw,(x+74,y-2),head,f(BOLD,26),NAVY)
    if body: txt(draw,(x+74,y+31),body,f(FONT,18),MID,spacing=2)
def draw_metal_bolt(size=(520,300),socket=False,nut=False):
    w,h=size; im=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse((40,max(1,h-65),max(41,w-25),max(2,h-20)),fill=(0,0,0,35))
    x0=max(42,int(w*0.25)); x1=max(x0+20,w-35)
    for i in range(36):
        c=int(105+125*math.sin((i/35)*math.pi)); d.rectangle((x0,h//2-40+i*2,x1,h//2-38+i*2),fill=(c,c+5,c+10,255))
    for x in range(x0+8,x1,16): d.line((x,h//2-38,x-12,h//2+38),fill=(65,72,82,255),width=3)
    if socket:
        d.rounded_rectangle((max(5,int(w*0.04)),max(4,h//2-int(h*0.32)),max(40,int(w*0.25)),min(h-4,h//2+int(h*0.32))),radius=max(6,int(h*0.1)),fill=(165,170,178,255),outline=(80,85,92,255),width=4)
        d.regular_polygon((max(22,int(w*0.15)),h//2,max(8,int(min(w,h)*0.14))),6,rotation=30,fill=(42,47,55,255))
    else:
        hx=max(12,int(w*0.07)); hw=max(28,int(w*0.12)); hh=max(16,int(h*0.22)); cx=hx+hw
        pts=[(hx,h//2),(cx-hw//2,h//2-hh),(cx+hw//2,h//2-hh),(hx+2*hw,h//2),(cx+hw//2,h//2+hh),(cx-hw//2,h//2+hh)]
        d.polygon(pts,fill=(180,185,194,255),outline=(76,82,90,255))
        if w>=260: txt(d,(cx,h//2),'10.9',f(BOLD,max(12,int(h*0.07))),(55,60,68),anchor='mm')
    if nut:
        cx=w-max(24,int(w*0.08)); cy=h//2; nw=max(14,int(min(w,h)*0.16)); nh=max(12,int(min(w,h)*0.14))
        pts=[(cx-nw,cy),(cx-nw//2,cy-nh),(cx+nw//2,cy-nh),(cx+nw,cy),(cx+nw//2,cy+nh),(cx-nw//2,cy+nh)]
        d.polygon(pts,fill=(175,181,190,255),outline=(78,84,92,255)); r=max(5,nw//3); d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(52,58,66,255))
    return im.filter(ImageFilter.GaussianBlur(0.25))

URLS={
'hexsocket':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Screw%20Head%20-%20Hex%20Socket.jpg',
'hexnut':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Hex-nut.png',
'boltnut':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Bolt%20and%20nut,%20annotated.jpg',
'socketphoto':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Screw%20with%20head%20Hex%20Socket-Slot-02.jpg'}
CACHE={}
def photo(key,size=(620,430)):
    if key in CACHE: src=CACHE[key].copy()
    else:
        try:
            req=urllib.request.Request(URLS[key],headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=20) as r: src=Image.open(io.BytesIO(r.read())).convert('RGB')
            CACHE[key]=src.copy()
        except Exception:
            src=Image.new('RGB',(900,600),(238,241,245)); bolt=draw_metal_bolt((760,420),socket=key in ('hexsocket','socketphoto'),nut=key in ('hexnut','boltnut')); src.paste(bolt,(70,90),bolt)
    return ImageOps.fit(src,size,method=Image.Resampling.LANCZOS)
def photo_card(im,box,key):
    x0,y0,x1,y1=box; p=photo(key,(x1-x0,y1-y0)); mask=Image.new('L',p.size,0); ImageDraw.Draw(mask).rounded_rectangle((0,0,*p.size),radius=28,fill=255)
    im.paste(p,(x0,y0),mask); ImageDraw.Draw(im).rounded_rectangle(box,radius=28,outline=(218,223,231),width=2)
def save(im,i): im.save(OUT/f'slide_{i:02d}.jpg','JPEG',quality=94,subsampling=0,optimize=True)

im=base(); title(im,1,'ВЫСОКОПРОЧНЫЙ КРЕПЁЖ','10.9','БОЛТЫ • ВИНТЫ • ГАЙКИ'); d=ImageDraw.Draw(im)
bullet(d,72,260,'ОТВЕТСТВЕННЫЕ\nСОЕДИНЕНИЯ','Для промышленного монтажа','✓'); bullet(d,72,390,'ПРОМЫШЛЕННОЕ\nКАЧЕСТВО','Точная геометрия и резьба','◆'); bullet(d,72,520,'ШИРОКИЙ ВЫБОР\nРАЗМЕРОВ','Популярные метрические размеры','●'); photo_card(im,(720,160,1350,625),'boltnut'); save(im,1)

im=base(); title(im,2,'ПРЕИМУЩЕСТВА',None,'НАШЕЙ ПРОДУКЦИИ'); d=ImageDraw.Draw(im)
for yy,h,b,ic in [(210,'ВЫСОКАЯ ПРОЧНОСТЬ','Для узлов с повышенными нагрузками','◆'),(320,'ТОЧНАЯ ГЕОМЕТРИЯ','Соответствие типоразмерам и стандартам','◎'),(430,'КАЧЕСТВЕННАЯ РЕЗЬБА','Ровный профиль для уверенного монтажа','≋'),(540,'НАДЁЖНАЯ ФИКСАЦИЯ','Стабильное соединение при корректной затяжке','✓')]: bullet(d,70,yy,h,b,ic)
photo_card(im,(820,165,1360,625),'hexsocket'); save(im,2)

im=base(); title(im,3,'АССОРТИМЕНТ',None,'ВЫСОКОПРОЧНОГО КРЕПЕЖА'); d=ImageDraw.Draw(im)
for x0,x1,h1,h2,key,body in [(35,455,'БОЛТЫ','DIN 933 / DIN 931','boltnut','Шестигранная головка\nПолная / неполная резьба'),(495,915,'ВИНТЫ','DIN 912','socketphoto','Цилиндрическая головка\nВнутренний шестигранник'),(955,1375,'ГАЙКИ','КЛАСС 10','hexnut','Для соединений с крепежом 10.9\nНадёжная совместимость')]:
    txt(d,(x0+20,190),h1,f(BOLD,34)); txt(d,(x0+20,233),h2,f(BOLD,24)); photo_card(im,(x0+20,278,x1-20,500),key); txt(d,(x0+24,525),body,f(FONT,20),MID)
save(im,3)

im=base(); title(im,4,'КЛАСС ПРОЧНОСТИ','10.9','ДЛЯ ОТВЕТСТВЕННЫХ СОЕДИНЕНИЙ'); d=ImageDraw.Draw(im)
for yy,h,b,ic in [(240,'ВЫСОКАЯ НАГРУЗКА','Подходит для ответственных узлов','↔'),(370,'УСТОЙЧИВОСТЬ\nК ДЕФОРМАЦИИ','Прочность при корректном подборе и монтаже','⬢'),(515,'НАДЁЖНОСТЬ\nВ РАБОТЕ','Для промышленного применения','⚙')]: bullet(d,70,yy,h,b,ic)
bolt=draw_metal_bolt((620,360),nut=True); im.paste(bolt,(760,240),bolt); save(im,4)

im=base(); title(im,5,'ТОЧНАЯ РЕЗЬБА И ГЕОМЕТРИЯ'); d=ImageDraw.Draw(im)
bullet(d,70,235,'ЧИСТЫЙ ПРОФИЛЬ РЕЗЬБЫ','Уверенное навинчивание без перекоса','≋'); bullet(d,70,370,'СООТВЕТСТВИЕ СТАНДАРТАМ','DIN / ISO — в зависимости от позиции','◎'); bullet(d,70,505,'СТАБИЛЬНЫЕ РАЗМЕРЫ','Предсказуемая посадка деталей','✓'); photo_card(im,(760,170,1355,625),'hexsocket'); save(im,5)

im=base(); title(im,6,'НАДЁЖНАЯ ФИКСАЦИЯ',None,'СТАБИЛЬНОЕ СОЕДИНЕНИЕ'); d=ImageDraw.Draw(im)
bullet(d,70,245,'ПРОЧНОЕ СОЕДИНЕНИЕ','Для статических и динамических нагрузок','↔'); bullet(d,70,390,'СОВМЕСТИМОСТЬ','Болты/винты 10.9 + гайки класса 10','⚙'); bullet(d,70,535,'КОНТРОЛИРУЕМЫЙ МОНТАЖ','Рекомендуемый момент затяжки — по документации','✓'); photo_card(im,(810,170,1360,620),'boltnut'); save(im,6)

im=base(); title(im,7,'МАТЕРИАЛ И ПОКРЫТИЕ',None,'ЗАЩИТА И ДОЛГОВЕЧНОСТЬ'); d=ImageDraw.Draw(im)
bullet(d,65,240,'ВЫСОКОПРОЧНАЯ СТАЛЬ','Класс 10.9 для болтов и винтов; класс 10 для гаек','◆'); bullet(d,65,390,'ЦИНКОВОЕ ПОКРЫТИЕ','Для оцинкованных позиций серии — защита поверхности','⬢'); bullet(d,65,540,'АККУРАТНАЯ ПОВЕРХНОСТЬ','Промышленный внешний вид и ровная обработка','✦'); bolt=draw_metal_bolt((600,340),nut=True); im.paste(bolt,(780,255),bolt); save(im,7)

im=base(); title(im,8,'СФЕРЫ ПРИМЕНЕНИЯ',None,'ТАМ, ГДЕ ВАЖНА НАДЁЖНОСТЬ'); d=ImageDraw.Draw(im)
for j,(lab,ic) in enumerate([('МАШИНОСТРОЕНИЕ','M'),('МЕТАЛЛОКОНСТРУКЦИИ','K'),('МОНТАЖ\nОБОРУДОВАНИЯ','O'),('ПРОИЗВОДСТВО','P'),('РЕМОНТ И СЕРВИС','R')]):
    x=45+j*275; rr(d,(x,220,x+240,540),24,(240,243,247),outline=(215,220,228),width=2); rr(d,(x+74,255,x+166,347),20,BLUE); txt(d,(x+120,301),ic,f(BOLD,42),WHITE,anchor='mm'); txt(d,(x+120,410),lab,f(BOLD,20),NAVY,anchor='mm',align='center')
save(im,8)

im=base(); title(im,9,'КАК ПОДОБРАТЬ КРЕПЁЖ',None,'ПРОСТОЙ ЧЕК-ЛИСТ'); d=ImageDraw.Draw(im)
for col,arr in enumerate([[('1','ДИАМЕТР (M)','Выберите нужный размер'),('2','ДЛИНА','Учитывайте толщину соединяемых деталей'),('3','ШАГ РЕЗЬБЫ','Стандартный или мелкий — по задаче')],[('4','СТАНДАРТ DIN / ISO','Например DIN 933, DIN 931, DIN 912'),('5','ТИП ГОЛОВКИ','Шестигранная или цилиндрическая'),('6','КОЛИЧЕСТВО','Подберите фасовку под объём работ')]]):
    x=70+col*675
    for j,(n,h,b) in enumerate(arr):
        y=220+j*135; rr(d,(x,y,x+58,y+58),12,RED); txt(d,(x+29,y+29),n,f(BOLD,24),WHITE,anchor='mm'); txt(d,(x+78,y),h,f(BOLD,24)); txt(d,(x+78,y+35),b,f(FONT,18),MID)
save(im,9)

im=base(); title(im,10,'РАЗМЕРЫ И МАРКИРОВКА',None,'ПРИМЕРЫ ОБОЗНАЧЕНИЙ'); d=ImageDraw.Draw(im)
txt(d,(70,220),'Популярные размеры:',f(BOLD,26)); x=70
for s in ['M6','M8','M10','M12','M16']: rr(d,(x,270,x+95,322),14,(241,244,248),outline=(190,198,210),width=2); txt(d,(x+47,296),s,f(BOLD,22),anchor='mm'); x+=110
txt(d,(70,365),'Болт / винт:',f(BOLD,26)); pill(d,70,405,'M10 × 50    DIN 933    10.9',520); txt(d,(70,505),'Гайка:',f(BOLD,26)); pill(d,70,545,'M10    DIN 934    класс 10',480)
bolt=draw_metal_bolt((560,330),nut=True); im.paste(bolt,(805,250),bolt); save(im,10)

im=base(); title(im,11,'КОМПЛЕКТАЦИЯ И УПАКОВКА',None,'УДОБНО ДЛЯ РАБОТЫ'); d=ImageDraw.Draw(im)
bullet(d,70,250,'НАДЁЖНАЯ УПАКОВКА','Защита при хранении и транспортировке','□'); bullet(d,70,395,'РАЗНЫЕ ФАСОВКИ','Подберите объём под конкретную задачу','▦'); bullet(d,70,540,'ПОНЯТНАЯ МАРКИРОВКА','Размер и стандарт удобно проверять перед монтажом','✓')
rr(d,(850,250,1305,560),28,(190,132,74),outline=(135,90,50),width=4); rr(d,(885,285,1270,535),18,(225,188,139))
for yy in [320,400,480]:
    for xx in [930,1040,1150]:
        b=draw_metal_bolt((120,70),socket=(xx==1040),nut=(yy==480)); im.paste(b,(xx-60,yy-35),b)
save(im,11)

im=base(); title(im,12,'РЕКОМЕНДАЦИИ ПО МОНТАЖУ',None,'ДЛЯ НАДЁЖНОГО СОЕДИНЕНИЯ'); d=ImageDraw.Draw(im)
for yy,h,b,ic in [(220,'ПОДБЕРИТЕ ИНСТРУМЕНТ','Ключ или шестигранник нужного размера','1'),(325,'СОБЛЮДАЙТЕ МОМЕНТ ЗАТЯЖКИ','Ориентируйтесь на техническую документацию','2'),(430,'ОЧИСТИТЕ ПОВЕРХНОСТИ','Удалите загрязнения перед сборкой','3'),(535,'ПРОВЕРЬТЕ СОЕДИНЕНИЕ','Особенно при вибрационных нагрузках','4')]: bullet(d,65,yy,h,b,ic)
photo_card(im,(845,175,1360,620),'socketphoto'); save(im,12)

im=base(); d=ImageDraw.Draw(im); rr(d,(18,18,76,70),14,RED); txt(d,(47,44),'13',f(BOLD,30),WHITE,anchor='mm'); logo(im,95,170,1.55)
txt(d,(300,175),'НАДЁЖНЫЙ КРЕПЁЖ',f(BOLDOB,48)); txt(d,(300,235),'ДЛЯ ОТВЕТСТВЕННЫХ СОЕДИНЕНИЙ',f(BOLDOB,38))
for j,(h,ic) in enumerate([('ПРОВЕРЕННОЕ\nКАЧЕСТВО','✓'),('ШИРОКИЙ\nАССОРТИМЕНТ','A'),('НАДЁЖНЫЙ\nПАРТНЁР','◆')]):
    x=300+j*250; rr(d,(x,350,x+64,414),14,RED); txt(d,(x+32,382),ic,f(BOLD,26),WHITE,anchor='mm'); txt(d,(x+78,356),h,f(BOLD,20),NAVY)
bolt=draw_metal_bolt((520,280),nut=True); im.paste(bolt,(870,320),bolt); save(im,13)

thumbs=[Image.open(OUT/f'slide_{i:02d}.jpg').resize((576,288),Image.Resampling.LANCZOS) for i in range(1,14)]
prev=Image.new('RGB',(1182,2206),(232,235,240))
for i,t in enumerate(thumbs[:12]): prev.paste(t,(10+(i%2)*591,10+(i//2)*318))
prev.paste(thumbs[12],(303,1913)); prev.save(OUT/'preview.jpg','JPEG',quality=90,optimize=True)
