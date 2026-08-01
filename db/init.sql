-- target path in your repo: db/init.sql
--
-- Runs automatically on first Postgres container start (mounted to
-- /docker-entrypoint-initdb.d/ in docker-compose.yml). If you change this
-- file after the container has already initialized once, you'll need to
-- `docker compose down -v` to wipe the volume and re-run it.

-- ============================================================
-- Patients: the stuffed animal roster
-- ============================================================
CREATE TABLE patients (
    patient_id      SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    species         TEXT NOT NULL,           -- e.g. 'bear', 'bunny', 'dinosaur'
    photo_url       TEXT,                    -- fill in later, or leave null for now
    default_quirks  TEXT,                    -- flavor text: "always says his ear hurts"
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- Visits: one row per hospital stay, from check-in to discharge
-- ============================================================
CREATE TABLE visits (
    visit_id                SERIAL PRIMARY KEY,
    patient_id              INTEGER NOT NULL REFERENCES patients(patient_id),
    qr_token                TEXT UNIQUE NOT NULL,   -- the value encoded in the wristband QR code
    chief_complaint         TEXT,                   -- why they came in, e.g. "tummy ache"
    status                  TEXT NOT NULL DEFAULT 'checked_in'
                                CHECK (status IN ('checked_in', 'in_treatment', 'discharged')),
    checked_in_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    discharged_at           TIMESTAMPTZ,
    discharge_instructions  TEXT
);

CREATE INDEX idx_visits_qr_token ON visits(qr_token);
CREATE INDEX idx_visits_status ON visits(status);

-- ============================================================
-- Vitals: repeated readings during a visit
-- ============================================================
CREATE TABLE vitals (
    vitals_id       SERIAL PRIMARY KEY,
    visit_id        INTEGER NOT NULL REFERENCES visits(visit_id),
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    temperature_f   NUMERIC(5,1),
    heart_rate_bpm  INTEGER,
    mood            TEXT,     -- e.g. 'happy', 'sleepy', 'grumpy', 'scared' — button-driven, not free text, in the UI
    notes           TEXT
);

CREATE INDEX idx_vitals_visit_id ON vitals(visit_id);

-- ============================================================
-- Medications: administered during a visit (Phase 3 tilt-screen writes here)
-- ============================================================
CREATE TABLE medications_administered (
    medication_id     SERIAL PRIMARY KEY,
    visit_id          INTEGER NOT NULL REFERENCES visits(visit_id),
    administered_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    medication_name   TEXT NOT NULL,
    dose              TEXT,
    method            TEXT DEFAULT 'tilt-administered'
);

CREATE INDEX idx_medications_visit_id ON medications_administered(visit_id);

-- ============================================================
-- Seed data: the initial patient roster
-- Edit this list to match your daughter's actual stuffed animals.
-- ============================================================
INSERT INTO patients (name, species, default_quirks) VALUES
    ('Mr. Snuggles',  'bear',      'always says his ear hurts'),
    ('Hopper',        'bunny',     'hops even when told to rest'),
    ('Rex',           'dinosaur',  'roars when scared of the thermometer'),
    ('Waddles',       'penguin',   'insists on an ice pack for everything'),
    ('Sir Barksalot', 'dog',       'wags tail during vitals, throws off the heart rate reading');
