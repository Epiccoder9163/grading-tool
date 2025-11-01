# LLM Grading Tool
A LLM-based grading tool to help teachers grade assignments

### This tool is a work in progress and should NOT be used in a production environment where the accuracy of the result is vital.

This program has only been tested on Ubuntu 24.04 LTS with an AMD RX 9060 XT, but is also confirmed working with an NVIDIA GPU.
This program should work with any Ollama supported GPU and operating system, but your mileage may vary.

## How to install
1. **Clone the repository**
   ```bash
   git clone https://github.com/epiccoder9163/grading-tool.git
   cd grading-tool
   ```
2. **Create a venv environment**
   ```bash
   python3 -m venv venv
   ```
3. **Enter the venv environment**
   ```bash
   source /venv/bin/activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the app**
    ```bash
    python3 ./main.py
    ```
    **Or run the GUI**
    ```bash
    python3 ./gui.py
    ```

## Usage
1. Run main.py
2. Insert your file paths
3. Wait for your results

## Limitations
 - Can only take image files (.png or .jpeg), no PDFs or other documents
 - Can only accept multiple choice or simple numerical answers, no special math characters.
 - Answers have to be boxed or highlighted for the LLM to find the answer correctly, otherwise it won't work
 - This program does need ollama to run, you can install it at https://ollama.com

