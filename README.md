# Article Tracker

## Overview

The Article Tracker is a FlaskApp web application that allows users to upload PDF files, input metadata about the articles, and generate statistics based on the uploaded articles. The statistics include the number of articles, pages, and words read per month, which are displayed as bar graphs.

## Features

- Upload PDF files and input metadata (title, author, date read)
- Automatically calculate the page count and word count from the uploaded PDF
- Generate monthly statistics for articles, pages, and words read
- Display statistics as bar graphs

## Installation

### Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/JamesSettles/article-tracker.git
    cd article-tracker
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Building the Application

To create an executable for the application, use PyInstaller:
    ```bash
    python app/open_flask.py
    ```

The executable will appear in /dist
