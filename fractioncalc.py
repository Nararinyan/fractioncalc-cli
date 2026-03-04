#!/usr/bin/env python3
"""
fractioncalc.py — CLI Fraction Calculator
Inspired by Ashyraffa32/FractionCalc
"""

from fractions import Fraction
import sys
import os

# ── ANSI colors ──────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
DIM    = "\033[2m"
BLUE   = "\033[94m"

def c(text, color):
    return f"{color}{text}{RESET}"

def clear():
    os.system("clear")

# ── Helpers ───────────────────────────────────────────────────
def parse_fraction(s: str) -> Fraction:
    """Parse '3/4', '0.75', or '3' into a Fraction."""
    s = s.strip()
    if '/' in s:
        num, den = s.split('/', 1)
        return Fraction(int(num.strip()), int(den.strip()))
    return Fraction(s)

def fmt(f: Fraction) -> str:
    """Format a Fraction nicely."""
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"

def fmt_result(f: Fraction) -> str:
    decimal = float(f)
    return f"{c(fmt(f), GREEN)}  {c(f'({decimal:.6g})', DIM)}"

# ── Input helpers ─────────────────────────────────────────────
def ask_fraction(label: str) -> Fraction:
    while True:
        raw = input(f"  {c(label, CYAN)}: ").strip()
        if not raw:
            continue
        try:
            return parse_fraction(raw)
        except (ValueError, ZeroDivisionError):
            print(c("  ✗ Format tidak valid. Contoh: 3/4 atau 0.75 atau 5", RED))

def ask_operator() -> str:
    ops = {'+': 'tambah', '-': 'kurang', '*': 'kali', '/': 'bagi'}
    print(f"  Operator: {c('+', YELLOW)} {c('-', YELLOW)} {c('*', YELLOW)} {c('/', YELLOW)}")
    while True:
        op = input(f"  {c('Pilih operator', CYAN)}: ").strip()
        if op in ops:
            return op
        print(c("  ✗ Operator tidak valid.", RED))

