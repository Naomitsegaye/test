import subprocess
import sys
import os
import pandas as pd
import streamlit as st

def install_required_packages():
    """Install required packages if they're not already installed"""
    required_packages = ['pandas', 'streamlit']

    for package in required_packages:
        try:
            # Try importing the package
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{package} installed successfully!")

# Install required packages
print("Checking and installing required packages...")
install_required_packages()

# Create the dataset
friend_swiping_data = {
    'name': ['Me', 'Alex', 'Taylor', 'Jordan', 'Morgan', 'Chris', 'Sam', 'Jamie', 'Pat', 'Drew'],
    'interest': ['Hiking', 'Reading', 'Gaming', 'Traveling', 'Music', 'Hiking', 'Tech', 'Cooking', 'Hiking', 'Music'],
    'personality': ['Adventurous', 'Thoughtful', 'Curious', 'Outgoing', 'Creative', 'Adventurous', 'Analytical', 'Sociable', 'Adventurous', 'Creative'],
    'swipes_on_me': ['Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes']
}

friend_swiping_df = pd.DataFrame(friend_swiping_data)

# Step 1.5: Subset the dataframe to only show profiles with my interest or personality
my_interest = friend_swiping_df.loc[friend_swiping_df['name'] == 'Me', 'interest'].values[0]
my_personality = friend_swiping_df.loc[friend_swiping_df['name'] == 'Me', 'personality'].values[0]

friend_swiping_df = friend_swiping_df[
    (friend_swiping_df['name'] != 'Me') & 
    ((friend_swiping_df['interest'] == my_interest) | (friend_swiping_df['personality'] == my_personality))
]

# Step 2: Add empty columns for 'my_swipes' and 'mutual_matches'
friend_swiping_df['my_swipes'] = ''
friend_swiping_df['mutual_matches'] = ''

# Function to run the swiping page
def get_friend_swiping_page(df):
    # Initialize session state variables
    if 'liked_profiles' not in st.session_state:
        st.session_state.liked_profiles = []
    if 'profile_index' not in st.session_state:
        st.session_state.profile_index = 0

    def show_profile(profile):
        st.write(f"**{profile['name']}, {profile['interest']} - {profile['personality']}**")
        st.write(f"Swipes on me: {profile['swipes_on_me']}")

    st.title("Friend Finder Swiping App")

    # Check if there are more profiles to show
    if st.session_state.profile_index < len(df):
        current_profile = df.iloc[st.session_state.profile_index]
        show_profile(current_profile)

        # Buttons for Like and Dislike
        col1, col2 = st.columns(2)
        if st.session_state.profile_index < len(df):
            if st.button("❤️ Like", key=f"like-{st.session_state.profile_index}"):
                df.at[st.session_state.profile_index, 'my_swipes'] = 'Yes'
                st.session_state.liked_profiles.append(current_profile)
                st.session_state.profile_index += 1

            if st.button("❌ Dislike", key=f"dislike-{st.session_state.profile_index}"):
                df.at[st.session_state.profile_index, 'my_swipes'] = 'No'
                st.session_state.profile_index += 1

    else:
        st.write("No more profiles to show!")

    # Update the 'mutual_matches' column
    df['mutual_matches'] = df.apply(
        lambda row: 'Match' if row['swipes_on_me'] == 'Yes' and row['my_swipes'] == 'Yes' else 
        'Potential Friend' if row['swipes_on_me'] == 'Yes' and row['my_swipes'] == 'No' else 
        'No', axis=1
    )

    # Print out mutual matches or potential friends
    st.subheader("Mutual Matches")
    matches = df[df['mutual_matches'] == 'Match']
    if not matches.empty:
        st.write(matches[['name', 'interest', 'personality']])
    else:
        st.write("No mutual matches yet!")

    st.subheader("Potential Friends")
    potential_friends = df[df['mutual_matches'] == 'Potential Friend']
    if not potential_friends.empty:
        st.write(potential_friends[['name', 'interest', 'personality']])
    else:
        st.write("No potential friends yet!")

if __name__ == "__main__":
    # Run the app
    print("Starting Friend Finder App...")
    get_friend_swiping_page(friend_swiping_df)
