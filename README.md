# Git Green Daily Contribution Generator

Automated daily Git commits to keep your GitHub contribution graph active and green.

---

## How It Works

GitHub credits contributions to your profile graph when:
1. Commits are pushed to the repository's **default branch** (`main`).
2. The commit author email matches your **verified GitHub email** (`isreeharim@gmail.com`).

There are two ways to run this:
- **Option 1 (Recommended): GitHub Actions** &mdash; Runs automatically in the cloud every day on a schedule. Your computer doesn't even need to be switched on.
- **Option 2: Local Windows Task Scheduler** &mdash; Runs on your local machine using PowerShell.

---

## Option 1: Setup via GitHub Actions (Cloud - Recommended)

### Step 1: Create a GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Name the repo (e.g. `gitgreen` or any name you prefer).
3. Set visibility to **Public** or **Private**.
   > *Note: If private, ensure "Private contributions" is enabled in your GitHub profile settings (`Settings > Profile > Contribution settings > Include private contributions`).*
4. Do **not** initialize with a README, .gitignore, or license (we already have local files).
5. Click **Create repository**.

### Step 2: Push Local Files to GitHub
Run the following in PowerShell from this folder:
```powershell
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

### Step 3: Enable Write Permissions for GitHub Actions
1. On your GitHub repository page, click **Settings**.
2. In the left sidebar, click **Actions** &rarr; **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Check **Allow GitHub Actions to create and approve pull requests**.
6. Click **Save**.

### Step 4: Test Trigger
1. Go to the **Actions** tab on your GitHub repository.
2. Click **Daily Contribution Generator** in the left menu.
3. Click the **Run workflow** dropdown button, then click **Run workflow**.
4. Once completed, check your GitHub profile page to see your green contribution square!

The action is set to run automatically every day at 04:30 UTC (`10:00 AM IST`), picking a random number between **20 and 25 commits** each day with natural timestamps and commit messages.

---

## Option 2: Setup Local Daily Task (Windows Task Scheduler)

If you prefer to run it locally on your PC:

1. You can manually run:
```powershell
.\autocommit.ps1
```
2. Or register a daily task with Windows Task Scheduler:
```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$PSScriptRoot\autocommit.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At "10:00AM"
Register-ScheduledTask -TaskName "GitGreenDailyCommit" -Action $action -Trigger $trigger -Description "Daily Git Commit to GitGreen (20-25 commits)"
```
