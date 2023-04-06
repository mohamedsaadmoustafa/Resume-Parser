# Resume Parser

A simple resume parser extracting information from CV or resumes.

## How will a resume get parsed?

This tool uses diffrent natural language processing techniques to parse resumes. Using this to see how well your resume is read by Application Tracking Systems (ATS) when applying to jobs.

## Deploying Demo

[Reseme Parser Streamlit](https://mohamedsaadmoustafa-reseme-parser-srcapp-lmw5d4.streamlitapp.com/) 

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mohamedsaadmoustafa-reseme-parser-srcapp-lmw5d4.streamlitapp.com)

## File Structure

```

Reseme-Parser
├── data
│   ├── degrees.csv
│   ├── samples
│   └── skills.csv
├── notebooks
│   └── reseme_parser.ipynb
├── scrappers
│   ├── abbreviations.py
│   └── reseme_examples.py
├── src
│   ├── app.py
│   ├── constants.py
│   ├── pipeline.py
│   ├── resume_text.py
│   └── visualization
│       └── cloudwords.py
├── images
│   └── header.png
├── upload
├── requirements.txt
└── README.md

8 directories, 13 files

```
