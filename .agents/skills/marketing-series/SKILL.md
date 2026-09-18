---
name: marketing-series
version: 1.0.0
description: "Genera la campaña de marketing open-source de un repo w-* (serie de 20 días reales × 6 plataformas × EN+ES, con PDFs LinkedIn EN+ES). USA esta skill cuando el usuario mencione 'hacer marketing', 'campaña', 'serie de 20 días', 'marketing de wkafka/wpipe/wsqlite...', 'generar PDFs LinkedIn', 'traducir la serie', o 'misma forma que los demás'. La regla de oro: NADA inventado — cada gancho se ancla a hechos REALES verificados en el repo."
compatibility: opencode
metadata:
  language: es
  author: wisrovi
  status: stable
  tags: [marketing, linkedin, pdf, bilingual, series, open-source]
  requires: [google-chrome, npx, mermaid-cli]
  workspace: w_libraries
inputs:
  - type: repo_path
    description: Ruta absoluta del repo fuente (p.ej. /home/wisrovi/Documents/w_libraries/wkafka_os/wkafka)
  - type: repo_slug
    description: Ruta relativa al motor web (p.ej. wkafka_os/wkafka) — se auto-detecta
  - type: language
    description: "EN y ES siempre (bilingüe obligatorio)"
  - type: platforms
    description: "Medium, Dev.to, Indie_Hackers, Reddit, LinkedIn, X"
  - type: days
    description: "20 días mínimo (un día por feature real verificada)"
outputs:
  - type: marketing_tree
    description: "marketing/<Plataforma>/<NN>_<Tema>/ con title.txt+title_es.txt y cuerpos *_en.md/*_es.md"
  - type: linkedin_pdfs
    description: "Por día LinkedIn: companion_en.pdf + companion_es.pdf (A6, HTML+CSS→chrome headless)"
  - type: commits
    description: "Commit+push granular POR REPO (1 checkout por día o por paquete), en la rama de marketing"
anti_trigger:
  - "Solo quiero el código de la librería"
  - "No toques marketing"
  - "No me generes nada"
triggers:
  - "hacer marketing"
  - "campaña"
  - "serie de 20 días"
  - "marketing de wkafka"
  - "marketing de wpipe"
  - "generar PDFs LinkedIn"
  - "misma forma que los demás"
  - "traducir la serie"
  - "20 días"
---

# Marketing Series Generator (SKILL)

## Rol

Marketing Engineer + Technical Writer bilingüe (EN/ES). Convierte un repo `w-*`
real en una campaña de 20 días × 6 plataformas, EN+ES, con PDFs LinkedIn EN+ES.

---

## FLUJO DE TRABAJO

```
1. VERIFICAR hechos REALES del repo (nunca inventar)
2. Construir _facts_<repo>.py (anclaje por día)
3. Generar árbol marketing/<Plataforma>/<NN>_<Tema>/
4. Generar títulos y cuerpos EN+ES por plataforma
5. Renderizar PDFs LinkedIn EN+ES (motor chrome)
6. Commit+push POR REPO con checkpoint
```

---

## REGLA DE ORO (Nº1 — no negociable)

> **NADA inventado.** Cada hook, métrica, versión, DOI o ejemplo citado DEBE
> ser verificado en el repo local (README, CHANGELOG, `examples/`, código).
> Prohibido fabricar: DOIs, cifras de descargas, benchmarks, features que no
> existen, URLs que no cargan.

Estructura de la serie: **20 días → 20 features reales y verificadas.**
Para wkafka (referencia completa ya existente): wkafka-array-streaming,
headers/keys, multimedia image, SASL, request-response client/server, manual
offset commit (exactly once/at least once), files streaming.

## 1. Verificación de hechos (antelación)

Antes de escribir UNA frase de marketing, ejecuta en el repo:

```bash
# Hechos reales: paquete exacto, repo, docs, version, MIT
cd <repo> && grep -nE "name|urls|Homepage|Roadmap|requires-python" pyproject.toml | head -20
grep -nE "version|licen" pyproject.toml CHANGELOG.md | head -12
git remote -v && git tag -l | tail -5

# Features reales: 20 candidatos del ejemplo REAl
ls examples/            # ejemplo exacto por día
ls examples/0*_*/       # nombres de cada serie real
```

