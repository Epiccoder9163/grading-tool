# LLM Grading Tool

A LLM-based grading tool to help teachers grade assignments

### This tool is a work in progress and should NOT be used in a production environment where the accuracy of the result is vital.

This program has only been tested on Zorin OS 18 (Ubuntu 24.04 LTS) with an AMD RX 9060 XT, but is also confirmed working with an NVIDIA GPU under CachyOS (Arch Linux).

This program should work with any Ollama supported GPU and operating system, but your mileage may vary.

Vision-enabled LLM Used - Qwen3-vl-math
https://huggingface.co/ElliottWise/qwen3-vl-math

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

	**MacOS/Linux**
   ```bash
   source /venv/bin/activate
   ```
	**Windows**

 	```bash
   venv/bin/activate
   ```
4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
5. **Run the app**

   ```bash
   python3 ./gui.py
   ```

   **Or run the TTY version (Depreciated)**
   ```bash
   python3 ./main.py
   ```

## Usage

1. Run gui.py
2. Insert your file paths
3. Save the assignment
4. Wait for your results
5. Export to CSV or TXT format (more formats coming soon!)

## Features
 - Can grade handwritten assignments
 - Can export to a file (CSV and TXT)
 - Can explain incorrect answers
 
## Limitations

- Can only take image files (.png or .jpeg), no PDFs or other documents
- Can only accept multiple choice or simple numerical answers, no special math characters.
- Answers have to be boxed or highlighted for the LLM to find the answer correctly, otherwise it (probably) won't work
- This program does need ollama to run, you can install it at https://ollama.com

## To Do
- Suggest new features in the issues tab!
 
## Credits

- Ollama
  - For the LLM backend
- Alibaba Cloud
  - For the Qwen3-VL model used for text extraction
