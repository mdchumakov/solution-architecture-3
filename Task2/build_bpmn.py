"""Create the descriptive BPMN collaboration and its diagram interchange data."""

from pathlib import Path
import xml.etree.ElementTree as E

NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}
for prefix, uri in NS.items():
    E.register_namespace(prefix, uri)


def el(parent, tag, **attrs):
    prefix, name = tag.split(":")
    return E.SubElement(parent, f"{{{NS[prefix]}}}{name}", {k: str(v) for k, v in attrs.items()})


root = E.Element(f"{{{NS['bpmn']}}}definitions", {"id": "Definitions_VitaStore", "targetNamespace": "https://vitastore.example/onboarding"})
collab = el(root, "bpmn:collaboration", id="Collaboration")
diagram = None
processes, nodes, flows, bounds = {}, {}, [], {}
pools = [
    ("Store", "Магазин · сотрудник / Store Ops", 80, 270),
    ("Platform", "Платформа подключения · автоматизация", 410, 470),
    ("Human", "Товаровед HQ · человек", 940, 210),
    ("AI", "ИИ-сервис · кандидаты SKU", 1210, 180),
    ("ERP", "SAP ERP · каталог и импорт", 1450, 260),
]
for ident, name, y, h in pools:
    processes[ident] = el(root, "bpmn:process", id="Process_"+ident, isExecutable="false")
    el(collab, "bpmn:participant", id="Pool_"+ident, name=name, processRef="Process_"+ident)
    bounds["Pool_"+ident] = (40, y, 3020, h)


def node(pool, ident, kind, name, x, y, w=140, h=80, message=False):
    if kind.endswith("Event"):
        w = h = 36
    if "Gateway" in kind:
        w = h = 50
    elem = el(processes[pool], "bpmn:"+kind, id=ident, name=name)
    if message:
        el(elem, "bpmn:messageEventDefinition", id=ident+"_message")
    nodes[ident] = (pool, elem)
    bounds[ident] = (x,y,w,h)
    return ident


def flow(ident, source, target, points, name="", message=False, label=None):
    tag = "messageFlow" if message else "sequenceFlow"
    parent = collab if message else processes[nodes[source][0]]
    attrs = {"id": ident, "sourceRef": source, "targetRef": target}
    if name:
        attrs["name"] = name
    el(parent, "bpmn:"+tag, **attrs)
    flows.append((ident, points, label))


# Store: corrected uploads start a new platform instance with a new file version.
node("Store","s_start","startEvent","Точка готова",110,165)
node("Store","s_upload","userTask","Загрузить CSV/XLS",200,145)
node("Store","s_wait","eventBasedGateway","Ожидать ответ",400,160)
node("Store","s_error","intermediateCatchEvent","Ошибки файла",540,260,message=True)
node("Store","s_fix","userTask","Исправить файл",200,250)
node("Store","s_config","intermediateCatchEvent","Пакет настроек",2440,165,message=True)
node("Store","s_test","userTask","Загрузить пакет; проверить кассу",2520,145)
node("Store","s_ok","exclusiveGateway","Проверка пройдена?",2730,160)
node("Store","s_repair","userTask","Устранить сбой",2520,250)
node("Store","s_send","sendTask","Подтвердить открытие",2820,145)
node("Store","s_end","endEvent","Открыт",2990,165)

# Platform: validation, human approval, ERP acknowledgement, store readiness.
node("Platform","p_start","startEvent","Файл получен",210,490,message=True)
node("Platform","p_validate","serviceTask","Проверить формат и дубли",300,470)
node("Platform","p_valid","exclusiveGateway","Файл корректен?",500,485)
node("Platform","p_error","sendTask","Вернуть ошибки",460,710)
node("Platform","p_badend","endEvent","Загрузка отклонена",660,732)
node("Platform","p_catalog","serviceTask","Запросить каталог ERP",650,470)
node("Platform","p_match","serviceTask","Получить кандидатов ИИ",870,470)
node("Platform","p_rules","businessRuleTask","Применить пороги и правила",1090,470)
node("Platform","p_review","sendTask","Передать исключения и выборку",1310,470)
node("Platform","p_answer","receiveTask","Получить решение товароведа",1520,470)
node("Platform","p_approved","exclusiveGateway","Пакет принят?",1720,485)
node("Platform","p_import","serviceTask","Импортировать в ERP; получить статус",1820,470)
node("Platform","p_imported","exclusiveGateway","ERP приняла?",2040,485)
node("Platform","p_rework","serviceTask","Сохранить исправления; обновить пакет",1530,710)
node("Platform","p_publish","sendTask","Отправить пакет на кассу",2190,470)
node("Platform","p_ready","receiveTask","Получить акт проверки",2780,470)
node("Platform","p_end","endEvent","Подключение завершено",2980,492)

