# Smart Fitness Session Analyzer - Assignment II

## Project information

- Selected option: Option A - Smart Fitness Session Analyzer
- Student name: Tobias Danielsen
- Student number: s385486
- Repository: https://github.com/TobiasDani/Smart-Fitness-Session-Analyzer-Oblig-2

## Short description

This project extends the Smart Fitness Session Analyzer from Assignment I.

Instead of using generated Python dictionaries, the program now reads participant and fitness session data from CSV files. The data is validated and converted to Python objects before each session is analyzed.

The program also handles invalid records, logs rejected rows, and saves the analysis results to output files.

## Project structure

The main application code is stored in the `fitness` package.

- `participant.py`: represents a participant and their baseline values
- `observation.py`: represents one fitness measurement
- `session.py`: groups observations into a session and performs the main analysis
- `report.py`: creates a structured result for a session
- `csv_reader.py`: reads and validates CSV files
- `reporting.py`: writes the result files
- `exceptions.py`: contains custom exception classes
- `utils.py`: contains small calculation functions

The `data` folder contains the official CSV input files.

The `output` folder contains the generated reports.

## Object-oriented design

Composition is used in the application. A `Session` contains a `Participant` and a list of `Observation` objects.

Encapsulation is used for the `_classification` attribute in `Session`, which is accessed through a property.

Inheritance and method overriding are not used because there is no useful "is-a" relationship between the main classes. Composition fits the data model better.

## CSV validation

Participant IDs must follow this format:

```text
P followed by three digits
Example: P001
```

Fitness session IDs must follow this format:

```text
FIT-YYYY-NNN
Example: FIT-2026-001
```

These identifiers are validated using regular expressions.

The program also checks:

- timestamp must be 0 or higher
- heart rate must be between 35 and 205
- skin response must be 0 or higher
- temperature must be between 25 and 42
- activity level must be between 0 and 1
- signal quality must be between 0 and 1
- participant IDs used in session files must exist in `participants.csv`
- required fields must not be missing

Rows that cannot be accepted are rejected and written to `rejected_records.txt`.

Each rejected row includes the source file, row number, field and reason.

## Signal quality

Signal quality values between 0 and 1 are accepted as valid measurements.

If the average signal quality for a session is below 0.6, the session is classified as `insufficient data`.

## Classification rules

The program uses the same basic rule-based analysis as Assignment I.

- `resting`: average activity is below 0.2 and average heart rate is no more than 8 BPM above baseline
- `moderate activity`: activity is above the resting range without reaching the high activity threshold
- `high activity`: average activity is at least 0.65 or average heart rate is at least 30 BPM above baseline
- `recovering`: heart rate drops by more than 8 BPM and activity drops by more than 0.10 between the first and second half of the session
- `insufficient data`: fewer than 3 usable observations or average signal quality is below 0.6

## Error handling

The program uses two custom exceptions:

- `InvalidIdentifierError`
- `InvalidRecordError`

It also handles file and CSV errors such as missing files, permission errors, invalid values and missing fields.

Invalid rows are rejected without stopping the rest of the file from being processed.

## Running the program

The project uses only the Python standard library.

From the repository root, run:

```bash
python main.py
```

The default files are:

```text
data/participants.csv
data/fitness_sessions.csv
data/fitness_sessions_invalid.csv
```

The full command can also be written as:

```bash
python main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv --invalid-sessions data/fitness_sessions_invalid.csv --output output
```

If your system uses `python3`, use:

```bash
python3 main.py
```

## Output files

The program creates these files:

```text
output/
    analysis_summary.csv
    analysis_report.txt
    rejected_records.txt
```

`analysis_summary.csv` contains one row for each processed session.

`analysis_report.txt` contains a readable explanation of the session results.

`rejected_records.txt` contains information about rows that were rejected.

## Example console output

```text
Accepted rows: 33
Rejected rows: 10
Created files:
output\analysis_summary.csv
output\analysis_report.txt
output\rejected_records.txt
```

## Tests

Run the tests with:

```bash
python tests.py
```

The tests cover:

- valid input files
- invalid input records
- missing files
- boundary values

## Known limitations

- The classification system is rule-based and intentionally simple.
- The measurement ranges are designed for the simulated assignment data and are not intended for medical use.
- If one required value in a row is invalid, the entire row is rejected.
- Recovery detection compares the first and second half of a session, so very short sessions are less useful for recovery analysis.
