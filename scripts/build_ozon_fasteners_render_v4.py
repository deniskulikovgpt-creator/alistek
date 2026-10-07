from PIL import Image, ImageEnhance
from pathlib import Path
import base64, json

ROOT = Path("ozon/rich-content/fasteners-10-9-render-v4")
ROOT.mkdir(parents=True, exist_ok=True)

source_b64 = (ROOT / "source_render.b64").read_text(encoding="utf-8")
source_bytes = base64.b64decode("".join(source_b64.split()))
source_path = ROOT / "_source_render.jpg"
source_path.write_bytes(source_bytes)

src = Image.open(source_path).convert("RGB")

# Exact crop coordinates from the approved 941x1672 render.
boxes = {
    1:(10,8,463,266),
    2:(474,8,930,266),
    3:(10,276,463,534),
    4:(474,276,930,534),
    5:(10,543,463,790),
    6:(474,543,930,790),
    7:(10,802,463,1043),
    8:(474,802,930,1043),
    9:(10,1050,463,1274),
    10:(474,1050,930,1274),
    11:(10,1281,463,1505),
    12:(474,1281,930,1505),
    13:(10,1515,930,1665),
}

slide_paths = []
for i in range(1, 14):
    crop = src.crop(boxes[i])
    slide = crop.resize((1440, 720), Image.Resampling.LANCZOS)
    slide = ImageEnhance.Sharpness(slide).enhance(1.40)
    slide = ImageEnhance.Contrast(slide).enhance(1.03)
    p = ROOT / f"slide_{i:02d}.jpg"
    slide.save(p, "JPEG", quality=88, subsampling=0, optimize=True)
    slide_paths.append(p)

# Preview contact sheet: 2 columns, final slide full width.
thumb_w, thumb_h, gap = 720, 360, 16
sheet_w = thumb_w * 2 + gap * 3
sheet_h = thumb_h * 7 + gap * 8
sheet = Image.new("RGB", (sheet_w, sheet_h), (238, 240, 244))
for i in range(12):
    thumb = Image.open(slide_paths[i]).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    col, row = i % 2, i // 2
    x = gap + col * (thumb_w + gap)
    y = gap + row * (thumb_h + gap)
    sheet.paste(thumb, (x, y))
last = Image.open(slide_paths[12]).resize((thumb_w * 2 + gap, thumb_h), Image.Resampling.LANCZOS)
sheet.paste(last, (gap, gap + 6 * (thumb_h + gap)))
sheet.save(ROOT / "preview.jpg", "JPEG", quality=90, optimize=True)

base = "https://raw.githubusercontent.com/deniskulikovgpt-creator/alistek/main/ozon/rich-content/fasteners-10-9-render-v4"
alts = [
    "Высокопрочный крепёж 10.9 — болты, винты и гайки",
    "Преимущества высокопрочного крепежа",
    "Ассортимент высокопрочного крепежа",
    "Класс прочности 10.9 для ответственных соединений",
    "Точная резьба и геометрия крепежа",
    "Надёжная фиксация резьбового соединения",
    "Материал и защитное покрытие крепежа",
    "Сферы применения высокопрочного крепежа",
    "Как подобрать крепёж",
    "Размеры и маркировка крепежа",
    "Комплектация и упаковка крепежа",
    "Рекомендации по монтажу крепежа",
    "Надёжный крепёж для ответственных соединений",
]

blocks = []
for i in range(1, 14):
    url = f"{base}/slide_{i:02d}.jpg"
    blocks.append({
        "imgLink": "",
        "img": {
            "src": url,
            "srcMobile": url,
            "alt": alts[i-1],
            "position": "width_full",
            "positionMobile": "width_full",
            "widthMobile": 1440,
            "heightMobile": 720
        }
    })

description = [
    "Высокопрочный крепёж для ответственных резьбовых соединений: болты и винты класса прочности 10.9, а также совместимые гайки класса 10.",
    "В ассортименте серии представлены болты с шестигранной головкой, винты с внутренним шестигранником и шестигранные гайки. Для отдельных позиций используются стандарты DIN 933, DIN 931, DIN 912 и DIN 934 — точный стандарт, размер и покрытие проверяйте в характеристиках конкретного товара.",
    "Класс прочности 10.9 относится к болтам и винтам и применяется в соединениях с повышенными требованиями к прочности. Для комплектации таких соединений используются гайки соответствующего класса, например класса 10.",
    "Крепёж подходит для машиностроения, металлоконструкций, монтажа оборудования, производства, ремонта и сервисных работ. Для оцинкованных позиций защитное покрытие помогает снизить воздействие внешней среды на поверхность металла.",
    "Перед заказом проверьте диаметр резьбы M, длину, шаг резьбы, стандарт DIN/ISO, тип головки, покрытие и количество в упаковке. При монтаже соблюдайте требования проекта и технической документации к инструменту и моменту затяжки."
]

items = []
for idx, paragraph in enumerate(description):
    items.append({"type": "text", "content": paragraph})
    if idx != len(description) - 1:
        items.extend([{"type":"br"},{"type":"br"}])

rich = {
    "content": [
        {
            "widgetName": "raShowcase",
            "type": "roll",
            "blocks": blocks
        },
        {
            "widgetName": "raTextBlock",
            "title": {
                "items": [],
                "size": "size1",
                "color": "color1",
                "align": "center"
            },
            "theme": "secondary",
            "padding": "type2",
            "gapSize": "s",
            "text": {
                "size": "size3",
                "align": "center",
                "color": "color1",
                "items": items
            }
        }
    ],
    "version": 0.3
}

payload = json.dumps(rich, ensure_ascii=False, indent=2)
(ROOT / "richcontent_10_9_ozon.json").write_text(payload, encoding="utf-8")
(ROOT / "richcontent_10_9_ozon.txt").write_text(payload, encoding="utf-8")
print("Generated 13 slides, preview, JSON and TXT.")

# workflow trigger