def ask_int(label: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            val = int(input(f"  {c(label, CYAN)}: ").strip())
            if min_val <= val <= max_val:
                return val
            print(c(f"  ✗ Harus antara {min_val}–{max_val}.", RED))
        except ValueError:
            print(c("  ✗ Masukkan angka bulat.", RED))

# ── Features ──────────────────────────────────────────────────
def feature_operate():
    """Operasi hingga 4 pecahan."""
    clear()
    print(c("\n  ── Operasi Pecahan ──", BOLD + BLUE))
    print(f"  {c('Berapa pecahan yang ingin dihitung? (2–4)', DIM)}\n")
    n = ask_int("Jumlah pecahan", 2, 4)

    fractions = []
    for i in range(n):
        fractions.append(ask_fraction(f"Pecahan {i+1}  (contoh: 3/4)"))

    ops = []
    for i in range(n - 1):
        print(f"\n  Operator antara pecahan {i+1} dan {i+2}:")
        ops.append(ask_operator())

    # Evaluate left to right
    result = fractions[0]
    expr_parts = [fmt(result)]
    for i, op in enumerate(ops):
        b = fractions[i + 1]
        expr_parts.append(op)
        expr_parts.append(fmt(b))
        if op == '+': result += b
        elif op == '-': result -= b
        elif op == '*': result *= b
        elif op == '/':
            if b == 0:
                print(c("\n  ✗ Tidak bisa membagi dengan nol!", RED))
                input(f"\n  {c('[Enter untuk kembali]', DIM)}")
                return
            result /= b

    expr = " ".join(expr_parts)
    print(f"\n  {c('Ekspresi :', DIM)} {c(expr, YELLOW)}")
    print(f"  {c('Hasil    :', DIM)} {fmt_result(result)}")
    input(f"\n  {c('[Enter untuk kembali]', DIM)}")

def feature_simplify():
    """Sederhanakan pecahan."""
    clear()
    print(c("\n  ── Sederhanakan Pecahan ──", BOLD + BLUE))
    f = ask_fraction("Masukkan pecahan (contoh: 12/16)")
    # Python's Fraction auto-simplifies
    print(f"\n  {c('Bentuk sederhana :', DIM)} {fmt_result(f)}")
    input(f"\n  {c('[Enter untuk kembali]', DIM)}")

def feature_convert():
    """Konversi pecahan ↔ desimal."""
    clear()
    print(c("\n  ── Konversi Pecahan ↔ Desimal ──", BOLD + BLUE))
    print(f"  {c('1.', YELLOW)} Pecahan → Desimal")
    print(f"  {c('2.', YELLOW)} Desimal → Pecahan")
    print()
    choice = input(f"  {c('Pilih (1/2)', CYAN)}: ").strip()

    if choice == '1':
        f = ask_fraction("Pecahan (contoh: 3/8)")
        print(f"\n  {c(fmt(f), GREEN)} = {c(f'{float(f):.10g}', YELLOW)}")
    elif choice == '2':
        raw = input(f"  {c('Desimal (contoh: 0.375)', CYAN)}: ").strip()
        try:
            f = Fraction(raw).limit_denominator(10000)
            print(f"\n  {c(raw, GREEN)} ≈ {c(fmt(f), YELLOW)}  {c(f'(nilai tepat: {float(f):.10g})', DIM)}")
        except ValueError:
            print(c("  ✗ Format tidak valid.", RED))
    else:
        print(c("  ✗ Pilihan tidak valid.", RED))

    input(f"\n  {c('[Enter untuk kembali]', DIM)}")

def feature_compare():
    """Bandingkan dua pecahan."""
    clear()
    print(c("\n  ── Bandingkan Pecahan ──", BOLD + BLUE))
    a = ask_fraction("Pecahan 1")
    b = ask_fraction("Pecahan 2")

    fa, fb = fmt(a), fmt(b)
    if a > b:
        sym = ">"
        msg = f"{c(fa, GREEN)} lebih besar dari {c(fb, YELLOW)}"
    elif a < b:
        sym = "<"
        msg = f"{c(fa, YELLOW)} lebih kecil dari {c(fb, GREEN)}"
    else:
        sym = "="
        msg = f"{c(fa, GREEN)} sama dengan {c(fb, GREEN)}"

    print(f"\n  {c(fa, CYAN)} {c(sym, BOLD+YELLOW)} {c(fb, CYAN)}")
    print(f"  {msg}")
    input(f"\n  {c('[Enter untuk kembali]', DIM)}")

def feature_help():
    clear()
    print(c("\n  ── Panduan Input ──", BOLD + BLUE))
    rows = [
        ("3/4",   "Pecahan biasa"),
        ("0.75",  "Desimal (otomatis dikonversi)"),
        ("5",     "Bilangan bulat"),
        ("-1/2",  "Pecahan negatif"),
        ("7/3",   "Pecahan tidak murni (otomatis disederhanakan)"),
    ]
    for ex, desc in rows:
        print(f"  {c(ex.ljust(10), YELLOW)} — {desc}")
    print()
    print(c("  Operator yang didukung: + - * /", DIM))
    input(f"\n  {c('[Enter untuk kembali]', DIM)}")

# ── Main menu ─────────────────────────────────────────────────
MENU = [
    ("1", "Operasi Pecahan",          feature_operate),
    ("2", "Sederhanakan Pecahan",     feature_simplify),
    ("3", "Konversi Pecahan ↔ Desimal", feature_convert),
    ("4", "Bandingkan Dua Pecahan",   feature_compare),
    ("5", "Panduan Input",            feature_help),
    ("0", "Keluar",                   None),
]

BANNER = f"""
{c('  ┌─────────────────────────────────┐', CYAN)}
{c('  │', CYAN)}    {c('FractionCalc', BOLD+YELLOW)}  {c('CLI Edition', DIM)}    {c('│', CYAN)}
{c('  │', CYAN)}    {c('inspired by Ashyraffa32', DIM)}       {c('│', CYAN)}
{c('  └─────────────────────────────────┘', CYAN)}
"""

def main():
    while True:
        clear()
        print(BANNER)
        for key, label, _ in MENU:
            color = RED if key == '0' else YELLOW
            print(f"  {c(f'[{key}]', color)}  {label}")
        print()

        choice = input(f"  {c('Pilih menu', CYAN)}: ").strip()
        matched = [(k, fn) for k, _, fn in MENU if k == choice]

        if not matched:
            continue
        key, fn = matched[0]
        if key == '0':
            clear()
            print(c("\n  Sampai jumpa! —fractioncalc\n", DIM))
            sys.exit(0)
        fn()

if __name__ == "__main__":
    main()
