import praw
import re
from collections import defaultdict

# Reddit API credentials
reddit = praw.Reddit(
    client_id='BIaJAboCWFSmpjvLV3HICg',
    client_secret='mQqJsYO3gCU8ALDkAt0Y-qgHR8qa4w',
    user_agent='BodyTypeAnalyzer/1.0 by Unhappy_Fig_9780'
)

# Initialize counter and regex pattern
body_type_counts = defaultdict(int)
pattern = re.compile(r'\b\d{1,2}\b')  # Matches 1-2 digit numbers

# Get the submission
submission = reddit.submission(url="https://www.reddit.com/r/trueratediscussions/comments/1ibpz4n/which_body_type_is_more_attractive_in_women_in/")

# Expand all comments
submission.comments.replace_more(limit=None)

# Process comments
for comment in submission.comments.list():
    # Skip deleted/removed comments
    if not comment.body or comment.body == '[removed]' or comment.body == '[deleted]':
        continue
    
    # Find all numbers in comment
    numbers = pattern.findall(comment.body)
    
    # Convert to integers and filter valid body types (1-17)
    valid_numbers = [int(num) for num in numbers if 1 <= int(num) <= 17]
    
    # Update counts
    for num in valid_numbers:
        body_type_counts[num] += 1

# Sort results
sorted_results = sorted(body_type_counts.items(), key=lambda x: x[1], reverse=True)

# Calculate total votes for percentages
total_votes = sum(count for _, count in sorted_results)

# Print formatted results
print("\nBody Type Preference Analysis")
print("=============================")
print(f"Total Votes: {total_votes}")
print("\nRank | Body Type | Votes | Percentage")
print("-----|-----------|-------|-----------")

for rank, (body_type, count) in enumerate(sorted_results, 1):
    percentage = (count / total_votes) * 100
    print(f"{rank:4d} | {body_type:9d} | {count:5d} | {percentage:6.1f}%")

# Add visualization
print("\nTop Preferences Visualization:")
max_bar_length = 40
max_count = max(count for _, count in sorted_results)

for body_type, count in sorted_results:
    bar_length = int((count / max_count) * max_bar_length)
    bar = '▇' * bar_length
    print(f"{body_type:2d} | {bar:{max_bar_length}} | {count}")
