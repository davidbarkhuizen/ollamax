**`solution/extract_code.py`**
```python
import os
import re
from typing import List

def extract_code_files(source_md_path: str, dest_folder_path: str) -> List[str]:
    """
    Extracts code blocks from a markdown file and writes them to a destination folder.
    
    Args:
        source_md_path: Path to the source markdown document.
        dest_folder_path: Path to the destination folder.
        
    Returns:
        List of destination paths of successfully extracted files.
    """
    results = []
    
    # Regex patterns
    # Marker: **`path**`
    marker_pattern = re.compile(r'^\*\*`(.+)`\*\*$')
    # Code block start: ``` (optionally followed by language identifier)
    code_start_pattern = re.compile(r'^`{3,}')
    # Code block end: ``` (with optional whitespace)
    code_end_pattern = re.compile(r'^\s*`{3,}\s*$')
    
    if not os.path.exists(source_md_path):
        raise FileNotFoundError(f"Source file {source_md_path} not found.")
        
    # Normalize destination folder path
    dest_folder_abs = os.path.abspath(dest_folder_path)
    
    with open(source_md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_code_block = False
    code_content = []
    extracted_path = None
    prev_line = None
    
    for line in lines:
        line_stripped = line.rstrip('\n\r')
        
        if not in_code_block:
            if code_start_pattern.match(line_stripped):
                # Check previous line for marker
                if prev_line is not None:
                    match = marker_pattern.match(prev_line.strip())
                    if match:
                        rel_path = match.group(1)
                        
                        # Check for '..' in path components
                        if '..' in rel_path.split('/'):
                            prev_line = line_stripped
                            continue
                            
                        dest_path = os.path.normpath(os.path.join(dest_folder_abs, rel_path))
                        
                        # Ensure dest_path is within dest_folder_abs
                        try:
                            common = os.path.commonpath([dest_folder_abs, dest_path])
                            if common != dest_folder_abs:
                                prev_line = line_stripped
                                continue
                        except ValueError:
                            # Different drives on Windows
                            prev_line = line_stripped
                            continue
                            
                        # Create directories if needed
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        
                        in_code_block = True
                        extracted_path = dest_path
                        code_content = []
            # Update prev_line for next iteration
            prev_line = line_stripped
        else:
            if code_end_pattern.match(line_stripped):
                # End of code block
                with open(extracted_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(code_content))
                results.append(extracted_path)
                in_code_block = False
                extracted_path = None
                code_content = []
            else:
                code_content.append(line_stripped)
                
    return results
```

**`solution/test_extract_code.py`**
```python
import os
import tempfile
import unittest
import shutil
from extract_code import extract_code_files

class TestExtractCodeFiles(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.source_md = os.path.join(self.temp_dir, 'source.md')
        self.dest_folder = os.path.join(self.temp_dir, 'dest')
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_valid_extraction(self):
        content = """Some text.

**`src/dicts_to_table.py`**
```python
def divide_by_zero(n: int) -> int:
    return n / 0
```

More text.
"""
        with open(self.source_md, 'w') as f:
            f.write(content)
            
        results = extract_code_files(self.source_md, self.dest_folder)
        
        self.assertEqual(len(results), 1)
        expected_path = os.path.join(self.dest_folder, 'src', 'dicts_to_table.py')
        self.assertIn(expected_path, results)
        self.assertTrue(os.path.exists(expected_path))
        with open(expected_path, 'r') as f:
            self.assertEqual(f.read(), 'def divide_by_zero(n: int) -> int:\n    return n / 0\n')
            
    def test_invalid_marker(self):
        content = """**`src/file.py`**
```python
code
```
"""
        with open(self.source_md, 'w') as f:
            f.write(content)
            
        results = extract_code_files(self.source_md, self.dest_folder)
        self.assertEqual(len(results), 0)
        
    def test_path_with_dotdot(self):
        content = """**`../escape.py`**
```python
code
```
"""
        with open(self.source_md, 'w') as f:
            f.write(content)
            
        results = extract_code_files(self.source_md, self.dest_folder)
        self.assertEqual(len(results), 0)
        
    def test_multiple_blocks(self):
        content = """**`a.py`**
```python
a
```

**`b.py`**
```python
b
```
"""
        with open(self.source_md, 'w') as f:
            f.write(content)
            
        results = extract_code_files(self.source_md, self.dest_folder)
        self.assertEqual(len(results), 2)
        
    def test_no_marker(self):
        content = """```python
code
```
"""
        with open(self.source_md, 'w') as f:
            f.write(content)
            
        results = extract_code_files(self.source_md, self.dest_folder)
        self.assertEqual(len(results), 0)
        
    def test_language_identifier(self):
        content = """**`src/code.py`**
```python
def func():
    pass
```
"""
        with open(self.source_md, 'w') as f:
            f.write(content)
            
        results = extract_code_files(self.source_md, self.dest_folder)
        self.assertEqual(len(results), 1)
        expected_path = os.path.join(self.dest_folder, 'src', 'code.py')
        self.assertTrue(os.path.exists(expected_path))

if __name__ == '__main__':
    unittest.main()
```