node("Human","h_start","startEvent","Пакет на проверку",1320,1020,message=True)
node("Human","h_review","userTask","Проверить исключения и выборку",1410,995)
node("Human","h_send","sendTask","Вернуть решение и исправления",1630,995)
node("Human","h_end","endEvent","Решение отправлено",1820,1020)

node("AI","a_start","startEvent","Запрос",810,1280,message=True)
node("AI","a_match","serviceTask","Сопоставить с каталогом",910,1255)
node("AI","a_send","sendTask","Вернуть кандидатов и оценки",1110,1255)
node("AI","a_end","endEvent","Ответ",1310,1280)

node("ERP","e_startcat","startEvent","Запрос каталога",620,1530,message=True)
node("ERP","e_cat","sendTask","Вернуть версию каталога",710,1505)
node("ERP","e_endcat","endEvent","Каталог выдан",910,1530)
node("ERP","e_startimp","startEvent","Пакет соответствий",1800,1530,message=True)
node("ERP","e_import","serviceTask","Проверить версию; импорт по batch_id",1890,1505)
node("ERP","e_reply","sendTask","Статус + цены либо ошибки",2100,1505)
node("ERP","e_endimp","endEvent","Ответ ERP",2300,1530)


def direct(ident, source, target, name=""):
    x,y,w,h = bounds[source]
    xx,yy,ww,hh = bounds[target]
    flow(ident,source,target,[(x+w,y+h/2),(xx,yy+hh/2)],name)


for i, (a,b) in enumerate([
    ("s_start","s_upload"),("s_upload","s_wait"),("s_config","s_test"),("s_test","s_ok"),("s_send","s_end"),
    ("p_start","p_validate"),("p_validate","p_valid"),("p_catalog","p_match"),("p_match","p_rules"),("p_rules","p_review"),("p_review","p_answer"),("p_answer","p_approved"),("p_import","p_imported"),("p_publish","p_ready"),("p_ready","p_end"),
    ("h_start","h_review"),("h_review","h_send"),("h_send","h_end"),
    ("a_start","a_match"),("a_match","a_send"),("a_send","a_end"),
    ("e_startcat","e_cat"),("e_cat","e_endcat"),("e_startimp","e_import"),("e_import","e_reply"),("e_reply","e_endimp"),
]):
    direct("f_"+str(i),a,b)
flow("s_wait_error","s_wait","s_error",[(425,210),(425,278),(540,278)])
flow("s_fix_flow","s_error","s_fix",[(540,278),(340,290)])
flow("s_retry","s_fix","s_upload",[(270,250),(270,225)])
flow("s_wait_config","s_wait","s_config",[(450,185),(2440,183)])
flow("s_pass","s_ok","s_send",[(2780,185),(2820,185)],"Да",label=(2780,160,40,20))
flow("s_fail","s_ok","s_repair",[(2755,210),(2755,290),(2660,290)],"Нет",label=(2690,265,40,20))
flow("s_retest","s_repair","s_test",[(2590,250),(2590,225)])
flow("p_invalid","p_valid","p_error",[(525,535),(525,710)],"Нет",label=(530,595,40,20))
direct("p_error_end","p_error","p_badend")
flow("p_valid_yes","p_valid","p_catalog",[(550,510),(650,510)],"Да",label=(580,485,40,20))
flow("p_approved_yes","p_approved","p_import",[(1770,510),(1820,510)],"Да",label=(1780,485,40,20))
flow("p_approved_no","p_approved","p_rework",[(1745,535),(1745,750),(1670,750)],"Нет",label=(1750,610,40,20))
flow("p_import_yes","p_imported","p_publish",[(2090,510),(2190,510)],"Да",label=(2120,485,40,20))
flow("p_import_no","p_imported","p_rework",[(2065,535),(2065,820),(1600,820),(1600,790)],"Нет",label=(2070,620,40,20))
flow("p_again","p_rework","p_catalog",[(1530,750),(1450,750),(1450,855),(720,855),(720,550)])

