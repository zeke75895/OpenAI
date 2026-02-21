# OpenAI DSA Problem Solver

A small project with scripts that call the OpenAI API to solve DSA problems from text files and save conversation logs.

## Contents

- `openAi-test.py` — main example script using the OpenAI Responses API and logging conversations.
- `deepseek-test.py` — secondary example script using DeepSeek's API and logging conversations.
- `dsa-questions/` — folder containing problem text files used as input.
- `OpenAiConversations/` — directory where `openAi-test.py` saves conversational logs.
- `deepSeekConversations/` — additional conversation logs.

## Dependencies

- Python 3.12 (recommended) or Python 3.10+.
- pip
- The required Python packages are listed in `requirements.txt`. Key packages include:
  - `openai` (OpenAI Python client)
  - `python-dotenv`

## Quick setup (macOS / Linux)

1. Clone the repository and change into the project directory:

   git clone <repo-url>
   cd <repo-folder>

2. Create and activate a virtual environment (recommended):

   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:

   pip install --upgrade pip
   pip install -r requirements.txt

4. Configure environment variables:

   - Create a file named `.env` in the project root.
   - Add your OpenAI API key to the file:

     OPEN_AI_API_KEY=sk-...

5. Run the example script:

   python openAi-test.py

   - The script reads a question file from `dsa-questions/` (see `question_filename` variable).
   - Conversation logs are written to `OpenAiConversations/`.

## Usage notes

- To change which question is asked, edit the `question_filename` variable in `openAi-test.py` to point to a file in `dsa-questions/`.
- If you get `FileNotFoundError`, make sure you run scripts from the project root so relative paths resolve correctly.
- The code expects an environment variable named `OPEN_AI_API_KEY` supplied via `.env` or your shell.

## Troubleshooting

- If package installation fails, confirm your Python version (`python3 --version`) and try upgrading `pip`.
- If API calls fail, check that your `OPEN_AI_API_KEY` is valid and not rate-limited.

## License

See the included `LICENSE` file.

---