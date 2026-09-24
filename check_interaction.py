import math

def parse_pdbqt(filename):
    atoms = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    atoms.append((x, y, z))
    except FileNotFoundError:
        pass
    return atoms

# Փորձենք կարդալ ֆայլերը
protein_atoms = parse_pdbqt("protein.pdbqt")
if not protein_atoms:
    protein_atoms = parse_pdbqt("protein_clean.pdb")

ligand_atoms = parse_pdbqt("sample_ligand.pdbqt")

print(f"[*] Սպիտակուցի ատոմների քանակը: {len(protein_atoms)}")
print(f"[*] Լիգանդի ատոմների քանակը: {len(ligand_atoms)}")

if protein_atoms and ligand_atoms:
    print("\n--- Հաշվարկվում են ամենամոտ կապակցման կետերը ---")
    min_dist = 999.9
    closest_pair = None
    
    # Նմուշի համար ստուգենք հեռավորությունները
    for l_atom in ligand_atoms:
        for p_atom in protein_atoms:
            dist = math.sqrt((l_atom[0]-p_atom[0])**2 + (l_atom[1]-p_atom[1])**2 + (l_atom[2]-p_atom[2])**2)
            if dist < min_dist:
                min_dist = dist
                closest_pair = (p_atom, l_atom)
                
    print(f"[+] Նվազագույն հեռավորությունը սպիտակուցի և լիգանդի միջև: {min_dist:.2f} Å (անգստրեմ)")
    if min_dist < 4.0:
        print("[+] Կապակցման կարգավիճակը: Լիգանդը գտնվում է ակտիվ գոտու մոտ կամ շփման մեջ է (լավ փոխազդեցություն)!")
    else:
        print("[-] Լիգանդը դեռ հեռու է կամ տեղադրված չէ ակտիվ կենտրոնում:")
else:
    print("[-] Ֆայլերից մեկը չհաջողվեց կարդալ կամ դատարկ են։")
