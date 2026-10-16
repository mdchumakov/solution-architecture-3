"""Editable, dependency-free SVG sources for the two architecture views."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class Diagram:
    def __init__(self, title, subtitle, width, height):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                      '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8" fill="#42526e"/></marker></defs>',
                      f'<rect width="{width}" height="{height}" fill="white"/>',
                      '<style>text{font-family:Arial,sans-serif;fill:#172b4d}.title{font-size:27px;font-weight:bold}.sub{font-size:16px}.box{font-size:17px}.label{font-size:14px;paint-order:stroke;stroke:white;stroke-width:5px;stroke-linejoin:round}.group{font-size:19px;font-weight:bold}</style>']
        self.text(30, 40, title, "title")
        self.text(30, 70, subtitle, "sub")

    def text(self, x, y, label, cls="box", anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(label)}</text>')

    def group(self, x, y, w, h, label):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#f7f9fc" stroke="#7a869a" stroke-dasharray="7 5"/>')
        self.text(x+16, y+30, label, "group")

    def box(self, x, y, w, h, lines, color="#deebff"):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{color}" stroke="#526581" stroke-width="1.5"/>')
        for i, line in enumerate(lines):
            self.text(x+w/2, y+(h-(len(lines)-1)*23)/2+5+i*23, line, anchor="middle")

    def edge(self, points, label, lx, ly, dashed=False):
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        p = " ".join(f"{x},{y}" for x, y in points)
        self.parts.append(f'<polyline points="{p}" fill="none" stroke="#42526e" stroke-width="1.7" marker-end="url(#arrow)"{dash}/>')
        for i, line in enumerate(label.split("\n")):
            self.text(lx, ly+i*18, line, "label")

    def save(self, name):
        (ROOT / name).write_text("\n".join(self.parts + ["</svg>"]))


def as_is():
    d = Diagram("VitaStore · AS-IS · C4 Container", "Система в фокусе: касса и бэк-офис магазина. Внешние зависимости показаны серым.", 1500, 1000)
    d.group(70, 300, 830, 400, "Система кассы и бэк-офиса · магазин")
    d.box(120, 400, 300, 150, ["POS и бэк-офис", "[Container: Windows / C#]", "Продажи, цены, драйверы"])
    d.box(550, 400, 300, 150, ["Локальная БД", "[Container: SQL Server /", "PostgreSQL, зависит от точки]", "Справочники и чеки"])
    d.box(120, 150, 300, 85, ["Кассир", "[Person]"], "#eaecef")
    d.box(1060, 400, 340, 150, ["SAP ERP · HQ on-premises", "[External software system]", "Товары, цены, кадры, финансы"], "#eaecef")
    d.box(550, 150, 300, 100, ["Excel товароведа HQ", "[External application]", "Ручное сопоставление SKU"], "#eaecef")
    d.box(1060, 150, 340, 100, ["Сервис лояльности", "[External system]", "Владелец и протокол неясны"], "#eaecef")
    d.box(120, 805, 300, 110, ["Фискальный регистратор", "[External device]", "Локальная печать чека"], "#eaecef")
    d.box(550, 805, 300, 110, ["Банковский терминал", "[External device]", "Разные модели и протоколы"], "#eaecef")
    d.edge([(270,235),(270,400)], "Работает через UI", 285,280)
    d.edge([(420,475),(550,475)], "Чтение / запись\nSQL",435,440)
    d.edge([(1060,510),(950,510),(950,640),(700,640),(700,550)], "XML по FTP, 02:00\nПрайс-листы из регламента", 965,580)
    d.edge([(700,400),(700,250)], "Инженер: CSV/XLS\nзатем email",710,310)
    d.edge([(850,200),(970,200),(970,430),(1060,430)], "Согласованный файл\nручной импорт",975,300)
    d.edge([(420,420),(470,420),(470,110),(1230,110),(1230,150)], "Онлайн-запрос лояльности; связь подтверждена INC-8402, протокол неизвестен",500,102,True)
    d.edge([(270,550),(270,805)], "COM / драйвер в POS",285,755)
    d.edge([(370,550),(370,740),(700,740),(700,805)], "USB / драйвер в POS",500,730)
    d.text(30,965,"Пунктирная связь: зависимость известна, детали требуют обследования. Обратный канал продаж в SAP не подтверждён.","sub")
    d.save("as-is.svg")


def to_be():
    d = Diagram("VitaStore · TO-BE · High-Level Design", "Отдельного сервера в магазине нет. Офлайн-данные и доступ к USB/COM остаются на планшете.", 1740, 1350)
    d.group(30,110,490,1020,"Магазин / Edge")
    d.group(575,110,690,1020,"Облако · SaaS / PaaS")
    d.group(1320,110,390,1020,"HQ и внешние участники")
    d.box(85,175,380,110,["Лёгкое приложение POS", "Планшет: UI и офлайн-продажа", "Кассир работает в приложении"])
    d.box(85,375,380,110,["Локальное хранилище", "Каталог, правила, журнал продаж", "Защищённый диск планшета"])
    d.box(85,575,380,110,["HAL / локальный агент", "Готовый SDK и адаптеры", "Единый интерфейс устройств"],"#fff0b3")
    d.box(60,835,205,110,["Регистратор", "Фискальный чек"],"#eaecef")
    d.box(295,835,205,110,["Терминал", "Банковская оплата"],"#eaecef")
    d.box(635,175,570,110,["Cloud POS + лояльность [SaaS]", "Онлайн-продажи, каталог и журнал", "Применяет правила Promo Engine"])
    d.box(635,385,270,110,["Интеграционный", "сервис [PaaS]", "Очередь и дедупликация"])
    d.box(950,385,255,110,["Promo Engine", "Собственный код", "PaaS"])
    d.box(635,600,270,110,["Подключение магазина", "PaaS: процесс и проверка", "БД + файлы + ИИ API"])
    d.box(950,600,255,110,["Smart Fulfillment", "Собственный код", "PaaS + managed DB"],"#dcfff1")
    d.box(635,835,270,110,["Payment Gateway", "Шлюз провайдера", "Онлайн-статусы"])
    d.box(950,835,255,110,["MDM / наблюдение", "Настройки, обновления", "Резервы и уведомления"])
    d.box(1360,385,310,110,["SAP ERP [on-premises]", "Эталон SKU и цен", "Учёт товаров и финансов"],"#eaecef")
    d.box(1360,600,310,110,["Товаровед HQ", "Проверяет исключения", "в кабинете подключения"],"#eaecef")
    d.box(1360,835,310,110,["Эквайер", "Платёжные статусы", "Онлайн-авторизация"],"#eaecef")
    d.edge([(465,215),(635,215)],"Продажи ↑\nHTTPS; ACK",480,180)
    d.edge([(635,260),(465,260)],"Каталог ↓",490,282)
    d.edge([(275,285),(275,375)],"Чтение / запись",290,335)
    d.edge([(85,230),(52,230),(52,630),(85,630)],"",0,0)
    d.text(65,530,"Локальный IPC: печать / оплата","label")
    d.edge([(200,685),(200,835)],"USB / COM",80,775)
    d.edge([(370,685),(370,835)],"Адаптер / USB",380,775)
    d.edge([(770,285),(770,385)],"События продаж",785,335)
    d.edge([(905,450),(925,450),(925,525),(1300,525),(1300,450),(1360,450)],"SAP API через защищённый канал",1010,515)
    d.edge([(1077,385),(1077,285)],"Правила акций",1090,335)
    d.edge([(770,600),(770,495)],"SKU и подтверждение ERP",640,555)
    d.edge([(1360,655),(1300,655),(1300,750),(925,750),(925,655),(905,655)],"Проверка SKU через HTTPS",1000,740)
    d.edge([(1077,600),(1077,560),(840,560),(840,495)],"Заказы / остатки",1100,580)
    d.edge([(500,890),(635,890)],"Онлайн",535,875)
    d.edge([(905,910),(925,910),(925,1010),(1300,1010),(1300,890),(1360,890)],"HTTPS / статусы провайдера",1000,1035)
    d.text(60,1030,"HAL печатает без облака.","sub")
    d.text(60,1060,"Платёж требует ответа эквайера.","sub")
    d.text(635,1090,"MDM управляет планшетами; мониторинг следит за очередями.","sub")
    d.text(30,1190,"Поток подключения: файл магазина → платформа → ИИ и товаровед → SAP → каталог POS. Подробности: Task2.","sub")
    d.text(30,1225,"У каждой продажи свой ID. Повторная доставка не создаёт новый чек или проводку. Правила конфликтов: README.","sub")
    d.text(30,1260,"Жёлтый — локальный HAL; зелёный — собственное преимущество; серый — HQ и внешние устройства / участники.","sub")
    d.text(30,1295,"Стрелки показывают основные обращения и сообщения. Ответы, служебные API и резервные соединения опущены.","sub")
    d.save("to-be.svg")


if __name__ == "__main__":
    as_is()
    to_be()
