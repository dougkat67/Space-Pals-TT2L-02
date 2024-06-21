import os
import subprocess

# Define the simplified shell script content for debugging
shell_script = '''#!/bin/bash

echo "Running git log command..."
git log --pretty=format:"%h %ae" --numstat

echo "Processing output with awk..."
git log --pretty=format:"%h %ae" --numstat | awk '
    {
        print $0  # Print each line for debugging
        if (NF == 3) {
            insertions[$2] += $1
            deletions[$2] += $2
            total_lines[$2] += ($1 + $2)
            files[$2]++
        } else if (NF == 2) {
            commits[$2]++
        }
    }
    END {
        printf "%-30s %-10s %-10s %-10s %-10s %-10s\\n", "Email", "Commits", "Files", "Insertions", "Deletions", "Total Lines"
        for (email in commits) {
            printf "%-30s %-10d %-10d %-10d %-10d %-10d\\n", email, commits[email], files[email], insertions[email], deletions[email], total_lines[email]
        }
    }
' OFS="\\t"
'''

# Specify the file name for the shell script
script_filename = 'git-user-stats.sh'

# Write the shell script to a file
with open(script_filename, 'w') as file:
    file.write(shell_script)

# Make the script executable
os.chmod(script_filename, 0o755)

# Specify the path to the Git repository
repo_path = 'C:/Users/isabe/Documents/TT2L-02'  # Update this path to your repository path

# Change the current working directory to the repository
os.chdir(repo_path)

# Run the script using Git Bash
git_bash_path = 'C:/Program Files/Git/git-bash.exe'  # Update this path to where Git Bash is installed
try:
    result = subprocess.run([git_bash_path, '-c', './' + script_filename], capture_output=True, text=True, check=True)
    print("Script executed successfully")
    print("Output:")
    print(result.stdout)
    print("Error output (if any):")
    print(result.stderr)
except subprocess.CalledProcessError as e:
    print("Error executing script")
    print("Return code:", e.returncode)
    print("Output:", e.output)
    print("Error output:", e.stderr)
except Exception as e:
    print("An unexpected error occurred")
    print(str(e))