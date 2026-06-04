---
name: resume-pdf-design
description: Write and design a tailored resume PDF from user-provided resumes, job descriptions, and raw career notes. Use when creating or revising resume PDFs, especially when local PDF generation needs to work without admin access.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [resume, PDF, career, documents, reportlab]
    related_skills: [ocr-and-documents]
---

# Resume PDF Design Workflow

Use this when the user asks to write, tailor, or design a resume PDF from uploaded resumes, a job description, or raw notes.

## Workflow

1. **Load document context**
   - If PDFs are involved, load `ocr-and-documents` first.
   - Extract prior resume text and job description text with PyMuPDF (`fitz`) when possible.
   - If `fitz` is missing, install user-space with:
     ```bash
     python3 -m pip install --user pymupdf reportlab
     ```
   - Do not ask the user what to do with each uploaded resume if the text prompt already states the goal.

2. **Synthesize the resume strategy**
   - Treat the job description as the target.
   - Use the user’s most recent pasted notes as highest-authority factual input.
   - Use older resumes mainly for historical dates, education, older role wording, and metrics.
   - Drop or compress irrelevant early roles unless they strengthen the target narrative.
   - Avoid inventing management-of-people claims if the user says they are not a people manager.

3. **Check important math before writing**
   - Always calculate churn/LTV/revenue math with a tool, not mentally.
   - Example: at $1,000/month, expected LTV is `$1000 / churn_rate`; 6% churn ≈ $16.7k, 16% churn ≈ $6.3k.

4. **Create both editable source and PDF**
   - Save a Markdown source version alongside the PDF for easy revision.
   - Recommended location pattern:
     ```text
     ~/.hermes/cache/resume_<role_slug>/Candidate_Role_Resume.md
     ~/.hermes/cache/resume_<role_slug>/Candidate_Role_Resume.pdf
     ```

5. **PDF generation approach**
   - Prefer a clean one-page resume unless the target role truly needs two pages.
   - On macOS/work laptops without admin access, avoid relying on WeasyPrint unless the native GTK/Pango libraries are already available.
   - If WeasyPrint fails with `cannot load library 'libgobject-2.0-0'`, switch to ReportLab instead of trying system-level installs.
   - Use ReportLab for reliable local PDF generation:
     - `SimpleDocTemplate`
     - Helvetica/Helvetica-Bold
     - compact margins around 0.4–0.5 inches
     - section dividers via `HRFlowable`
     - small but readable font sizes around 8.75–10pt

6. **Verify before final delivery**
   - Re-open the generated PDF with PyMuPDF.
   - Confirm page count, file size, and extracted text.
   - Make sure the PDF is attached in the final response with `[FILE:/path/to/file.pdf]`.
   - Mention the editable source path briefly.

## Pitfalls

- ReportLab’s default stylesheet already includes names like `Title` and `Bullet`; use unique names such as `ResumeTitle` and `ResumeBullet` to avoid `KeyError: Style 'Title' already defined in stylesheet`.
- Do not overstate titles. If the role is called “Manager” but the user does not manage people, frame them as a “Community & Member Engagement Operator” or similar execution-oriented title.
- Keep the response short after delivery; the user wants the file, not a long explanation.
