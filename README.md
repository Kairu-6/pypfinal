# 🛠️ Universal Helper Functions

## Overview
To maintain consistency, prevent redundant code, and eliminate critical bugs across all four user roles (Admin, Staff, Permit Officer, Vehicle Owner), the system utilizes a centralized library of "Universal Helper Functions." 

These functions handle the core mechanics of the program—such as file reading/writing, date/time validation, and data extraction. By forcing all modules to route their data through these shared functions, we guarantee that the database format is never corrupted, regardless of which role is interacting with it.

---

### `get_valid_date()`
* **Explanation:** A robust input prompt that forces users to enter a mathematically sound date (accounting for leap years and month lengths). It accepts both slashes (`/`) and dashes (`-`), and silently standardizes the output into the international format required by our database files.
* **Why it was introduced:** In the original guideline, it's stated that no usage of external libraries is allowed, this caused all roles to separately implement our own date validating functions. After clarification with lecturer, module datetime is actually allowe, thus we created this function to combine date sanitisation directly with the prompt.
* **How it works:** It traps the user in a `while True` loop until they provide a valid input or type 'q' to quit. It uses Python's built-in `datetime.strptime()` to attempt to parse the string. If the user enters an impossible date (e.g., `29/02/2026`), `datetime` throws a `ValueError`, which the `try/except` block catches and prompts the user again. Once validated, it uses `.strftime("%Y-%m-%d")` to format the date before returning it as a string.

### `load_from_file(file_name)`
* **Explanation:** A universal file reader that safely opens a `.txt` database, separates the header row from the data, cleans out any accidental blank lines or hidden whitespace, and returns the data as a clean 2D array (list of lists).
* **Why it was introduced:** We noticed that in the beginning, we had multiple lines of code in multiple spots only to open text files and parse the data. THis function standardises the format and processing of raw data from the files.
* **How it works:** It attempts to open the requested file using a context manager (`with open`). It uses `.readline()` to extract and isolate the first line as the `headers` array. It then loops through the remaining lines, stripping invisible characters (`\n`, `\t`) and splitting them by commas to build the `data_list` array. It uses a `try/except` block to prevent the entire program from crashing if a required text file is missing.

### `save_to_file(data_list, file_name, headers)`
* **Explanation:** The universal counterpart to `load_from_file`. It takes a 2D array of system data and safely overwrites the specified `.txt` database file in the exact comma-separated format required.
* **Why it was introduced:** Similar to load_from_file, but for storage.
* **How it works:** It receives the target filename, the header array, and the 2D data array. It opens the file in write mode (`"w"`), which completely clears the old file. It writes the headers first, and then iterates through every list inside `data_list`, using `",".join(entry)` to sew the list back into a perfect comma-separated string before writing it to the new line. 

### `get_valid_time()`
* **Explanation:** An input prompt that ensures users enter a mathematically valid 24-hour time format (HH:MM). 
* **Why it was introduced:** Similar to get_valid_date, but for time.
* **How it works:** Similar to the date validator, it traps the user in a loop. It splits the user's string by the colon (`:`) and checks if both halves are numeric. It then verifies that the first half (hours) is strictly between `00` and `23`, and the second half (minutes) is between `00` and `59`. 

### `get_record(full_id, data_list)`
* **Explanation:** A dynamic search engine that scans any loaded database array for a specific alphanumeric ID (e.g., searching for space `S05` or permit `D01`) and returns that entire row of data.
* **Why it was introduced:** Before this function, every role (Admin, Staff, Owner) had to write their own custom for loops to search for parking spaces, users, or permits. This led to inconsistent error handling and redundant code. It was introduced to serve as a single, bulletproof search engine that ensures case-insensitive matching and prevents "Index Out of Range" crashes across the entire system.
* **How it works:** It takes the target ID string and standardizes it to uppercase using `.strip().upper()`. It then iterates through the provided `data_list`. Because our databases are standardized, the ID is always in the 0th index of the row (`item[0]`). If it finds a match, it returns the list representing that row. If the loop finishes without a match, it returns `False`.

### `get_id_number(record, index_of_id)`
* **Explanation:** A specialized string-slicer used to isolate the numerical value from an alphanumeric ID (e.g., turning `"S12"` into the integer `12`) so that the system can properly sequence and sort data without string-comparison errors.
* **Why it was introduced:** Python evaluates strings differently than numbers (for example, alphabetically, the string "S2" is considered "greater" than "S10"). This caused critical bugs when sorting records or trying to automatically generate the next available ID (like P015). This function was introduced to safely separate the math from the text, ensuring accurate sorting and preventing accidental ID duplication.
* **How it works:** It locates the specific alphanumeric string within a record using the `index_of_id` argument. It then uses string slicing (`full_id[1:]`) to chop off the leading letter. Finally, it casts the remaining numeric characters into an `int()` and returns it.

### `enter_id(id_name)`
* **Explanation:** A secure input prompt specifically designed to validate alphanumeric IDs (like "S05") that are typed manually by the Admin when attempting to update or delete records.
* **Why it was introduced:** When prompting the Admin to update or remove a record, a simple typo (like typing 12 instead of S12, or adding extra spaces) would either crash the program or fail to find the record. This function was introduced as a "gatekeeper" to catch formatting errors, handle confusing edge cases (like leading zeros in S02), and guarantee that the system only processes valid ID structures.
* **How it works:** It forces the user to input a string and checks if the very first character is a letter using `.isalpha()`. It then safely extracts the numeric portion. Notably, it includes a specific condition to handle leading zeros (e.g., ensuring `02` is processed safely without crashing) before returning both the prefix letter and the integer.

### `permit_types_sort_key(permit)`
* **Explanation:** A custom lambda sorting key used exclusively by the Admin module to organize the `permit_types.txt` file logically by priority (Daily -> Monthly -> Annual) rather than alphabetically.
* **Why it was introduced:** If we relied on Python's default alphabetical sorting, "Annual" (A) would appear before "Daily" (D), making the permit menus confusing to read. This custom key was introduced to override the default behavior, ensuring that permits are always presented to the user in a logical, hierarchical order based on duration (Daily -> Monthly -> Annual), followed by their sequential ID number.
* **How it works:** It uses a dictionary mapping (`PERMIT_PRIORITY`) to assign a numeric weight to the prefix letters: D=1, M=2, A=3. It extracts the prefix letter and the ID number from the permit record. It then returns a tuple `(priority, id_num)`. The `.sort()` function uses this tuple to first group all 'D's together, then all 'M's, and then sorts them numerically within their respective groups.