# Lovie Hospital — Roadmap
<!-- target path in your repo: ROADMAP.md (repo root) -->
<!-- Revision 2 — expanded with the distributed-architecture track (Tags, Historian, Gateway Network, Project Inheritance, Redundancy) -->

This is a learning project first, an app for your daughter second — though hopefully she never notices the difference. Each phase below is scoped to teach specific things you asked to get exposure to, while producing something she can actually play with along the way.

## Phase 0 — Environment ✅ done

Get Docker, Ignition Maker Edition, Postgres, and Git running locally, and confirm the pieces talk to each other. Covered in `docs/SESSION-1-SETUP.md`.

## Phase 1 — The core spine ✅ done

**Goal:** a stuffed animal can check in, get vitals recorded, and get discharged, entirely inside Ignition, with real data in Postgres.

What you touched: Ignition's database connections, and your first Jython scripting inside Ignition via the Project Library (`hospital.patients` — check-in, vitals, discharge, all talking straight to Postgres).

Worth naming honestly: this phase went straight from UI to database via scripting, and skipped Tags entirely — which is backwards from how most real Ignition projects are built. That's deliberate for a fast first win, and Phase 1.5 goes back and does it the more idiomatic way.

## Phase 1.5 — Tags, UDTs, and script scope (new)

**Goal:** rebuild the patient/visit data model as Tags instead of only living in Postgres rows, and understand *where* your code actually runs.

