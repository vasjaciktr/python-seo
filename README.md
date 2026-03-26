# Python for SEO

Small collection of Python scripts I use in SEO workflows:  
Google Sheets automation, Google Search Console export, and table processing.

## Scripts

### openai_sheets_generate.py
Generate descriptions from Google Sheets using OpenAI API.

### gsc_export.py
Export Google Search Console data (queries/pages) into CSV.

### csv_splitter.py
Split large CSV into smaller files with header preserved and optional ZIP archive.

Use cases:
- bulk imports with row limits
- feed splitting
- large dataset handling

### lost-backlinks-check.py
Check whether purchased backlinks are still there. The script returns page code status, redirected URL, found backlinks, and errors.

## Environment variables

OPENAI_API_KEY  2

Scripts use local environment variables for authentication.
