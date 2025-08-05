import streamlit as st

st.title("🧪 Test App")
st.write("If you can see this, the app is working correctly!")

# Test basic functionality
if st.button("Test Button"):
    st.success("✅ Button works! App is functioning properly.")

# Test sidebar
with st.sidebar:
    st.header("Test Sidebar")
    test_input = st.text_input("Test Input", "Hello World")
    st.write(f"You entered: {test_input}")

# Test columns
col1, col2 = st.columns(2)
with col1:
    st.metric("Test Metric 1", "100", "10")
with col2:
    st.metric("Test Metric 2", "200", "-5")

st.info("🎉 All tests passed! Your Streamlit environment is working correctly.")
