from meeko import PDBQTReceptor

# Ենթադրենք՝ ունենք protein.pdb ֆայլ
# Կարդում և վերածում ենք PDBQT-ի
try:
    receptor_prep = PDBQTReceptor("protein.pdb")
    receptor_prep.write_pdbqt_file("protein.pdbqt")
    print("Սպիտակուցը հաջողությամբ վերածվեց 'protein.pdbqt' ֆայլի:")
except FileNotFoundError:
    print("Ուշադրություն. 'protein.pdb' ֆայլը չի գտնվել պանակում: Խնդրում ենք համոզվել, որ սպիտակուցի ֆայլն առկա է։")
