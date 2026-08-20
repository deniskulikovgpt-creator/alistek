from __future__ import annotations

from pathlib import Path
from typing import Sequence

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1440
BLUE = "#083D8C"
INK = "#18283B"
MUTED = "#5B6F85"
WHITE = "#FFFFFF"
OFFWHITE = "#F5F9FD"
GOLD = "#D8A23B"

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "avito" / "tourist-protection" / "sankt-peterburg"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_COND = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"


def font(size: int, bold: bool = False, condensed: bool = False) -> ImageFont.FreeTypeFont:
    p = FONT_COND if condensed else (FONT_BOLD if bold else FONT_REG)
    return ImageFont.truetype(p, size=size)


def vertical_gradient(top: str = OFFWHITE, bottom: str = "#DDECF8") -> Image.Image:
    a = Image.new("RGB", (1, H), top)
    p = a.load()
    t = Image.new("RGB", (1, 1), top).getpixel((0, 0))
    b = Image.new("RGB", (1, 1), bottom).getpixel((0, 0))
    for y in range(H):
        k = y / max(1, H - 1)
        p[0, y] = tuple(int(t[i] * (1 - k) + b[i] * k) for i in range(3))
    return a.resize((W, H))


def rounded(draw: ImageDraw.ImageDraw, box, radius=28, fill=WHITE, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def shield(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, fill=WHITE, stroke=BLUE):
    pts = [(x, y), (x+s, y), (x+s*0.92, y+s*0.72), (x+s*0.5, y+s), (x+s*0.08, y+s*0.72)]
    draw.polygon(pts, fill=fill, outline=stroke)
    draw.line([pts[-1], pts[0], pts[1], pts[2], pts[3], pts[4], pts[0]], fill=stroke, width=max(3, s//22), joint="curve")
    f = font(int(s*0.5), bold=True, condensed=True)
    bb = draw.textbbox((0,0), "A", font=f)
    draw.text((x+s/2-(bb[2]-bb[0])/2, y+s*0.13), "A", font=f, fill=BLUE)


def header(draw: ImageDraw.ImageDraw, number: int):
    rounded(draw, (36, 32, 124, 120), 10, BLUE)
    draw.text((80, 76), str(number), font=font(50, bold=True), fill=WHITE, anchor="mm")
    shield(draw, 156, 32, 78, fill=WHITE, stroke=BLUE)
    draw.text((256, 64), "ALISTEK", font=font(58, bold=True, condensed=True), fill=BLUE, anchor="lm")
    draw.line((36, 144, W-36, 144), fill="#BFD4E7", width=3)


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = word if not cur else cur + " " + word
        if draw.textlength(test, font=f) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, f, fill, width, spacing=12):
    x, y = xy
    lines = wrap(draw, text, f, width)
    lh = f.size + spacing
    for i, line in enumerate(lines):
        draw.text((x, y+i*lh), line, font=f, fill=fill)


def title(draw, x, y, lines: Sequence[tuple[str, str]], max_width: int, base_size=88):
    yy = y
    for txt, color in lines:
        size = base_size
        f = font(size, bold=True, condensed=True)
        while draw.textlength(txt, font=f) > max_width and size > 48:
            size -= 2
            f = font(size, bold=True, condensed=True)
        draw.text((x, yy), txt, font=f, fill=color)
        yy += int(size*1.02)
    return yy


def icon_check(draw, cx, cy, r=28, fill=BLUE):
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=fill)
    draw.line((cx-r*0.45, cy, cx-r*0.1, cy+r*0.35, cx+r*0.5, cy-r*0.42), fill=WHITE, width=max(5,r//5), joint="curve")


def icon_number(draw, cx, cy, n, r=34):
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=BLUE)
    draw.text((cx, cy), str(n), font=font(36,bold=True), fill=WHITE, anchor="mm")


def bullet_list(draw, x, y, items: Sequence[str], width=700, fs=38, gap=28, numbered=False):
    yy = y
    for i, item in enumerate(items, 1):
        if numbered:
            icon_number(draw, x+34, yy+32, i)
        else:
            icon_check(draw, x+30, yy+30, 24)
        f = font(fs, bold=numbered)
        lines = wrap(draw, item, f, width-90)
        for j, line in enumerate(lines):
            draw.text((x+80, yy+j*(fs+10)), line, font=f, fill=INK)
        yy += max(70, len(lines)*(fs+10)) + gap


def city_skyline(draw, y=1040, x0=1000, x1=1880, color="#88ACCA"):
    draw.rectangle((x0, y, x1, y+250), fill="#DCE9F4")
    x = x0+20
    widths = [90,130,75,150,95,115,80,145,100]
    heights = [190,260,155,310,205,245,175,280,210]
    for w,h in zip(widths, heights):
        draw.rectangle((x, y-h, x+w, y), fill=color)
        for wx in range(x+18, x+w-12, 28):
            for wy in range(y-h+22, y-20, 34):
                draw.rectangle((wx,wy,wx+9,wy+14), fill="#EAF4FB")
        x += w+15
        if x > x1-80:
            break


def dome_landmark(draw, x, y, scale=1.0):
    c = GOLD
    dark = "#8A6B2B"
    draw.rectangle((x, y, x+360*scale, y+300*scale), fill="#D5E4F0", outline=dark, width=4)
    for i in range(6):
        xx=x+(35+i*52)*scale
        draw.rectangle((xx,y+110*scale,xx+20*scale,y+300*scale),fill="#F5F0DA",outline=dark,width=3)
    draw.ellipse((x+72*scale,y-160*scale,x+288*scale,y+70*scale), fill=c, outline=dark, width=5)
    draw.rectangle((x+150*scale,y-210*scale,x+210*scale,y-145*scale),fill=c,outline=dark,width=4)
    draw.line((x+180*scale,y-260*scale,x+180*scale,y-205*scale),fill=dark,width=6)
    draw.line((x+160*scale,y-245*scale,x+200*scale,y-245*scale),fill=dark,width=6)


def suitcase(draw, x, y, w=250, h=330, color="#0B4F96"):
    rounded(draw, (x,y,x+w,y+h), 28, color, "#06336E", 6)
    draw.rounded_rectangle((x+w*0.32,y-45,x+w*0.68,y+20),radius=14,outline="#06336E",width=8)
    for xx in (x+30,x+w-50):
        draw.ellipse((xx,y+h-8,xx+28,y+h+20),fill="#263746")
    draw.line((x+w*0.62,y+25,x+w*0.62,y+h-25),fill="#77BDED",width=5)


def person_lawyer(draw, x, y, scale=1.0, headset=False):
    skin="#E8B18F"; hair="#35271F"; blazer=BLUE; shirt=WHITE
    draw.ellipse((x+70*scale,y,x+230*scale,y+170*scale),fill=skin,outline="#7F513D",width=4)
    draw.pieslice((x+45*scale,y-25*scale,x+255*scale,y+195*scale),180,360,fill=hair)
    draw.polygon([(x+15*scale,y+165*scale),(x+285*scale,y+165*scale),(x+340*scale,y+500*scale),(x-40*scale,y+500*scale)],fill=blazer)
    draw.polygon([(x+105*scale,y+165*scale),(x+195*scale,y+165*scale),(x+170*scale,y+360*scale),(x+130*scale,y+360*scale)],fill=shirt)
    draw.line((x+80*scale,y+195*scale,x+135*scale,y+365*scale),fill="#041F50",width=int(12*scale))
    draw.line((x+220*scale,y+195*scale,x+165*scale,y+365*scale),fill="#041F50",width=int(12*scale))
    draw.ellipse((x+110*scale,y+70*scale,x+122*scale,y+82*scale),fill="#2A1B17")
    draw.ellipse((x+180*scale,y+70*scale,x+192*scale,y+82*scale),fill="#2A1B17")
    draw.arc((x+125*scale,y+95*scale,x+185*scale,y+135*scale),0,180,fill="#9F4F50",width=4)
    if headset:
        draw.arc((x+72*scale,y+25*scale,x+230*scale,y+170*scale),190,350,fill="#263746",width=int(10*scale))
        draw.ellipse((x+214*scale,y+90*scale,x+245*scale,y+132*scale),fill="#263746")
        draw.line((x+230*scale,y+120*scale,x+250*scale,y+150*scale),fill="#263746",width=int(8*scale))


def plane_window(draw, x, y, w=520, h=620):
    rounded(draw,(x,y,x+w,y+h),120,"#D7E7F4","#7CA8CB",10)
    rounded(draw,(x+55,y+55,x+w-55,y+h-55),95,"#8ED2F2","#BFD8EA",7)
    for cx,cy,r in [(x+170,y+240,70),(x+260,y+220,95),(x+355,y+250,75)]:
        draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill=WHITE)
    draw.polygon([(x+40,y+455),(x+440,y+330),(x+480,y+395),(x+205,y+525)],fill="#F2F5F8",outline="#557FA3")
    draw.polygon([(x+205,y+525),(x+380,y+470),(x+400,y+510),(x+260,y+555)],fill="#2E7DBB")


def statue(draw,x,y,scale=1.0):
    c="#263C55"
    draw.polygon([(x,y+460*scale),(x+330*scale,y+400*scale),(x+410*scale,y+520*scale),(x-30*scale,y+540*scale)],fill="#A77843")
    draw.ellipse((x+80*scale,y+115*scale,x+275*scale,y+300*scale),fill=c)
    draw.polygon([(x+120*scale,y+230*scale),(x+30*scale,y+420*scale),(x+100*scale,y+425*scale),(x+180*scale,y+290*scale)],fill=c)
    draw.polygon([(x+260*scale,y+245*scale),(x+390*scale,y+170*scale),(x+405*scale,y+200*scale),(x+295*scale,y+290*scale)],fill=c)
    draw.ellipse((x+155*scale,y+55*scale,x+220*scale,y+120*scale),fill=c)
    draw.polygon([(x+170*scale,y+110*scale),(x+245*scale,y+245*scale),(x+130*scale,y+270*scale)],fill=c)


def beach_scene(draw,x,y):
    draw.rectangle((x,y+360,x+720,y+610),fill="#F6D58A")
    draw.rectangle((x,y,x+720,y+360),fill="#83CEF2")
    draw.ellipse((x+530,y+55,x+640,y+165),fill="#FFD466")
    draw.pieslice((x+70,y+90,x+410,y+350),180,360,fill="#0B5FA7")
    draw.pieslice((x+70,y+90,x+410,y+350),210,240,fill=WHITE)
    draw.pieslice((x+70,y+90,x+410,y+350),270,300,fill=WHITE)
    draw.line((x+240,y+220,x+215,y+520),fill="#6F5739",width=12)
    draw.line((x+340,y+330,x+550,y+540),fill="#6F5739",width=18)
    draw.line((x+520,y+315,x+385,y+545),fill="#6F5739",width=18)
    draw.polygon([(x+345,y+325),(x+520,y+315),(x+525,y+370),(x+390,y+525)],fill="#F5F7FA",outline=BLUE)
    for i in range(5):
        draw.line((x+360+i*33,y+330,x+410+i*25,y+500),fill=BLUE if i%2==0 else WHITE,width=24)
    suitcase(draw,x+530,y+315,150,210,"#C12B35")


def bridge_scene(draw,x,y,w=850,h=520):
    draw.rectangle((x,y,x+w,y+h),fill="#62BCEB")
    draw.rectangle((x,y+h*0.7,x+w,y+h),fill="#1B6FA8")
    draw.polygon([(x+120,y+h*0.68),(x+380,y+h*0.15),(x+415,y+h*0.19),(x+250,y+h*0.72)],fill="#253B52")
    draw.polygon([(x+w-120,y+h*0.68),(x+w-380,y+h*0.15),(x+w-415,y+h*0.19),(x+w-250,y+h*0.72)],fill="#253B52")
    draw.rectangle((x+30,y+h*0.64,x+250,y+h*0.78),fill="#263C55")
    draw.rectangle((x+w-250,y+h*0.64,x+w-30,y+h*0.78),fill="#263C55")
    draw.line((x,y+h*0.79,x+w,y+h*0.79),fill=WHITE,width=5)


def cta(draw, text, sub=None):
    rounded(draw,(45,H-205,W-45,H-45),36,BLUE)
    draw.ellipse((85,H-177,205,H-57),fill=WHITE)
    draw.arc((112,H-153,178,H-87),20,160,fill=BLUE,width=12)
    draw.text((250,H-154),text,font=font(52,bold=True,condensed=True),fill=WHITE)
    if sub:
        draw.text((252,H-92),sub,font=font(30),fill="#BFE7FF")


def panel_base(number:int):
    img=vertical_gradient()
    draw=ImageDraw.Draw(img)
    header(draw,number)
    return img,draw


def save(img: Image.Image, n: int):
    img.save(OUT_DIR/f"{n:02d}.jpg",quality=92,subsampling=0,optimize=True)


def make1():
    img,d=panel_base(1)
    y=title(d,65,200,[("ЗАЩИТА ТУРИСТА",BLUE),("В САНКТ-ПЕТЕРБУРГЕ",BLUE)],840,84)
    d.text((70,y+18),"ВОЗВРАТ ДЕНЕГ ЗА ТУР",font=font(50,bold=True,condensed=True),fill=INK)
    bullet_list(d,70,y+100,["Отказали в возврате денег?","Туроператор нарушил условия?","Нужна претензия или иск?"],770,38,18)
    rounded(d,(65,775,795,930),28,"#E8F3FC",BLUE,4)
    d.text((95,810),"ЮРИДИЧЕСКАЯ ПОМОЩЬ",font=font(40,bold=True,condensed=True),fill=BLUE)
    d.text((95,862),"ТУРИСТАМ ПО ВСЕЙ РОССИИ",font=font(34,bold=True,condensed=True),fill=INK)
    city_skyline(d,1050,920,1880,"#9ABBD3")
    dome_landmark(d,1010,690,0.85)
    person_lawyer(d,1415,300,1.25)
    suitcase(d,1250,820,240,320)
    cta(d,"ОСТАВЬТЕ ЗАЯВКУ", "Проведём первичный правовой анализ ситуации")
    save(img,1)


def make2():
    img,d=panel_base(2)
    title(d,70,205,[("КОГДА МЫ ПОМОЖЕМ?",BLUE)],1020,88)
    bullet_list(d,70,345,["Отказ в возврате денег за тур, авиабилеты или отель","Перенос или отмена поездки по вине туроператора","Навязанные дополнительные услуги","Некачественный отдых или размещение","Страховые случаи за рубежом"],950,38,22)
    plane_window(d,1250,240,540,640)
    suitcase(d,1360,835,280,370)
    rounded(d,(75,1080,1100,1260),30,"#EAF4FC",BLUE,4)
    d.text((110,1118),"РАЗБЕРЁМ ДОГОВОР И ДОКУМЕНТЫ",font=font(42,bold=True,condensed=True),fill=BLUE)
    d.text((110,1180),"Определим законный порядок действий",font=font(34),fill=INK)
    save(img,2)


def make3():
    img,d=panel_base(3)
    title(d,70,205,[("НАШИ ПРЕИМУЩЕСТВА",BLUE)],1050,86)
    bullet_list(d,70,350,["Практический опыт в туристических спорах","Работаем по договору и без скрытых условий","Подготовка претензий и судебных документов","Дистанционная помощь по всей России","Понятная стратегия без ложных гарантий"],900,37,24)
    city_skyline(d,1050,1030,1880,"#9BB9CE")
    statue(d,1300,350,1.15)
    rounded(d,(1040,920,1850,1125),30,WHITE,BLUE,4)
    d.text((1080,960),"ЗАЩИЩАЕМ ПРАВА ТУРИСТОВ",font=font(42,bold=True,condensed=True),fill=BLUE)
    d.text((1080,1020),"Досудебно и в суде",font=font(34),fill=INK)
    cta(d,"КОНСУЛЬТАЦИЯ ЮРИСТА", "Санкт-Петербург и вся Россия")
    save(img,3)


def make4():
    img,d=panel_base(4)
    title(d,70,205,[("КАК МЫ РАБОТАЕМ",BLUE)],1050,88)
    bullet_list(d,65,345,["Вы оставляете заявку или пишете в чат","Мы изучаем ситуацию и документы","Готовим претензию и расчёт требований","Направляем документы ответственному лицу","При необходимости сопровождаем дело в суде"],1000,36,18,True)
    rounded(d,(1180,250,1845,1195),45,"#E6F1FA",None,0)
    person_lawyer(d,1380,330,1.35,True)
    rounded(d,(1230,920,1800,1120),24,WHITE,BLUE,4)
    d.text((1270,960),"СВЯЗЬ С ЮРИСТОМ",font=font(42,bold=True,condensed=True),fill=BLUE)
    d.text((1270,1020),"на каждом этапе",font=font(36),fill=INK)
    save(img,4)


def make5():
    img,d=panel_base(5)
    title(d,70,205,[("ВЕРНЁМ ТО,",BLUE),("ЧТО ВАМ ПОЛОЖЕНО",BLUE)],950,84)
    bullet_list(d,70,440,["Стоимость тура","Авиабилеты","Проживание","Экскурсии и услуги","Неустойка, убытки и компенсация"],850,40,22)
    beach_scene(d,1050,255)
    rounded(d,(1030,930,1820,1125),30,WHITE,BLUE,4)
    d.text((1070,965),"ОЦЕНИМ ОБЪЁМ ТРЕБОВАНИЙ",font=font(42,bold=True,condensed=True),fill=BLUE)
    d.text((1070,1028),"с учётом документов и обстоятельств",font=font(31),fill=INK)
    cta(d,"НАПИШИТЕ В АВИТО", "Укажите дату поездки и стоимость тура")
    save(img,5)


def make6():
    img,d=panel_base(6)
    title(d,70,205,[("НЕ ОТКЛАДЫВАЙТЕ",BLUE),("ЗАЩИТУ СВОИХ ПРАВ",BLUE)],1030,80)
    d.text((75,415),"Сроки и доказательства имеют значение",font=font(45,bold=True,condensed=True),fill=INK)
    draw_wrapped(d,(75,490),"Сохраните договор, чеки, ваучер, переписку и документы о расходах. Чем раньше разобрать ситуацию, тем проще определить порядок действий.",font(36),MUTED,820,15)
    bridge_scene(d,1010,270,850,590)
    rounded(d,(70,790,850,1040),30,"#EAF4FC",BLUE,4)
    d.text((110,835),"ЧТО ПОДГОТОВИТЬ",font=font(42,bold=True,condensed=True),fill=BLUE)
    d.text((115,905),"• договор и чеки\n• переписку\n• фото и документы о расходах",font=font(34),fill=INK,spacing=16)
    cta(d,"ОСТАВЬТЕ ЗАЯВКУ", "Получите консультацию по туристическому спору")
    save(img,6)


if __name__ == "__main__":
    for fn in (make1,make2,make3,make4,make5,make6):
        fn()
    for i in range(1,7):
        p=OUT_DIR/f"{i:02d}.jpg"
        with Image.open(p) as im:
            assert im.size == (W,H)
            assert im.format == "JPEG"
        print(p, p.stat().st_size)
