# Lovie Hospital — Roadmap
<!-- target path in your repo: ROADMAP.md (repo root) -->

This is a learning project first, an app for your daughter second — though hopefully she never notices the difference. Each phase below is scoped to teach specific things you asked to get exposure to, while producing something she can actually play with at the end of it.

## Phase 0 — Environment (this session)

Get Docker, Ignition Maker Edition, Postgres, and Git running locally, and confirm the pieces talk to each other. Covered in `docs/SESSION-1-SETUP.md`. Nothing to learn yet beyond "does it boot."

## Phase 1 — The core spine

**Goal:** a stuffed animal can check in, get vitals recorded, and get discharged, entirely inside Ignition, with real data in Postgres.

What you'll touch: Perspective view design in the Designer (drag-and-drop, but you'll want to understand bindings and containers), Ignition's named queries and database connections, and your first Jython scripting inside Ignition (button click events, message handlers). The `db/init.sql` and `ignition-scripts/hospital_patients.py` in this repo are the starting point.

Concretely, you're building: a patient roster view, a check-in screen (manual entry first — QR comes in Phase 2), a vitals-entry screen with number pads and mood buttons, and a discharge screen that writes a checkout timestamp and instructions back to Postgres.

## Phase 2 — QR wristbands + mobile check-in

**Goal:** scan a QR code on a printed wristband with a phone running the Perspective mobile app, and have it pull up that patient's chart.

What you'll learn: how Perspective's mobile app differs from the web client, QR/barcode scanning components in Perspective, and how you encode a stable patient identifier into a QR code (a URL-safe token tied to the patient's row in Postgres, not just their name). You'll generate the actual QR images with a small Python script — a good first taste of scripting *outside* Ignition that feeds data *into* it.

## Phase 3 — The tilt-sensor medication screen

**Goal:** the "drinking beer app" effect — tilt the phone, medication administers, something animates.

What you'll learn: Perspective's device orientation / accelerometer bindings (available in the mobile app, not the web client), expression bindings that map tilt angle to an animated property (rotation, fill level, position), and debouncing/thresholding logic so it registers a deliberate tilt rather than every wobble. This is the most visually fun phase and a good one to revisit once you're comfortable with bindings from Phase 1.

## Phase 4 — The simulation API (patients "calling in")

**Goal:** a separate backend service that decides which stuffed animal shows up next, with a photo and a complaint, so she isn't just clicking through a static list.

What you'll learn: building a small REST API (Python, FastAPI is the natural pick), API design (what does "a new patient arrived" look like as an endpoint?), and how Ignition calls out to an external HTTP API from a Jython script (`system.net.httpClient`) or how the API calls into Ignition instead (Ignition's Web Dev module, or writing straight to Postgres and letting Ignition poll). This is also where a stuffed-animal "database" (could just be the same Postgres, or a separate service) with photos comes in.

## Phase 5 — MQTT

**Goal:** get real exposure to the messaging pattern that underpins most modern industrial Ignition deployments, in a context low-stakes enough to break repeatedly.

What you'll learn: MQTT pub/sub concepts (topics, QoS, retained messages), running a broker (Mosquitto, already in `docker-compose.yml`), and Ignition's MQTT story specifically — the native path is Cirrus Link's MQTT Engine/Transmission modules (free to trial, this is the "gold standard" integration and worth doing properly rather than hacking around it). A natural use here: the simulation API (Phase 4) publishes "new patient arrived" over MQTT instead of a database poll, and Ignition subscribes and reacts in real time — this is the more idiomatic pattern than Phase 4's polling approach, so it's worth revisiting Phase 4 with this lens.

## Phase 6 — Kafka

**Goal:** exposure to event streaming at a different layer than MQTT — Kafka is not a drop-in replacement for MQTT, it's a different tool for a different job (durable, replayable event log vs. lightweight pub/sub), and understanding *why* you'd reach for one over the other is most of the value here.

What you'll learn: running Kafka locally (Redpanda is a much lighter single-binary stand-in that speaks the Kafka API — worth using instead of full Kafka+Zookeeper for a laptop setup), and a bridge pattern: MQTT topics feed into Kafka topics (this is a very real production pattern — MQTT for device/edge messaging, Kafka for durable downstream analytics), Ignition's own Kafka connectivity for consuming/publishing event streams directly. A good concrete goal: every vitals reading and discharge gets published as an event to Kafka, and a tiny separate consumer script prints a running "shift log" — your first taste of event-driven architecture.

## Phase 7 — Polish

QR-printable wristband templates, an iframe-embedded "hospital dashboard" (this is where you get iframe exposure — embedding an external page, like a simple stats dashboard built outside Ignition, inside a Perspective view), and whatever your daughter asks for after playing with it for a week. Kids are excellent at generating scope.

## Suggested pacing

There's no clock on this, but if you want a rhythm: Phase 0–1 is a good single weekend. Phases 2–3 are each a weekend. Phases 4–6 are the deep end — treat each as its own multi-session arc rather than a weekend, since they involve genuinely new concepts (APIs, message brokers, event streams) rather than just more Ignition screens.

## Version control note

Every phase's Ignition work (Perspective views, scripts, tag configs) should live in this git repo, not just in the Gateway's internal project storage. Ignition supports external/version-controllable project structure — set this up in Phase 0 so every phase from here on commits cleanly. Details in `docs/SESSION-1-SETUP.md`.
