def create_settings():
    with open("settings.ini", mode="w") as file:
        file.write("""[SERVER]
host = localhost
port = 8000

[LOGGING]
level = WARNING
backup_bytes = 1000000
backup_count = 3""")