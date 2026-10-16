"""Render the capability heatmap with the Python standard library."""

from html import escape
from pathlib import Path

GROUPS = [
    ("01  Продажи", [("Чек и возврат", "Магазин", "p"), ("Приём оплаты", "Магазин", "p"), ("Печать ценников", "Магазин", "n"), ("Смена и инкассация", "Магазин / HQ", "n")]),
    ("02  Маркетинг", [("Управление акциями", "HQ: Promo Engine", "n"), ("Лояльность", "HQ / магазин", "p"), ("Работа с покупателями", "HQ / магазин", "n")]),
    ("03  Ассортимент и закупки", [("Единый каталог SKU", "HQ / магазин", "p"), ("Цены и поставщики", "HQ", "n"), ("Заказы поставщикам", "HQ", "n")]),
    ("04  Логистика", [("Приёмка товара", "Магазин", "n"), ("Остатки и инвентаризация", "Магазин / HQ", "p"), ("Пополнение магазинов", "HQ", "n"), ("Click & Collect", "Smart Fulfillment", "u")]),
    ("05  Люди и финансы", [("Кадры и премии", "HQ / магазин", "p"), ("Бухгалтерский учёт", "HQ: SAP", "n"), ("Расчёты с поставщиками", "HQ: SAP", "n")]),
    ("06  Развитие сети", [("Обследование точки", "M&A / Store Ops", "n"), ("Перенос и сверка SKU", "Data Integration", "p"), ("Настройка и открытие", "Store Ops / магазин", "p")]),
    ("07  ИТ и контроль", [("Поддержка касс и серверов", "Store Ops", "p"), ("Управление устройствами", "Store Ops", "p"), ("Доступы и аудит", "ИТ HQ", "n"), ("Резервное копирование", "ИТ HQ", "n")]),
]


def render():
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="1040" viewBox="0 0 1480 1040">',
         '<rect width="1480" height="1040" fill="#f7f9fc"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#172b4d}.title{font-size:28px;font-weight:bold}.h{font-size:18px;font-weight:bold}.body{font-size:16px}.small{font-size:14px;fill:#42526e}</style>',
         '<text x="35" y="45" class="title">VitaStore · карта бизнес-возможностей L1 / L2</text>',
         '<text x="35" y="77" class="body">П — проблемная или дорогая зона   ·   У — уникальное преимущество   ·   Серый — остальные функции</text>']
    colors = {"p": ("#fff0ee", "#c9372c", "П"), "u": ("#dcfff1", "#216e4e", "У"), "n": ("#f1f3f5", "#b3bac5", "")}
    for i, (title, items) in enumerate(GROUPS):
        x, y = 35 + (i % 4) * 360, 110 + (i // 4) * 450
        s += [f'<rect x="{x}" y="{y}" width="335" height="420" rx="12" fill="white" stroke="#dfe1e6"/>', f'<text x="{x+16}" y="{y+32}" class="h">{escape(title)}</text>']
        for j, (name, owner, state) in enumerate(items):
            yy = y + 55 + j * 85
            fill, stroke, mark = colors[state]
            s += [f'<rect x="{x+12}" y="{yy}" width="311" height="72" rx="7" fill="{fill}" stroke="{stroke}"/>', f'<text x="{x+24}" y="{yy+27}" class="body">{escape(name)}</text>', f'<text x="{x+24}" y="{yy+52}" class="small">{escape(owner)}</text>', f'<text x="{x+295}" y="{yy+52}" class="h">{mark}</text>']
    s += ['<text x="1115" y="600" class="h">Где искать решение</text>', '<text x="1115" y="635" class="body">Task1: Buy vs Build</text>', '<text x="1115" y="665" class="body">Task2: подключение точки</text>', '<text x="1115" y="695" class="body">Task3: архитектура</text>', '<text x="1115" y="725" class="body">Task4: стоимость владения</text>', '<text x="35" y="1020" class="small">Источник: docs/context.md и docs/task1.md. Дополнения базовых функций розницы пояснены в README.</text>', '</svg>']
    Path(__file__).with_name("capabilities.svg").write_text("\n".join(s))


if __name__ == "__main__":
    render()
