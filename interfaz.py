import flet as ft
import requests


def main(page: ft.Page):
    page.title = "Sistema de Métodos Numéricos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE

    # ---------------- CONFIGURACIÓN DE RED ----------------
    ip_input = ft.TextField(
        label="IP del Backend",
        value="127.0.0.1:8000",
        width=300
    )

    # ---------------- BISECCIÓN ----------------
    a_in = ft.TextField(label="Valor a", value="1", width=140)
    b_in = ft.TextField(label="Valor b", value="2", width=140)
    res_bis = ft.Column()

    def calc_biseccion(e):
        res_bis.controls.clear()
        url = f"http://{ip_input.value.replace('http://', '')}/biseccion"

        try:
            payload = {
                "a": float(a_in.value),
                "b": float(b_in.value),
                "tol": 0.000001
            }

            r = requests.post(url, json=payload, timeout=5)
            r.raise_for_status()
            data = r.json()

            if "error" in data:
                res_bis.controls.append(
                    ft.Text(data["error"], color=ft.Colors.RED)
                )
            else:
                raiz = data["resultado_final"]["raiz"]

                res_bis.controls.append(
                    ft.Text(
                        f"Raíz: {raiz}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN
                    )
                )

                filas = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(i["iteracion"]))),
                            ft.DataCell(ft.Text(str(i["c"]))),
                            ft.DataCell(ft.Text(str(i["error"])))
                        ]
                    )
                    for i in data["iteraciones"][:5]
                ]

                res_bis.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("i")),
                            ft.DataColumn(ft.Text("c")),
                            ft.DataColumn(ft.Text("Error"))
                        ],
                        rows=filas
                    )
                )

        except Exception as ex:
            res_bis.controls.append(
                ft.Text(f"Error: {ex}", color=ft.Colors.RED)
            )

        page.update()

    # ---------------- SECANTE ----------------
    x0_in = ft.TextField(label="x0", value="0", width=140)
    x1_in = ft.TextField(label="x1", value="1", width=140)
    res_sec = ft.Column()

    def calc_secante(e):
        res_sec.controls.clear()
        url = f"http://{ip_input.value.replace('http://', '')}/secante"

        try:
            payload = {
                "x0": float(x0_in.value),
                "x1": float(x1_in.value),
                "tolerancia": 0.000001,
                "max_iter": 100
            }

            r = requests.post(url, json=payload, timeout=5)
            r.raise_for_status()
            data = r.json()

            if "error" in data:
                res_sec.controls.append(
                    ft.Text(data["error"], color=ft.Colors.RED)
                )
            else:
                raiz = data["resultado_final"]["raiz"]

                res_sec.controls.append(
                    ft.Text(
                        f"Raíz: {raiz}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    )
                )

                filas = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(i["iteracion"]))),
                            ft.DataCell(ft.Text(str(i["x2"]))),
                            ft.DataCell(ft.Text(str(i["error"])))
                        ]
                    )
                    for i in data["iteraciones"][:5]
                ]

                res_sec.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("i")),
                            ft.DataColumn(ft.Text("x2")),
                            ft.DataColumn(ft.Text("Error"))
                        ],
                        rows=filas
                    )
                )

        except Exception as ex:
            res_sec.controls.append(
                ft.Text(f"Error: {ex}", color=ft.Colors.RED)
            )

        page.update()

    # ---------------- VISTAS ----------------
    view_bis = ft.Column(
        controls=[
            ft.Text("Función: 4x² - 5x", italic=True),
            ft.Row([a_in, b_in]),
            ft.Button(
                "Calcular Bisección",
                on_click=calc_biseccion
            ),
            res_bis
        ],
        visible=True,
        scroll=ft.ScrollMode.ALWAYS
    )

    view_sec = ft.Column(
        controls=[
            ft.Text("Función: e⁻ˣ - x", italic=True),
            ft.Row([x0_in, x1_in]),
            ft.Button(
                "Calcular Secante",
                on_click=calc_secante
            ),
            res_sec
        ],
        visible=False,
        scroll=ft.ScrollMode.ALWAYS
    )

    # ---------------- CAMBIO DE VISTA ----------------
    def show_view(index):
        view_bis.visible = index == 0
        view_sec.visible = index == 1
        page.update()

    # ---------------- BOTONES DE NAVEGACIÓN ----------------
    tab_buttons = ft.Row(
        controls=[
            ft.Button(
                "Bisección",
                on_click=lambda e: show_view(0)
            ),
            ft.Button(
                "Secante",
                on_click=lambda e: show_view(1)
            ),
        ]
    )

    # ---------------- UI FINAL ----------------
    page.add(
        ft.Text(
            "Configuración de Conexión",
            weight=ft.FontWeight.BOLD
        ),
        ip_input,
        ft.Divider(),
        tab_buttons,
        view_bis,
        view_sec
    )


if __name__ == "__main__":
    ft.run(main)
