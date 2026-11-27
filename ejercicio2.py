from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog


class Huesped:
    def __init__(
        self,
        nombres: str,
        apellidos: str,
        documento_identidad: int,
        fecha_ingreso: datetime,
    ):
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__documento_identidad = documento_identidad
        self.__fecha_ingreso = fecha_ingreso
        self.__fecha_salida: datetime | None = None

    def get_fecha_ingreso(self) -> datetime:
        return self.__fecha_ingreso

    def get_fecha_salida(self) -> datetime | None:
        return self.__fecha_salida

    def set_fecha_salida(self, fecha_salida: datetime):
        self.__fecha_salida = fecha_salida

    def obtener_dias_alojamiento(self) -> int:
        if self.__fecha_salida is None:
            return 0
        diferencia = self.__fecha_salida - self.__fecha_ingreso
        return diferencia.days


class Habitacion:
    def __init__(self, numero_habitacion: int, disponible: bool, precio_dia: float):
        self.__numero_habitacion = numero_habitacion
        self.__disponible = disponible
        self.__precio_dia = precio_dia
        self.__huesped: Huesped | None = None

    def get_numero_habitacion(self) -> int:
        return self.__numero_habitacion

    def get_disponible(self) -> bool:
        return self.__disponible

    def set_disponible(self, disponible: bool):
        self.__disponible = disponible

    def get_precio_dia(self) -> float:
        return self.__precio_dia

    def get_huesped(self) -> Huesped | None:
        return self.__huesped

    def set_huesped(self, huesped: Huesped | None):
        self.__huesped = huesped


class Hotel:
    def __init__(self):
        self.lista_habitaciones: list[Habitacion] = []
        for i in range(1, 11):
            precio = 120000.0 if i <= 5 else 160000.0
            self.lista_habitaciones.append(Habitacion(i, True, precio))

    def buscar_fecha_ingreso_habitacion(self, numero: int) -> str:
        for hab in self.lista_habitaciones:
            if hab.get_numero_habitacion() == numero and hab.get_huesped() is not None:
                return hab.get_huesped().get_fecha_ingreso().strftime("%Y/%m/%d")
        return ""

    def buscar_habitacion_ocupada(self, numero: int) -> bool:
        for hab in self.lista_habitaciones:
            if hab.get_numero_habitacion() == numero and not hab.get_disponible():
                return True
        return False


class VentanaHabitaciones(tk.Toplevel):
    def __init__(self, master, hotel: Hotel):
        super().__init__(master)
        self.hotel = hotel
        self.title("Habitaciones")
        self.resizable(False, False)
        self.inicio()
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self):
        panel_habitaciones = tk.Frame(self, padx=15, pady=15)
        panel_habitaciones.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for idx, hab in enumerate(self.hotel.lista_habitaciones):
            fila = idx // 5
            columna = idx % 5
            estado = "Disponible" if hab.get_disponible() else "No disponible"
            color_fondo = "#dcfce7" if hab.get_disponible() else "#fee2e2"

            tarjeta = tk.Label(
                panel_habitaciones,
                text=f"Habitación {hab.get_numero_habitacion()}\n${hab.get_precio_dia():,.0f}/día\n{estado}",
                bg=color_fondo,
                relief=tk.GROOVE,
                borderwidth=2,
                width=16,
                height=4,
                font=("Arial", 9),
            )
            tarjeta.grid(row=fila, column=columna, padx=6, pady=6)

        panel_inferior = tk.Frame(self, pady=10)
        panel_inferior.pack(side=tk.BOTTOM, fill=tk.X)

        contenedor_controles = tk.Frame(panel_inferior)
        contenedor_controles.pack()

        tk.Label(contenedor_controles, text="Habitación a reservar:").pack(
            side=tk.LEFT, padx=5
        )
        self.spin_habitacion = tk.Spinbox(contenedor_controles, from_=1, to=10, width=5)
        self.spin_habitacion.pack(side=tk.LEFT, padx=5)

        tk.Button(
            contenedor_controles, text="Aceptar", command=self.seleccionar_habitacion
        ).pack(side=tk.LEFT, padx=5)

    def seleccionar_habitacion(self):
        try:
            num = int(self.spin_habitacion.get())
            if not (1 <= num <= 10):
                raise ValueError
            if not self.hotel.buscar_habitacion_ocupada(num):
                self.destroy()
                VentanaIngreso(self.master, self.hotel, num)
            else:
                messagebox.showerror(
                    "Mensaje", "La habitación está ocupada", parent=self
                )
        except ValueError:
            messagebox.showerror(
                "Error", "Número de habitación inválido (1-10)", parent=self
            )


