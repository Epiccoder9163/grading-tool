# LLM Grading Tool

A LLM-based grading tool to help teachers grade assignments

![A screenshot of the program](URL "readme/screenshot.png")
### This tool is a work in progress and should NOT be used in a production environment where the accuracy of the result is vital.

This program has only been tested on Zorin OS 18 (Ubuntu 24.04 LTS) as well as Fedora 43 with an AMD RX 9060 XT (16gb), but is also confirmed working with an NVIDIA RTX 4080 under CachyOS (Arch Linux).

This program should work with any Ollama supported GPU and operating system, but your mileage may vary.

Vision-Enabled LLM Used - [Qwen3-VL:8B](https://ollama.com/library/qwen3-vl)


## How to install
1. **Install and confirm Ollama is running**
	
	[Download Ollama](https://ollama.com/download)
	
	 Confirm Ollama is running

 	```bash
	ollama status
	```
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

 	```powershell
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
   python3 ./Legacy/main.py
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
- This program needs ollama to run, you can install it at https://ollama.com
- May have limitations grading (particularly explaining) longer and more complex single-page assignments due to the simple grading pipeline
- There need to be the same number of pages in the homework and answer key. There also should be the same number of questions.

## To Do
- Suggest new features and report bugs in the issues tab!
 
## Credits

- Ollama
  - For the LLM backend
- Alibaba Cloud
  - For the Qwen3-VL model used for text extraction

[![Star History Chart](https://api.star-history.com/svg?repos=Epiccoder9163/grading-tool&type=date&legend=top-left)](https://www.star-history.com/#Epiccoder9163/grading-tool&type=date&legend=top-left)