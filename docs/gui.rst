GUI, Docker y EC2
=================

La interfaz gráfica **no se publica en PyPI**. El paquete no importa
Streamlit ni Tkinter. ``streamlit_app.py`` solo consume
:class:`~bohr_h_andresdperezc.BohrAtom`.

Streamlit (local)
-----------------

::

   python -m pip install -e ".[gui]"
   streamlit run streamlit_app.py

Abra http://localhost:8501. Controles:

- :math:`Z` de 1 a 10
- :math:`n` de 1 a 8
- transiciones :math:`n_i \to n_f` (emisión o absorción)
- gráficos de niveles y órbitas

Docker y EC2
------------

La imagen (cuando esté en Docker Hub, usuario ``andresperez3``) expone
el mismo Streamlit en el puerto **8501**. Cualquier sistema operativo
abre el navegador; no hace falta Tkinter.

Construir y publicar (lo hace el autor del paquete)::

   docker build -t andresperez3/bohr-h-andresdperezc:0.1.0 .
   docker push andresperez3/bohr-h-andresdperezc:0.1.0

Usar en cualquier PC::

   docker run --rm -p 8501:8501 andresperez3/bohr-h-andresdperezc:0.1.0

Luego http://localhost:8501.

En una instancia EC2: el contenedor debe escuchar en ``0.0.0.0:8501`` y
el Security Group abre TCP 8501 a internet, **sin contraseña** (decisión
del proyecto). No conviene dejarla encendida 24/7 si no se está
mostrando.

El ``Dockerfile`` está en la raíz del repositorio. Streamlit escucha
en ``0.0.0.0:8501`` (imprescindible para Docker y EC2).