Nunca uses: `pip install` (bloqueado por PEP 668 en este sistema) — el motor
PDF no necesita librerías Python (usa google-chrome + npx).

## 2. Anclaje por día (hechos reales → tema de marketing)

Cada día = 1 feature REAL verificada. Tabla de mapeo por repo (serie 20 días):

| Day | Feature real (código) | Gancho de marketing |
|-----|----------------------|---------------------|
| 01  | basics (decorator)    | "El 90% de los demos oscuros" |
| 02  | headers/keys         | "Los bytes no viajan solos" |
| 03  | multimedia           | "Imágenes que portan contexto" |
| 04  | security SASL        | "Seguridad que se configura" |
| 05  | request-response     | "El patrón que Kafka no da gratis" |
| 06  | manual offset        | "exactly once, una sola vez" |
| 07  | files streaming      | "PDF/ZIP que viajan con nombre" |

Cada entrada genuina se ancla a un nombre EXACTO de `examples/` del repo.

## 3. Estructura de archivos (obligatoria)

Por repos, por plataforma y por día:

```text
marketing/<Plataforma>/<NN>_<Tema>/
    title.txt            # EN
    title_es.txt         # ES
    <NN>_<PLAT>_Wkafka_<Tema>_en.md    # avatar EN
    <NN>_<PLAT>_Wkafka_<Tema>_es.md    # avatar ES
```

Plataformas: `Medium`, `Dev.to`, `Indie_Hackers`, `Reddit`, `LinkedIn`, `X`.
Además, por día de LinkedIn: `companion_en.pdf` y `companion_es.pdf` (A6).

## 4. Tonos y formatos por plataforma

| Plataforma | Tono | Formato |
|-----------|------|---------|
| Medium     | Tutorial largo, código comentado | Título + hook + 3 pains + code + wins + CTA |
| Dev.to     | Técnico directo, reproducible | Título + intro + code_sample + tabla |
| Indie_Hackers | Founder, standalone, audiencia indie | Título + hook + pains + revenue/square |
| Reddit     | Honesto, sin emojis, valor directo | Título + cuerpo real + pruébalo |
| LinkedIn   | Profesional + PDF companion | Título + hook + wins + mermaid diagram |
| X          | Corto, gancho + tagline | 1 párrafo + hashtags |

## 5. Motor PDF LinkedIn (sin pip — chrome headless)

```bash
# HTML+CSS → PDF A6 (EN+ES por día), motor IDÉNTICO al de wkafka/wpipe
google-chrome --headless=new --disable-gpu --no-sandbox \
    --no-pdf-header-footer --print-to-pdf=companion_en.pdf \
    "file:///tmp/opencode/wpipe/page.html"
```

- HTML: HTML/CSS inline (Helvetica/Segoe, paleta por plataforma, logo w-*,
  day chip, mermaid diagrama). Ver motor real: `wpipe/posters/generate_linkedin_pdfs.py`.
- Diagrama Mermaid: `npx -y @mermaid-js/mermaid-cli` (si Chrome no renderiza).
- Output: `companion_en.pdf` + `companion_es.pdf` en la carpeta del día LinkedIn.

## 6. Commit + push por repo

```bash
cd <repo> && git add marketing/ && git commit -m "marketing: <repo> Day NN <tema> EN+ES x6 plataformas"
git push origin <branch>
```

Cada `NN` día = 1 commit independiente (historial granular, igual que series
anteriores: wkafka D03/D04/D05 pusheados individualmente).

---

## Entregables finales

1. `marketing/<Plataforma>/<NN>_<Tema>/` completo EN+ES × 6 plataformas × 20 días.
2. `marketing/LinkedIn/<NN>_<Tema>/companion_{en,es}.pdf` EN+ES por día.
3. Importables y reproducible — motores reales sin inventar nada.
4. `git log` por repo: 1 commit por día de marketing (traza completa).
