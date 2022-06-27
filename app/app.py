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

	ListaEstado = ["Hacer","Haciendo","Hecha"]
	ListaColumnas = ["Nombre","Estado","Fecha"]
	Eleccion = st.sidebar.selectbox("Menu",["Crear","Leer","Modificar","Eliminar","Acerca de"])
	
	create_table()		# funcionesDB

	if Eleccion == "Crear":
		st.subheader("Crear Item")
		col1,col2 = st.beta_columns(2)
		
		with col1:
			TareaNombre = st.text_area("Tarea para hacer")

		with col2:
			
			TareaEstado = st.selectbox("Estado",ListaEstado)
			TareaFecha = st.date_input("Fecha")

		if st.button("Crear tarea"):
			add_data(TareaNombre, TareaEstado, TareaFecha)
			st.success("Creado ::{}".format(TareaNombre))


	if Eleccion == "Leer":
		# st.subheader("View Items")
		with st.beta_expander("Ver Todas"):
			TodasLasTareas = view_all_data()
			# st.write(result)
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

		with st.beta_expander("Estados de tareas"):
			DataframeTareas = MiDataframe['Estado'].value_counts().to_frame()
			# st.dataframe(task_df)
			DataframeTareas = DataframeTareas.reset_index()
			st.dataframe(DataframeTareas)

			GraficoTorta = px.pie(DataframeTareas, names='index', values='Estado')
			st.plotly_chart(GraficoTorta, use_container_width=True)


	if Eleccion == "Modificar":
		st.subheader("Editar tarea")

		with st.beta_expander("Datos actuales"):
			TodasLasTareas = view_all_data()
			# st.write(result)
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

		ListaUnicaDeNombres = [i[0] for i in view_all_task_names()]
		TareaSeleccionada = st.selectbox("Nombre", ListaUnicaDeNombres)
		TareaObtenida = get_task(TareaSeleccionada)
		# st.write(task_result)

		if TareaObtenida:
			TareaNombre = TareaObtenida[0][0]
			TareaEstado = TareaObtenida[0][1]
			TareaFecha = TareaObtenida[0][2]

			col1,col2 = st.beta_columns(2)
			
			with col1:
				NuevaTareaNombre = st.text_area("Tarea para hacer",TareaNombre)

			with col2:
				NuevaTareaEstado = st.selectbox("Estado",ListaEstado,ListaEstado.index(TareaEstado))
				NuevaTareaFecha = st.date_input("Fecha",datetime.strptime(TareaFecha, '%Y-%m-%d'))

			if st.button("Modificar tarea"):
				edit_task_data(NuevaTareaNombre,NuevaTareaEstado,NuevaTareaFecha,TareaNombre,TareaEstado,TareaFecha)
				st.success("Modificado ::{} ".format(TareaNombre))

			with st.beta_expander("Ver datos modificados"):
				TodasLasTareas = view_all_data()
				# st.write(result)		# Para verlo como una lista sin formato
				MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
				st.dataframe(MiDataframe)


	if Eleccion == "Eliminar":
		st.subheader("Eliminar tarea")
		with st.beta_expander("Datos actuales"):
			TodasLasTareas = view_all_data()
			# st.write(result)		# Para verlo como una lista sin formato
			MiDataframe = pd.DataFrame(TodasLasTareas, columns = ListaColumnas)
			st.dataframe(MiDataframe)

		ListaUnicaDeNombres = [i[0] for i in view_all_task_names()]
		NombreEliminar =  st.selectbox("Seleccione tarea", ListaUnicaDeNombres)

		if st.button("Eliminar"):
			delete_data(NombreEliminar)
			st.warning("Eliminado: '{}'".format(NombreEliminar))

		with st.beta_expander("Ver datos modificados"):
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