messages = [
    ("m_upload","s_upload","p_start",[(270,225),(270,380),(228,380),(228,490)],"CSV/XLS + store_id",(280,355,150,25)),
    ("m_error","p_error","s_error",[(460,750),(390,750),(390,370),(558,370),(558,296)],"Список ошибок",(400,380,120,25)),
    ("m_catreq","p_catalog","e_startcat",[(670,550),(670,910),(610,910),(610,1548),(620,1548)],"Запрос эталонных SKU",(435,1180,165,25)),
    ("m_catresp","e_cat","p_catalog",[(780,1505),(780,900),(750,900),(750,550)],"Каталог + версия",(790,1140,150,25)),
    ("m_matchreq","p_match","a_start",[(900,550),(900,920),(828,920),(828,1280)],"Исходные SKU + каталог",(845,950,180,25)),
    ("m_matchresp","a_send","p_match",[(1180,1255),(1180,900),(970,900),(970,550)],"Кандидаты + оценки",(1000,1180,160,25)),
    ("m_review","p_review","h_start",[(1350,550),(1350,890),(1338,890),(1338,1020)],"Исключения + выборка",(1160,920,160,25)),
    ("m_decision","h_send","p_answer",[(1700,995),(1700,900),(1560,900),(1560,790),(1500,790),(1500,590),(1590,590),(1590,550)],"Принять / исправить",(1730,920,160,25)),
    ("m_import","p_import","e_startimp",[(1860,550),(1860,910),(1900,910),(1900,1410),(1818,1410),(1818,1530)],"Связи SKU + batch_id + версия",(1910,1190,230,25)),
    ("m_importresp","e_reply","p_import",[(2170,1505),(2170,900),(1920,900),(1920,550)],"Статус ERP + пакет цен / ошибки",(2200,1190,250,25)),
    ("m_settings","p_publish","s_config",[(2260,470),(2260,380),(2458,380),(2458,201)],"Каталог + настройки",(2265,355,165,25)),
    ("m_open","s_send","p_ready",[(2890,225),(2890,380),(2850,380),(2850,470)],"Акт проверки",(2900,355,120,25)),
]
for ident,a,b,points,label,position in messages:
    flow(ident,a,b,points,label,True,position)

# Standard BPMN DI allows the file to open without auto-layout.
diagram = el(root,"bpmndi:BPMNDiagram",id="Diagram")
plane = el(diagram,"bpmndi:BPMNPlane",id="Plane",bpmnElement="Collaboration")
for ident,(x,y,w,h) in bounds.items():
    attrs = {"id": ident+"_di", "bpmnElement": ident}
    if ident.startswith("Pool_"):
        attrs["isHorizontal"] = "true"
    shape = el(plane,"bpmndi:BPMNShape",**attrs)
    el(shape,"dc:Bounds",x=x,y=y,width=w,height=h)
    if ident in nodes:
        tag = nodes[ident][1].tag.split("}")[-1]
        if tag.endswith("Event") or "Gateway" in tag:
            label = el(shape,"bpmndi:BPMNLabel")
            el(label,"dc:Bounds",x=x-40,y=y+h+5,width=w+80,height=42)
for ident,points,label in flows:
    edge=el(plane,"bpmndi:BPMNEdge",id=ident+"_di",bpmnElement=ident)
    for x,y in points:
        el(edge,"di:waypoint",x=x,y=y)
    if label:
        lab=el(edge,"bpmndi:BPMNLabel")
        x,y,w,h=label
        el(lab,"dc:Bounds",x=x,y=y,width=w,height=h)
E.indent(root)
E.ElementTree(root).write(Path(__file__).with_name("onboarding.bpmn"),encoding="utf-8",xml_declaration=True)
