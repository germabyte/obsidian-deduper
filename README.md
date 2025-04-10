# 🧠 Obsidian Duplicate Finder

## 1. Introduction and Purpose

**Obsidian Duplicate Finder** is a standalone desktop application that helps users identify and remove duplicate or near-duplicate Markdown (`.md`) files from an [Obsidian](https://obsidian.md/) vault. This user-friendly tool:

- Scans all Markdown files in a selected folder (vault)
- Detects duplicates using text similarity
- Previews and compares files side-by-side
- Allows users to delete redundant files with one click

### Problem Statement

Obsidian users often accumulate similar or duplicate notes due to imports, idea repetition, or editing across devices. Manually sorting these is time-consuming and error-prone.

### Value Proposition

This tool streamlines vault organization by automatically identifying similar Markdown files. Users can:

- Control the similarity detection threshold
- Visually inspect matched content
- Selectively delete duplicate files
- Save time and reduce clutter in their note vaults

---

## 2. Dependencies (Required Software/Libraries)

### ✅ Required Software

- **Python 3.x**  
  ➤ Download: [https://www.python.org/downloads](https://www.python.org/downloads)

### ✅ Required Python Libraries

| Library         | Description                                           | Installation Command        |
|----------------|-------------------------------------------------------|-----------------------------|
| `tkinter`      | Used to build the graphical interface                 | *Pre-installed with Python* |
| `nltk`         | Provides stopword filtering for better text matching  | `pip install nltk`          |
| `scikit-learn` | Enables text similarity calculation with TF-IDF       | `pip install scikit-learn`  |
| `numpy`        | Supports numeric operations like averaging            | `pip install numpy`         |

> After installing NLTK, download English stopwords by running:
```python
import nltk
nltk.download('stopwords')
```

---

## 3. Getting Started (Installation & Execution)

### 📦 Download the App

1. Go to the GitHub repository.
2. Click the green **`<> Code`** button.
3. Select **Download ZIP**.
4. Extract the ZIP file to a folder.

### ▶️ Run the Program

1. Open a terminal or command prompt.
2. Navigate to the extracted folder using the `cd` command:
```bash
cd path/to/extracted/folder
```
3. Start the program with:
```bash
python obsidian-deduper.py
```

---

## 4. User Guide (How to Effectively Use the Program)

### 💡 How to Use

1. **Launch the App**  
   The interface will open with controls and an empty results pane.

2. **Select Your Vault Folder**  
   Click **“Select Vault Folder”** and choose the folder containing `.md` files.

3. **Adjust Similarity Threshold (Optional)**  
   The default is 80%. Lower it to catch looser matches, or increase for stricter matches.

4. **Click “Find Duplicates”**  
   The program scans and lists duplicate groups in a tree view.

5. **Review and Compare**  
   Click a file to preview its content on the right pane.

6. **Delete Duplicates**  
   Select individual files or entire groups and click **“Delete Selected Files”**.

---

## 5. Use Cases and Real-World Examples

### 1. 📝 Prevent Duplicate Meeting Notes
- **Situation:** You wrote similar summaries from different days.
- **Solution:** Run the app and it groups them for review.
- **Benefit:** Merge notes and delete redundancy.

### 2. 🗂 Clean Up After Data Imports
- **Situation:** Imported data from another platform multiple times.
- **Solution:** Set a 75% threshold and scan.
- **Benefit:** Easily catch near-duplicate content.

### 3. 📉 Reduce Vault Size Before Sync
- **Situation:** Cloud sync fails due to storage size.
- **Solution:** Delete unnecessary duplicates after reviewing them.
- **Benefit:** Leaner vault and faster syncs.

---

## 6. Disclaimer & Important Notices

- This repository and its contents **may change at any time** without prior notice.
- Updates might render some parts of this README outdated.
- There is **no guarantee** of ongoing maintenance or updates.
- The code is provided **"as-is"**, without any warranties or support.
- Always **back up your files** before deleting any content.
