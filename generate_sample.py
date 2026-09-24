from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation

# 1. Ստեղծում ենք նմուշային մոլեկուլ SMILES կոդից (Ասպիրին)
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
mol = Chem.MolFromSmiles(smiles)

# 2. Ավելացնում ենք ջրածիններ և ստեղծում 3D կոորդինատներ
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, randomSeed=42)
AllChem.MMFFOptimizeMolecule(mol)

# 3. Նախապատրաստում և անմիջապես գրում ենք ֆայլի մեջ
preparator = MoleculePreparation()
preparator.prepare(mol)
preparator.write_pdbqt_file("sample_ligand.pdbqt")

print("Նմուշային լիգանդը հաջողությամբ վերածվեց և պահպանվեց 'sample_ligand.pdbqt' ֆայլում:")
