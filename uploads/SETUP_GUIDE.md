# Auup Self-Hosted Setup Guide
## Upload 25 designs/day with your own Firebase + local backend

---

## What You Get

| Feature | Original | Self-Hosted |
|---|---|---|
| Daily upload limit | 5 | **25** (change freely in `.env`) |
| Auto-fill tags | Paid only | **Unlocked** |
| Data storage | Auup's servers | **Your Firebase** |
| Backend | Auup's cloud | **Your local Node.js** |
| Subscription required | Yes | **No** |

---

## Prerequisites

- Node.js 18+ installed  →  https://nodejs.org
- A Google account (for Firebase)
- Google Chrome browser

---

## STEP 1 — Create Your Firebase Project

### 1.1 — Create the project

1. Go to https://console.firebase.google.com
2. Click **"Create a project"**
3. Enter a name, e.g. `auup-mine`
4. Disable Google Analytics (optional, click Continue)
5. Click **"Create project"** → wait ~30 seconds → **Continue**

---

### 1.2 — Enable Firebase Authentication

1. In the left sidebar click **Build → Authentication**
2. Click **"Get started"**
3. Under "Sign-in method" tab, click **Email/Password**
4. Toggle **"Enable"** → Save

---

### 1.3 — Enable Firestore Database

1. In the left sidebar click **Build → Firestore Database**
2. Click **"Create database"**
3. Select **"Start in production mode"** → Next
4. Choose a region closest to you (e.g. `us-central1`) → **Enable**
5. Wait for it to initialize

---

### 1.4 — Enable Firebase Storage

1. In the left sidebar click **Build → Storage**
2. Click **"Get started"**
3. Select **"Start in production mode"** → Next
4. Choose the same region as Firestore → **Done**

---

### 1.5 — Get Your Web App Config (for the extension)

1. In Firebase Console, click the **gear icon ⚙️** next to "Project Overview"
2. Click **"Project settings"**
3. Scroll down to **"Your apps"** section
4. Click **"Add app"** → select the **Web** icon `</>`
5. Give it a nickname: `auup-extension` → click **"Register app"**
6. You'll see a config block like:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "auup-mine.firebaseapp.com",
  projectId: "auup-mine",
  storageBucket: "auup-mine.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890abcdef",
  measurementId: "G-XXXXXXXXXX"
};
```

**Copy this entire block — you need it in Step 3.**

---

### 1.6 — Get Service Account Key (for the backend)

1. Still in **Project Settings**, click the **"Service accounts"** tab
2. Click **"Generate new private key"** → **"Generate key"**
3. A `.json` file downloads — keep it safe, **never share it**
4. Open the file and note these three values:
   - `"project_id"`
   - `"client_email"`
   - `"private_key"` (the long string starting with `-----BEGIN PRIVATE KEY-----`)

---

## STEP 2 — Set Up the Backend

### 2.1 — Install dependencies

```bash
cd auup-selfhosted/backend
npm install
```

### 2.2 — Edit `.env`

Open `backend/.env` and fill in your values:

```env
# From your service account JSON file:
FIREBASE_PROJECT_ID=auup-mine
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxx@auup-mine.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BA...\n-----END PRIVATE KEY-----\n"
FIREBASE_STORAGE_BUCKET=auup-mine.appspot.com

# Change this to whatever limit you want:
DAILY_UPLOAD_LIMIT=25

PORT=3000
```

> **Important about the private key:**  
> Copy the entire private key from the JSON file.  
> Replace all actual newlines with `\n` so it fits on one line.  
> Keep the surrounding double-quotes.

### 2.3 — Start the backend

```bash
node server.js
```

You should see:
```
🚀 Auup self-hosted backend running on http://localhost:3000
📋 Daily upload limit: 25 designs/day
🔥 Firebase project: auup-mine
```

**Leave this terminal open while using the extension.**

---

## STEP 3 — Patch the Extension with Your Firebase Config

### 3.1 — Open `run-me-once.js`

It's inside the `extension-patched/` folder. Open it in any text editor and fill in:

```javascript
const YOUR = {
  FIREBASE_API_KEY: "AIzaSyXXXXXXXXXXXXX",      // from Step 1.5
  PROJECT_ID: "auup-mine",                         // your project ID
  MESSAGING_SENDER_ID: "123456789012",             // from Step 1.5
  APP_ID: "1:123456789012:web:abcdef...",          // from Step 1.5
  MEASUREMENT_ID: "G-XXXXXXXXXX",                  // from Step 1.5
};
```

### 3.2 — Run the script

```bash
cd extension-patched
node run-me-once.js
```

Output:
```
✅ js/home.js patched with your Firebase config!
   Now load the extension folder in Chrome.
