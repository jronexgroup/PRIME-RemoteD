# PRIME REMOTE D - Windows Agent

Lightweight agent that runs on your Windows PC and executes remote commands.

## Quick Start

### Install

```cmd
pip install -r requirements.txt
```

### Configure

Edit `config.json`:

```json
{
    "device_id": "home-pc",
    "device_name": "Office PC",
    "api_key": "YOUR_API_KEY",
    "backend_url": "https://your-app.onrender.com"
}
```

### Run

```cmd
python agent.py
```

### Auto-Start

Run as Administrator:
```cmd
install.bat
```

This creates a Windows Task Scheduler task that starts the agent on login.

## Manual Start

```cmd
start.bat
```

Runs agent in background (no console window).

## Project Structure

```
agent/
├── agent.py              # Main entry
├── config.py             # Config loader
├── api.py                # HTTP client
├── polling.py            # Long polling
├── executor.py           # Command dispatcher
├── logger.py             # Logging setup
├── commands/
│   ├── power.py          # Shutdown/Restart/Sleep/Lock
│   ├── screen.py         # Screenshot
│   └── system.py         # System info
├── config.json           # Device config
├── requirements.txt      # Dependencies
├── install.bat           # Auto-start installer
└── start.bat             # Manual start
```

## Supported Commands

| Command | Description |
|---------|-------------|
| `shutdown` | Shutdown PC |
| `restart` | Restart PC |
| `sleep` | Sleep mode |
| `lock` | Lock workstation |
| `screenshot` | Capture screen |
| `system_info` | System information |

## Logs

Logs are stored in `logs/agent.log` with automatic rotation.

## Troubleshooting

- **Connection failed:** Check `config.json` backend_url
- **Unauthorized:** Verify API key matches backend
- **Auto-start not working:** Run `install.bat` as Administrator
