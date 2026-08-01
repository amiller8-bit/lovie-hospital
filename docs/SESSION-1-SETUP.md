# Session 1 — Environment Setup
<!-- target path in your repo: docs/SESSION-1-SETUP.md -->

Goal for this session: Docker running, Ignition Gateway up and activated, Postgres seeded, git repo initialized. No Perspective screens yet — that's Phase 1.

## 1. Assemble the repo locally

Create a folder called `lovie-hospital` and lay out the files from this delivery according to the mapping in `README.md`. Then:

```bash
cd lovie-hospital
git init
git add .
git commit -m "Phase 0: project scaffold"
```

If you want this on GitHub (recommended — real version control practice): create an empty repo on github.com (no README/gitignore, you already have one), then:

```bash
git remote add origin https://github.com/<your-username>/lovie-hospital.git
git branch -M main
git push -u origin main
```

## 2. Install Docker Desktop

If you don't have it: https://www.docker.com/products/docker-desktop. Confirm it works:

```bash
docker --version
docker compose version
```

## 3. Get a free Ignition Maker Edition license

Maker Edition is Inductive Automation's free-for-hobbyists tier (limited tag count, fine for this project). Register at https://inductiveautomation.com/ignition/maker-edition. After registering, your Inductive Automation account will show an 8-character license key (format `XXXX-XXXX`) and an activation token — you'll need both.

## 4. Create the secrets files

In `lovie-hospital/`, create a `secrets/` folder (already gitignored) with three files:

```bash
mkdir secrets
echo -n "your-chosen-password" > secrets/gateway_admin_password.txt
echo -n "XXXX-XXXX" > secrets/ignition_license_key.txt
echo -n "your-activation-token" > secrets/ignition_activation_token.txt
```

## 5. Check the Ignition image tag

Open `docker-compose.yml` and check the comment above the `gateway` service — confirm the pinned version tag against https://hub.docker.com/r/inductiveautomation/ignition/tags and update it if a newer 8.1.x patch is out.

## 6. Bring the stack up

```bash
docker compose up -d
docker compose logs -f gateway
```

Watch the logs for the Gateway to finish starting (a minute or two on first run — it's unpacking and auto-commissioning). Once it settles, open http://localhost:9088 and log in with `admin` / the password you put in `secrets/gateway_admin_password.txt`. Confirm under Config -> Licensing that Maker Edition activated successfully.

## 7. Confirm Postgres seeded correctly

```bash
docker compose exec postgres psql -U lovie -d lovie_hospital -c "SELECT name, species FROM patients;"
```

You should see your five seed patients. Edit `db/init.sql` now if you want the roster to match your daughter's actual stuffed animals — you'll need `docker compose down -v` (wipes the Postgres volume) and `docker compose up -d` again for edits to take effect, since the init script only runs on first container creation.

## 8. Connect Ignition to Postgres

In the Gateway web UI: Config -> Databases -> Drivers, confirm a PostgreSQL driver is listed (built in). Then Config -> Databases -> Connections -> Create new Database Connection:
- Name: `LovieHospital` (must match `DB_CONNECTION` in the script library file)
- JDBC Driver: PostgreSQL
- Connect URL: `jdbc:postgresql://postgres:5432/lovie_hospital` (use the service name `postgres`, not `localhost` — Ignition is reaching Postgres over the Docker network)
- Username: `lovie`
- Password: `lovie_dev_password`

Save, and confirm the connection shows "Valid" status.

## 9. Open the Designer, create the project, paste the script

Launch the Designer (there's a "Launch Designer" link on the Gateway home page — this downloads a small launcher app). Create a new project, e.g. `LovieHospital`. Follow the instructions at the top of `ignition-scripts/hospital_patients.py` to create the script package and paste the code in.

## 10. Set up version control for the Ignition project

Ignition 8.1 supports storing a project's resources on disk in a git-friendly structure instead of only inside the Gateway's internal database, via project "external" resources / the Gateway's version control integration (Config -> Projects -> your project -> Version Control, or exporting the project as a resource tree). This is worth setting up before Phase 1 gets underway, since every future phase's Designer work should land in commits, not just live in the Gateway. Give this its own short session — it's fiddly the first time, so don't stack it on top of everything else above.

## You're done with Session 1 when

Gateway is up, Maker Edition is activated, Postgres has the seeded roster, the `LovieHospital` database connection shows valid, and `hospital.patients.get_patient_roster()` typed into the Designer's Script Console returns your five stuffed animals as a dataset. That last check is the real finish line — it proves Ignition, Postgres, and your first Jython script are all talking to each other.
