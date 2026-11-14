NOVACARE V1.7

Keep your existing novacare.db beside app.py. Do not delete it.
Install: py -m pip install -r requirements.txt
Run: py -m streamlit run app.py

Dashboard now displays the astronaut portrait from the SQLite photo BLOB in a framed card.
Wearable Devices has Start 30-second demo simulation / Stop demo simulation controls.
Assign a registered wearable to an astronaut, then start the simulator. Fictional HR, SpO2, temperature, respiration, blood pressure and stress samples are saved every 30 seconds and labelled SIMULATION.
This is test data only, not real sensor data or medical guidance. Real sensor packets should use the authenticated receiver integration.
