# NOVACARE V1.3 – Mission Control UI + Astronaut CRUD

## Install / run
```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Important database note
Keep your existing `novacare.db` in the same folder as `app.py`. Do not delete it; it contains your astronaut profiles, readings, and wearable registrations. This update uses the existing table structure.

## Hosted deployment
For Streamlit Community Cloud, deploy `app.py` from the repository root and set these in the app's Secrets settings:

```toml
NOVACARE_ADMIN_USER = "choose-an-operator-name"
NOVACARE_ADMIN_PASSWORD = "choose-a-long-unique-password"
```

Do not commit deployment credentials or `novacare.db`. The database contains profiles and health readings. Community Cloud does not guarantee persistence of files stored on the app server, so this setup is for demos only; do not enter real health data.

## What's updated
- Dark navy / neon-cyan mission-control visual style inspired by the supplied reference.
- Responsive hero banner and dark input fields.
- Dashboard profile card displays the astronaut's uploaded portrait and medical summary.
- Astronaut Management supports adding, editing, replacing portrait, and deleting profiles.
- Deleting an astronaut also deletes their health records and sets their registered wearables to Unassigned. The delete action requires a confirmation checkbox.
- Existing analytics, alerts, health history, wearable registration and receiver files are retained.

## Health / safety
This is an educational prototype. Alert flags are personal-baseline trend indicators, not validated age-specific clinical thresholds, diagnosis, or emergency triage. Test wearable sensors against appropriate reference instruments before relying on readings.
