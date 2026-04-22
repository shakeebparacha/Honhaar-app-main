import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import uuid

# Set page config
st.set_page_config(page_title="Student Account Manager", layout="wide")

# Data storage path
DATA_FILE = "student_data.json"
ADMIN_PASSWORD = "admin123"  # Change this to your desired password

# Initialize session state
if 'show_admin_login' not in st.session_state:
    st.session_state.show_admin_login = False
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'submission_id' not in st.session_state:
    st.session_state.submission_id = None

def load_data():
    """Load existing data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_student_record(student_data):
    """Add new student record and return submission ID"""
    data = load_data()
    submission_id = str(uuid.uuid4())[:8].upper()  # Generate unique ID
    student_data['submission_id'] = submission_id
    data.append(student_data)
    save_data(data)
    return submission_id

def get_record_by_submission_id(submission_id):
    """Retrieve a record by submission ID"""
    data = load_data()
    for record in data:
        if record.get('submission_id') == submission_id:
            return record
    return None

def main():
    st.title("📚 Student Account Manager")
    st.markdown("Store student or guardian account information based on age")
    st.divider()
    
    # Top Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([2, 2, 1])
    
    with col_nav3:
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.show_admin_login = True
    
    # Admin Login Section (when clicked)
    if st.session_state.get('show_admin_login', False):
        st.warning("### Admin Login")
        admin_password = st.text_input("Enter Admin Password", type="password", key="admin_pwd_input")
        col_login1, col_login2 = st.columns(2)
        with col_login1:
            if st.button("Login", use_container_width=True, type="primary"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.session_state.show_admin_login = False
                    st.success("✅ Admin logged in!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password!")
        with col_login2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_admin_login = False
                st.rerun()
        st.divider()
    
    # Check if admin is logged in
    if st.session_state.admin_logged_in:
        # =============== ADMIN VIEW ===============
        st.success("✅ Admin Mode Active")
        col_logout = st.columns([1, 1, 1, 1, 1])[-1]
        with col_logout:
            if st.button("Logout", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        st.divider()
        st.header("🔍 Admin Dashboard")
        
        # Load data
        data = load_data()
        
        if data:
            total_records = len(data)
            student_records = sum(1 for record in data if record.get('type') == 'student')
            guardian_records = sum(1 for record in data if record.get('type') == 'guardian')
            
            metric1, metric2, metric3 = st.columns(3)
            with metric1:
                st.metric("Total Records", total_records)
            with metric2:
                st.metric("Age > 18 Records", student_records)
            with metric3:
                st.metric("Age ≤ 18 Records", guardian_records)
            
            st.divider()
            
            # Filter options
            filter_type = st.selectbox("Filter by Type", ["All", "Students (Age > 18)", "Guardians (Age ≤ 18)"])
            search_id = st.text_input("Search by Submission ID or App ID")
            
            # Apply filters
            if filter_type == "All":
                filtered_records = data
            elif filter_type == "Students (Age > 18)":
                filtered_records = [r for r in data if r.get('type') == 'student']
            else:
                filtered_records = [r for r in data if r.get('type') == 'guardian']
            
            if search_id:
                filtered_records = [r for r in filtered_records if search_id.upper() in r.get('submission_id', '').upper() or search_id.upper() in r.get('app_id', '').upper()]
            
            st.subheader(f"📋 Records ({len(filtered_records)} found)")
            
            if filtered_records:
                # Create detailed view
                display_detail = []
                for record in filtered_records:
                    if record.get('type') == 'student':
                        display_detail.append({
                            "📌 ID": record.get('submission_id'),
                            "App ID": record.get('app_id'),
                            "Email": record.get('email'),
                            "ID Card": record.get('id_card_no'),
                            "Status": record.get('recommended_status'),
                            "Bank": record.get('bank_name'),
                            "Account/IBAN": record.get('account_no_iban'),
                            "Department": record.get('department_name'),
                            "Remarks": record.get('remarks', ''),
                            "Submitted": record.get('timestamp')
                        })
                    else:
                        display_detail.append({
                            "📌 ID": record.get('submission_id'),
                            "App ID": record.get('app_id'),
                            "Candidate": record.get('name_candidate'),
                            "Contact": record.get('contact_no'),
                            "Guardian": record.get('guardian_name'),
                            "Bank": record.get('bank_name'),
                            "Account/IBAN": record.get('account_no_iban'),
                            "Department": record.get('department_name'),
                            "Remarks": record.get('remarks', ''),
                            "Submitted": record.get('timestamp')
                        })
                
                df_detail = pd.DataFrame(display_detail)
                st.dataframe(df_detail, use_container_width=True, hide_index=True)
                
                st.divider()
                
                # Export all records
                if st.button("📥 Export to CSV", use_container_width=True):
                    display_export = []
                    for record in filtered_records:
                        if record.get('type') == 'student':
                            display_export.append({
                                "Submission ID": record.get('submission_id'),
                                "Type": "Student",
                                "App ID": record.get('app_id'),
                                "Email": record.get('email'),
                                "ID Card": record.get('id_card_no'),
                                "Status": record.get('recommended_status'),
                                "Bank Name": record.get('bank_name'),
                                "Account/IBAN": record.get('account_no_iban'),
                                "Department": record.get('department_name'),
                                "Remarks": record.get('remarks'),
                                "Timestamp": record.get('timestamp')
                            })
                        else:
                            display_export.append({
                                "Submission ID": record.get('submission_id'),
                                "Type": "Guardian",
                                "App ID": record.get('app_id'),
                                "Candidate": record.get('name_candidate'),
                                "Contact No": record.get('contact_no'),
                                "CNIC B-Form": record.get('cnic_b_form'),
                                "DOB": record.get('dob'),
                                "Age": record.get('age'),
                                "Department": record.get('department_name'),
                                "Guardian Name": record.get('guardian_name'),
                                "Guardian CNIC": record.get('guardian_cnic'),
                                "Relation": record.get('relation'),
                                "Account/IBAN": record.get('account_no_iban'),
                                "Account Title": record.get('title_account'),
                                "Bank Name": record.get('bank_name'),
                                "Remarks": record.get('remarks'),
                                "Timestamp": record.get('timestamp')
                            })
                    
                    csv = pd.DataFrame(display_export).to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name=f"all_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            else:
                st.info("No records found.")
        else:
            st.info("📭 No records in the system yet.")
    
    else:
        # =============== STUDENT VIEW ===============
        st.info("👤 Student Mode - Fill the form below to submit your information")
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("📝 Submit Your Information")
            
            # Show submission confirmation
            if st.session_state.submission_id:
                st.success(f"""
                ✅ **Your data has been successfully submitted!**
                
                **Your Reference Number: `{st.session_state.submission_id}`**
                
                Save this number to view your submission later.
                """)
                st.divider()
                if st.button("Submit Another Record", use_container_width=True):
                    st.session_state.submission_id = None
                    st.rerun()
            else:
                # Basic Information
                st.subheader("Basic Information")
                app_id = st.text_input("Application ID", key="app_id")
                age = st.number_input("Age", min_value=1, max_value=100, key="age")
                department_name = st.text_input("Department Name", key="department_name")
                
                st.divider()
                
                if age > 18:
                    st.subheader("📋 Your Information (Age > 18)")
                    email = st.text_input("Email", key="email")
                    id_card_no = st.text_input("ID Card Number", key="id_card_no")
                    recommended_status = st.selectbox("Recommended Status", ["Approved", "Hold", "Rejected", "Pending"], key="rec_status")
                    bank_name = st.text_input("Bank Name", key="bank_name_adult")
                    account_no_iban = st.text_input("Account No. / IBAN", key="account_iban_adult")
                    remarks_adults = st.text_area("Remarks", key="remarks_adult", height=80)
                    
                    st.divider()
                    
                    if st.button("📤 Submit Record", use_container_width=True, type="primary"):
                        if not app_id or not email or not id_card_no or not bank_name or not account_no_iban:
                            st.error("❌ Please fill in all required fields!")
                        else:
                            record = {
                                "type": "student",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "app_id": app_id,
                                "email": email,
                                "id_card_no": id_card_no,
                                "recommended_status": recommended_status,
                                "bank_name": bank_name,
                                "account_no_iban": account_no_iban,
                                "remarks": remarks_adults,
                                "department_name": department_name,
                                "age": age
                            }
                            submission_id = add_student_record(record)
                            st.session_state.submission_id = submission_id
                            st.rerun()
                else:
                    st.subheader("👨‍👩‍👧 Guardian Information (Age ≤ 18)")
                    name_candidate = st.text_input("Name of Candidate", key="name_candidate")
                    contact_no = st.text_input("Contact No", key="contact_no")
                    cnic_b_form = st.text_input("CNIC B-Form Number", key="cnic_b_form")
                    
                    st.markdown("**Date of Birth**")
                    col_dob1, col_dob2, col_dob3 = st.columns(3)
                    with col_dob1:
                        dob_day = st.number_input("Day", min_value=1, max_value=31, key="dob_day")
                    with col_dob2:
                        dob_month = st.number_input("Month", min_value=1, max_value=12, key="dob_month")
                    with col_dob3:
                        dob_year = st.number_input("Year", min_value=1900, max_value=2024, key="dob_year")
                    
                    guardian_name = st.text_input("Guardian Name", key="guardian_name_minor")
                    guardian_cnic = st.text_input("Guardian CNIC No.", key="guardian_cnic")
                    relation = st.text_input("Relation to Student", key="relation_minor")
                    account_no_iban_minor = st.text_input("Account No / Complete IBAN", key="account_iban_minor")
                    title_account = st.text_input("Title of Account", key="title_account")
                    bank_name_minor = st.text_input("Bank Name", key="bank_name_minor")
                    remarks_minor = st.text_area("Remarks", key="remarks_minor", height=80)
                    
                    st.divider()
                    
                    if st.button("📤 Submit Record", use_container_width=True, type="primary"):
                        if not app_id or not name_candidate or not contact_no or not cnic_b_form or not guardian_name or not guardian_cnic:
                            st.error("❌ Please fill in all required fields!")
                        else:
                            record = {
                                "type": "guardian",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "app_id": app_id,
                                "name_candidate": name_candidate,
                                "contact_no": contact_no,
                                "cnic_b_form": cnic_b_form,
                                "dob": f"{dob_day:02d}/{dob_month:02d}/{dob_year}",
                                "age": age,
                                "department_name": department_name,
                                "guardian_name": guardian_name,
                                "guardian_cnic": guardian_cnic,
                                "relation": relation,
                                "account_no_iban": account_no_iban_minor,
                                "title_account": title_account,
                                "bank_name": bank_name_minor,
                                "remarks": remarks_minor
                            }
                            submission_id = add_student_record(record)
                            st.session_state.submission_id = submission_id
                            st.rerun()
        
        with col2:
            st.header("🔍 View Your Submission")
            st.markdown("Enter your **Reference Number** to view your submitted information")
            
            search_submission_id = st.text_input("Enter Your Reference Number (e.g., ABC12345)", key="search_ref", placeholder="Your Reference Number")
            
            if st.button("Search", use_container_width=True, type="secondary"):
                if search_submission_id.strip():
                    record = get_record_by_submission_id(search_submission_id.upper().strip())
                    if record:
                        st.success("✅ Your record found!")
                        st.divider()
                        
                        if record.get('type') == 'student':
                            st.subheader("📋 Your Information")
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.write(f"**App ID:** {record.get('app_id')}")
                                st.write(f"**Email:** {record.get('email')}")
                                st.write(f"**ID Card:** {record.get('id_card_no')}")
                            with col_info2:
                                st.write(f"**Age:** {record.get('age')}")
                                st.write(f"**Department:** {record.get('department_name')}")
                                st.write(f"**Status:** {record.get('recommended_status')}")
                            
                            st.divider()
                            st.write(f"**Bank Name:** {record.get('bank_name')}")
                            st.write(f"**Account/IBAN:** {record.get('account_no_iban')}")
                            st.write(f"**Remarks:** {record.get('remarks', 'N/A')}")
                            st.write(f"**Submitted:** {record.get('timestamp')}")
                        else:
                            st.subheader("👨‍👩‍👧 Your Information")
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.write(f"**Name:** {record.get('name_candidate')}")
                                st.write(f"**App ID:** {record.get('app_id')}")
                                st.write(f"**Contact:** {record.get('contact_no')}")
                                st.write(f"**CNIC B-Form:** {record.get('cnic_b_form')}")
                                st.write(f"**DOB:** {record.get('dob')}")
                            with col_info2:
                                st.write(f"**Age:** {record.get('age')}")
                                st.write(f"**Department:** {record.get('department_name')}")
                                st.write(f"**Guardian:** {record.get('guardian_name')}")
                                st.write(f"**Relation:** {record.get('relation')}")
                            
                            st.divider()
                            st.write(f"**Bank Name:** {record.get('bank_name')}")
                            st.write(f"**Account Title:** {record.get('title_account')}")
                            st.write(f"**Account/IBAN:** {record.get('account_no_iban')}")
                            st.write(f"**Remarks:** {record.get('remarks', 'N/A')}")
                            st.write(f"**Submitted:** {record.get('timestamp')}")
                    else:
                        st.error("❌ Reference Number not found. Please check and try again.")
                else:
                    st.error("❌ Please enter a Reference Number.")
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    **📌 Note:** 
    - Students receive a unique Reference Number after submission
    - Use the Reference Number to view your own submitted information
    - Admins can access all records with secure password login
    - All data is automatically saved and can be exported
    """)

if __name__ == "__main__":
    main()
