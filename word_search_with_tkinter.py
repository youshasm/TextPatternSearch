import time
from tkinter import *
import re

# KMP search algorithm implementation
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    # Create the longest prefix suffix (lps) array
    lps = [0] * m
    compute_lps_array(pattern, m, lps)

    i = 0  # index for text[]
    j = 0  # index for pattern[]
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def compute_lps_array(pattern, m, lps):
    length = 0  # length of the previous longest prefix suffix
    i = 1
    lps[0] = 0  # lps[0] is always 0

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

# Function to perform KMP search with case sensitivity and whole word options
def search_word_in_file_with_kmp(file_name, search_word, case_sensitive, whole_word):
    kmp_results = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for row_number, line in enumerate(file, start=1):
                line = line.strip()
                
                # Check for case sensitivity
                if not case_sensitive:
                    line = line.lower()
                    search_word = search_word.lower()
                
                # Perform KMP search
                column_index = kmp_search(line, search_word)
                
                # If whole word option is checked, use regex to match whole words only
                if whole_word:
                    pattern = r'\b' + re.escape(search_word) + r'\b'
                    match = re.search(pattern, line)
                    if match:
                        column_index = match.start()
                    else:
                        column_index = -1
                
                if column_index != -1:
                    kmp_results.append([file_name, row_number, column_index + 1])
    except UnicodeDecodeError:
        print(f"Error reading the file {file_name} due to encoding issues.")
        return None  
    return kmp_results  

# Function to perform brute-force search with case sensitivity and whole word options
def search_word_in_file_with_brute_force(file_name, search_word, case_sensitive, whole_word):
    brute_results = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for row_number, line in enumerate(file, start=1):
                line = line.strip()
                
                # Check for case sensitivity
                if not case_sensitive:
                    line = line.lower()
                    search_word = search_word.lower()

                # Use regex for whole word match
                if whole_word:
                    pattern = r'\b' + re.escape(search_word) + r'\b'
                    matches = [(m.start(), m.end()) for m in re.finditer(pattern, line)]
                    for match in matches:
                        brute_results.append([file_name, row_number, match[0] + 1])
                else:
                    for column_index in range(len(line) - len(search_word) + 1):
                        if line[column_index:column_index + len(search_word)] == search_word:
                            brute_results.append([file_name, row_number, column_index + 1])
    except UnicodeDecodeError:
        print(f"Error reading the file {file_name} due to encoding issues.")
        return None  
    return brute_results

# Function to display the search results
def display_result():
    word_to_search = input_field.get()
    files = ['Research#1.txt', 'Research#2.txt', 'Research#3.txt', 'Research#4.txt', 'Research#5.txt',
             'Research#6.txt', 'Research#7.txt', 'Research#8.txt', 'Research#9.txt', 'Research#10.txt']
    
    # Determine if case-sensitive search is enabled
    case_sensitive = check2_var.get() == 1
    
    # Determine if whole word search is enabled
    whole_word = check1_var.get() == 1

    # KMP Search
    result_message1 = []  
    current_time = time.time()
    for file_name in files:
        position = search_word_in_file_with_kmp(file_name, word_to_search, case_sensitive, whole_word)
        if position:
            for p in position:
                result_message1.append(f"Word '{word_to_search}' found in {p[0]} at row {p[1]}, column {p[2]}")

    end_time = time.time()
    kmp_time=end_time - current_time
    result_window1 = Toplevel(window)
    result_window1.geometry("400x300")
    result_window1.configure(bg="light grey")

    # Create scrollable frame for KMP results
    canvas1 = Canvas(result_window1, bg="light grey")
    scrollbar1 = Scrollbar(result_window1, orient="vertical", command=canvas1.yview)
    scrollable_frame1 = Frame(canvas1, bg="light grey")

    scrollable_frame1.bind(
        "<Configure>",
        lambda e: canvas1.configure(scrollregion=canvas1.bbox("all"))
    )

    canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
    canvas1.configure(yscrollcommand=scrollbar1.set)
    heading_label1 = Label(scrollable_frame1, text="KMP Search Results", font=('Arial', 14, 'bold'), bg="light grey")
    heading_label1.pack(pady=10)

    result_text1 = "\n".join(result_message1)  
    result_label1 = Label(scrollable_frame1, text=result_text1, background="light grey", justify=LEFT)
    result_label1.pack(pady=20)

    canvas1.pack(side="left", fill="both", expand=True)
    scrollbar1.pack(side="right", fill="y")

    # Brute Force Search
    current_time = time.time()
    result_message2 = []
    for file_name in files:
        position = search_word_in_file_with_brute_force(file_name, word_to_search, case_sensitive, whole_word)
        if position:
            for p in position:
                result_message2.append(f"Word '{word_to_search}' found in {p[0]} at row {p[1]}, column {p[2]}")

    end_time = time.time()
    brute_force_time=end_time - current_time
    result_window2 = Toplevel(window)
    result_window2.geometry("400x300")
    result_window2.configure(bg="light grey")

    # Create scrollable frame for brute force results
    canvas2 = Canvas(result_window2, bg="light grey")
    scrollbar2 = Scrollbar(result_window2, orient="vertical", command=canvas2.yview)
    scrollable_frame2 = Frame(canvas2, bg="light grey")

    scrollable_frame2.bind(
        "<Configure>",
        lambda e: canvas2.configure(scrollregion=canvas2.bbox("all"))
    )

    canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
    canvas2.configure(yscrollcommand=scrollbar2.set)
    heading_label2 = Label(scrollable_frame2, text="Brute Force Search Results", font=('Arial', 14, 'bold'), bg="light grey")
    heading_label2.pack(pady=10)
    result_text2 = "\n".join(result_message2)  
    result_label2 = Label(scrollable_frame2, text=result_text2, background="light grey", justify=LEFT)
    result_label2.pack(pady=20)

    canvas2.pack(side="left", fill="both", expand=True)
    scrollbar2.pack(side="right", fill="y")
    time_window = Toplevel(window)
    time_window.geometry("300x200")
    time_window.configure(bg="light grey")
    
    # Add labels to display the times
    kmp_time_label = Label(time_window, text=f"KMP Search Time: {kmp_time:.6f} seconds", font=('Arial', 10), bg="light grey")
    brute_force_time_label = Label(time_window, text=f"Brute Force Search Time: {brute_force_time:.6f} seconds", font=('Arial', 10), bg="light grey")
    
    # Pack the labels into the window
    kmp_time_label.pack(pady=20)
    brute_force_time_label.pack(pady=20)

# GUI code to create the search interface
window = Tk()
window.configure(bg="light grey")
window.geometry("550x200")

# Input field and labels
Text1 = Label(window, text="Find what:", background="light grey")
input_field = Entry(window, width=40)

# Whole word match checkbox
check1_var = IntVar()
check1 = Checkbutton(window, text="Match whole word only", variable=check1_var, background="light grey")

# Case sensitive checkbox
check2_var = IntVar()
check2 = Checkbutton(window, text="Match case", variable=check2_var, background="light grey")

# Search and Cancel buttons
search_button = Button(window, text="Search", command=display_result)
stop_button = Button(window, text="Cancel", command=window.destroy)

# Place elements on the window
Text1.place(relx=0.1, rely=0.1)
input_field.place(relx=0.2, rely=0.1)
check1.place(relx=0.05, rely=0.4)
check2.place(relx=0.05, rely=0.6)
search_button.place(relx=0.65, rely=0.1)
stop_button.place(relx=0.75, rely=0.1)

window.mainloop()
