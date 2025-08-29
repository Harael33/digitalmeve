*** a/src/digitalmeve/generator.py
--- b/src/digitalmeve/generator.py
@@
+from __future__ import annotations
+
+from pathlib import Path
+from typing import Any, Dict, Optional, Tuple, Union
+
+# On utilise l’implémentation “métier” du module core
+from .core import generate_meve as _core_generate_meve
+
+__all__ = ["generate_meve"]
+
+PathLike = Union[str, Path]
+
+
+def _default_out_path(infile: PathLike) -> Path:
+    """
+    Calcule le nom de fichier de sortie par défaut : <input>.meve.json
+    """
+    p = Path(infile)
+    return p.with_name(p.name + ".meve.json")
+
+
+def generate_meve(
+    infile: PathLike,
+    outfile: Optional[PathLike] = None,
+    issuer: Optional[str] = None,
+) -> Tuple[bool, Path, Dict[str, Any]]:
+    """
+    Génère un MEVE pour `infile`.
+
+    Cette fonction est un *wrapper* autour de `core.generate_meve` et garantit
+    un contrat de retour stable pour les tests :
+
+        (ok, out_path, info)
+
+    - ok: bool indiquant si l'opération s’est bien passée
+    - out_path: chemin du fichier JSON généré
+    - info: dict d’informations (métadonnées du MEVE)
+    """
+    # Appel de l’implémentation cœur
+    result = _core_generate_meve(
+        infile=infile,
+        outfile=outfile,
+        issuer=issuer,
+    )
+
+    # Normalisation du retour pour couvrir les 2 signatures possibles :
+    # 1) (ok, info)
+    # 2) (ok, out_path, info)
+    if isinstance(result, tuple) and len(result) == 2:
+        ok, info = result
+        out_path = Path(outfile) if outfile else _default_out_path(infile)
+        return ok, out_path, info  # type: ignore[return-value]
+
+    if isinstance(result, tuple) and len(result) == 3:
+        ok, out_path, info = result
+        return bool(ok), Path(out_path), dict(info)
+
+    raise TypeError("Unexpected return from core.generate_meve")
