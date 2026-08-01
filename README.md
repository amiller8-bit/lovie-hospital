# Lovie Hospital 🧸🏥
<!-- target path in your repo: README.md (repo root) -->

A pretend third-shift hospital for your daughter's stuffed animals, built on Inductive Automation's Ignition. Patients check in via QR-coded wristbands scanned in the Perspective mobile app, get their vitals and mood tracked, receive medication through a phone-tilt animation, and get discharged with instructions.

This repo doubles as Drew's re-entry into hands-on coding: Docker, Postgres, Git, Ignition/Perspective, Jython scripting, MQTT, and eventually Kafka.

## Setting up the folder structure

I couldn't create subfolders directly in your connected outputs folder this session, so every file below is named with its intended path baked into the filename. When you set this up locally (see `docs/SESSION-1-SETUP.md`), create these folders and drop each file at the path implied by its name:

```
lovie-hospital/
├── README.md
├── ROADMAP.md
├── docker-compose.yml
├── .gitignore
├── db/
│   └── init.sql
├── ignition-scripts/
│   └── hospital_patients.py
└── docs/
    └── SESSION-1-SETUP.md
```

File → target path mapping:
- `lovie-hospital-README.md` → `README.md`
- `lovie-hospital-ROADMAP.md` → `ROADMAP.md`
- `lovie-hospital-docker-compose.yml` → `docker-compose.yml`
- `lovie-hospital-gitignore` → `.gitignore`
- `lovie-hospital-db-init.sql` → `db/init.sql`
- `lovie-hospital-ignition-scripts-hospital_patients.py` → `ignition-scripts/hospital_patients.py`
- `lovie-hospital-docs-SESSION-1-SETUP.md` → `docs/SESSION-1-SETUP.md`

## What's here

- **ROADMAP.md** — the phased build plan and what each phase teaches you
- **docker-compose.yml** — local stack: Ignition Gateway (Maker Edition), Postgres, Mosquitto (MQTT broker)
- **db/init.sql** — Postgres schema + seed data (the stuffed-animal patient roster)
- **ignition-scripts/** — Jython script code meant to be pasted into the Ignition Designer's script library (Ignition doesn't load raw `.py` files from disk without going through Designer/project export — notes are in the file)
- **docs/SESSION-1-SETUP.md** — your first working session: get everything running locally

## Status

Phase 1 (core spine) scaffold only. Nothing has been run against a live Gateway yet — start with `docs/SESSION-1-SETUP.md`.
