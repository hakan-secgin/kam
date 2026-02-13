import flet as ft
import flet.canvas as cv
import math

def main(page: ft.Page):
    page.title = "Flet Ölçüm Uygulaması"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    # State
    points = []
    ref_pixels = 0
    ref_real_length = 0
    mode = "REF"  # REF or MEASURE
    ratio = 0  # Real / Pixels

    canvas = cv.Canvas(
        expand=True,
    )

    result_text = ft.Text("Adım 1: Referans için iki noktaya dokunun", size=18, weight=ft.FontWeight.BOLD)
    
    def calculate_dist(p1x, p1y, p2x, p2y):
        return math.sqrt((p2x - p1x)**2 + (p2y - p1y)**2)

    def draw_lines():
        canvas.shapes.clear()
        # Draw recorded points
        for p in points:
            canvas.shapes.append(cv.Circle(p.x, p.y, 5, paint=ft.Paint(color=ft.Colors.YELLOW)))
        
        # Draw line if two points exist
        if len(points) == 2:
            canvas.shapes.append(cv.Line(
                points[0].x, points[0].y, 
                points[1].x, points[1].y, 
                paint=ft.Paint(color=ft.Colors.YELLOW, stroke_width=3)
            ))
        
        canvas.update()

    def handle_tap(e: ft.TapEvent):
        nonlocal points, ref_pixels, ratio
        
        if len(points) < 2:
            # GestureDetector TapEvent coordinates are in e.local_position
            points.append(ft.Offset(e.local_position.x, e.local_position.y))
            draw_lines()
            
        if len(points) == 2:
            dist = calculate_dist(points[0].x, points[0].y, points[1].x, points[1].y)
            if mode == "REF":
                ref_pixels = dist
                show_ref_dialog()
            else:
                if ratio > 0:
                    real_dist = dist * ratio
                    result_text.value = f"Ölçülen: {real_dist:.2f} unit"
                    page.update()

    def show_ref_dialog():
        def close_dlg(e):
            nonlocal ratio, ref_real_length, mode
            try:
                ref_real_length = float(ref_input.value)
                ratio = ref_real_length / ref_pixels
                mode = "MEASURE"
                result_text.value = "Adım 2: Ölçmek istediğiniz nesneye dokunun"
                points.clear()
                draw_lines()
                page.dialog.open = False
                page.update()
            except ValueError:
                ref_input.error_text = "Geçerli bir sayı girin"
                page.update()

        ref_input = ft.TextField(label="Gerçek Uzunluk (örn: 8.56 cm)", keyboard_type=ft.KeyboardType.NUMBER)
        page.dialog = ft.AlertDialog(
            title=ft.Text("Referans Uzunluğu Girin"),
            content=ref_input,
            actions=[ft.TextButton("Tamam", on_click=close_dlg)],
        )
        page.dialog.open = True
        page.update()

    def reset_app(e):
        nonlocal points, ref_pixels, ref_real_length, ratio, mode
        points = []
        ref_pixels = 0
        ref_real_length = 0
        ratio = 0
        mode = "REF"
        result_text.value = "Adım 1: Referans için iki noktaya dokunun"
        draw_lines()
        page.update()

    # UI Components
    # Note: Camera is only supported in native builds (Android/iOS)
    # For local/web testing, we use a placeholder or black box
    try:
        camera = ft.Camera(
            id="ca1",
            expand=True,
        )
    except Exception:
        camera = ft.Container(expand=True, bgcolor=ft.Colors.BLACK, content=ft.Text("Kamera Modu (Yalnızca Mobil)", color=ft.Colors.WHITE))

    controls_box = ft.Container(
        content=ft.Column([
            result_text,
            ft.Row([
                ft.Button("Sıfırla", icon=ft.Icons.REFRESH, on_click=reset_app),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border_radius=ft.BorderRadius.only(top_left=20, top_right=20)
    )

    page.add(
        ft.GestureDetector(
            content=ft.Stack([
                camera,
                canvas,
            ], expand=True),
            on_tap_down=handle_tap,
            expand=True
        ),
        controls_box
    )

ft.run(main)
