import sys
import os
import subprocess
import pandas as pd
import streamlit as st
import random

def install_required_packages():
    """Install required packages if they're not already installed"""
    required_packages = ['pandas', 'streamlit']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{package} installed successfully!")

# Install required packages
print("Checking and installing required packages...")
install_required_packages()

# Create expanded dataset with personality and interests
friend_swiping_data = {
    'name': ['Me', 'Alex', 'Taylor', 'Jordan', 'Morgan', 'Chris', 'Sam', 'Riley', 'Jamie', 'Casey'],
    'age': [25, 22, 28, 24, 30, 27, 23, 29, 26, 31],
    'personality': ['Introverted', 'Extroverted', 'Introverted', 'Extroverted', 'Introverted', 
                   'Extroverted', 'Introverted', 'Extroverted', 'Introverted', 'Extroverted'],
    'interest': ['Gaming', 'Reading', 'Gaming', 'Travel', 'Music', 
                 'Sports', 'Gaming', 'Reading', 'Travel', 'Music'],
    'bio': [
        "Loves gaming and quiet evenings.",
        "Avid reader and aspiring writer.",
        "Tech enthusiast and gamer.",
        "Foodie and world traveler.",
        "Music producer and DJ.",
        "Sports fanatic and coach.",
        "Gaming streamer and developer.",
        "Book club organizer.",
        "Adventure seeker.",
        "Classical musician."
    ],
    'img': [
        "https://randomuser.me/api/portraits/men/10.jpg",
        "https://randomuser.me/api/portraits/women/21.jpg",
        "https://randomuser.me/api/portraits/men/33.jpg",
        "https://randomuser.me/api/portraits/women/45.jpg",
        "https://randomuser.me/api/portraits/men/67.jpg",
        "https://randomuser.me/api/portraits/women/89.jpg",
        "https://randomuser.me/api/portraits/men/91.jpg",
        "https://randomuser.me/api/portraits/women/12.jpg",
        "https://randomuser.me/api/portraits/men/34.jpg",
        "https://randomuser.me/api/portraits/women/56.jpg"
    ],
    'swipes_on_me': ['No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']
}

# Create DataFrame and add empty columns for tracking
friend_swiping_df = pd.DataFrame(friend_swiping_data)
friend_swiping_df['my_swipes'] = ''
friend_swiping_df['mutual_matches'] = ''

# Get my personality and interest
my_personality = friend_swiping_df.loc[friend_swiping_df['name'] == 'Me', 'personality'].iloc[0]
my_interest = friend_swiping_df.loc[friend_swiping_df['name'] == 'Me', 'interest'].iloc[0]

# Filter DataFrame to show only people with similar interests or personality
filtered_df = friend_swiping_df[
    ((friend_swiping_df['personality'] == my_personality) | 
     (friend_swiping_df['interest'] == my_interest)) &
    (friend_swiping_df['name'] != 'Me')
].copy()

def update_matches(df):
    """Update mutual_matches based on swipe patterns"""
    conditions = [
        (df['swipes_on_me'] == 'Yes') & (df['my_swipes'] == 'Yes'),
        (df['swipes_on_me'] == 'Yes') & (df['my_swipes'] == 'No'),
        (df['swipes_on_me'] == 'No') & (df['my_swipes'] == 'Yes'),
        (df['swipes_on_me'] == 'No') & (df['my_swipes'] == 'No')
    ]
    choices = ['Match', 'Potential Friend', 'No', 'No']
    df['mutual_matches'] = np.select(conditions, choices, default='')
    return df

def get_friend_swiping_page(df):
    st.title("Friend Finder Swiping App")
    
    # Initialize session state variables
    if 'profile_index' not in st.session_state:
        st.session_state.profile_index = 0
    
    def show_profile(profile):
        st.image(profile['img'], width=300)
        st.write(f"**{profile['name']}, {profile['age']}**")
        st.write(f"Personality: {profile['personality']}")
        st.write(f"Interest: {profile['interest']}")
        st.write(f"_{profile['bio']}_")
    
    # Check if there are more profiles to show
    if st.session_state.profile_index < len(df):
        current_profile = df.iloc[st.session_state.profile_index]
        show_profile(current_profile)
        
        # Buttons for Like and Dislike
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❤️ Like"):
                # Update my_swipes to Yes
                df.at[df.index[st.session_state.profile_index], 'my_swipes'] = 'Yes'
                df = update_matches(df)
                st.session_state.profile_index += 1
        
        with col2:
            if st.button("❌ Dislike"):
                # Update my_swipes to No
                df.at[df.index[st.session_state.profile_index], 'my_swipes'] = 'No'
                df = update_matches(df)
                st.session_state.profile_index += 1
    else:
        st.write("No more profiles to show!")
    
    # Show matches and potential friends
    st.subheader("Your Matches")
    matches = df[df['mutual_matches'] == 'Match']
    if not matches.empty:
        for _, match in matches.iterrows():
            st.write(f"🤝 {match['name']} - {match['interest']} enthusiast")
    else:
        st.write("No matches yet!")
    
    st.subheader("Potential Friends")
    potential_friends = df[df['mutual_matches'] == 'Potential Friend']
    if not potential_friends.empty:
        for _, friend in potential_friends.iterrows():
            st.write(f"👋 {friend['name']} - {friend['interest']} enthusiast")
    else:
        st.write("No potential friends yet!")

if __name__ == "__main__":
    # Run the app
    print("Starting Friend Finder App...")
    get_friend_swiping_page(filtered_df)
