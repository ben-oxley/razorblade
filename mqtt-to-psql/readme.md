# Quick Setup
### Make the script executable:

```bash
chmod +x mqtt_to_postgres.py
```

### Test it manually with uv

```bash
uv run mqtt_to_postgres.py
```

### Enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mqtt_bridge.service
sudo systemctl start mqtt_bridge.service
```
