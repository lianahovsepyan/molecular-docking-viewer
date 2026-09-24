import os
import datetime

# Ստեղծում ենք աշխատանքային փուլի ամփոփագիրը
summary_text = f"""==================================================
ՄՈԼԵԿՈՒԼԱՅԻՆ ԴՈԿԻՆԳԻ ՆԱԽԱՊԱՏՐԱՍՏՈՒՄ - ԱՄՓՈՓԱԳԻՐ
Ամսաթիվ / Ժամ: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Աշխատանքային պանակ: {os.getcwd()}
==================================================
Հիմնական ֆայլեր և չափեր:
1. protein.pdbqt -> {os.path.getsize('protein.pdbqt')} բայթ
2. sample_ligand.pdbqt -> {os.path.getsize('sample_ligand.pdbqt')} բայթ
3. conf.txt -> {os.path.getsize('conf.txt')} բայթ
==================================================
Կարգավիճակ: Բոլոր մուտքային ֆայլերը և կոնֆիգուրացիոն պարամետրերը հաջողությամբ կարգավորվել են և պատրաստ են հետագա վերլուծության համար։
"""

with open("docking_summary_report.txt", "w") as f:
    f.write(summary_text)

print(summary_text)
print("\n[+] Հաշվետվությունը հաջողությամբ գրվեց 'docking_summary_report.txt' ֆայլում:")
