text = """

"""

# Split up the text by lines.
lines = text.split("\n")

lines = [line.strip() if line.strip() != "@@@" else "" for line in lines]

# Print each line.
for line in lines:
    # if line != "":
    #     print(line)
    print(line)
