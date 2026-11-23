# MindBalance Tracker

A Full Stack Django + PostgreSQL (Supabase) web application that helps university students track daily wellness metrics and visualize weekly stress and sleep trends with role-based access control.

## Features Implemented
### Standard Features (Project Development 1)
- Account Registration, Login, and Logout (Django Auth with password hashing)
- Role-Based User Dashboards (University Student vs. System Administrator)
- User Profile Management

### Core Feature (Project Development 2 – Vertical Slice)
- **Daily Wellness Logging (Full CRUD):** Authenticated students can create, view, edit, and delete daily wellness logs (sleep hours, mood, stress level 1–10, academic workload 1–10, stress triggers, and reflection notes) persisted in Supabase PostgreSQL.
- **Relational Data & Validation:** Uses `ForeignKey` to `User` and `ManyToManyField` to `StressTrigger`. Enforces one log per student per day, blocks future dates, validates numeric ranges, and restricts viewing/editing/deleting strictly to the record owner.
- **Weekly Trends & Role-Based Analytics:** Students view summary metrics and a 7-day interactive Chart.js trend graph; Administrators access anonymized, system-wide wellness statistics.

## Setup Steps
1. Clone the repository and navigate into the project folder:
   ```powershell
   git clone [https://github.com/CatOfMoonVeil/MindBalance-Radaza-Gyro-G06.git](https://github.com/CatOfMoonVeil/MindBalance-Radaza-Gyro-G06.git)
   cd MindBalance-Radaza-Gyro-G06