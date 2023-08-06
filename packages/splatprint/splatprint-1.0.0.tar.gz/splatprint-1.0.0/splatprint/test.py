from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory/"readme.md").read_text()

print(long_description)