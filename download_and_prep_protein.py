import urllib.request
from meeko import PDBQTReceptor

# 1. Ներբեռնում ենք 1AKI (Lysozyme) ֆայլը RCSB PDB-ից
url = "https://files.rcsb.org/download/1AKI.pdb"
filename = "protein.pdb"

print("Ներբեռնվում է սպիտակուցի PDB ֆայլը...")
urllib.request.urlretrieve(url, filename)
print("Ներբեռնումն ավարտվեց:")

# 2. Վերածում ենք PDBQT-ի Meeko-ի միջոցով
receptor_prep = PDBQTReceptor(filename)
receptor_prep.write_pdbqt_file("protein.pdbqt")

print("Սպիտակուցը հաջողությամբ պատրաստվեց և պահպանվեց 'protein.pdbqt' ֆայլում:")
