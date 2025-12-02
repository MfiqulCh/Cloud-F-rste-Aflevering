"""
My first application
"""

import toga
import httpx

from toga.style.pack import COLUMN, ROW
from toga.style import Pack
from services.dcr_active_repository import check_login_from_dcr, DcrActiveRepository, EventsFilter, DcrUser

class CloudApp(toga.App):
    graph_id = 2004854
    dcr_ar = None
    current_instance_id = None

    def startup(self):
       
       #Login Box
       login_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
       username_label = toga.Label("Username:", style=Pack(padding=(5, 5)))
       self.username_input = toga.TextInput(style=Pack(flex=1, padding=(5, 5)))

       username_row = toga.Box(
           style = Pack(direction=ROW),
           children = [username_label, self.username_input]
       )

       password_label = toga.Label("Password:", style=Pack(padding=(5, 5)))
       self.password_input = toga.PasswordInput(style=Pack(flex=1, padding=(5, 5)))

       password_row = toga.Box(
           style = Pack(direction=ROW),
           children = [password_label, self.password_input]
       )

       login_button = toga.Button(
           "Login",
           on_press = self.login_handler,
           style = Pack(padding=10)
       )

       login_box.add(username_row)
       login_box.add(password_row)
       login_box.add(login_button)



       #All Instances Box
       self.all_instances_box = toga.Box(style=Pack(direction=COLUMN, flex=1))


       #Instance Box
       instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
       instance_label = toga.Label("Each Instance Will Appear Here", style=Pack(padding=5))

       instance_box.add(instance_label)
       

       
       info_box = toga.Box(style=Pack(direction=ROW, padding=5))

       role_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 10, 0, 10)))

       current_role_label = toga.Label("Current Role:", style=Pack(padding_bottom=5))
       select_other_role_label = toga.Label("Select Other Role:", style=Pack(padding_bottom=5))

       self.role_selection = toga.Selection(
           items=role_items,
           value=role_items[0],
           on_change=self.role_changed,
           style=Pack(padding_bottom=5),
       )

       role_box.add(current_role_label)
       role_box.add(select_other_role_label)
       role_box.add(self.role_selection)

       instance_information_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 10, 0, 10)))

       current_instance_label = toga.Label("Current Instance:", style=Pack(padding_bottom=5))
       not_added_yet_label = toga.Label("Not Added Yet!", style=Pack(padding_bottom=5))

       instance_information_box.add(current_instance_label)
       instance_information_box.add(not_added_yet_label)

       info_box.add(role_box)
       info_box.add(instance_information_box)

       instance_box.add(info_box)

       event_scroll = toga.ScrollContainer(
           horizontal=False,
           style=Pack(direction=COLUMN, flex=1)
       )

       event_box = toga.Box(style=Pack(direction=COLUMN))

       for event in events:
           event_button = toga.Button(
               text=f"{event['label']} (role: {event['role']})",
               id=event['id'],
               on_press=self.execute_event,
               style=Pack(padding=5),
           )
           event_box.add(event_button)
       
       event_scroll.content = event_box
       instance_box.add(event_scroll)

       #Logout Box
       logout_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
       
       logout_button = toga.Button(
           "Logout",
           on_press = self.logout_pressed,
           style=Pack(padding=10)
       )

       logout_box.add(logout_button)

       option_container = toga.OptionContainer(
           content = [
               toga.OptionItem("Login", login_box),
               toga.OptionItem("All instances", self.all_instances_box),
               toga.OptionItem("Instance run", instance_box),
               toga.OptionItem("Logout", logout_box),
               ],
            on_select = self.option_item_changed,
            style=Pack(direction=COLUMN))
       
       self.option_container = option_container
       
       self.main_window = toga.MainWindow(title=self.formal_name)
       self.main_window.content = self.option_container

       self.option_container.content["Logout"].enabled = False
       self.option_container.content["All instances"].enabled = False
       self.option_container.content["Instance run"].enabled = False

       self.main_window.show()
        
    
    
    async def option_item_changed(self, widget):
        print('[i] You Have Selected Another Option Item!')
        if widget.current_tab.text == "All instances":
            await self.show_instances_box()

    async def login_handler(self, widget):
        print(f"[i] Login Detected With Username: {self.username_input.value}")

        connected = await check_login_from_dcr(
            self.username_input.value, 
            self.password_input.value
        )

        if connected:
            self.username = DcrUser(self.username_input.value, self.password_input.value)
            self.dcr_ar = DcrActiveRepository(self.username)

            self.option_container.content["All instances"].enabled = True
            self.option_container.content["Instance run"].enabled = True
            self.option_container.content["Logout"].enabled = True

            self.option_container.current_tab = "All instances"
            self.option_container.content["Login"].enabled = False
        else:
            print("[x] Login failed try again!")
    
    async def show_instances_box(self):
        self.all_instances_box.clear()

        all_instances_label = toga.Label("All Instances Will Be Listed Here", style=Pack(padding=5))

        buttons_box = toga.Box(style=Pack(direction=COLUMN, padding=5)) 

        events = await self.dcr_ar.get_events(self.graph_id, self.current_instance_id, EventsFilter.ALL)
        role_items = []
        if self.user.role:
            role_items.append(self.user.role)
        for event in events:
            event_role = event.role
            if event_role not in role_items:
                role_items.append(event_role)
                
        self.role_selection = toga.Selection(
            items = role_items,
            onchenge = self.role_changed,
            style=Pack(padding_bottom=5),
        )
        
        if len(role_items) > 0:
            self.role_selection.value = role_items[0]
            self.user.role = self.role_selection.value
        
        create_button = toga.Button(
            "Create New Instance",
            on_press=self.create_new_instance,
            style=Pack(padding=(0, 5, 0, 0)),
        )

        delete_button = toga.Button(
            "Delete All Instances",
            on_press=self.delete_all_instances,
            style=Pack(padding=(0, 0, 0, 5), color="red"),
        )

        buttons_box.add(create_button)
        buttons_box.add(delete_button)

        self.all_instances_box.add(all_instances_label)
        self.all_instances_box.add(buttons_box)

        all_instances_container = toga.ScrollContainer(
            horizontal=False,
            style=Pack(direction=COLUMN, flex=1),
        )
        instances_box = toga.Box(style=Pack(direction=COLUMN))

        self.instances = {}
        dcr_ar_instances = await self.dcr_ar.get_instances(self.graph_id)
        if len(dcr_ar_instances) > 0:
            self.instances = dcr_ar_instances
        
        for inst_id, inst_name in self.instances.items():
            row_box = toga.Box(style=Pack(direction=ROW))

            instance_button = toga.Button(
                inst_name,
                on_press=self.show_instance,
                style=Pack(padding=5),
                id=inst_id,
            )
            row_box.add(instance_button)

            del_button = toga.Button(
                "X",
                on_press=self.delete_instance_by_id,
                style=Pack(padding=5, color="red"),
                id=f"X{inst_id}",
            )
            row_box.add(del_button)

            instances_box.add(row_box)
        
        all_instances_container.content = instances_box
        self.all_instances_box.add(all_instances_container)

        self.all_instances_box.refresh()
    
    async def delete_all_instances(self, widget):
        print("[i] Delete All Instances")

        for instance_id in list(self.instances.keys()):
            await self.dcr_ar.delete_instance(self.graph_id, instance_id)
        await self.show_instances_box()
    
    async def create_new_instance(self, widget):
        print("[i] Create New Instance")

        new_id = await self.dcr_ar.create_new_instance(self.graph_id)
        self.current_instance_id = new_id

        await self.show_instances_box()
        self.option_container.current_tab = "Instance run"
    
    async def show_instance(self, widget):
        self.current_instance_id = widget.id
        print(f"[i] You Want To Show: {self.current_instance_id}")

        self.option_container.current_tab = "Instance run"  
    
    async def delete_instance_by_id(self, widget):
        instance_id = widget.id[1:]
        print(f"[i] You Want To Delete: {instance_id}")

        await self.dcr_ar.delete_instance(self.graph_id, instance_id)
        await self.show_instances_box()

    async def role_changed(self, widget):
        print(f'[i] You Changed The Role To {self.role_selection.value}!')

    async def execute_event(self, widget):
        print(f'[i] You want to execute event: {widget.id}!')
    
    async def logout_pressed(self, widget):
        print('[i] Logout Pressed!')

def main():
    return CloudApp()
