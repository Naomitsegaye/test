# IMPORT PACKAGES AND OBJECTS 
from friend_swiping_file import get_friend_swiping_page
from initialize_file import get_initialize_page
from login_signup_file import get_login_signup_page
from create_account_file import get_create_account_page
from sign_in_file import get_sign_in_page
from admin_landing_file import get_admin_landing_page
from student_landing_file import get_student_landing_page
from profile_info_file import get_profile_info_page
from population_data_file import full_population_df
import streamlit as st
from activities_recommender_file import get_activities_recommender_page

get_initialize_page()  
if st.session_state.page == 'login_signup_page':
    get_login_signup_page()  
elif st.session_state.page == 'create_account_page':
    get_create_account_page()  
elif st.session_state.page == 'sign_in_page':
    get_sign_in_page()  
elif st.session_state.page == 'admin_landing_page':
    get_admin_landing_page()  
elif st.session_state.page == 'student_landing_page':
    get_student_landing_page()  
elif st.session_state.page == 'friend_swiping_page':  
    get_friend_swiping_page()
elif st.session_state.page == 'profile_info_page':
    get_profile_info_page()
elif st.session_state.page == 'activities_recommender_page':
    get_activities_recommender_page()
