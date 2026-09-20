# Email Extractor

A simple Python automation tool that extracts email addresses from a text file and saves the results into a separate file.

## Features

* Reads text from an input file
* Extracts email addresses using Regular Expressions (Regex)
* Removes duplicate email addresses
* Saves unique email addresses to an output file
* Displays the number of extracted email addresses

## Files

* `email_extractor.py` — Main Python program
* `input.txt` — Contains the text to search
* `emails.txt` — Contains the extracted unique email addresses

## Technologies Used

* Python
* `re` module
* File handling

## How It Works

1. The program reads the content of `input.txt`.
2. It uses Regex to find email addresses.
3. Duplicate email addresses are removed.
4. The unique emails are saved in `emails.txt`.
5. The program displays the extracted emails and their total number.

## Example

If the input contains:

```text
Contact Ahmed at ahmed@gmail.com.
For registration, email registration@university.org.
You can also contact Ahmed at ahmed@gmail.com.
```

The output will contain:

```text
ahmed@gmail.com
registration@university.org
```

