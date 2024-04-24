import flet as ft
from decimal import Decimal, getcontext
import math

def main(page: ft.Page):
    page.title = "Mislang's Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    text_result_box: list[str] = []
    result: ft.TextField = ft.TextField(value="0", text_size="20", show_cursor=True, text_align="end", width="440")
    controls: set[str] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "/", "*", ".", "^", "%", "(", ")", "!")

    def update_text_result_box(data: str) -> None:
        nonlocal text_result_box

        if data == "ln":
            data = "math.log"

        elif data == "log":
            data = "math.log10"

        elif data == "÷":
            data = "/"

        elif data == "×":
            data = "*"

        elif data == "√":
            data = "math.sqrt"

        elif data == "−":
            data = "-"

        elif data == "!":
            data = "math.factorial"

        text_result_box.append(data)
        result.value = ''.join(text_result_box)
        page.update()


    def on_keyboard(event: ft.KeyboardEvent) -> None:
        nonlocal text_result_box

        if event.ctrl and event.key == "Backspace":
            text_result_box = []
            result.value = "0"
            page.update()
        
        elif event.key == "Backspace":
            if text_result_box:
                text_result_box.pop()
                if text_result_box:
                    result.value = ''.join(text_result_box)
                else:
                    result.value = "0"
                page.update()
            else:
                result.value = "0"
                page.update()

        elif event.shift and event.key == "1":
            update_text_result_box(data="!")

        elif event.shift and event.key == "=":
            update_text_result_box(data="+")

        elif event.shift and event.key == "8":
            update_text_result_box(data="*")

        elif event.key == "-":
            update_text_result_box(data="-")

        elif event.key == "/":
            update_text_result_box(data="/")
            
        elif event.shift and event.key == "5":
            update_text_result_box(data="%")

        elif event.shift and event.key == "6":
            update_text_result_box(data="**")

        elif event.shift and event.key == "9":
            update_text_result_box(data="(")

        elif event.shift and event.key == "0":
            update_text_result_box(data=")")

        elif event.key == "Enter":
            if text_result_box:
                result.value = eval(''.join(text_result_box)) # TODO: Implement a solver function for text_result_box
            else:
                result.value = "0"
            text_result_box = []
            page.update()

        elif event.key in controls:
            update_text_result_box(event.key)

        print(text_result_box)

    
    def button_clicked(event) -> None:
        nonlocal text_result_box
        
        data: str = event.control.data
        if data == "CE":
            text_result_box = []
            result.value = "0"
            page.update()

        elif data == "=":
            if text_result_box:
                result.value = eval(''.join(text_result_box)) # TODO: Implement a solver function for text_result_box
            else:
                result.value = "0"
            text_result_box = []
            
            page.update()

        else:
            update_text_result_box(data)

        print(text_result_box)
    
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Container(
            alignment=ft.alignment.center,
            width=500,
            bgcolor=ft.colors.BLACK12,
            border_radius=ft.border_radius.all(20),
            padding=30,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment="end"),
                    
                    ft.Row(controls=[
                                    ft.ElevatedButton(text="x!", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="!"),
                                    ft.ElevatedButton(text="(", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="("),
                                    ft.ElevatedButton(text=")", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data=")"),
                                    ft.ElevatedButton(text="%", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="%"),
                                    ft.ElevatedButton(text="CE", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="CE")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="ln", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="ln"),
                                    ft.ElevatedButton(text="7", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="7"),
                                    ft.ElevatedButton(text="8", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="8"),
                                    ft.ElevatedButton(text="9", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="9"),
                                    ft.ElevatedButton(text="÷", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="÷")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="log", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="log"),
                                    ft.ElevatedButton(text="4", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="4"),
                                    ft.ElevatedButton(text="5", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="5"),
                                    ft.ElevatedButton(text="6", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="6"),
                                    ft.ElevatedButton(text="×", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="×")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="√", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="√"),
                                    ft.ElevatedButton(text="1", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="1"),
                                    ft.ElevatedButton(text="2", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="2"),
                                    ft.ElevatedButton(text="3", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="3"),
                                    ft.ElevatedButton(text="−", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="−")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="x^y", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="^"),
                                    ft.ElevatedButton(text="0", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="0"),
                                    ft.ElevatedButton(text=".", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="."),
                                    ft.ElevatedButton(text="=", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="="),
                                    ft.ElevatedButton(text="+", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="+")
                                    ], alignment="center"),
                ]
            )
        )
    )


ft.app(main)
