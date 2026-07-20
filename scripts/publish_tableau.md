# Publish Anshivya Tableau Dashboard

Tableau Public does **not** run on Linux. You publish once from **Windows or Mac**, then the Flask app embeds it automatically.

## What is already prepared

| File | Purpose |
|------|---------|
| `Anshivya Churn Visualisation.twb` | Workbook renamed from the original; data path points to `data/train.csv` |
| `data/train.csv` | Bank churn dataset (copy for Tableau) |
| `templates/visualization.html` | Embeds `AnshivyaChurnVisualisation/Dashboard1` on Tableau Public |

## One-time publish steps

### 1. Install Tableau Public (Windows or Mac)

Download: https://public.tableau.com/en-us/s/download

### 2. Open the workbook

Open **`Anshivya Churn Visualisation.twb`** from this project folder.

If Tableau asks to reconnect the data source, point it to:

```
data/train.csv
```

(in this project folder)

### 3. Customize the dashboard title (optional)

In Tableau: **Dashboard → Title** → set to **"Anshivya — Bank Churn Analytics"**

### 4. Publish to Tableau Public

1. **Server → Tableau Public → Save to Tableau Public**
2. Sign in (create a free account if needed)
3. When asked for the workbook name, use exactly:

   **`AnshivyaChurnVisualisation`**

4. Publish. The dashboard sheet should remain named **`Dashboard 1`**.

### 5. Verify the embed URL

After publishing, open:

https://public.tableau.com/views/AnshivyaChurnVisualisation/Dashboard1

If that loads, your Flask page at `/visualization` will work too.

### 6. Run Flask locally

```bash
cd ~/project/creditpulse/CREDIT-PULSE
source .venv/bin/activate
python app.py
```

Open: http://localhost:9092/visualization

---

## If the embed name differs

If Tableau gives a different workbook name (e.g. `AnshivyaChurnVisualisation` with extra characters), update these lines in `templates/visualization.html`:

```html
<param name='name' value='YOUR_WORKBOOK_NAME/Dashboard1' />
```

Get the exact embed code from Tableau: **Share → Embed Code** on your published viz.

---

## Linux users

You cannot install Tableau Public on Arch/Linux natively. Options:

- Use a Windows/Mac machine once to publish
- Use a Windows VM
- Ask someone with Tableau Public to publish using your `.twb` file

After publishing, Linux is fine — the dashboard loads from Tableau Public in the browser.
