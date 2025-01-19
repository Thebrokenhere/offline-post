import sqlite3
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect("offline_conversations.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            message TEXT NOT NULL,
            sender TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Add a message to the conversation
def add_message(user_name, message, sender):
    conn = sqlite3.connect("offline_conversations.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (user_name, message, sender) 
        VALUES (?, ?, ?)
    """, (user_name, message, sender))
    conn.commit()
    conn.close()

# Get conversation history for a user
def get_conversation(user_name):
    conn = sqlite3.connect("offline_conversations.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT message, sender, timestamp 
        FROM conversations 
        WHERE user_name = ?
        ORDER BY timestamp
    """, (user_name,))
    conversation = cursor.fetchall()
    conn.close()
    return conversation

# Main Program
if __name__ == "__main__":
    init_db()
    print("Offline Chat System")
    print("Type 'STOP' at any time to exit the program.")

    user_name = input("Enter your name: ")

    if user_name.strip().upper() == "STOP":
        print("Program stopped by user.")
        exit()

    while True:
        print("\n1. Start a new conversation")
        print("2. View conversation history")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice.strip().upper() == "STOP":
            print("Program stopped by user.")
            break

        if choice == "1":
            print(f"Starting a new conversation with {user_name}...")
            while True:
                user_message = input(f"{user_name}: ")
                if user_message.strip().upper() == "STOP":
                    print("Program stopped by user.")
                    exit()
                elif user_message.lower() == "exit":
                    print("Conversation ended.")
                    break
                add_message(user_name, user_message, "User")
                bot_reply = f"System Response to: {user_message}"  # You can enhance this with AI-based responses
                print(f"System: {bot_reply}")
                add_message(user_name, bot_reply, "System")
        elif choice == "2":
            conversation = get_conversation(user_name)
            if not conversation:
                print("No conversation history found.")
            else:
                print("\nConversation History:")
                for msg, sender, timestamp in conversation:
                    print(f"[{timestamp}] {sender}: {msg}")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
