#!/usr/bin/env python3
"""Da eseguire dopo OGNI modifica a index.html: aggiorna BUILD, version.json e gli hash della CSP.
Se non lo fai la CSP blocca lo script e l'app resta vuota."""
import re, hashlib, base64, datetime, json, os
d = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(d, "index.html")
s = open(p, encoding="utf-8").read()
new = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
s = re.sub(r'const BUILD = "\d{14}";', 'const BUILD = "%s";' % new, s, 1)
hs = ["'sha256-%s'" % base64.b64encode(hashlib.sha256(m.group(1).encode("utf-8")).digest()).decode()
      for m in re.finditer(r"<script>(.*?)</script>", s, re.S)]
csp = ("default-src 'self'; script-src %s; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data: blob:; "
       "connect-src 'self' https://api.anthropic.com https://api.github.com data: blob:; "
       "manifest-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'") % " ".join(hs)
tag = '<meta http-equiv="Content-Security-Policy" content="%s">' % csp
if 'http-equiv="Content-Security-Policy"' in s:
    s = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>', lambda m: tag, s, 1)
else:
    s = s.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + tag + "\n", 1)
open(p, "w", encoding="utf-8").write(s)
open(os.path.join(d, "version.json"), "w").write(json.dumps({"v": new}, separators=(",", ":")) + "\n")
print("BUILD", new, "-", len(hs), "script inline in CSP")
