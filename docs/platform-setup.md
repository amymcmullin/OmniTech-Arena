# Platform setup (CTFd)

These are the notes from the first setup at iTECH (October 2026), including the problems we hit along the way.

## 1. Install CTFd with Docker

```
git clone https://github.com/CTFd/CTFd.git
cd CTFd
docker compose up -d
```

- The site runs at `http://localhost:8000`.
- On a **fresh start**, CTFd can show *"localhost didn't send any data"* for 30–90 seconds while the database initializes. Wait, then reload.
- Every page redirects to `/setup` until the **setup wizard** is finished. That includes `/admin` and `/login`. The account you create in the wizard is the **only** admin. Accounts made with **Register** are always students.

### Starting over
```
docker compose down
Remove-Item -Recurse -Force .data      # Windows PowerShell  (rm -rf .data on Mac/Linux)
docker compose up -d
```

## 2. Loading games: use `tools/deploy.py`, not backup import

- **Use `tools/deploy.py`** (see the main README). It works through CTFd's normal API, so it works on any CTFd version, and it **adds** games without touching existing ones.
- **Don't use Admin → Config → Backup → Import.**
  - It **replaces everything** on the server.
  - It fails across CTFd versions. Our server runs a newer CTFd than the backup was made on, and the import failed partway with `Tablespace is missing for a table`. We had to delete `.data` and start over.
  - CTFd also can't import backups into a SQLite database at all.

## 3. Keep the board grouped by game

**Admin Panel → Config → Theme → Theme Settings** has two boxes. Paste one line into each and click **Update**:

| Box | Paste |
|---|---|
| Challenge Category Order Custom Function | `(a, b) => a.localeCompare(b, undefined, {numeric: true})` |
| Challenge Order Custom Function | `(a, b) => a.value - b.value \|\| a.name.localeCompare(b.name)` |

Categories then sort `01…08` → `OS …` → `SC …` → `UP …`, and challenges inside each category go from lowest to highest points.

## 4. Student accounts (bulk import)

**Admin Panel → Config → Backup → Import CSV → type: Users**

Use [`tracks/helpdesk-cisco-it-support/templates/student_import_template.csv`](../tracks/helpdesk-cisco-it-support/templates/student_import_template.csv). Columns:

| Column | Notes |
|---|---|
| `name` | Display name on the scoreboard (we use first name + last initial). Must be unique. |
| `email` | Login (we use the student's school email). Must be unique. |
| `password` | Temporary password. |
| `change_password` | `true` forces students to choose a new password at first login (recommended). |
| `bracket_id` | Optional. Delete the column if you don't use brackets, because a blank cell rejects the row. |

- Students can log in with either their email or their display name.
- **Never commit real rosters to this repository.** It's public.
- If you edit the CSV in Excel, numeric passwords with leading zeros (e.g. `0101`) lose the zero. Edit the file in a text editor instead.

## 5. Settings we use

| Setting | Value | Why |
|---|---|---|
| User mode | Users (individual) | Self-paced, not team events |
| Start / End | blank | Games are always open |
| Score visibility | Admins only (optional) | With rolling start dates, a newcomer shouldn't be ranked against students who've played for months |
| Brackets | none | Once any bracket exists, CTFd makes **every** student pick one before continuing. Create all brackets at once if you ever use them. |

## 6. Modules and Audiences (newer CTFd only)

Newer CTFd builds have **Modules** (groups of challenges) and **Audiences** (groups of students):

- A challenge in a module is visible **only** to students in an audience that's been granted that module. Challenges that aren't in any module are visible to everyone.
- Students **don't** see a module picker, and only an admin can add a student to an audience.
- So modules work as an *instructor unlock*, not a student menu. iTECH currently leaves all games **outside** modules so students can choose freely.
