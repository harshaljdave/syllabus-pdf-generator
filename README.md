# Syllabus PDF Generator

This project is a  **College Capstone project** developed to automate the creation of syllabus PDFs, making it easier for educators, institutions, and students to access and share course information in a standardized, printable format.

---

## Project Overview

Syllabus PDF Generator allows users to input structured data about a course (including objectives, theory and practical syllabus, textbooks, reference books, and outcomes). The project uses these inputs to generate a formatted syllabus PDF using LaTeX templates. All user inputs and generated metadata are stored for reference and editing.

---

## Tech Stack

- **Backend:** Python (Django)
    - Handles web requests, forms, PDF generation logic, and database interaction.
- **Database:** MongoDB
    - Stores syllabus metadata, filenames, and content for efficient retrieval and editing.
- **PDF Generation:** LaTeX
    - Course data is mapped to LaTeX `.tex` templates for high-quality PDF output.
- **Frontend:** HTML, CSS, JavaScript
    - Provides a user interface for syllabus data entry and management.
- **Libraries/Dependencies:**
    - `pymongo` (Python MongoDB client)
    - LaTeX packages: `longtable`, `multirow`, `enumitem`, `xcolor`, `colortbl`, etc.

---

## Workflow

1. **Data Entry:**  
   Users enter syllabus details through a web form:  
    - Academic year, branch, subject code, name  
    - Teaching and examination scheme  
    - Prerequisites, objectives, theory & practical content  
    - Textbooks, reference books, MOOC references  
    - Course outcomes

2. **Data Storage:**  
   Entered data is stored in MongoDB. The structure includes:
    - Filename and branch (in a `filename` collection)
    - Syllabus content (in a `filecontent` collection)

3. **PDF Generation:**  
   - The backend maps user data to a LaTeX template (see `syllabus/*.tex` files).
   - LaTeX packages are used for formatting tables and layout.
   - The Python backend invokes PDF generation (with error handling and cleanup for auxiliary files).

4. **Edit & Update:**  
   - Users can edit syllabi. Updated data replaces the old entry in MongoDB.
   - Regenerating the PDF updates the syllabus document.

5. **Download & Share:**  
   - The final PDF is made available for download and distribution.

---

## Usage

Clone the repository:

```bash
git clone https://github.com/harshaljdave/syllabus-pdf-generator.git
```

Set up Python, MongoDB, and LaTeX in your environment (see project documentation for details).  
Run the Django server and access the web interface to begin generating syllabi.

---

## Contribution

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

---

## Author

- [harshaljdave](https://github.com/harshaljdave)

---

## License

No license specified.

---

## Links

- [GitHub Repository](https://github.com/harshaljdave/syllabus-pdf-generator)
