# List of letters used to label the multiple-choice options
choices = ["A", "B", "C", "D"]

def format_subject(subject):
    """
    Convert a snake_case subject string into a space-separated phrase.
    
    For example:
        "computer_science" -> " computer science"
    
    Args:
        subject (str): Subject name in snake_case.
    
    Returns:
        str: Subject name with words separated by spaces.
    """
    # Split the string on underscores
    parts = subject.split("_")
    result = ""
    # Concatenate each part, prefixing a space
    for word in parts:
        result += " " + word
    return result

def format_example(df, idx, include_answer=True):
    """
    Generate the text for a single multiple-choice question example.
    
    The resulting format is:
        Follow the answer instructions strictly, and answer only with the letter corresponding to the correct answer:<question>
        A. <option 1>
        B. <option 2>
        ...
         - Answer: <letter>
    
    Args:
        df (pandas.DataFrame): DataFrame with columns [question, option1, option2, ..., answer].
        idx (int): Index of the row to format.
        include_answer (bool): If True, include the correct answer at the end.
    
    Returns:
        str: Formatted text containing the question, options, and (optionally) the answer.
    """
    # Header with instructions for the model
    prompt = "Follow the answer instructions strictly, and answer only with the letter corresponding to the correct answer: "
    # Add the question text (column 0)
    prompt += df.iloc[idx, 0]
    
    # Calculate the number of options (all columns except question and answer)
    num_options = df.shape[1] - 2
    # Iterate over each option and append to the prompt
    for j in range(num_options):
        letter = choices[j]
        option_text = df.iloc[idx, j + 1]
        prompt += "\n{}. {}".format(letter, option_text)
    
    # Marker to add the answer
    prompt += "\n - Answer:"
    if include_answer:
        # Add the correct answer (last column)
        answer = df.iloc[idx, num_options + 1]
        prompt += " {}\n\n".format(answer)
    return prompt

def gen_prompt(train_df, subject, k=-1):
    """
    Build a full prompt containing multiple question examples.
    
    Starts with an introduction mentioning the subject, then includes up to k examples
    (or all examples if k = -1).
    
    Args:
        train_df (pandas.DataFrame): Training DataFrame with questions and answers.
        subject (str): Subject name in snake_case to include in the introduction.
        k (int): Number of examples to include. -1 for all.
    
    Returns:
        str: Complete prompt with introduction and examples.
    """
    # Introduction mentioning the subject
    intro = "The following are multiple choice questions (with answers) about {}.\n\n"
    prompt = intro.format(format_subject(subject))
    
    # If k is not specified, use all rows of the DataFrame
    if k == -1:
        k = train_df.shape[0]
    
    # Append each formatted example to the prompt
    for i in range(k):
        prompt += format_example(train_df, i)
    
    return prompt
