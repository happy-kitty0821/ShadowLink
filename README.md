<h1 align="center" style="color:#4B5563; font-size:3rem;">
  🕶️ ShadowLink
</h1>
<p align="center" style="font-size:1.2rem;">
  <em>Stealthy. Modular. Python-powered C2 framework built with Django for Red Team simulations.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Built%20With-Django-green" />
  <img src="https://img.shields.io/badge/Language-Python-blue" />
  <img src="https://img.shields.io/badge/Use-Ethical%20Hacking-red" />
</p>

---

<style>
  h2 {
    color: #4B5563;
    font-size: 1.5rem;
    border-bottom: 2px solid #E5E7EB;
    padding-bottom: 4px;
  }

  ul {
    line-height: 1.6;
  }

  code {
    background: #F3F4F6;
    padding: 2px 4px;
    border-radius: 4px;
  }
</style>

## 🚀 Overview

**ShadowLink** is a mid-tier Command & Control (C2) framework designed for Red Team simulations. Built using the Django framework, it enables ethical hackers and security researchers to simulate advanced post-exploitation tactics in a secure and modular environment.

---

## 🛠️ Features

> ✅ Mid-complexity project scope with support for expanding into advanced features.

- 🔐 Agent Registration with UID + Host Details
- 🧠 Modular Command Execution (Server to Agent)
- 📸 Screenshot Capture (Agent to Server)
- 🖥️ Live Screenshot Feed (MJPEG or interval-based refresh)
- ⌨️ Keystroke Logging (via `pynput`)
- 📂 File Upload / Download System
- 🌍 Agent Geolocation Mapping (IP-based)
- 🕵️ Beacon Interval + Jitter Support
- 🧩 Web Dashboard for Operator Control
- 🧪 Command Output Tracking & History
- 🔑 AES-Encrypted Comms Channel
- 🧰 Dockerized Development & Deployment (optional)
- 📦 REST API for Agent Communication

---

## ⚙️ Requirements

- Python 3.9+
- Django 4.x
- Django REST Framework
- Celery + Redis (for async tasks)
- PostgreSQL or SQLite (for dev)

---

## 📁 Project Structure

```bash
ShadowLink/
├── Project/           # Django project core
├── control/            # Agent, command & file logic
├── agent/              # Python agent scripts
├── templates/          # Dashboard UI
├── static/             # JS, CSS, Images
├── api/                # REST & WebSocket endpoints
└── README.md
