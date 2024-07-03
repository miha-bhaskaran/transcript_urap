import re

def extract_after_backslash(input_string):
    # Regex pattern to find everything after the last backslash
    pattern = r'[^\\]*$'
    
    # # Search for the pattern in the input string
    # match = re.search(pattern, input_string)
    # if match:
    #     print()
    #     return match.group()  # Return the matched substring
    # else:
    #     return "No match found"
    return re.search(r'[^\/]*$', input_string).group()

# Example usage
# input_string = "vaOSL\\page-0.csv"
# result = extract_after_backslash(input_string)
# print("Matched substring:", result)


# extract_after_backslash('vaOSLLIJEPOR/page-1.csv')