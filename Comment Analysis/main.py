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

# Display results
print("Body Type Rating Summary:")
print("=========================")
for body_type, count in sorted_results:
    print(f"Body Type {body_type}: {count} votes")