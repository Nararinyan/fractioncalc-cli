from fractions import Fraction

def sapa():
    print(f"Halo {greet}")

greet = input("Siapa nama kamu? ")
sapa()

def hitung(angka1, operator, angka2):
    if operator == "+":
        return Fraction(angka1) + Fraction(angka2)
    elif operator == "-":
        return Fraction(angka1) - Fraction(angka2)
    elif operator == "x":
        return Fraction(angka1) * Fraction(angka2)
    elif operator == "/":
        if angka2 == "0":
            print("Tak bisa bagi dengan 0!")
            return
        else:
            return Fraction(angka1) / Fraction(angka2)
    elif operator == "^":
        return Fraction(angka1) ** Fraction(angka2)

    else:
        print("Operator tidak dikenal!")

while True:
    angka1 = input("Masukkan angka: ")
    if angka1 == "q":
            break
    operator = input("Masukkan operasi: ")
    angka2 = input("Masukkan angka kedua: ")
    hasil = hitung(angka1, operator, angka2)
    if hasil is not None:
        print(f"Hasilnya adalah: {hasil}")



