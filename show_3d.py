import webbrowser
import os

def read_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()
    return ""

protein_data = read_file("protein.pdbqt")
if not protein_data:
    protein_data = read_file("protein_clean.pdb")

ligand_data = read_file("sample_ligand.pdbqt")

# Ստեղծում ենք HTML ֆայլ, որը 3Dmol.js գրադարանով ցույց է տալիս քո ֆայլերը
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Docking 3D View</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/3dmol/2.0.3/3dmol-min.js"></script>
    <style>
        body {{ margin: 0; background: #111; color: white; text-align: center; font-family: sans-serif; }}
        #container {{ width: 100vw; height: 92vh; position: relative; }}
    </style>
</head>
<body>
    <h3>Սպիտակուցի և Լիգանդի 3D Փոխազդեցություն</h3>
    <div id="container"></div>

    <script>
        let element = document.querySelector("#container");
        let viewer = $3Dmol.createViewer(element, {{backgroundColor: "black"}});

        // Ավելացնում ենք սպիտակուցը
        let proteinData = `{protein_data.replace('`', '').strip()}`;
        viewer.addModel(proteinData, "pdbqt");
        viewer.setStyle({{(model: -1)}}, {{cartoon: {{color: "cyan"}}}});

        // Ավելացնում ենք լիգանդը
        let ligandData = `{ligand_data.replace('`', '').strip()}`;
        viewer.addModel(ligandData, "pdbqt");
        viewer.setStyle({{(model: -1)}}, {{stick: {{colorscheme: "magentaC"}}}});

        viewer.zoomTo();
        viewer.render();
    </script>
</body>
</html>
"""

with open("view_docking.html", "w") as f:
    f.write(html_content)

# Ավտոմատ բացում ենք բրաուզերում
file_path = "file://" + os.path.abspath("view_docking.html")
webbrowser.open(file_path)
print("[+] 3D վիզուալիզացիան հաջողությամբ գեներացվեց և բացվեց բրաուզերում։")
