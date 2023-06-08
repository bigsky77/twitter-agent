def generate_markdown_table(reports):
    header = ["Agent Name", "Agent ID", "Follower Count", "Average Likes to Followers Ratio"]
    markdown_table = "| " + " | ".join(header) + " |\n"
    markdown_table += "| " + " | ".join("---" for _ in header) + " |\n"

    for report in reports:
        row = [report["Agent Name"], report["Agent ID"], report["Follower Count"], report["Average Likes to Followers Ratio"]]
        markdown_table += "| " + " | ".join(str(cell) for cell in row) + " |\n"

    return markdown_table

def update_readme(reports):
    # Read the current README file
    with open("README.md", "r") as f:
        lines = f.readlines()

    # Generate the markdown table
    markdown_table = generate_markdown_table(reports)

    # Find the line to replace in the README (I'm assuming it's a line starting with "## Currently Deployed Agents")
    line_number = next(i for i, line in enumerate(lines) if line.startswith("## Currently Deployed Agents"))

    # Replace the line with the new markdown table
    lines[line_number + 1] = markdown_table

    # Write the updated README back to the file
    with open("README.md", "w") as f:
        f.writelines(lines)
