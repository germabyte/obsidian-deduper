# 🧠 Obsidian Duplicate Finder

## 1. Introduction and Purpose

**Obsidian Duplicate Finder** is a standalone desktop application designed to help users identify and remove duplicate or near-duplicate Markdown (`.md`) files in an [Obsidian](https://obsidian.md/) vault. The tool provides a visual interface for:

- Scanning all Markdown files in a selected folder (vault)
- Calculating textual similarity using TF-IDF and cosine similarity
- Grouping similar documents
- Previewing and selectively deleting redundant files

### Problem Statement

Users working extensively in Obsidian or any Markdown-based note-taking system often accumulate redundant notes due to copy-pasting, repeated imports, or overlapping ideas. Manually identifying such duplicates is tedious and error-prone.

### Value Proposition

This application automates the process of duplicate detection, saving time and decluttering knowledge bases. It offers:

- Adjustable similarity threshold
- Real-time file preview
- Batch or individual file deletion with confirmation
- Progress tracking for large vaults

---

## 2. Dependencies (Required Software/Libraries)

The following software and Python libraries are **required** to run the program:

### ✅ Software

- **Python 3.x**  
  Required to run the application.  
  ➤ Download from: [https://www.python.org/downloads](https://www.python.org/downloads)

### ✅ Python Libraries

The following Python libraries are used in this program:

| Library | Description | Install Command |
|--------|-------------|------------------|
| `tkinter` | GUI library (built-in with Python) | *Included by default* |
| `nltk` | Used for English stopword filtering | `pip install nltk` |
| `scikit-learn` | Used for text vectorization and similarity calculation | `pip install scikit-learn` |
| `numpy` | Handles numerical computations and averages | `pip install numpy` |

> ⚠️ After installing `nltk`, make sure stopwords are downloaded by running:
```python
import nltk
nltk.download('stopwords')
```

---

## 3. Getting Started (Installation & Execution)

### 📦 Download the Application

1. Visit the GitHub repository page.
2. Click the green **`<> Code`** button.
3. Select **Download ZIP**.
4. Extract the ZIP file to a location of your choice.

### ▶️ Run the Program

1. Open your terminal or command prompt:
   - **Windows:** Press `Win + R`, type `cmd`, and hit Enter.
   - **macOS:** Open **Terminal** from Applications > Utilities.
   - **Linux:** Use your system terminal.

2. Navigate to the folder where you extracted the program using:
```bash
cd path/to/extracted/folder
```

3. Run the application using:
```bash
python obsidian_duplicate_finder.py
```

---

## 4. User Guide (How to Effectively Use the Program)

### ✅ Step-by-Step Instructions

1. **Launch the Application.**  
   The GUI window will open.

2. **Select Your Obsidian Vault Folder.**  
   Click **“Select Vault Folder”** and choose the folder containing your `.md` files.

3. **Set Similarity Threshold (Optional).**  
   Adjust the percentage slider to set how similar files must be to be considered duplicates. Default is **80%**.

4. **Click “Find Duplicates”.**  
   The program scans your folder and shows duplicate groups in a tree view.

5. **Preview Files.**  
   Click on any file to view its contents on the right.

6. **Delete Files.**  
   - Select individual files or whole groups.
   - Click **“Delete Selected Files”** to remove them permanently after confirmation.

---

## 5. Use Cases and Real-World Examples

### 📘 Use Case 1: Removing Copied Notes from Online Sources
**Scenario:** You imported multiple versions of a note from the web with slight changes.

- **Input:** Two `.md` files with overlapping paragraphs.
- **Action:** Run the tool and set the threshold to 85%.
- **Output:** Both files are flagged in the same group, allowing you to keep the cleaner version.

---

### 🧑‍💻 Use Case 2: Merging Similar Meeting Notes
**Scenario:** You take notes for meetings but forget and create new ones each time.

- **Input:** `meeting_2024.md`, `project_meeting.md`
- **Action:** Tool detects >90% similarity and groups them.
- **Output:** You merge relevant content and delete duplicates.

---

### 📁 Use Case 3: Optimizing Vault Size
**Scenario:** Your vault exceeds cloud sync storage due to redundant notes.

- **Input:** A large folder of 1000+ notes.
- **Action:** Scan with 75% threshold.
- **Output:** Hundreds of similar files grouped, helping you reclaim space.

---

## 6. Disclaimer & Important Notices

- This repository and its contents **may be updated at any time without notice**.
- Updates may render parts of this README outdated.
- No commitment is made to maintain or update the README.
- The software is provided **"as-is"** without any guarantees of performance, compatibility, or correctness.
- Use at your own risk. Always back up your data before deleting files.
