import flet as ft
import platform as pt
import psutil as psu
from datetime import datetime,timedelta
import asyncio
import cpuinfo

class cpup(ft.Text): #Я ненавижу нахуй асинхрон
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_cpup)
    def will_unmount(self): # И что это бля значит???
        #Как будто инстанс будет аки винчестер монтироваться. бред какой-то
        self.running=False
    
    async def update_cpup(self):
        while True:
            self.value=str(psu.cpu_percent(interval=1)) + " %" #Аж в долях процентов. О как!!
            self.update() # И почему теперь он может апдейтиться, а внизу кода не может????
            await asyncio.sleep(1)

class runclock(ft.Text):
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_clck)
    def will_unmount(self):
        self.running=False

    async def update_clck(self):
        while True:
            self.value=timedelta(seconds=datetime.now().timestamp()-psu.boot_time())
            self.update() # см. выше
            await asyncio.sleep(1)

class ramusage(ft.Text):
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_clck)
    def will_unmount(self):
        self.running=False

    async def update_clck(self):
        while True:
            self.value=str(psu.virtual_memory()[2]) + " %" + "       Исп. " + str(round(psu.virtual_memory()[3]/1000000000,2)) + " ГБ"
            self.update() # см. выше
            await asyncio.sleep(1)

class cpuclock(ft.Text):
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_clck)
    def will_unmount(self):
        self.running=False

    async def update_clck(self):
        while True:
            self.value=str(psu.cpu_freq(percpu=False)[0])
            self.update() # см. выше
            await asyncio.sleep(1)

def main(page: ft.Page):
    #cpup = ft.Text(psu.cpu_percent())
    #timeee=ft.Text()
    a=psu.cpu_freq(percpu=False)
    t = ft.Tabs(
        selected_index=1,
        animation_duration=500,
        tabs=[
            ft.Tab(
                text="Общее",
                icon=ft.icons.COMPUTER,
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Характеристика")),
                        ft.DataColumn(ft.Text("Значение")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Имя ПК')),
                                ft.DataCell(ft.Text(pt.node())),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Система')),
                                ft.DataCell(ft.Text(pt.system() +" "+ pt.version() +" "+ pt.win32_edition()))
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Дата последнего запуска')),
                                ft.DataCell(ft.Text(datetime.fromtimestamp(psu.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Время с последнего запуска')),
                                ft.DataCell(runclock(timedelta(seconds=datetime.now().timestamp()-psu.boot_time()))),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Нагрузка ЦП')),
                                ft.DataCell(cpup(psu.cpu_percent())),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Нагрузка ОЗУ')),
                                ft.DataCell(ramusage(psu.virtual_memory()[2])),
                            ]
                        ),
                    ]
                )
            ),
            ft.Tab(
                text="ЦП",
                
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Характеристика")),
                        ft.DataColumn(ft.Text("Значение")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Имя ЦП')),
                                ft.DataCell(ft.Text(cpuinfo.cpu.info[0]['ProcessorNameString'])),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Нагрузка ЦП')),
                                ft.DataCell(cpup(psu.cpu_percent())),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Ядра')),
                                ft.DataCell(ft.Text(psu.cpu_count(logical=False)))
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Потоки')),
                                ft.DataCell(ft.Text(psu.cpu_count(logical=True))),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Настоящая частота')),
                                ft.DataCell(cpuclock(psu.cpu_freq(percpu=False)[0])),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Мин. частота')),
                                ft.DataCell(ft.Text(a[1])),
                            ]
                        ),
                        
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Макс. частота')),
                                ft.DataCell(ft.Text(a[2])),
                            ]
                        ),
                    ]
                )
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text(""),               
            ),

        ],
        expand=1,
    
    )

    page.add(t)

    


ft.app(main)
