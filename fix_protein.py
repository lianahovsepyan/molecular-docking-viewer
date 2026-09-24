from meeko import PDBQTReceptorPreparation
import sys

# Կարդում ենք մեր մաքրված սպիտակուցի ֆայլը
with open("protein_clean.pdb", "r") as f:
    pdb_str = f.read()

# Պատրաստում ենք PDBQT ֆորմատի համար
preparator = PDBQTReceptorPreparation()
# Meeko-ն աշխատում է string-ով
pdbqt_string = preparator.prepare(pdb_str)

with open("protein.pdbqt", "w") as f:
    f.write(pdbqt_string)

print("Հիանալի՛ է: 'protein.pdbqt'-ն հաջողությամբ ստեղծվեց!")
