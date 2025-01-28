import praw
import re
import matplotlib.pyplot as plt  # Import matplotlib for visualization

def analyze_reddit_post(post_url):
    """
    Analyzes a Reddit post to count mentions of body types (numbers 1-18) in comments.

    Args:
        post_url (str): The URL of the Reddit post.

    Returns:
        dict: A dictionary where keys are body type numbers (1-18) and values
              are the counts of mentions in the comments.
    """

    # 1. Reddit API Credentials (Replace with your own!)
    reddit = praw.Reddit(
        client_id='BIaJAboCWFSmpjvLV3HICg',
        client_secret='mQqJsYO3gCU8ALDkAt0Y-qgHR8qa4w',
        user_agent='BodyTypeAnalyzer/1.0 by Unhappy_Fig_9780'
    )

    # 2. Get Reddit Post
    try:
        submission = reddit.submission(url=post_url)
    except Exception as e:
        print(f"Error fetching Reddit post: {e}")
        return None

    # 3. Fetch Comments (and handle "load more comments" if needed for very large threads)
    submission.comment_sort = "best" # You can choose comment sorting (best, top, new, etc.)
    submission.comments.replace_more(limit=None) # Fetch all "load more comments" - be careful with very large threads

    comments = submission.comments.list()

    # 4. Count Body Type Mentions
    body_type_counts = {str(i): 0 for i in range(1, 19)} # Initialize counts for 1 to 18

    for comment in comments:
        comment_text = comment.body.lower() # Convert to lowercase for easier matching

        # Use regular expressions to find numbers 1-18 (as words or digits)
        for i in range(1, 19):
            number_str = str(i)
            # Regex to find the number as a whole word or surrounded by non-alphanumeric characters
            pattern = r'\b' + re.escape(number_str) + r'\b'  # \b for word boundary, re.escape for literal number

            mentions = re.findall(pattern, comment_text)
            body_type_counts[number_str] += len(mentions)

    return body_type_counts

def display_results(body_type_counts):
    """
    Displays the body type mention counts in a sorted bar chart for better visualization.

    Args:
        body_type_counts (dict): Dictionary of body type counts from analyze_reddit_post.
    """
    if not body_type_counts:
        print("No body type counts found or analysis failed.")
        return

    sorted_body_types = sorted(body_type_counts.items(), key=lambda item: item[1], reverse=True) # Sort by count descending

    body_types = [item[0] for item in sorted_body_types]
    counts = [item[1] for item in sorted_body_types]

    plt.figure(figsize=(10, 6)) # Adjust figure size as needed for better readability
    plt.bar(body_types, counts, color='skyblue') # Create a bar chart, you can change color

    plt.xlabel("Body Type Number")
    plt.ylabel("Number of Mentions")
    plt.title("Reddit's Top Body Type Preferences")
    plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability if needed
    plt.tight_layout() # Adjust layout to prevent labels from being cut off
    plt.show() # Display the chart

if __name__ == "__main__":
    reddit_post_url = "https://www.reddit.com/r/trueratediscussions/comments/1ibpz4n/which_body_type_is_more_attractive_in_women_in/" # Your Reddit post URL
    counts = analyze_reddit_post(reddit_post_url)

    if counts:
        display_results(counts)