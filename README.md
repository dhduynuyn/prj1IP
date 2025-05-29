# File Transfer Application - Instructions, Setup, and Commands

## I. Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.x:** The application is developed using Python 3. You can download it from [python.org](https://www.python.org/).
2.  **Required Python Libraries:**
    *   `DearPyGui`: For the graphical user interface.
    *   Other standard libraries (`socket`, `threading`, `json`, `os`, `shlex`) are typically included with Python.

    You can install `DearPyGui` using pip:
    ```bash
    pip install dearpygui
    ```

## II. Setup

1.  **Download or Clone the Project:**
    Obtain the project files. If it's a Git repository, clone it:
    ```bash
    # git clone <repository_url>
    # cd <project_directory_name>
    ```
    Ensure you are in the main project directory (`22125036_22125117/`) which contains `server.py` and `app.py`.

2.  **Prepare Server Files (Optional):**
    *   The server shares files from the `Server/` directory.
    *   Place any files you want to make available for download into the `Server/` directory within the project structure. If this directory doesn't exist, create it.

3.  **Executable Files (Optional):**
    *   If you plan to use the pre-compiled executables (`server.exe`, `app.exe`), ensure they are present in the `Release/` folder. No Python installation or library installation is needed if using these.

## III. Running the Project

You need to run the Server first, then the Client.

### 1. Start the Server

**Option A: Using Python script**
   1. Open a terminal or command prompt.
   2. Navigate to the project's root directory.
      ```bash
      cd path/to/22125036_22125117
      ```
   3. Run the server script:
      ```bash
      python server.py
      ```
   4. The terminal will indicate that the server is listening (e.g., "Server listening on port 12000"). Keep this terminal window open.

**Option B: Using the executable (if available)**
   1. Navigate to the `Release/` folder within your project directory.
   2. Double-click `server.exe`.
   3. A terminal window will open, showing that the server is running. Keep this window open.

### 2. Start the Client

**Option A: Using Python script**
   1. Open a **new** terminal or command prompt.
   2. Navigate to the project's root directory.
      ```bash
      cd path/to/22125036_22125117
      ```
   3. Run the client application script:
      ```bash
      python app.py
      ```
   4. The GUI application window should appear.

**Option B: Using the executable (if available)**
   1. Navigate to the `Release/` folder within your project directory.
   2. Double-click `app.exe`.
   3. The GUI application window should launch.

## IV. Interacting with the Interface (Client Application Commands)

Once the client GUI is running:

1.  **List Files (Refresh):**
    *   Click the **Refresh button** (looks like a Smile-icon).
    *   This sends a `LIST` command to the server. The file and directory tree from the server's `Server/` directory will be displayed in the "Directory Panel".

2.  **Download File(s):**
    *   In the "Directory Panel", select the file(s) or folder(s) you wish to download.
    *   Click the **Download button** (looks like a Heart-icon).
    *   This sends `GET <filename>` commands to the server for each selected file.
    *   Download progress for each file will be shown in the "Download Panel".

3.  **Downloaded Files Location:**
    *   Downloaded files are saved in the `Client/` directory within your project structure. If this directory doesn't exist, it will likely be created automatically upon the first download.

4.  **Quit (Client):**
    *   Simply close the GUI window. This will send a `QUIT` command to the server for that specific client connection.

5.  **Stop Server:**
    *   Close the terminal window where the server is running, or press `Ctrl+C` in that terminal.

## V. File Locations Summary

*   **`Server/`**: Contains files made available by the server for download. You need to populate this directory manually with files you wish to share.
*   **`Client/`**: Stores files downloaded by the client application. This directory is typically created automatically by the client if it doesn't exist.
*   **`Release/`**: (If using executables) Contains `server.exe` and `app.exe`.
*   **`Element/`**: Contains GUI assets like images for buttons and background.
*   **`Font/`**: Contains custom font files used by the GUI.

This condensed version focuses directly on how to get the application up and running and how to use its core functionalities.