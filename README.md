# GCR Materials

GCR Materials is a Python script that empowers you to efficiently retrieve and download course materials from Google Classroom using the Google Classroom API and Google Drive API. This tool is especially useful for fetching materials from multiple courses and organizing them into individual folders.

## Setup

1. **Clone the Repository**: Begin by cloning this repository to your local machine.

2. **Google OAuth Consent Screen Setup**:

   In order for GCR Materials to access your Google Classroom and Google Drive data securely, you need to set up a Google OAuth consent screen. This process involves configuring how the script interacts with your Google account. Follow these steps:

   - **2.1. Create a Project**:

     1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
     2. Create a new project or select an existing project by clicking on the project dropdown at the top of the screen and selecting "New Project" or an existing project.

   - **2.2. Enable the Required APIs**:

     1. In the left sidebar, click on "APIs & Services" > "Library."
     2. Search for "Google Classroom API" and "Google Drive API" one by one.
     3. Enable both APIs for your project.

   - **2.3. Configure OAuth Consent Screen**:

     1. In the left sidebar, click on "APIs & Services" > "OAuth consent screen."
     2. Choose "External" or "Internal" user type based on your needs.
     3. Fill in the required fields such as "Application name" and "Support email."
     4. Under "Scopes for Google APIs," add the following scopes:
        - `https://www.googleapis.com/auth/classroom.courses.readonly`
        - `https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly`
        - `https://www.googleapis.com/auth/drive.readonly`

   - **2.4. Create Credentials**:

     1. After configuring the OAuth consent screen, go to "APIs & Services" > "Credentials."
     2. Click on the "Create Credentials" button and select "OAuth client ID."
     3. Choose "Desktop app" as the application type.
     4. Provide a name for the OAuth client ID.
     5. Click "Create."
     6. You will see a message saying "To create an OAuth client ID, you must first set a product name on the Consent screen."
     7. Click "Configure consent screen" and select the product name you set in the previous step.
     8. Click "Save" and go back to the credentials page.

   - **2.5. Download Credentials JSON**:
     1. On the credentials page, click the download icon next to the created OAuth client ID. This will download a JSON file containing your credentials.
     2. Rename the downloaded JSON file to `credentials.json`.

3. **Place Credentials File**: Move the `credentials.json` file you obtained in the previous step to the root directory of the cloned repository.

## Usage

Run the script using the following command in your terminal:

```bash
python gcr.py
```

This will download all the active courses' materials into the current directory.

### Options

1. **--course**:
   Fetch and download materials for a specific course:

   ```bash
   python gcr.py --course 'course-name'
   ```

2. **--courses**:
   Fetch and download materials for multiple courses listed in a text file split by lines:

   ```bash
   python gcr.py --courses 'path/to/courses.txt'
   ```

3. **--download-path**:
   Specify the download path for the materials. If not provided, materials will be downloaded in the current directory:
   ```bash
   python gcr.py --download-path 'path/to/download/at'
   ```

## Contributing

Contributions to GCR Materials are welcome! If you have improvements, bug fixes, or new features to propose, please open an issue first to discuss the changes.

## License

GCR Materials is open-source and licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
