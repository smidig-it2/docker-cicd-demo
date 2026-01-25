# Flask kvadrat-API med CI/CD, Docker og GitHub Actions

Dette repoet er en del av prosjektheftet til læreverket **Smidig IT-2** i faget **Informasjonsteknologi 2** i videregående skole.

Prosjektet viser hvordan et enkelt Flask-API kan testes, bygges og legges ut automatisk ved hjelp av CI/CD.  
Testene kjøres i Docker i GitHub Actions. Produksjonsimaget publiseres på Docker Hub, og applikasjonen kjøres som en webtjeneste på Render.

CI/CD-oppsettet aktiveres trinnvis. I starten kjøres bare testene automatisk. Senere slås også publisering til Docker Hub og varsling av Render på.

---

## Oversikt

Prosjektet består av fire hoveddeler:

**Flask-API (`src/`)**  
Et enkelt API med ruter for å beregne kvadratet av et tall og vise versjonsnummer.

**Enhetstester (`tests/`)**  
Tester som bruker Flask sin innebygde testklient og kan kjøres både lokalt og i Docker.

**Docker-images**  
- testimage: inneholder Flask, pytest og testene  
- produksjonsimage: inneholder kun applikasjonen og avhengighetene

**CI/CD med GitHub Actions**  
Når kode pushes til GitHub, kan stegene kjøres automatisk, først testene og senere også bygging, publisering og utrulling.

---

## Kom i gang

Du kan bruke dette repoet som mal:

1. Logg inn på GitHub.  
2. Gå til:  
   https://github.com/smidig-it2/docker-cicd-demo  
3. Klikk **Use this template** og velg **Create a new repository**.  
4. Gi repoet navn og opprett det.  
5. Klon repoet til PC-en din og åpne det i VS Code.

---

## Kjøre testene lokalt (uten Docker)

Åpne et terminalvindu i rotmappen og kjør:

    pytest

Testene skal da passere uten feil.

---

## Bygge og kjøre testimaget i Docker

Bygg testimaget:

    docker build -f Dockerfile.test -t docker-cicd-tests .

Kjør testene i container:

    docker run --rm docker-cicd-tests

Testresultatet vises i terminalvinduet.

---

## Kjøre testene automatisk på GitHub

Endre til:

    APP_VERSION = "1.1"

i **/src/app.py**.

Kjør deretter:

    pytest

lokalt. Én test skal nå feile.

Stage, commit og push endringen.  
Gå til fanen **Actions** i GitHub-repoet og se at siste kjøring feiler og vises med rød sirkel.

For at testen skal passere, må du endre i **/tests/test_api.py** til:

    assert data["version"] == "1.1"

Stage, commit og push på nytt.  
Under **Actions** skal du nå se at kjøringen er fullført uten feil og vises med grønn sirkel.

---

## Bygge og publisere produksjonsimaget

1. Opprett en bruker på Docker Hub.  
2. Lag et **Personal Access Token** med rettigheter: `Read, Write, Delete`.  
3. Legg inn følgende secrets i GitHub-repoet under  
   **Settings → Secrets and variables → Actions**:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

4. I **.github/workflows/cicd.yaml**, fjern kommentartegnet `#` foran alle linjene i stegene:
   - Bygg produksjonsimage  
   - Logg inn på Docker Hub  
   - Tag og push image til Docker Hub  

Husk at i VS Code kan du markere flere linjer og trykke **Ctrl+'** for å legge til eller fjerne `#` på flere linjer samtidig.

Stage, commit og push.  
Gå til Docker Hub og se at produksjonsimaget nå ligger der.

---

## Kjøre imaget på Render

1. Opprett en bruker på Render.  
2. Opprett en ny **Web Service** med imaget fra Docker Hub.  
3. Når tjenesten er startet, finn nettadressen øverst på siden i Render.  
   Legg til:

    /api/version

I nettleseren skal du se:

    {"version":"1.1"}

---

## Oppdatere imaget på Render automatisk

Render bruker imaget fra Docker Hub, men må få beskjed når et nytt image er publisert.  
Dette gjøres med en **Deploy Hook**.

1. Gå til **Settings** for webtjenesten din på Render.  
2. Rull ned til **Deploy Hook** og kopier den private URL-en.  
3. Legg den inn som secret i GitHub-repoet:
   - Name: `RENDER_DEPLOY_HOOK`
   - Secret: den private URL-en fra Render

4. I **.github/workflows/cicd.yaml**, fjern kommentartegnet `#` foran alle linjene i steget:
   - Trigger deploy på Render

Endre nå til:

    APP_VERSION = "1.2"

i **/src/app.py**, og til:

    assert data["version"] == "1.2"

i **/tests/test_api.py**.

Stage, commit og push.  
Sjekk at alle stegene passerer under **Actions** i GitHub.

Åpne deretter nettadressen fra Render med:

    /api/version

Du skal nå se:

    {"version":"1.2"}

Dette viser at hele CI/CD-kjeden fungerer automatisk.

---

## Oppsummering

Workflow-filen som styrer hele prosessen, er:
    
    .github/workflows/cicd.yaml

Når du pusher kode til `main`, kjøres alle `.yaml` og `.yml` filer i mappen `.github/workflows` automatisk av GitHub Actions:

1. GitHub bygger testimaget.  
2. Testene kjøres i Docker.  
3. Hvis testene passerer, bygges produksjonsimaget.  
4. Produksjonsimaget publiseres på Docker Hub.  
5. Render får beskjed om å hente ny versjon av imaget.

Status for hver kjøring ser du under fanen **Actions** i GitHub-repoet.

---

## Mappestruktur

    docker-cicd-demo/
    │
    ├─ src/                # Flask-applikasjonen (app.py)
    ├─ tests/              # Enhetstester (test_api.py)
    ├─ .github/workflows/  # CI/CD workflow (cicd.yaml)
    ├─ Dockerfile          # Produksjonsimage
    ├─ Dockerfile.test     # Testimage
    ├─ requirements.txt
    ├─ requirements-test.txt
    └─ pytest.ini

---

## Krav

- Git  
- Docker Desktop  
- Python hvis du vil kjøre testene lokalt uten Docker  
- GitHub-konto  
- Docker Hub-konto  
- Render-konto  

---

## Lisens

Dette prosjektet er lisensiert under MIT-lisensen. Se `LICENSE` for mer informasjon.
