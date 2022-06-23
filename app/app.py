import streamlit as st
import pandas as pd 
from funcionesDB import *
import streamlit.components.v1 as stc
from datetime import datetime

# Data Viz Pkgs
import plotly.express as px 





def main():

	HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """
	stc.html(HTML_BANNER)



	choice = st.sidebar.selectbox("Menu",["Crear","Leer","Modificar","Borrar","Acerca de"])
	
	create_table()		# funcionesDB

	if choice == "Crear":
		st.subheader("Add Item")
		col1,col2 = st.beta_columns(2)
		
		with col1:
			task = st.text_area("Task To Do")

		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Added ::{} ::To Task".format(task))


	if choice == "Leer":
		# st.subheader("View Items")
		with st.beta_expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		with st.beta_expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='index',values='Status')
			st.plotly_chart(p1,use_container_width=True)


	if choice == "Modificar":
		st.subheader("Edit Items")

		with st.beta_expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.beta_columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				#HAY QUE BUSCAR EL INDICEEEEEEEEEEEEEEEEEEEEEEEEEEE ************************
				new_task_status = st.selectbox("Status",["ToDo","Doing","Done"],1)
				new_task_due_date = st.date_input("Fecha",datetime.strptime(task_due_date, '%Y-%m-%d'))

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated ::{} ::To {}".format(task,new_task))

			with st.beta_expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)		# Para verlo como una lista sin formato
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)


	if choice == "Borrar":
		st.subheader("Delete")
		with st.beta_expander("View Data"):
			result = view_all_data()
			# st.write(result)		# Para verlo como una lista sin formato
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)

		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.beta_expander("Updated Data"):
			result = view_all_data()
			# st.write(result)			# Para verlo como una lista sin formato
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

	if choice == "Acerca de":
		st.subheader("About ToDo List App")
		st.info("Built with Streamlit")
		st.info("Jesus Saves @JCharisTech")
		st.text("Jesse E.Agbe(JCharis)")


if __name__ == '__main__':
	main()

