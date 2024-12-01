import flet as ft
import platform as pt
import psutil as psu
from datetime import datetime,timedelta
import asyncio
import cpuinfo
import GPUtil

global gpuspec
gpuspec = GPUtil.getGPUs()

class gpup(ft.Text): #Я ненавижу нахуй асинхрон
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_cpup)
    def will_unmount(self): 
        self.running=False
    
    async def update_cpup(self):
        while True:
            self.value=str(gpuspec[0].load*100) + " %" 
            self.update() 
            await asyncio.sleep(1)

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

#Я знаю что это ужасная имплементация, и Бог простит меня за то, что я собираюсь сделать, но я сижу третью ночь на Да Хун Пао, и я хочу чтобы программа страдала за меня

#За сим...
#ВЫПУСКАЙТЕ ЯДРА!!!!!!!!!!!
#ГОЙДААААААААААААААААААААААААААА!

'''class core1(ft.Text):
    global corecount 
    corecount= len(psu.cpu_percent(interval=1,percpu=True))
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_cpup)
    def will_unmount(self):
        self.running=False
    
    async def update_cpup(self):
        while True:
            finalstr = ''
            for i in range(corecount):
                finalstr += " " + str(psu.cpu_percent(interval=1,percpu=True)[i]) + " % "
            self.value=finalstr 
            self.update()
            await asyncio.sleep(0.5)
'''
#Окей я знал что это хуёвая имплементация, но чтоб настолько...
#Пока нигде не юзаем, потом придумаем получше

## TODO : Сделать универсальный динамический класс (я пытался)

class runclock(ft.Text):
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_clck)
    def will_unmount(self):
        self.running=False

    async def update_clck(self):
        while True:
            self.value=timedelta(seconds=datetime.now().timestamp()-psu.boot_time()) ## часы 
            self.update() # см. выше
            await asyncio.sleep(0.4)

class ramusage(ft.Text): ## Оперативка
    def did_mount(self):
        self.running=True
        self.page.run_task(self.update_clck)
    def will_unmount(self):
        self.running=False

    
    async def update_clck(self):
        while True:
            self.value=str(psu.virtual_memory()[2]) + " %" + "       Исп. " + str(round(psu.virtual_memory()[3]/1000000000,2)) + " ГБ"
            self.update() # см. выше
            await asyncio.sleep(0.3)

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
            await asyncio.sleep(0.2)

def main(page: ft.Page):
    page.window.height=500
    page.window.width=510
    page.window.resizable=False
    page.window.maximizable=False
    a=psu.cpu_freq(percpu=False)
    swap = psu.swap_memory()
    svmem = psu.virtual_memory()
    gpus = len(gpuspec)
    if gpus > 1:
        secondone = 1
    else: secondone=0
#ГОЙДААААААААААААААААААААААААААА!
    t = ft.Tabs(
        selected_index=0,
        animation_duration=500,
        tabs=[
            ft.Tab(
                text="Общее",
                icon=ft.icons.COMPUTER,
                content=ft.Column([ft.DataTable(
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
                ),ft.Container(ft.Text('[C] Unproductive.',text_align=ft.TextAlign.RIGHT),alignment=ft.alignment.bottom_right) ]) #---------Вставляй виджеты сюда
            ),
            ft.Tab(
                text="ЦП",
                
                content=ft.Column([ft.DataTable(
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
                ), ])         #---------Вставляй виджеты сюда
            ),
            ft.Tab(
                
                text="Видеокарта", 
                content=ft.Tabs(selected_index=0,animation_duration=500,
                                tabs=[
                                    ft.Tab(
                                        text='1',visible=gpus>0,
                                         content=ft.Column([ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Характеристика")),
                        ft.DataColumn(ft.Text("Значение")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Имя GPU')),
                                ft.DataCell(ft.Text(gpuspec[0].name)),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Нагрузка GPU')),
                                ft.DataCell(gpup(str(gpuspec[0].load*100)+" %"))
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Температура')),
                                ft.DataCell(ft.Text(str(gpuspec[0].temperature)+ " °C")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Всего памяти')),
                                ft.DataCell(ft.Text(str(gpuspec[0].memoryTotal) + " MB, " + str(gpuspec[0].memoryTotal // 1000) + " GB")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Занятой памяти')),
                                ft.DataCell(ft.Text(str(gpuspec[0].memoryUsed) + " MB, " + str(gpuspec[0].memoryUsed // 1000) + " GB")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('GPU UUID')),
                                ft.DataCell(ft.Text(str(gpuspec[0].uuid))),
                            ]
                        ),
                    ]
                ),ft.Container(ft.Text('[C] Unproductive.',text_align=ft.TextAlign.RIGHT),alignment=ft.alignment.bottom_right) ])
                                    ),

                                    ft.Tab(
                                        text='2',visible=gpus>1,
                                         content=ft.Column([ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Характеристика")),
                        ft.DataColumn(ft.Text("Значение")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Имя GPU')),
                                ft.DataCell(ft.Text(gpuspec[secondone].name)),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Нагрузка GPU')),
                                ft.DataCell(gpup(str(gpuspec[secondone].load*100)+" %"))
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Температура')),
                                ft.DataCell(ft.Text(str(gpuspec[secondone].temperature)+ " °C")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Всего памяти')),
                                ft.DataCell(ft.Text(str(gpuspec[secondone].memoryTotal) + " MB, " + str(gpuspec[secondone].memoryTotal // 1000) + " GB")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Занятой памяти')),
                                ft.DataCell(ft.Text(str(gpuspec[secondone].memoryUsed) + " MB, " + str(gpuspec[secondone].memoryUsed // 1000) + " GB")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('GPU UUID')),
                                ft.DataCell(ft.Text(str(gpuspec[secondone].uuid))),
                            ]
                        ),
                    ]
                ),ft.Container(ft.Text('[C] Unproductive.',text_align=ft.TextAlign.RIGHT),alignment=ft.alignment.bottom_right) ])
                                    ),
                                    

                                    
                                ]
                    
                )               
            ),

            ft.Tab(text='ОЗУ',content=ft.Column([ft.DataTable(
                columns=[
                        ft.DataColumn(ft.Text("Характеристика")),
                        ft.DataColumn(ft.Text("Значение")),
                    ],
                rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Размер ОЗУ')),
                                ft.DataCell(ft.Text(str(svmem.total//1024//1024//1000) + " ГБ // Точно : " + str(svmem.total))),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Доступно ОЗУ')),
                                ft.DataCell(ft.Text(str(svmem.available//1024//1024//1000) + " ГБ // Точно : " + str(svmem.available)))
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('% ОЗУ')),
                                ft.DataCell(ramusage(psu.virtual_memory()[2])),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Размер SWAP')),
                                ft.DataCell(ft.Text(str(swap.total//1024//1024//1000) + " ГБ // Точно : " + str(swap.total))),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('Доступно SWAP')),
                                ft.DataCell(ft.Text(str(swap.free//1024//1024//1000) + " ГБ // Точно : " + str(swap.free)))
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text('% SWAP')),
                                ft.DataCell(ft.Text(str(swap.percent)+" %")),
                            ]
                        ),
                    ]
            )])),
        
            
        
        ],
        expand=1,
    
    )

    page.add(t)

    


ft.app(main)
