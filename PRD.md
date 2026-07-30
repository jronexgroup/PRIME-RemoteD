# PRIME REMOTE D

## Product Requirements Document (PRD) v1.0

---

## 1. Overview

**Product Name:** PRIME REMOTE D

**Version:** 1.0

**Platform:**
- Windows 10 Agent
- Telegram Bot
- FastAPI Backend (Render Free)

**Purpose:**
PRIME REMOTE D is a lightweight, secure remote command system that enables a user to control their Windows PC from anywhere using Telegram.

The system is designed to consume minimal RAM and CPU while remaining responsive through long polling. No database is required in Version 1 because commands are processed in real time.

---

## 2. Objectives

- Control Windows PC remotely
- Low RAM & CPU usage
- No Firebase
- No database
- Secure communication
- Easy deployment
- Easily expandable

---

## 3. System Architecture

```
User
 │
 ▼
Telegram
 │
 ▼
Telegram Bot API
 │
 ▼
FastAPI Backend (Render Free)
 │
 │ Long Polling
 ▼
Windows Python Agent
 │
 ▼
Windows API / Python Scripts
```

---

## 4. Technology Stack

### Backend
- Python 3.13+
- FastAPI
- Uvicorn
- httpx
- Pydantic

### Hosting
- Render Free

### Bot
- Telegram Bot API

### Windows Agent
- Python
- psutil
- pyautogui
- pillow
- pyperclip
- pycaw
- subprocess

### Communication
- HTTPS
- JSON

### Authentication
- API Key
- Device ID
- Telegram User Whitelist

### Database
- None (V1)

---

## 5. Communication Flow

### Command Flow

```
Telegram
    ↓
FastAPI receives webhook
    ↓
Backend validates Telegram user
    ↓
Backend creates command
    ↓
Windows Agent receives command
    ↓
Agent executes command
    ↓
Agent sends result
    ↓
Backend sends Telegram response
```

---

## 6. Long Polling

Instead of heartbeat every 5 seconds:

**Agent sends:**
```
GET /commands?timeout=30
```

**Backend waits for 30 seconds.**
- If no command: Return empty response. Agent immediately reconnects.
- If command exists: Return immediately.

**Benefits:**
- Less bandwidth
- Less CPU
- Less RAM
- Instant response

---

## 7. Agent Startup

When Windows boots, Python Agent starts automatically.

**Steps:**
1. Read config.json
2. Verify API Key
3. Connect backend
4. Register device
5. Start long polling

---

## 8. Device Configuration

### config.json

```json
{
    "device_id": "home-pc",
    "device_name": "Office PC",
    "api_key": "********",
    "backend_url": "https://example.onrender.com"
}
```

---

## 9. API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/telegram/webhook` | POST | Receive Telegram updates |
| `/commands` | GET | Long polling endpoint |
| `/result` | POST | Command execution result |
| `/upload` | POST | Upload screenshots/files |
| `/health` | GET | Health check |

---

## 10. Command Protocol

```json
{
    "id": "cmd_001",
    "type": "shutdown",
    "args": {}
}
```

Every command has:
- `id`
- `type`
- `args`

---

## 11. Result Protocol

```json
{
    "id": "cmd_001",
    "status": "success",
    "message": "Shutdown initiated.",
    "data": {}
}
```

---

## 12. Supported Commands

### Power
- Shutdown
- Restart
- Sleep
- Lock

### Screen
- Screenshot

### Clipboard
- Get Clipboard
- Set Clipboard

### Audio
- Set Volume
- Mute
- Unmute

### Files
- Download File

### Applications
- Open App

### Scripts
- Run Predefined Script

### System
- System Information

---

## 13. Telegram UI

### /start - Main Menu

```
🖥 Devices
⚡ Power
📸 Screenshot
📂 Files
📋 Clipboard
🔊 Volume
⚙ System
```

### Power Menu

```
🔴 Shutdown
🟡 Restart
🔵 Sleep
🟢 Lock
```

---

## 14. Windows Agent Modules

| Module | Purpose |
|---|---|
| agent.py | Main entry |
| config.py | Load configuration |
| api.py | Backend communication |
| polling.py | Long polling |
| executor.py | Command dispatcher |
| power.py | Shutdown, restart, sleep |
| screen.py | Screenshot |
| clipboard.py | Clipboard functions |
| volume.py | Audio control |
| apps.py | Open applications |
| files.py | File upload |
| system.py | System information |
| logger.py | Logging |

---

## 15. Security

- HTTPS only
- Unique API Key
- Device ID validation
- Telegram User ID whitelist
- Command validation
- Execute only predefined commands
- Reject unknown commands
- No direct shell execution from Telegram

---

## 16. Performance Goals

| Metric | Target |
|---|---|
| RAM | < 30 MB |
| CPU Idle | < 1% |
| Startup | < 3 seconds |
| Command Latency | 1-3 seconds |

---

## 17. Error Handling

| Error | Action |
|---|---|
| Unknown command | Return "Unsupported command" |
| Execution failure | Return error message |
| Backend offline | Retry with exponential backoff |

---

## 18. Logging

Store:
- Startup
- Shutdown
- Commands
- Errors

Rotate logs automatically.

---

## 19. Future Roadmap

### Version 2
- Webcam Capture
- Microphone Recording
- Process Manager
- Task Manager
- File Explorer
- Multi-device Support
- Device Groups
- Notifications
- Update Agent
- Remote Terminal (restricted)
- Flutter Mobile App

---

## 20. Project Structure

```
prime-remote-d/
├── backend/
│   ├── main.py
│   ├── telegram.py
│   ├── auth.py
│   ├── routes/
│   ├── services/
│   └── models/
├── agent/
│   ├── agent.py
│   ├── api.py
│   ├── polling.py
│   ├── executor.py
│   ├── power.py
│   ├── screen.py
│   ├── volume.py
│   ├── clipboard.py
│   ├── files.py
│   ├── apps.py
│   ├── system.py
│   ├── logger.py
│   └── config.json
├── requirements.txt
└── README.md
```

---

## 21. Success Criteria

- PC responds from anywhere with internet access
- Commands execute within a few seconds
- Low resource consumption during idle
- Secure command execution
- Stable long polling
- Easy deployment on Render Free

---

## Final Vision

PRIME REMOTE D is designed as a lightweight, secure, and extensible remote management platform. Version 1 focuses on reliable remote command execution through Telegram, while laying the foundation for future expansion into a complete remote device management ecosystem supporting multiple operating systems and richer control capabilities.
