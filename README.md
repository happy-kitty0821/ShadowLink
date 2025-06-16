<h1 align="center">
  🕶️ ShadowLink
</h1>
<p align="center"><em>Stealthy. Modular. Python-powered C2 framework built with Django for Red Team simulations.</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/Built%20With-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Use-Ethical%20Hacking-red?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=happy-kitty0821&label=Profile%20views&color=0e75b6&style=flat" alt="profile-views" />
</p>

---

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
├── control/           # Agent, command & file logic
├── agent/             # Python agent scripts
├── templates/         # Dashboard UI
├── static/            # JS, CSS, Images
├── api/               # REST & WebSocket endpoints
└── README.md
````

---

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=happy-kitty0821&show_icons=true&theme=radical" alt="GitHub Stats" />
</p>

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=happy-kitty0821&theme=radical" alt="GitHub Streak" />
</p>

---

## 👨‍💻 Developer

> **Aayush Wanem**
> 🧑‍🎓 BSc (Hons) Computing — Itahari International College
> 🔗 [LinkedIn](https://www.linkedin.com/in/aayushwanem) | ✉️ [Email](mailto:aayushwanem@gmail.com) | 🌐 [GitHub](https://github.com/happy-kitty0821)

---

## ⚖️ Legal Disclaimer

> This project is intended for **authorized security testing and research purposes only**.
> Unauthorized use of ShadowLink against systems you do not own or have permission to test is **illegal and unethical**.
> The developers are not responsible for any misuse or damage caused by this tool.

---

## 🧩 License

This project is licensed under the [MIT License](LICENSE).

---

<h4 align="center">⚔️ ShadowLink — Observe. Command. Persist.</h4>
```

---
