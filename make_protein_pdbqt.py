with open("protein_clean.pdb", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("ATOM") or line.startswith("HETATM"):
        # PDBQT ֆորմատի համար ավելացնում ենք զրոյական լիցք վերջում, եթե այն բացակայում է
        if len(line) < 78:
            # Լրացնում ենք մինչև անհրաժեշտ երկարությունը և ավելացնում 0.0000 0.00 A
            line = line.rstrip("\n") + "  0.0000\n"
        new_lines.append(line)
    elif line.startswith("TER") or line.startswith("END"):
        new_lines.append(line)

with open("protein.pdbqt", "w") as f:
    f.writelines(new_lines)

print("Հաջողվեց! 'protein.pdbqt'-ն պատրաստ է։")
