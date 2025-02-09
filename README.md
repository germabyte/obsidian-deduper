# obsidian-deduper

A graphical application designed to identify and manage duplicate Markdown files within an Obsidian vault. This tool efficiently scans your vault, compares file contents based on text similarity, and groups files that are duplicates or nearly identical. It is ideal for anyone looking to keep their Obsidian vault organized and free of redundant content.

---

## 1. Introduction and Purpose

**Introduction:**  
obsidian-deduper is a user-friendly desktop application built with Python and Tkinter. It scans your Obsidian vault for duplicate Markdown files by analyzing the contents and calculating their similarity using advanced text processing techniques.

**Purpose:**  
- **Problem Solved:** Helps identify and clean up duplicate or similar files that may clutter your vault.  
- **Value Proposition:**  
  - Simplifies vault maintenance by automatically detecting duplicates.  
  - Saves time and reduces manual effort when organizing notes.  
  - Provides a clear visual interface to preview and delete duplicates safely.

---

## 2. Dependencies (Required Software)

The following software and libraries are required to run obsidian-deduper:

- **Python 3.6 or Higher**  
  - **Description:** The programming language used to develop this application.  
  - **Installation:** Download and install Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

- **Tkinter**  
  - **Description:** A standard GUI toolkit for Python that creates the application's graphical interface.  
  - **Installation:**  
    - Windows and macOS: Usually comes pre-installed with Python.  
    - Linux: Install via your package manager (e.g., `sudo apt-get install python3-tk`).

- **scikit-learn**  
  - **Description:** Library used for computing text similarities using techniques like TF-IDF and cosine similarity.  
  - **Installation:**  
    ```bash
    pip install scikit-learn
    ```

- **NumPy**  
  - **Description:** Provides support for large, multi-dimensional arrays and matrices along with a collection of mathematical functions.  
  - **Installation:**  
    ```bash
    pip install numpy
    ```

- **nltk (Natural Language Toolkit)**  
  - **Description:** Helps in processing and cleaning text data, especially for removing stopwords.  
  - **Installation:**  
    ```bash
    pip install nltk
    ```  
  - **Additional Setup:** The program will automatically download the NLTK stopwords. If needed, this can also be triggered manually with:  
    ```bash
    python -m nltk.downloader stopwords
    ```

---

## 3. Getting Started (Installation and Execution)

### Downloading the Code

1. Navigate to the obsidian-deduper GitHub repository page.
2. Click the green **`<> Code`** button.
3. Select **`Download ZIP`** from the dropdown menu.
4. Save the ZIP file to a preferred location on your computer.

### Extracting the ZIP

- **Windows:** Right-click on the downloaded ZIP file and choose **"Extract All..."**.  
- **macOS:** Double-click the ZIP file to automatically extract its content.  
- **Linux:** Use your file manager’s extract option or run the command:  
  ```bash
  unzip obsidian-deduper.zip
  ```

### Running the Program

1. Open a terminal (Command Prompt on Windows or Terminal on macOS/Linux).
2. Change the directory to the extracted repository folder using the `cd` command. For example:
   ```bash
   cd path/to/obsidian-deduper
   ```
3. Execute the program by running:
   ```bash
   python obsidian-deduper.py
   ```
4. The graphical interface will launch, displaying the "Obsidian Duplicate Finder" window.

---

## 4. Using the Program (User Guide)

Once the program is running, follow these steps to detect and manage duplicate files:

1. **Select Vault Folder:**  
   - Click the **"Select Vault Folder"** button.
   - In the dialog that appears, navigate to and select the folder containing your Obsidian vault (the directory with your Markdown files).

2. **Set Similarity Threshold:**  
   - Use the provided spinbox to set the sensitivity (percentage) for determining duplicate files. A higher percentage means only very similar files are flagged.

3. **Find Duplicates:**  
   - Click on the **"Find Duplicates"** button.
   - The application will read all Markdown files, compute text similarities, and display duplicate groups.
   - A progress bar will update as the scanning process proceeds.

4. **Review Duplicate Groups:**  
   - The left pane displays groups with the number of similar files, along with details like file path, size, and last modified date.
   - Click on a group or individual file to preview its content in the right pane.

5. **Delete Selected Files:**  
   - Select one or more files (or an entire group) in the treeview.
   - Click the **"Delete Selected Files"** button.
   - For duplicate groups, a dialog may appear allowing you to choose specifically which files to remove.

---

## 5. Use Cases and Examples

### Use Case 1: Organizing a Personal Knowledge Base

- **Scenario:** A user maintains a personal Obsidian vault for journaling and research notes. Over time, duplicate or near-duplicate entries are created.
- **Example:**  
  - **Input:** Multiple Markdown files with very similar content about "Project Ideas".
  - **Expected Output:** The program groups these files under one duplicate group with an average similarity (e.g., 85%), highlighting them for review or deletion.

### Use Case 2: Optimizing Documentation in a Team Environment

- **Scenario:** A small team uses Obsidian for collaborative documentation. Duplicate files can occur due to multiple contributions.
- **Example:**  
  - **Input:** Two or more files containing almost identical meeting notes.
  - **Expected Output:** The application identifies these as duplicates, allowing the team to consolidate the notes into a single, updated file.

### Use Case 3: Cleaning Up Datasets from Automated Imports

- **Scenario:** A researcher imports a large collection of Markdown files from various sources. Some files may carry redundant information.
- **Example:**  
  - **Input:** Markdown files with overlapping content related to research data.
  - **Expected Output:** The program groups duplicates together, enabling the user to efficiently remove or combine similar files, thus enhancing dataset quality.

---

## 6. Disclaimer

This repository is continuously updated, and changes to the code may render parts of this README file outdated. No guarantee is made that this file will consistently reflect the current state of the repository.
