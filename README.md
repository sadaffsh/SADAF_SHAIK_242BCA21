# 🔬 Lab Equipment Fault Reporting System

A two-page web app built with **Streamlit** and **Supabase** that lets lab users report faulty equipment and gives admins a live dashboard to monitor everything in real time with no refreshing needed.

---

## 📌 Overview

- **Users App** — Lab users can select equipment (Chemistry or Physics lab), view its current status, and mark it as faulty or working.
- **Admin Dashboard** — Admins get a live overview of all equipment with auto-refresh every 5 seconds. No page reload needed.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Frontend / UI |
| Supabase | Database (PostgreSQL) |

---

## 🚀 How to Run

1. **Clone the repo**
   ```bash
   git clone [https://github.com/sadaffsh/SADAF_SHAIK_242BCA21.git]
   cd sadafSE
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit supabase
   ```

3. **Run the Client App**
   ```bash
   streamlit run client.py
   ```

4. **Run the Admin Dashboard**
   ```bash
   streamlit run admin.py
   ```

---

## 📂 Project Structure

```
sadafSE/
├── client.py      # Lab user interface — report faults
└── admin.py       # Admin dashboard — live equipment monitor
```

## 🔗 Hosted App Link

[Users App](https://faulty-equipment-reporter.streamlit.app/)
[Admin App](https://server-faulty-equipment-reporter.streamlit.app/)