What you'll learn: User Defined Types (UDTs) — Ignition's structured tag templates, perfect for modeling "a patient" as a reusable tag structure (name, species, current mood, current temp, status) rather than only a database row; tag change scripts (code that fires when a tag's value changes — Gateway-scoped, running on the server regardless of who's looking at a screen); and the distinction between **Gateway scope** (scripts that run on the server, independent of any open client — tag change scripts, timer scripts, gateway message handlers) versus **Client/Session scope** (scripts tied to a specific person's open session — button click events, Perspective session scripts). This distinction matters for everything from here forward: get it wrong and you'll write logic that silently only works while a screen happens to be open.

Concretely: patients become tags under a UDT, vitals updates write to tags (with a Gateway-scoped tag change script also logging to Postgres for history), and at least one deliberate example of Gateway-scope vs. Client-scope logic side by side, so the difference is visible rather than theoretical.

## Phase 2 — QR wristbands + mobile check-in

**Goal:** scan a QR code on a printed wristband with a phone running the Perspective mobile app, and have it pull up that patient's chart.

What you'll learn: how Perspective's mobile app differs from the web client, QR/barcode scanning components in Perspective, and how you encode a stable patient identifier into a QR code (a URL-safe token tied to the patient's tag/row, not just their name). You'll generate the actual QR images with a small Python script — a good first taste of scripting *outside* Ignition that feeds data *into* it.

## Phase 2.5 — Tag Historian (new)

**Goal:** get real exposure to time-series storage, and an honest opinion on when it beats a plain relational table.

What you'll learn: configuring a Tag Historian provider (Maker Edition includes the Historian Core and SQL Historian modules, so this is fully available), historizing the vitals tags from Phase 1.5, and querying history back out (`system.tag.queryTagHistory`) to build a simple "vitals over time" chart for a patient's stay. Deliberately revisit the Phase 1 vitals table here and compare: what does the historian give you for free (interpolation, easy time-range queries, built-in charting components) that a hand-rolled table doesn't, and where does a plain table still make more sense (one-time facts like discharge instructions)?

## Phase 3 — The tilt-sensor medication screen

**Goal:** the "drinking beer app" effect — tilt the phone, medication administers, something animates.

What you'll learn: Perspective's device orientation / accelerometer bindings (available in the mobile app, not the web client), expression bindings that map tilt angle to an animated property (rotation, fill level, position), and debouncing/thresholding logic so it registers a deliberate tilt rather than every wobble.

## Phase 4 — The simulation API (patients "calling in")

**Goal:** a separate backend service that decides which stuffed animal shows up next, with a photo and a complaint, so she isn't just clicking through a static list.

What you'll learn: building a small REST API (Python, FastAPI is the natural pick), API design (what does "a new patient arrived" look like as an endpoint?), and how Ignition calls out to an external HTTP API from a Jython script (`system.net.httpClient`) or how the API calls into Ignition instead (Ignition's Web Dev module, or writing straight to Postgres/Tags and letting Ignition poll or subscribe).

## Phase 5 — MQTT

**Goal:** get real exposure to the messaging pattern that underpins most modern industrial Ignition deployments, in a context low-stakes enough to break repeatedly.

What you'll learn: MQTT pub/sub concepts (topics, QoS, retained messages), running a broker (Mosquitto, already in `docker-compose.yml`), and Ignition's MQTT story specifically — the native path is Cirrus Link's MQTT Engine/Transmission modules. One thing to sanity-check when you get here: there's at least one reported Maker Edition + 8.3 compatibility hiccup with Cirrus Link's modules — worth a quick forum check before relying on it. A natural use here: the simulation API (Phase 4) publishes "new patient arrived" over MQTT instead of a database poll, and Ignition subscribes and reacts in real time.

## Phase 6 — Kafka

**Goal:** exposure to event streaming at a different layer than MQTT — Kafka is not a drop-in replacement for MQTT, it's a different tool for a different job (durable, replayable event log vs. lightweight pub/sub).

What you'll learn: running Kafka locally (Redpanda is a much lighter single-binary stand-in that speaks the Kafka API), a bridge pattern where MQTT topics feed into Kafka topics (a very real production pattern — MQTT for device/edge messaging, Kafka for durable downstream analytics), and Ignition's own Kafka connectivity for consuming/publishing event streams directly. A good concrete goal: every vitals reading and discharge gets published as an event to Kafka, and a tiny separate consumer script prints a running "shift log."

## Phase 7 — Gateway Network + Project Inheritance (new)

**Goal:** stop treating this as one monolithic Gateway, and build it as a small distributed system — the way most real Ignition deployments actually look.

What you'll learn: **Gateway Network**, Ignition's mechanism for connecting multiple Gateways together (Maker Edition supports up to three concurrently active Gateways, which is exactly enough for this); remote Tag Providers, so one Gateway can see another's tags as if they were local; and **Project Inheritance** — a parent project holding shared logic/theming/UDT definitions, with child projects per department that inherit from it and add their own specifics.

Concretely: split into a `LovieHospital-Reception` Gateway (check-in, QR scanning) and a `LovieHospital-Ward` Gateway (vitals, medication, discharge), each its own Docker container, connected over the Gateway Network, with a shared parent project defining the UDTs and common scripts, and each department's project inheriting from it. This is the single biggest structural change in the whole roadmap — expect it to take real time, and expect to hit real Gateway Network connection/certificate friction, which is itself the point.

## Phase 8 — Redundancy sandbox (new, side-quest)

**Goal:** hands-on exposure to active/standby Gateway failover — with an honest caveat up front.

Maker Edition Gateways are locked to Independent mode; there's no redundancy support, by design. So this phase is explicitly disposable and separate from the real stack: spin up a temporary pair of *unlicensed trial* Gateways (Ignition's default trial mode includes every module, restarting every 2 hours) purely to configure and break an active/standby pair, watch failover happen, and understand the concept — then tear it down. Nothing here is permanent, and nothing here touches Lovie Hospital's real data.

## Phase 9 — Polish

QR-printable wristband templates, an iframe-embedded "hospital dashboard" (embedding an external page, like a simple stats dashboard built outside Ignition, inside a Perspective view), and whatever your daughter asks for after playing with it for a week. Kids are excellent at generating scope.

## Suggested pacing

There's no clock on this, but if you want a rhythm: Phase 0–1 is a single weekend (done). Phase 1.5 is a good next weekend — it changes how you think about the rest of the project, so it's worth not rushing. Phases 2–3 are each roughly a weekend. Phase 2.5 is a short add-on to whichever weekend feels natural. Phases 4–6 are the deep end — treat each as its own multi-session arc. Phase 7 (Gateway Network + inheritance) is the other deep end — probably the single largest phase in the roadmap — and Phase 8 (redundancy) is a contained one-session detour whenever you want a break from the main line.

## Version control note

Every phase's Ignition work (Perspective views, scripts, tag configs, UDT definitions) should live in this git repo, not just in the Gateway's internal project storage. Ignition supports external/version-controllable project structure — set this up soon, ideally before Phase 1.5, so UDTs and tag configs get committed cleanly too. Details in `docs/SESSION-1-SETUP.md`.