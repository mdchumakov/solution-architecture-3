"""Rebuild the reviewable TCO tables from explicit case-study assumptions."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def money(value):
    return f"{value / 1_000_000:.2f}".replace(".", ",")


def calculate(data):
    n, years = data["stores"], data["years"]
    a, b = data["as_is"], data["to_be"]
    rows = [
        ("Оборудование, разово (CapEx)", n * a["replacement_per_store"], n * b["equipment_per_store"], False),
        ("Лицензии / Cloud POS и MDM (OpEx)", n * 12 * a["license_month_per_store"], n * 12 * b["saas_month_per_store"], True),
        ("ФОТ поддержки (OpEx)", a["support_fte"] * a["fte_year"], b["support_fte"] * b["fte_year"], True),
        ("Каналы связи (OpEx)", n * 12 * a["network_month_per_store"], n * 12 * b["network_month_per_store"], True),
        ("Ремонт и обслуживание (OpEx)", n * a["maintenance_year_per_store"], n * b["maintenance_year_per_store"], True),
        ("Выезды и командировки (OpEx)", n * a["visits_year_per_store"], 0, True),
        ("Облако и ИИ, доля 100 магазинов (OpEx)", 0, b["cloud_year"], True),
        ("HAL и шлюз, фиксированная плата (OpEx)", 0, n * b["hal_year_per_store"], True),
        ("Разработка и интеграция, разово", 0, b["integration_once"], False),
        ("Обучение и перенос, разово", 0, b["training_once"], False),
        ("Параллельная работа и резерв перехода, разово", 0, b["parallel_once"], False),
    ]
    annual_a = sum(a for _, a, _, recurring in rows if recurring)
    annual_b = sum(b for _, _, b, recurring in rows if recurring)
    upfront_a = sum(a for _, a, _, recurring in rows if not recurring)
    upfront_b = sum(b for _, _, b, recurring in rows if not recurring)
    total_a = upfront_a + years * annual_a
    total_b = upfront_b + years * annual_b
    return rows, annual_a, annual_b, upfront_a, upfront_b, total_a, total_b


def report(data):
    rows, aa, ab, ua, ub, ta, tb = calculate(data)
    years = data["years"]
    if years != 3 or data["stores"] <= 0:
        raise ValueError("This assignment requires three years and a positive store count")
    savings = aa - ab
    net = ub - ua
    payback = f"{12 * net / savings:.2f}" if savings > 0 and net > 0 else "не применимо"
    lines = ["# Расчёт TCO", "", "Сгенерировано из `assumptions.json`. Суммы в млн ₽, без НДС, в постоянных ценах.", "",
             "| Статья | AS-IS год 1 | Год 2 | Год 3 | TO-BE год 1 | Год 2 | Год 3 |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    totals = [0] * 6
    for label, a, b, recurring in rows:
        values = [a, a if recurring else 0, a if recurring else 0, b, b if recurring else 0, b if recurring else 0]
        totals = [x + y for x, y in zip(totals, values)]
        lines.append("| " + label + " | " + " | ".join(map(money, values)) + " |")
    lines.append("| **Итого** | " + " | ".join(money(v) for v in totals) + " |")
    lines += ["", f"TCO за три года: AS-IS **{money(ta)} млн ₽**, TO-BE **{money(tb)} млн ₽**.", "",
              f"Экономия: **{money(ta - tb)} млн ₽ ({100 * (ta - tb) / ta:.2f}%)**.", "",
              f"Ежегодные расходы: {money(aa)} → {money(ab)} млн ₽; снижение {100 * savings / aa:.2f}%.", "",
              f"ROI на дополнительные вложения: ({money(years * savings)} − {money(net)}) / {money(net)} = **{100 * (ta - tb) / net:.2f}%**.", "",
              f"Простой срок окупаемости: {money(net)} / ({money(savings)} / 12) = **{payback} месяца**.", "",
              "## Денежный поток относительно AS-IS", "",
              "| Период | Изменение потока, млн ₽ | Накопленный эффект, млн ₽ |",
              "| --- | ---: | ---: |", f"| Старт | {money(-net)} | {money(-net)} |"]
    for year in range(1, years + 1):
        lines.append(f"| Год {year} | {money(savings)} | {money(-net + year * savings)} |")
    extra_support = (5 - data["to_be"]["support_fte"]) * data["to_be"]["fte_year"]
    extra_saas = 0.3 * data["stores"] * 12 * data["to_be"]["saas_month_per_store"]
    scenarios = [
        ("Базовый", ta, tb),
        ("Старое оборудование не требует замены", ta - ua, tb),
        ("Экономия начинается на 6 месяцев позже", ta, tb + savings / 2),
        ("SaaS +30%, поддержка TO-BE 5 FTE", ta, tb + years * (extra_saas + extra_support)),
    ]
    lines += ["", "## Чувствительность", "", "| Условие | AS-IS | TO-BE | Экономия | Снижение TCO |",
              "| --- | ---: | ---: | ---: | ---: |"]
    for label, a, b in scenarios:
        lines.append(f"| {label} | {money(a)} | {money(b)} | {money(a-b)} | {100*(a-b)/a:.2f}% |")
    lines += ["", f"Запас дополнительных расходов до границы экономии 40%: **{money(0.6 * ta - tb)} млн ₽** за три года.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare saved tables with recalculated results")
    args = parser.parse_args()
    data = json.loads((ROOT / "assumptions.json").read_text())
    result = report(data)
    target = ROOT / "calculation.md"
    if args.check:
        if target.read_text() != result:
            raise SystemExit("TCO table is stale; run python3 Task4/calculate.py")
        print("TCO table matches the assumptions and formulas")
    else:
        target.write_text(result)
        print(f"Updated {target}")
