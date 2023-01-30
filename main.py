#modulos 
import flet
from flet import *
import os

controls_dict = {}

class Button(UserControl):
    def __init__(self, btn_name, btn_width, btn_function):
        self.btn_name = btn_name
        self.btn_width = btn_width
        self.btn_function = btn_function
        super().__init__()
    
    def build(self):
        return ElevatedButton(
            on_click=self.btn_function,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(self.btn_name,size=11,weight="bold"),
                ],
            ),
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)},
                color={"":"white"}
            ),
            height=48,
            width=self.btn_width
        )



class FileNameChanger(UserControl):
    def __init__(self):
        #para habilitar el método Filepicker() en flet, necesitamos llamar a varios métodos y agregarlos a la página
        # esta es una manera de usarlo cuando se trabaja con orientación a objetos
        # esta sera la devolucion a la llamada de los archivos   
        # Cuando accedemos al cuadro de diálogo Abrir archivo, debemos crear un método que haga algo después de que el usuario envíe    
        self.btn_callback_files = FilePicker(
            on_result=self.name_change_files
        )
        # esta sera la devolucion a la llamada de las carpetas
        self.btn_callback_folder = FilePicker(
            on_result=self.name_changer_folder_files
        )
        #ahora creamos una lsita para almacenar la ruta de nuestros archivos /carpetas
        self.session = []
        super().__init__()

    #funcion para eliminar columna
    def clear_column(self, e):
        control = controls_dict["files"]
        control.content =None
        self.update()

    #retorna una lista de elementos selecionados 
    def return_file_list(self,file_icon,file_name,file_path):
        return Column(
            controls=[
                Row(
                    controls=[
                        Icon(file_icon,size=12),
                        Text(file_name,size=13),
                    ]
                ),
                Row(
                    controls=[
                        Text(file_path,
                        size=9,
                        no_wrap=False,
                        color="white54")
                    ]
                ),
            ],
        )

    def final_name_change(self, e):
        control = controls_dict['files']
        #Hacemos esto porque queremos mostrar los nombres actualizados
        control.content = Column(scroll='auto',expand=True)
        self.update()
        #Necesitamos verificar la sesión si es un archivo único / múltiple o una carpeta. Nuevamente usamos el módulo OS aquí
        if os.path.isfile(self.session[0]):
            for count, file in enumerate(self.session):
                #En este bucle for se enumera la lista de archivos de la sesión actual
                #Esto nos proporciona la ruta raíz del archivo
                #Lo necesitamos para cambiar los archivos y guardarlos en el mismo lugar
                current_dir = os.path.dirname(file)
                """importante: He configurado esta lógica para cambiar archivos PNG, ya que necesitaba la aplicación mientras trabajaba con grandes cantidades de hojas de sprites. Sin embargo, la clase es escalable y cualquiera puede cambiar la extensión para incluir archivos como ccv, jpeg, pdf, etc. Pero por ahora, nos quedaremos con PNG"""
                new_file = os.path.join(current_dir + "/" +str(count) + ".png")
                #El .png puede cambiar, o mejor aún, los usuarios pueden tener opciones dentro de la aplicación
                # Ahora, podemos cambiar el nombre de los archivos
                os.rename(file,new_file)
                control.content.controls.append(
                    self.return_file_list(
                        icons.FILE_COPY_ROUNDED,f"{count}.png",new_file
                    )
                )
                control.content.update()
        # Ahora necesitamos manejar carpetas
        if os.path.isdir(self.session[0]):
            counter = 0
            control.content.controls.append(
                Row(
                    controls=[
                        Icon(icons.FOLDER_COPY_ROUNDED,size=12),
                        Text(self.session[0],size=13),
                    ]
                )
            )
            control.content.controls.append(
                Container(
                    padding=padding.only(left=18),
                    content=Column(expand=True),
                )
            )
            for file in os.listdir(self.session[0]):
                file = os.path.join(self.session[0] +"/" + file)
                # Queremos asegurarnos de que sólo cambiamos el nombre de los archivos de la carpeta seleccionada
                if os.path.isfile(file):
                    new_file = os.path.join(
                        self.session[0] + "/" + str(counter) + ".png"
                    )
                    os.rename(file, new_file)
                    control.content.controls[1].content.controls.append(
                        self.return_file_list(
                            icons.FILE_COPY_ROUNDED, f"{counter}.png",self.session[0]
                        )
                    )
                    control.content.update()
                    counter +=1

    def name_changer_folder_files(self, e:FilePickerResultEvent):
        self.session= []
        if e.path:
            control = controls_dict["files"]
            control.content = Column(
                scroll="auto",
                expand=True
            )
            self.session.append(e.path)
            self.update()
            control.content.controls.append(
                Row(
                    controls=[
                        Icon(icons.FOLDER_COPY_ROUNDED,
                        size=12),
                        Text(e.path, size=13)
                    ]
                ),
            )
            control.content.controls.append(
                Container(
                    padding=padding.only(left=18),
                    content=Column(expand=True),
                )
            )
            #ocupando el modulo os
            for file in os.listdir(e.path):
                #Estamos pasando la ruta de la carpeta al método Listdir, que devolverá una lista de todas las cosas en la ruta de acceso
                file_path = os.path.join(e.path + "/" + file)
                control.content.controls[1].content.controls.append(
                    self.return_file_list(icons.FILE_COPY_ROUNDED,file,file_path)
                )
                control.content.update()
    
    #Vamos a crear las funciones que mostrarán los archivos y carpetas en la pantalla. Haremos esto en dos partes, una para cada botón
    def name_change_files(self, e:FilePickerResultEvent):
        #Necesitamos llamar a nuestra sesión, que será la ruta absoluta para cada archivo
        self.session = []
        if e.files:#verificamos los archivos de file
            control = controls_dict['files']#aca almacenamos nuestra columna creada en base a los datos que nos retornara e.files de filepicker result
            control.content = Column(scroll='auto',expand=True)
            self.update()
            for file in e.files:
                self.session.append(file.path)
                control.content.controls.append(
                    self.return_file_list(
                        #aca pasamos los argumentos
                        icons.FILE_COPY_ROUNDED,file.name,file.path
                    )
                )
                control.content.update()
        else:
            pass
        """Esta parte debe mostrar los archivos seleccionados en la pantalla"""

    def name_changer_title(self):
        return Container(
            content=Row(
                expand=True,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Python Filename Changer",
                    size=14,
                    weight="bold"),
                    IconButton(
                        content=Text("x",
                        weight="bold",
                       ),
                       on_click=lambda __: self.page.window_close(),
                    ),
                ],
            )
        )

    def name_changer_step_one(self):
        return Container(
            height=80,
            border=border.all(0.8,"white24"),
            border_radius=6,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    #crear clase butom e insertala aca
                    Button(
                        "Update File(s)",
                        240,
                        #Ahora podemos pasar una función a la que se llamará después de que el usuario seleccione un archivo
                        lambda __:self.btn_callback_files.pick_files(allow_multiple=True)
                    ),
                    #Para usar el filepicker() que acabamos de crear, necesitamos agregarlo a la pantalla, por lo que debemos pasarlo con esta declaración return.
                    self.btn_callback_files,
                    self.btn_callback_folder,
                    Button(
                        "Update Folder",
                        240,
                        lambda __:self.btn_callback_folder.get_directory_path(),
                    ),
                ],
            ),
        )

    def name_changer_step_two(self):
        self.container = Container(
            height=160,
            border=border.all(0.80, "white24"),
            border_radius=6,
            padding=12,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )
        #Debemos almacenar este objeto en algún lugar para que podamos llamarlo fácilmente
        controls_dict['files']= self.container
        return self.container

    def name_changer_step_tree(self):
        return Container(
            height=80,
            border_radius=6,
            border=border.all(0.8, "white24"),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                spacing=5,
                controls=[
                    Row(
                        spacing=0,
                        controls=[
                            IconButton(
                                icon=icons.HIGHLIGHT_REMOVE_ROUNDED,
                                icon_size=21,
                                on_click=lambda e: self.clear_column(e) 
                            ),
                            IconButton(
                                icon=icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                icon_size=21,
                                on_click=lambda e: self.final_name_change(e)
                            ),
                        ]
                    )
                ]
            )
        )

    def build(self):
        return Column(
            expand=True,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                #aca van los componentes de la aplicación
                self.name_changer_title(),
                Divider(height=20, color="transparent"),
                Text("Step 1. Get a file or folder", size=12,weight="bold"),
                self.name_changer_step_one(),
                Divider(height=10, color="transparent"),
                Text("Step 2. Output files/folder", size=12,weight="bold"),
                self.name_changer_step_two(),
                Divider(height=10, color="transparent"),
                Text("Step 3. Update File Name(s)", size=12,weight="bold"),
                self.name_changer_step_tree()
            ]
        )

def main(page:Page):
    page.window_width = 600
    page.window_height = 620
    #page.window_title_bar_hidden= True
    page.theme_mode= ThemeMode.DARK
    #page.window_title_bar_buttons_hidden = True
    page.padding = 25
    page.add(FileNameChanger())
    page.update()
    pass


if __name__ == "__main__":
    flet.app(target=main)