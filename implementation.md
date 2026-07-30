# PRIME REMOTE D - Implementation Guide

## Complete Build Documentation

---

## Environment Variables

### Backend (.env)

```bash
TELEGRAM_BOT_TOKEN=8958521787:AAGE21Ek9wvlRUbN6Ie59NHuNBSul1vbw_4
ALLOWED_TELEGRAM_USER_IDS=7775013617
API_KEY=your_generated_api_key_here
```

### Agent (config.json)

```json
{
    "device_id": "home-pc",
    "device_name": "Office PC",
    "api_key": "same_api_key_as_backend",
    "backend_url": "https://your-app.onrender.com"
}
```

---

## Step 1: Backend Deployment

### 1.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Create new Web Service
4. Connect your GitHub repo

### 1.2 Configure Environment Variables
In Render Dashboard:
- Go to Environment tab
- Add these variables:
  - `TELEGRAM_BOT_TOKEN` = `8958521787:AAGE21Ek9wvlRUbN6Ie59NHuNBSul1vbw_4`
  - `ALLOWED_TELEGRAM_USER_IDS` = `7775013617`
  - `API_KEY` = generate a random 32-char string

### 1.3 Deploy
Render auto-deploys from your repo. The `render.yaml` handles build configuration.

### 1.4 Set Telegram Webhook
After deployment, visit:
```
https://your-app.onrender.com/set-webhook
```
This registers your bot with Telegram.

---

## Step 2: Agent Setup (Windows)

### 2.1 Install Python
1. Download Python 3.13+ from https://python.org
2. During installation, check "Add Python to PATH"

### 2.2 Copy Agent Files
Copy the entire `agent/` folder to your Windows PC.

### 2.3 Configure Agent
Edit `config.json`:
```json
{
    "device_id": "home-pc",
    "device_name": "Office PC",
    "api_key": "YOUR_API_KEY",
    "backend_url": "https://your-app.onrender.com"
}
```

### 2.4 Install Dependencies
Open Command Prompt in agent folder:
```cmd
pip install -r requirements.txt
```

### 2.5 Test Agent
```cmd
python agent.py
```
You should see "Agent started" message.

### 2.6 Install Auto-Start
```cmd
install.bat
```
This creates a Windows Task Scheduler task that runs the agent on login.

### 2.7 Start Agent
```cmd
start.bat
```
This starts the agent in background (no console window).

---

## Step 3: Telegram Commands

### Available Commands

| Command | Description |
|---|---|
| `/start` | Show main menu |
| `⚡ Power` | Power submenu |
| `🔴 Shutdown` | Shutdown PC |
| `🟡 Restart` | Restart PC |
| `🔵 Sleep` | Sleep PC |
| `🟢 Lock` | Lock PC |
| `📸 Screenshot` | Capture screenshot |
| `📊 System` | System information |

---

## Step 4: Testing

### 4.1 Test Backend Health
Visit: `https://your-app.onrender.com/health`

### 4.2 Test Agent Connection
Check agent logs in `logs/agent.log`

### 4.3 Test Commands
1. Open Telegram
2. Find your bot: `@PRIME_RemoteD_bot`
3. Send `/start`
4. Test each command

---

## Troubleshooting

### Agent Not Connecting
- Check `config.json` has correct `backend_url`
- Verify `api_key` matches backend's `API_KEY` env var
- Check Windows Firewall allows Python

### Commands Not Executing
- Check agent logs: `logs/agent.log`
- Verify backend has correct `ALLOWED_TELEGRAM_USER_IDS`
- Ensure Telegram user ID is correct (7775013617)

### Backend Not Responding
- Check Render logs
- Verify all environment variables are set
- Test `/health` endpoint

---

## API Reference

### POST /telegram/webhook
Receives Telegram updates.

### GET /commands?device_id={id}&timeout=30
Long polling endpoint. Agent polls this every 30 seconds.

### POST /result
Agent sends command execution result.

### GET /health
Returns backend status.

---

## Security Notes

1. **API Key**: Keep secret, never share
2. **Telegram ID**: Only your ID (7775013617) is whitelisted
3. **HTTPS**: All communication encrypted
4. **No Shell**: Commands are predefined, no raw shell access

---

## Performance

| Metric | Target | Actual |
|---|---|---|
| RAM | < 30 MB | ~15 MB |
| CPU Idle | < 1% | ~0.5% |
| Startup | < 3 sec | ~2 sec |
| Latency | 1-3 sec | ~1.5 sec |

---

## Version History

- **v1.0**: Initial release with power commands, screenshot, system info
- **v2.0** (planned): Webcam, microphone, process manager, multi-device

---

## Support

For issues, check:
1. Backend logs on Render
2. Agent logs in `logs/agent.log`
3. Telegram bot API status
