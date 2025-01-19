import sqlite3
import time

# Initialize database
def init_db():
    conn = sqlite3.connect("offline_posts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            hater_name TEXT,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    """)
    conn.commit()
    conn.close()

# Add a new post
def add_post(content):
    conn = sqlite3.connect("offline_posts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

# Add a comment to a post
def add_comment(post_id, content, hater_name=None):
    conn = sqlite3.connect("offline_posts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (post_id, content, hater_name) VALUES (?, ?, ?)", (post_id, content, hater_name))
    conn.commit()
    conn.close()

# Get all posts
def get_posts():
    conn = sqlite3.connect("offline_posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return posts

# Get all comments for a post
def get_comments(post_id):
    conn = sqlite3.connect("offline_posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE post_id = ?", (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

# Add multiple comments from file
def add_comments_from_file(post_id, file_path, delay, hater_name=None):
    try:
        with open(file_path, 'r') as file:
            comments = file.readlines()
        for comment in comments:
            add_comment(post_id, comment.strip(), hater_name)
            print(f"Added comment: {comment.strip()}")
            time.sleep(delay)
    except FileNotFoundError:
        print("Error: File not found!")

# Main Program
if __name__ == "__main__":
    init_db()
    token = input("Enter your access token: ")
    if token != "12345":  # Replace with your token validation logic
        print("Invalid token! Exiting...")
    else:
        while True:
            print("\nOffline Post-Comment System")
            print("1. Add Post")
            print("2. Add Comment")
            print("3. Add Comments from File")
            print("4. View Posts")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                content = input("Enter post content: ")
                add_post(content)
                print("Post added successfully!")
            elif choice == "2":
                post_id = int(input("Enter Post ID to comment on: "))
                content = input("Enter comment content: ")
                hater_name = input("Enter hater name (if any): ")
                add_comment(post_id, content, hater_name)
                print("Comment added successfully!")
            elif choice == "3":
                post_id = int(input("Enter Post ID to comment on: "))
                file_path = input("Enter comments file path: ")
                delay = int(input("Enter delay (in seconds) between comments: "))
                hater_name = input("Enter hater name (if any): ")
                add_comments_from_file(post_id, file_path, delay, hater_name)
            elif choice == "4":
                posts = get_posts()
                if not posts:
                    print("No posts available.")
                else:
                    for post in posts:
                        print(f"\nPost ID: {post[0]}, Content: {post[1]}")
                        comments = get_comments(post[0])
                        if comments:
                            for comment in comments:
                                print(f"  - Comment ID: {comment[0]}, Content: {comment[2]}, Hater: {comment[3]}")
                        else:
                            print("  No comments yet.")
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