class VentanaIngreso(tk.Toplevel):
    def __init__(self, master, hotel: Hotel, numero_habitacion: int):
        super().__init__(master)
        self.hotel = hotel
        self.numero_habitacion = numero_habitacion
        self.title("Ingreso")
        self.resizable(False, False)
        self.inicio()
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self):
        panel = tk.Frame(self, padx=15, pady=15)
        panel.pack()

        tk.Label(
            panel,
            text=f"Habitación: {self.numero_habitacion}",
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        tk.Label(panel, text="Fecha (aaaa-mm-dd):").grid(
            row=1, column=0, sticky="w", pady=4, padx=(0, 8)
        )
        self.campo_fecha_ingreso = tk.Entry(panel, width=18)
        self.campo_fecha_ingreso.grid(row=1, column=1, pady=4)

        tk.Label(panel, text="Huésped", font=("Arial", 9, "bold")).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(8, 4)
        )

        tk.Label(panel, text="Nombre:").grid(row=3, column=0, sticky="w", pady=4)
        self.campo_nombre = tk.Entry(panel, width=18)
        self.campo_nombre.grid(row=3, column=1, pady=4)

        tk.Label(panel, text="Apellidos:").grid(row=4, column=0, sticky="w", pady=4)
        self.campo_apellidos = tk.Entry(panel, width=18)
        self.campo_apellidos.grid(row=4, column=1, pady=4)

        tk.Label(panel, text="Doc. Identidad:").grid(
            row=5, column=0, sticky="w", pady=4
        )
        self.campo_documento = tk.Entry(panel, width=18)
        self.campo_documento.grid(row=5, column=1, pady=4)

        tk.Button(panel, text="Aceptar", width=10, command=self.registrar_ingreso).grid(
            row=6, column=0, pady=(12, 0), padx=4
        )
        tk.Button(panel, text="Cancelar", width=10, command=self.destroy).grid(
            row=6, column=1, pady=(12, 0), padx=4
        )

    def registrar_ingreso(self):
        fecha_str = self.campo_fecha_ingreso.get().strip()
        nombre = self.campo_nombre.get().strip()
        apellidos = self.campo_apellidos.get().strip()
        doc_str = self.campo_documento.get().strip()

        if not fecha_str or not nombre or not apellidos or not doc_str:
            messagebox.showerror(
                "Error", "Todos los campos son obligatorios", parent=self
            )
            return

        try:
            fecha_ingreso = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error",
                "La fecha no está en el formato solicitado (aaaa-mm-dd)",
                parent=self,
            )
            return

        try:
            documento = int(doc_str)
        except ValueError:
            messagebox.showerror(
                "Error", "El documento de identidad debe ser numérico", parent=self
            )
            return

        huesped = Huesped(nombre, apellidos, documento, fecha_ingreso)
        habitacion = self.hotel.lista_habitaciones[self.numero_habitacion - 1]
        habitacion.set_huesped(huesped)
        habitacion.set_disponible(False)

        messagebox.showinfo(
            "Mensaje", "El huésped ha sido registrado", parent=self
        )
        self.destroy()


