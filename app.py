modify this code based on import subprocess
import sys
import os



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

# Now import the required packages
import pandas as pd
import streamlit as st


#### Add more columns with one personality, another column for one interest for dataset foe 10 records and the name me is for myself 
# FRIEND SWIPING DATA
### Create a new column named match with yes or no 
friend_swiping_data = {
    'name': ['Me',''Alex', 'Taylor', 'Jordan', 'Morgan', 'Chris'],
    'age': [25, 22, 28, 24, 30],
    'bio': [
        "Loves hiking and the outdoors.",
        "Avid reader and aspiring writer.",
        "Tech enthusiast and gamer.",
        "Foodie and world traveler.",
        "Music producer and DJ."
    ],
    'img': [
        "https://randomuser.me/api/portraits/men/10.jpg",
        "https://randomuser.me/api/portraits/women/21.jpg",
        "https://randomuser.me/api/portraits/men/33.jpg",
        "https://randomuser.me/api/portraits/women/45.jpg",
        "https://randomuser.me/api/portraits/men/67.jpg"
    ]
}

friend_swiping_df = pd.DataFrame(friend_swiping_data)


# GET FRIEND SWIPING VISUAL FUNCTION
## Filter in the dataset has similar interest and personality 
def get_friend_swiping_page(df):
    # Initialize session state variables
    if 'liked_profiles' not in st.session_state:
        st.session_state.liked_profiles = []
    if 'profile_index' not in st.session_state:
        st.session_state.profile_index = 0

    def show_profile(profile):
        st.image(profile['img'], width=300)
        st.write(f"**{profile['name']}, {profile['age']}**")
        st.write(f"_{profile['bio']}_")

    st.title("Friend Finder Swiping App")

    ## add a column for my matches based on ppl I have matched and update it in the dataset everytime make a match
    # Check if there are more profiles to show
    if st.session_state.profile_index < len(df):
        current_profile = df.iloc[st.session_state.profile_index]
        show_profile(current_profile)

        # Buttons for Like and Dislike
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❤️ Like"):
                st.session_state.liked_profiles.append(current_profile)
                st.session_state.profile_index += 1
        with col2:
            if st.button("❌ Dislike"):
                st.session_state.profile_index += 1
    else:
        st.write("No more profiles to show!")

    # Show the list of liked profiles
    st.subheader("Liked Profiles")
    if st.session_state.liked_profiles:
        for idx, liked in enumerate(st.session_state.liked_profiles):
            st.write(f"{idx + 1}. {liked['name']}, {liked['age']} - {liked['bio']}")
    else:
        st.write("You haven't liked anyone yet!")


if __name__ == "__main__":
    # Run the app
    print("Starting Friend Finder App...")
    get_friend_swiping_page(friend_swiping_df)
