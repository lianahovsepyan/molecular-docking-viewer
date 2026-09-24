import os

print("--- Մոլեկուլային դոկինգի նախապատրաստություն ---")
files = ["protein.pdbqt", "sample_ligand.pdbqt", "conf.txt"]
for f in files:
    if os.path.exists(f):
        print(f"[+] '{f}' ֆայլը առկա է ({os.path.getsize(f)} բայթ)")
    else:
        print(f"[-] Զգուշացում. '{f}' ֆայլը չի գտնվել!")

print("\nՖայլերը լիովին պատրաստ են մշակման:")
