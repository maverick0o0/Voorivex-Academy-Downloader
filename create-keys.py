import re

# Read the content from html-data.txt
with open("html-data.txt", "r") as file:
    content = file.read()

# Define the regex patterns and their corresponding format strings
regex_formats = {
    r"bears/(l.*?\.mp4)": "jiujitsu-hunters/00-groups/bears/{}",
    r"hades/(H.*?\.mp4)": "jiujitsu-hunters/00-groups/hades/{}",
    r"hawk/(l.*?\.mp4)": "jiujitsu-hunters/00-groups/hawk/{}",
    r"vampires/(\d.*?\.mp4)": "jiujitsu-hunters/00-groups/vampires/{}",
    r"squidward/(.*?\.mp4)": "jiujitsu-hunters/00-groups/squidward/{}" ,
    r"000-lives\/(l.*?\.mp4)": "jiujitsu-hunters/000-lives/{}" ,
    r"0000-last-stand\/(L.*?\.mp4)": "jiujitsu-hunters/0000-last-stand/{}" ,
}

# Apply the regex patterns and store the results in a list
results = []

for pattern, format_string in regex_formats.items():
    matches = re.findall(pattern, content)
    formatted_results = [format_string.format(match) for match in matches]
    results.extend(formatted_results)

# Save the results in keys.txt
with open("keys.txt", "w") as file:
    file.write("\n".join(results))
