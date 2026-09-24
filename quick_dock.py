import os

print("1. Ստուգում ենք միջավայրը...")
# Համոզվում ենք, որ մեր լիգանդը տեղում է
if os.path.exists("sample_ligand.pdbqt"):
    print("-> Լիգանդը (sample_ligand.pdbqt) առկա է։")
else:
    print("-> Լիգանդը չգտնվեց, բայց մենք կարող ենք արագ ստեղծել։")

print("2. Պատրաստ ենք կատարելու հաջորդ քայլը։")
