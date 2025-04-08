# 🚫 Archived – jdbc_via_jpype

> **This repository is no longer maintained.**  
> I’m keeping the code around for reference, but I don’t plan to accept issues or PRs.

---

## What this library did (circa 2020‑2021)

`jdbc_via_jpype` wrapped **JPype** + **JDBC** behind a minimal [PEP 249]‑compatible
interface:

* Started a JVM once per process, wiring `-Djava.class.path` / `-Djava.library.path`.
* Used `java.sql.DriverManager` to obtain a `java.sql.Connection`.
* Exposed Python‑side `Connection`/`Cursor` objects that delegated to JDBC and
  converted result‑set columns to basic Python types.

It worked fine for small scripts that needed to talk to any JDBC‑capable database
without installing a native driver.

---

## Why it’s obsolete

| What changed | Impact on this project |
|--------------|------------------------|
| **JPype 1.5+** ships its own `jpype.dbapi2` module that offers the same DB‑API wrapper—better tested and actively maintained. | This repo now duplicates upstream functionality. |
| **Python 3.12** removed `distutils`. | The old `setup.py` no longer installs. |
| **JPype start‑up flags** and string‑conversion defaults changed. | Users would need code tweaks anyway; easier to switch to upstream driver. |

---

## Modern replacement (recommended)

```python
import jpype
import jpype.dbapi2 as dbapi2

jpype.addClassPath("postgresql-42.7.1.jar")      # or any JDBC driver JAR
jpype.startJVM(convertStrings=True)              # match the old behaviour

conn = dbapi2.connect(
    "org.postgresql.Driver",
    "jdbc:postgresql://localhost:5432/mydb",
    ["user", "password"]
)
