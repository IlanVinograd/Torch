# Torch - File Management Tool

![Torch](https://github.com/IlanVinograd/Torch/blob/main/icon256x256.png)

Torch is a simple and intuitive file management application that allows you to browse, select, and copy files or folders with ease. This app is designed to work seamlessly on Windows.

## Illustration

Here’s a quick demonstration of Torch in action:

![TorchPNG](https://github.com/IlanVinograd/Torch/blob/main/torch.gif)

## Features

- **File/Folder Navigation**:
  - Double-click to enter folders.
  - Backspace to navigate back to the parent directory.

- **File Selection**:
  - Use `Ctrl + Click` to select multiple files or folders.
  - Use `Shift + Click` to select a range of files or folders.
  - `Select All` to select all files and folders in the current directory.
  - `Deselect All` to clear your selection.

- **Copy Functionality**:
  - Copies the content of selected files to the clipboard in the format:
    ```
    file_name:
    file_content
    ```

- **Help Tab**:
  - Includes detailed instructions on how to use the application.

- **Desktop Shortcut**:
  - Quickly create a shortcut for the app on your desktop.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/torch.git
   cd torch
2. Navigate to the app directory:
   ```bash
   cd app
   ```
3. Run the setup script to create a desktop shortcut:
   ```bsh
   setup.bat
   ```

**⚠ Important Note:**  
Due to the nature of the setup script and some of its functionality, Windows Defender or other antivirus programs might flag it as a potential threat. This is a **false positive**.  

- If you’re concerned, you can inspect the source code yourself or rebuild the project from scratch.  
- The source code is fully open for transparency and available in this repository.