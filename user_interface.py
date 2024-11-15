import streamlit as st
import pandas as pd
import tool_box as tb
import GS_Coding_Exercise as gs

# Initialize session state variables if they are not already set
if 'input_data' not in st.session_state:
    st.session_state.input_data = tb.reset()  # Reset input data to original state
    st.session_state.edited_data = st.session_state.input_data.copy()  # Create a copy of input data for edits
    st.session_state.horizontal = True  # Set default orientation for radio button display

# Set page layout and create sidebar navigation tabs
st.set_page_config(layout="wide")
tab = st.sidebar.radio("Select", ["Add/Remove Client", "Aggregated data"])

# First Tab: Add/Remove Client
if tab == "Add/Remove Client":
    # Divide the page into two columns for input and data display
    ColA, ColB = st.columns(2)

    # Left Column for form input
    with ColA:
        with st.form(key='form_1'):
            st.title("Add/Remove Client")
            
            # Radio button to select action: Add or Remove
            add_remove = st.radio(
                "Action",
                ["Add", "Remove"],
                horizontal=st.session_state.horizontal,
            )

            # Input fields for client data
            country = st.text_input("Country ")
            client_names = st.text_input("client_names")
            product_type = st.selectbox("product_type", ['Stocks', 'Bonds', 'FX', 'Credit'])
            notional_traded = st.number_input("notional_traded (in thousand USD)", 100, 10**6, step=500, value=1000)

            # Load, Save, Reset, and Clear all buttons with container width set to True
            submit_button_Load = st.form_submit_button(label='Load', use_container_width=True)
            ColS, ColR = st.columns(2)
            with ColS:
                submit_button_save = st.form_submit_button(label='Save', use_container_width=True, help="Saves current dataframe to input worksheet in Excel")
            with ColR:
                submit_button_reset = st.form_submit_button(label='Reset', use_container_width=True, help="Resets dataframe to original table from input worksheet in Excel")

            # Clear all button to remove all entries in DataFrame
            submit_button_clear = st.form_submit_button(label='Clear all', use_container_width=True, help="Clears current dataframe")

    # Right Column to display and manage client data
    with ColB:
        st.title('Client data')
        placeholder = st.empty()  # Placeholder to dynamically update DataFrame display
        placeholder.dataframe(st.session_state.edited_data)  # Show current DataFrame in Streamlit

        if submit_button_Load:
            # If "Add" is selected, add new client row to the data
            if add_remove == "Add":
                st.session_state.edited_data = tb.add_row(st.session_state.edited_data, country, client_names, product_type, notional_traded)
                placeholder.dataframe(st.session_state.edited_data)
            else:
                # If "Remove" is selected, attempt to delete the specified client
                try:
                    client, st.session_state.edited_data = tb.delete_row(st.session_state.edited_data, country, client_names, product_type, notional_traded)

                    # If no matching client found, raise an error
                    if client.empty: 
                        raise ValueError("No matching client found.")

                    # Display the updated DataFrame after row deletion
                    placeholder.dataframe(st.session_state.edited_data)

                except ValueError as e:
                    # Show an error message if no matching client was found
                    error_message = 'Client details did not match the data present, please check the information and load again.'
                    placeholder.dataframe(st.session_state.edited_data)
                    st.markdown(f"<span style='color:red; font-weight:bold'>{error_message}</span>", unsafe_allow_html=True)

        # Reset DataFrame to original input data
        if submit_button_reset:
            st.session_state.input_data = tb.reset()
            st.session_state.edited_data = st.session_state.input_data.copy()
            placeholder.dataframe(st.session_state.edited_data)

        # Save the edited DataFrame to the 'input' worksheet in Excel
        if submit_button_save:
            security_message = 'This action will overide the existing original data, if you confirm, the data shown above will become the original data! Do You Confirm? '
            st.markdown(f"<span style='color:red; font-weight:bold'>{security_message} </span> ", unsafe_allow_html=True)
            ColYes, ColNo = st.columns(2)
            with ColYes:
                confirm_btn = st.button("Confirm", use_container_width=True)
            with ColNo:
                cancel_btn = st.button("Cancel", use_container_width=True)

            if confirm_btn: tb.save_data(st.session_state.edited_data, 'input')
            
            if cancel_btn: placeholder.dataframe(st.session_state.edited_data)

        # Clear all rows from the DataFrame
        if submit_button_clear:
            st.session_state.edited_data = tb.clear_all() 
            placeholder.dataframe(st.session_state.edited_data)

# Second Tab: Aggregated Data
elif tab == "Aggregated data":
    # Divide the page into two columns for data display and graph options
    ColA, ColB = st.columns([1, 1.3])

    # Left Column for selecting and displaying aggregated data
    with ColA:
        st.title('Aggregated data')

        # Radio button to select data source (original data or edited data)
        original_edited = st.radio(
            "Data source",
            ["On original data", "On edited data"],
            horizontal=st.session_state.horizontal,
            key="1"
        )

        # Display the selected data and aggregated data
        ColC, ColD = st.columns([2, 1])
        
        with ColC:
            placeholder = st.empty()
            # Aggregate data based on the selected data source
            if original_edited == "On original data":
                data = tb.data
                agg_data = gs.aggregate_data(data)
            else:
                data = st.session_state.edited_data
                agg_data = gs.aggregate_data(st.session_state.edited_data)

            # Display the aggregated data
            placeholder.dataframe(agg_data)
            st.button("Save output",help="Saves aggregated data to output worksheet in excel", use_container_width=True)
        # Radio button to select the graph type (by country, by client, or both)
        with ColD:
            graph_by = st.radio("Graph settings", ["Graph by country", "Graph by Client", "Graph both"], key="2")

    # Right Column to display graphs based on the selected grouping
    with ColB:
        st.title('Graphs')

        # Display graph by country
        if graph_by == "Graph by country":
            grouped_data = tb.plot_histogram(data, 'country')
            st.write("Total notional traded by Country")
            st.bar_chart(data=grouped_data.set_index('country'))

        # Display graph by client names
        elif graph_by == "Graph by Client":
            grouped_data = tb.plot_histogram(data, 'client_names')
            st.write("Total notional traded by Client")
            st.bar_chart(data=grouped_data.set_index('client_names'))

        # Display both graphs (country and client)
        else:       
            grouped_data = tb.plot_histogram(data, 'country')
            st.write("Total notional traded by Country")
            st.bar_chart(data=grouped_data.set_index('country'))

            grouped_data = tb.plot_histogram(data, 'client_names')
            st.write("Total notional traded by Client")
            st.bar_chart(data=grouped_data.set_index('client_names'))