```

---

## STEP 4 — Load the Extension in Chrome

1. Open Chrome and go to `chrome://extensions`
2. Toggle **"Developer mode"** ON (top right)
3. Click **"Load unpacked"**
4. Browse to and select the `extension-patched/` folder
5. The Auup icon appears in your toolbar

---

## STEP 5 — First Run

1. Click the Auup icon → the dashboard opens
2. Click **Sign Up** and create an account  
   *(This uses your own Firebase Auth — no data goes to Auup's servers)*
3. Check your email for verification, click the link
4. Sign in
5. Go to **Redbubble Store** tab → **Add Redbubble Store**
6. Log in to Redbubble in the popup tab
7. Auup detects your account and adds it

---

## STEP 6 — Configure Upload Schedule

In the extension, go to your store's **Schedule Setting**:

| Setting | Recommended |
|---|---|
| Number of designs to upload | 25 |
| Waiting time between uploads | 5 minutes (300 seconds) |

This gives a **perfect spread**: 25 uploads over ~2 hours.

> To change the default in code: in `backend/.env` change `DAILY_UPLOAD_LIMIT=25`.  
> To change interval: the extension UI lets you set minutes between uploads.  
> **Minimum recommended interval: 3 minutes** to avoid Redbubble rate-limiting.

---

## How to Change the Daily Limit

Edit **one line** in `backend/.env`:

```env
DAILY_UPLOAD_LIMIT=50   # or any number you want
```

Then restart the backend (`Ctrl+C` then `node server.js`).

The extension Dashboard will automatically show the new limit the next time it loads your profile.

---

## Firestore Data Structure

Your data is stored in Firestore under these collections:

```
users/
  {email}/
    email, name, plan, todayUploaded, todayDate

accounts/
  {email}_{redbubbleAccountId}/
    email, providerAccountId, name, status
    images[]          ← upload queue
    uploaded_images[] ← history
    schedule: { break_time, daily_upload }
    productSetting: { ... }
```

You can view and edit all data in the Firebase Console → Firestore.

---

## Troubleshooting

**Extension shows "Failed to fetch profile"**  
→ Make sure the backend is running (`node server.js` in `backend/` folder)  
→ Check `chrome://extensions` → Auup → Errors — look for CORS or network errors

**"You reached daily upload limit" still appears**  
→ Your backend's `/auth/check-remaining-upload` is being called correctly  
→ Check the backend console — it logs every request  
→ The limit resets at midnight UTC. Or manually edit Firestore: `users/{email}.todayUploaded = 0`

**Firebase auth errors on sign-up**  
→ Double-check you ran `node run-me-once.js` with the correct API key  
→ Verify Email/Password sign-in is enabled in Firebase Console → Authentication

**Extension says "Account not found" after login**  
→ Make sure the backend is running when you add the Redbubble store  
→ Check Firestore → `accounts` collection — your account should appear there

**Upload fails mid-way**  
→ The extension opens a real Chrome tab and fills in the Redbubble upload form  
→ Check that you're logged in to Redbubble  
→ Redbubble may have changed their UI — this is the same limitation as the original extension

---

## Running the Backend Automatically (Optional)

If you want the backend to start automatically when your computer boots:

**On Mac/Linux** — add to crontab:
```bash
@reboot cd /path/to/auup-selfhosted/backend && node server.js >> /tmp/auup.log 2>&1
```

**Or use PM2:**
```bash
npm install -g pm2
cd backend
pm2 start server.js --name auup-backend
pm2 save
pm2 startup   # follow the printed command
```

---

## Summary of All Changes Made to the Extension

| File | Change |
|---|---|
| `js/home.js` | API URLs → `localhost:3000` |
| `js/home.js` | Firebase config → your project |
| `js/home.js` | Default daily_upload `5` → `25` |
| `js/home.js` | Limit fallback `5` → `25` |
| `js/home.js` | Max queue = `10 × daily_limit` (was 5×) |
| `js/home.js` | Auto-fill tags — unlocked from paid plan |
| `js/background.js` | API URL → `localhost:3000` |
| `manifest.json` | Added `http://localhost/*` to host_permissions |
| `manifest.json` | CSP updated to allow localhost connections |
