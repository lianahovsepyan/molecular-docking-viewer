from rdkit import Chem
from meeko import MoleculePreparation

# Օրինակ՝ եթե ունեք լիգանդի ֆայլ (օրինակ՝ ligand.sdf)
# Կարդում ենք RDKit-ի միջոցով
# reader = Chem.SDMolSupplier('ligand.sdf')
# mol = next(reader)

# Կամ կարող ենք ստուգել, որ նախապատրաստման դասը պատրաստ է աշխատանքի
prep = MoleculePreparation()
print("Meeko-ն և RDKit-ը պատրաստ են մոլեկուլների մշակման համար:")
