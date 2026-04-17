# 💪 PowerFit Gym Management System

A full-stack web application for managing a gym — built with **Flask + SQLite**. Handles member registration, plan management, attendance tracking, admin controls, and Google Sheets export. Designed and deployed for **PowerFit Gym, Pune, Maharashtra**.

---


> Home page with trainer showcase, member dashboard, and admin panel.

| Home Page | Admin Panel | Member Dashboard |
|-----------|-------------|-----------------|
| Trainer showcase + plans | Member table + actions | Attendance + schedule |

---

## ✨ Features

### 🏠 Public Home Page
- Hero section with gym branding and CTA
- Features strip (Strength, Cardio, Nutrition)
- **Trainer Showcase** — real photos of Head Trainer Hari Om with hover effects, glow animations, and a motivational quote banner
- "Why Choose Us" stats section
- Membership plans (Basic / Standard / Premium) with inline join form
- About page (mission, vision, trainers, facilities)
- Contact form with gym location and Google Maps link

### 🔐 Authentication
- Role-based login system: **Admin** and **Member**
- Session-based authentication with Flask sessions
- Default credentials: admin / `1234`, members use full name / `1234`
- Login page with customer/admin role toggle

### 🛡️ Admin Panel
- **Member Management** — tabbed view (All / Active / Expired / Deleted)
- **Add New Member** — inline slide-open form with plan selector (no redirect)
- **Approve / Delete** members
- **Mark Attendance** for active members with one click
- **Check-ins & Revenue** — editable inline inputs for daily summary
- **Post a Notice** — modal to type and publish gym notices (visible on member dashboards)
- **Export to Google Sheets** — copies all member data to clipboard as TSV + downloads CSV backup + opens `sheets.new` in browser. Paste with Ctrl+V for instant import
- Trainer schedule table

### 👤 Member Dashboard
- Membership info (plan, status, expiry date)
- Attendance counter and history chips
- Attendance calendar (FullCalendar)
- Weekly workout schedule
- Progress bars (attendance, streak, plan duration used)
- Gym notices (synced from admin panel via localStorage)
- Quick action buttons

### 📅 Attendance Page (Admin)
- Full calendar view of all member check-ins
- Color-coded attendance events per member

---

## 🗂️ File Structure

```
powerfit/
│
├── main.py                        # Flask app — all routes and DB logic
│
├── gym.db                         # SQLite database (auto-created on first run)
│
├── templates/
│   ├── index.html                 # Home, About, Plans, Contact, Login (SPA-style)
│   ├── admin.html                 # Admin dashboard
│   ├── dashboard.html             # Member dashboard
│   └── attendance.html            # Admin attendance calendar
│
└── static/
    ├── css/
    │   ├── base.css               # Shared: navbar, footer, buttons, layout
    │   ├── index.css              # Home page: hero, plans, trainer showcase, contact
    │   ├── login.css              # Login card and form styles
    │   └── admin.css              # Admin panel: tables, tabs, modals, actions
    │
    └── images/
        ├── trainer1.jpeg          # Trainer photos (Hari Om)
        ├── trainer2.jpeg
        ├── trainer3.jpeg
        └── trainer4.jpeg
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3, Flask |
| **Database** | SQLite 3 (via Python `sqlite3` module) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Fonts** | Google Fonts — Oswald (headings) + Lato (body) |
| **Calendar** | FullCalendar v6.1.8 |
| **Styling** | Custom CSS with CSS variables (no frameworks) |
| **Auth** | Flask sessions |
| **Export** | Clipboard API + CSV Blob download + `sheets.new` |

---

## 🗄️ Database Schema

### `members`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `name` | TEXT | Member full name |
| `age` | INTEGER | Member age |
| `plan` | TEXT | 1 Month / 3 Months / 6 Months / 1 Year |
| `joining_date` | TEXT | YYYY-MM-DD |
| `expiry_date` | TEXT | Auto-calculated from plan |
| `status` | TEXT | `pending` / `active` / `expired` / `deleted` |

### `users`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `username` | TEXT | Member full name or `admin` |
| `password` | TEXT | Plain text (default: `1234`) |
| `role` | TEXT | `admin` or `member` |

### `attendance`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `member_name` | TEXT | Member's full name |
| `date` | TEXT | YYYY-MM-DD |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/powerfit-gym.git
cd powerfit-gym

# 2. Install dependencies
pip install flask

# 3. Run the app
python main.py
```

The app will start at **http://127.0.0.1:5000**

### Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `1234` |
| Member | Member's full name | `1234` |

---

## 📋 Routes Reference

| Method | Route | Description | Access |
|--------|-------|-------------|--------|
| GET | `/` | Home / About / Plans / Login | Public |
| POST | `/login_check` | Authenticate user | Public |
| GET | `/logout` | Clear session | Auth |
| POST | `/add_member` | Register new member | Public / Admin |
| GET | `/admin` | Admin dashboard | Admin |
| GET | `/approve/<id>` | Approve pending member | Admin |
| GET | `/delete/<id>` | Soft-delete member | Admin |
| GET | `/mark_attendance/<id>` | Mark today's attendance | Admin |
| GET | `/dashboard` | Member dashboard | Member |
| GET | `/attendance` | Attendance calendar | Admin |

---

## 📤 Google Sheets Export

Clicking **"Export to Google Sheets"** in the Admin Actions panel:

1. Copies all member data (tab-separated) to clipboard
2. Downloads a `.csv` backup file to your device
3. Opens **sheets.new** in a new browser tab

In the new Google Sheet: click cell **A1** → press **Ctrl+V** (or **⌘V** on Mac) to paste all data instantly.

Columns exported: `#, Name, Age, Plan, Joining Date, Expiry Date, Status`

---

## 🎨 Design System

All styles use CSS custom properties defined in `base.css`:

```css
--orange: #e8521a;       /* Primary accent */
--orange-dark: #c0410f;  /* Hover state */
--black: #1a1a1a;        /* Backgrounds, navbars */
--dark: #2d2d2d;         /* Text */
--grey: #f5f5f5;         /* Page backgrounds */
--mid: #666;             /* Secondary text */
--white: #ffffff;
--font-head: 'Oswald', sans-serif;
--font-body: 'Lato', sans-serif;
```

---

## 🔮 Possible Future Improvements

- [ ] Member photo uploads
- [ ] WhatsApp / SMS notifications on plan expiry
- [ ] Online payment integration (Razorpay)
- [ ] Automated Google Sheets sync via Google Sheets API + Service Account
- [ ] Multi-gym / branch support
- [ ] Mobile app (React Native / Flutter)
- [ ] Diet plan generator per member

---

## 👨‍💻 Built By
laksh bethariya 
linkedin:https://www.linkedin.com/in/laksh-bethariya/
