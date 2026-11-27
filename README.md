# ACTIVIDAD5-POO
# Actividad 5 - Interfaz Gráfica de Usuario (GUI)

## Información General
- **Universidad:** Universidad Nacional de Colombia
- **Materia:** Programación Orientada a Objetos (POO)
- **Nombre de la actividad:** Actividad 5 - Interfaz Gráfica de Usuario (GUI) en Python
- **Estudiante:** Laura Jiménez Úsuga
- **Docente:** Walter Hugo Arboleda Mazo

## Descripción del Proyecto
Este repositorio contiene la solución a los dos ejercicios de Programación Orientada a Objetos (POO) del Capítulo 8 del texto guía *"Ejercicios de Programación Orientada a Objetos con Java y UML"* (Leonardo Bermón Angarita), desarrollados en **Python** utilizando la librería gráfica `tkinter`:

1. **Ejercicio 8.4 - Cuadros de Diálogo (Página 517):** Sistema de cálculo de nómina empresarial (`nomina.py`) implementado mediante las enumeraciones `TipoCargo` y `TipoGenero`, las clases de dominio `Empleado` y `ListaEmpleados`, y las ventanas gráficas `VentanaPrincipal`, `VentanaAgregarEmpleado` y `VentanaNomina`. Permite registrar empleados validando campos mediante cuadros de diálogo (`messagebox`), visualizar los sueldos individuales y el total mensual en una tabla (`Treeview`), y exportar la información en un archivo de texto plano (`Nómina.txt`) seleccionando la carpeta destino (`filedialog`).
2. **Ejercicio 8.5 - Gestión de Contenidos (Página 546):** Sistema de gestión de ingreso y salida de huéspedes de un hotel de 10 habitaciones (`hotel.py`) implementado mediante las clases `Huesped`, `Habitacion` y `Hotel`, junto con las ventanas `VentanaPrincipal`, `VentanaHabitaciones`, `VentanaIngreso` y `VentanaSalida`. Utiliza administradores de geometría (`pack` y `grid`) para visualizar la disponibilidad y tarifas de las habitaciones ($120.000/día del 1 al 5 y $160.000/día del 6 al 10), validar fechas de ingreso/salida y calcular el total a pagar por estadía.

## Estructura del Repositorio
```text
├── nomina.py     # Ejercicio 8.4: Cuadros de Diálogo (Sistema de Nómina)
├── hotel.py      # Ejercicio 8.5: Gestión de Contenidos (Sistema de Hotel)
└── README.md     # Documentación del proyecto
