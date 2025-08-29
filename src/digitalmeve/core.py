*** a/src/digitalmeve/core.py
--- b/src/digitalmeve/core.py
@@
-from datetime import UTC, datetime
+from datetime import datetime, timezone
@@
-    # horodatage en UTC, suffixe 'Z'
-    created_at = datetime.now(UTC).replace(microsecond=0).isoformat() + "Z"
+    # horodatage en UTC compatible py3.10 : timezone.utc et suffixe 'Z'
+    created_at = (
+        datetime.now(timezone.utc)
+        .replace(microsecond=0)
+        .isoformat()
+        .replace("+00:00", "Z")
+    )