class VentanaSalida(tk.Toplevel):
    def __init__(self, master, hotel: Hotel, numero_habitacion: int):
        super().__init__(master)
        self.hotel = hotel
        self.numero_habitacion = numero_habitacion
        self.habitacion_ocupada = self.hotel.lista_habitaciones[numero_habitacion - 1]
        self.title("Salida huéspedes")
        self.resizable(False, False)
        self.inicio()
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self):
        panel = tk.Frame(self, padx=20, pady=15)
        panel.pack()

        tk.Label(
            panel,
            text=f"Habitación: {self.numero_habitacion}",
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=4)

        fecha_ing = self.hotel.buscar_fecha_ingreso_habitacion(self.numero_habitacion)
        tk.Label(panel, text=f"Fecha de ingreso: {fecha_ing}").grid(
            row=1, column=0, sticky="w", pady=4
        )

        tk.Label(panel, text="Fecha de salida (aaaa-mm-dd):").grid(
            row=2, column=0, sticky="w", pady=(8, 2)
        )
        self.campo_fecha_salida = tk.Entry(panel, width=22)
        self.campo_fecha_salida.grid(row=3, column=0, sticky="ew", pady=4)

        tk.Button(panel, text="Calcular", command=self.calcular_pago).grid(
            row=4, column=0, sticky="ew", pady=6
        )

        self.lbl_dias = tk.Label(panel, text="Cantidad de días: ")
        self.lbl_dias.grid(row=5, column=0, sticky="w", pady=4)

        self.lbl_total = tk.Label(panel, text="Total: $", font=("Arial", 9, "bold"))
        self.lbl_total.grid(row=6, column=0, sticky="w", pady=4)

        self.btn_registrar_salida = tk.Button(
            panel,
            text="Registrar salida",
            state=tk.DISABLED,
            command=self.registrar_salida,
        )
        self.btn_registrar_salida.grid(row=7, column=0, sticky="ew", pady=(10, 0))

    def calcular_pago(self):
        fecha_s_str = self.campo_fecha_salida.get().strip()
        try:
            fecha_salida = datetime.strptime(fecha_s_str, "%Y-%m-%d")
            huesped = self.habitacion_ocupada.get_huesped()
            fecha_ingreso = huesped.get_fecha_ingreso()

            if fecha_ingreso < fecha_salida:
                huesped.set_fecha_salida(fecha_salida)
                dias = huesped.obtener_dias_alojamiento()
                total = dias * self.habitacion_ocupada.get_precio_dia()

                self.lbl_dias.config(text=f"Cantidad de días: {dias}")
                self.lbl_total.config(text=f"Total: ${total:,.0f}")
                self.btn_registrar_salida.config(state=tk.NORMAL)
            else:
                messagebox.showerror(
                    "Mensaje",
                    "La fecha de salida es menor o igual que la de ingreso",
                    parent=self,
                )
        except ValueError:
            messagebox.showerror(
                "Mensaje",
                "La fecha no está en el formato solicitado (aaaa-mm-dd)",
                parent=self,
            )

    def registrar_salida(self):
        self.habitacion_ocupada.set_huesped(None)
        self.habitacion_ocupada.set_disponible(True)
        messagebox.showinfo(
            "Mensaje", "Se ha registrado la salida del huésped", parent=self
        )
        self.destroy()


class VentanaPrincipal(tk.Tk):
    def __init__(self, hotel: Hotel):
        super().__init__()
        self.hotel = hotel
        self.title("Hotel")
        self.geometry("280x350")
        self.resizable(False, False)
        self.centrar_ventana(280, 350)
        self.inicio()

    def centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self):
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(
            label="Consultar habitaciones", command=self.consultar_habitaciones
        )
        menu_opciones.add_command(
            label="Salida de huéspedes", command=self.salida_huespedes
        )
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def consultar_habitaciones(self):
        VentanaHabitaciones(self, self.hotel)

    def salida_huespedes(self):
        entrada = simpledialog.askstring(
            "Salida de huéspedes", "Ingrese número de habitación:", parent=self
        )
        if entrada is None:
            return
        try:
            numero = int(entrada)
            if not (1 <= numero <= 10):
                messagebox.showinfo(
                    "Mensaje",
                    "El número de habitación debe estar entre 1 y 10",
                    parent=self,
                )
            elif self.hotel.buscar_habitacion_ocupada(numero):
                VentanaSalida(self, self.hotel, numero)
            else:
                messagebox.showinfo(
                    "Mensaje",
                    "La habitación ingresada no ha sido ocupada",
                    parent=self,
                )
        except ValueError:
            messagebox.showerror(
                "Error", "Campo nulo o error en formato de número", parent=self
            )


if __name__ == "__main__":
    mi_hotel = Hotel()
    app = VentanaPrincipal(mi_hotel)
    app.mainloop()
