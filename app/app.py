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
    <h1 style="color:white;text-align:center;">Administracion de datos</h1>
    <p style="color:white;text-align:center;">Version demo</p>
    </div>
    """
	stc.html(HTML_BANNER)

	ListaEstado = ["ToDo","Doing","Done"]
	ListaColumnas = ["Task","Status","Date"]
	Eleccion = st.sidebar.selectbox("Menu",["Crear","Leer","Modificar","Borrar","Acerca de"])
	
	create_table()		# funcionesDB

	if Eleccion == "Crear":
		st.subheader("Add Item")
		col1,col2 = st.beta_columns(2)
		
		with col1:
			TareaNombre = st.text_area("Task To Do")

		with col2:
			
			TareaEstado = st.selectbox("Status",ListaEstado)
			TareaFecha = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(TareaNombre, TareaEstado, TareaFecha)
			st.success("Added ::{} ::To Task".format(task))


	if Eleccion == "Leer":
		# st.subheader("View Items")
		with st.beta_expander("View All"):
			TodasLasTareas = view_all_data()
			# st.write(result)
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

		with st.beta_expander("Task Status"):
			DataframeTareas = MiDataframe['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			DataframeTareas = DataframeTareas.reset_index()
			st.dataframe(DataframeTareas)

			GraficoTorta = px.pie(DataframeTareas, names='index', values='Status')
			st.plotly_chart(GraficoTorta, use_container_width=True)


	if Eleccion == "Modificar":
		st.subheader("Edit Items")

		with st.beta_expander("Current Data"):
			TodasLasTareas = view_all_data()
			# st.write(result)
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

		ListaUnicaDeNombres = [i[0] for i in view_all_task_names()]
		TareaSeleccionada = st.selectbox("Task", ListaUnicaDeNombres)
		TareaObtenida = get_task(TareaSeleccionada)
		# st.write(task_result)

		if TareaObtenida:
			TareaNombre = TareaObtenida[0][0]
			TareaEstado = TareaObtenida[0][1]
			TareaFecha = TareaObtenida[0][2]

			col1,col2 = st.beta_columns(2)
			
			with col1:
				NuevaTareaNombre = st.text_area("Task To Do",task)

			with col2:
				NuevaTareaEstado = st.selectbox("Status",ListaEstado,ListaEstado.index(TareaEstado))
				NuevaTareaFecha = st.date_input("Fecha",datetime.strptime(TareaFecha, '%Y-%m-%d'))

			if st.button("Update Task"):
				edit_task_data(NuevaTareaNombre,NuevaTareaEstado,NuevaTareaFecha,TareaNombre,TareaEstado,TareaFecha)
				st.success("Updated ::{} ::To {}".format(TareaNombre,NuevaTareaNombre))

			with st.beta_expander("View Updated Data"):
				TodasLasTareas = view_all_data()
				# st.write(result)		# Para verlo como una lista sin formato
				MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
				st.dataframe(MiDataframe)


	if Eleccion == "Borrar":
		st.subheader("Delete")
		with st.beta_expander("View Data"):
			TodasLasTareas = view_all_data()
			# st.write(result)		# Para verlo como una lista sin formato
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

		ListaUnicaDeNombres = [i[0] for i in view_all_task_names()]
		NombreEliminar =  st.selectbox("Select Task", ListaUnicaDeNombres)

		if st.button("Delete"):
			delete_data(NombreEliminar)
			st.warning("Deleted: '{}'".format(NombreEliminar))

		with st.beta_expander("Updated Data"):
			TodasLasTareas = view_all_data()
			# st.write(result)			# Para verlo como una lista sin formato
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

	if Eleccion == "Acerca de":
		st.subheader("Acerca de : App con Streamlit")
		st.info("Hecho con Streamlit")
		st.info("Gabriel Quinteros")
		st.text("guru_vb@hotmail.com")


if __name__ == '__main__':
	main()

