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
           on_press = self.login_pressed,
           style = Pack(padding=10)
       )

       login_box.add(username_row)
       login_box.add(password_row)
       login_box.add(login_button)



       #All Instances Box
       all_instances_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
       all_instances_label = toga.Label("All Instances Will Be Listed Here", style=Pack(padding=5))

       buttons_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

       create_button = toga.Button(
           "Create New Instance",
           on_press = self.create_new_instance,
           style = Pack(padding=(0, 5, 0, 0)),
       )
       
       delete_button = toga.Button(
           "Delete All Instances",
           on_press = self.delete_all_instances,
           style=Pack(padding=(0, 0, 0, 5), color='red'),
       )

       buttons_box.add(create_button)
       buttons_box.add(delete_button)

       all_instances_box.add(all_instances_label)
       all_instances_box.add(buttons_box)

       all_instances_container = toga.ScrollContainer(horizontal=False, style=Pack(direction=COLUMN, flex=1))
       instances_box = toga.Box(style=Pack(direction=COLUMN))

       instances = [{'id': 1, 'name':'instance 1'},
                    {'id': 2, 'name':'instance 2'},
                    {'id': 3, 'name':'instance 3'}]
       
       for instance in instances:
           buttons_box = toga.Box(style=Pack(direction=ROW))
           instance_button = toga.Button(
               instance['name'],
               on_press = self.show_instance,
               style = Pack(padding=5),
               id = instance['id']
           )

           buttons_box.add(instance_button)

           del_button = toga.Button(
               'X',
               on_press = self.delete_instance_by_id,
               style = Pack(padding=5, color ='red'),
               id = f'X{instance['id']}'
           )

           buttons_box.add(del_button)

           instances_box.add(buttons_box)
       
       all_instances_container.content = instances_box
       all_instances_box.add(all_instances_container)
       


       #Instance Box
       instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
       instance_label = toga.Label("Each Instance Will Appear Here", style=Pack(padding=5))

       instance_box.add(instance_label)

       role_items = list(['', 'Doctor', 'Nurse', 'Patient'])
       selected_role_item = 'Doctor'
       events = [{'id' : 'Diagnose', 'label' : 'Diagnose', 'role' : 'Doctor'},
                 {'id' : 'Operate', 'label' : 'Operate', 'role' : 'Doctor'},
                 {'id' : 'Give Treatment', 'label' : 'Give Treatment', 'role' : 'Nurse'},
                 {'id' : 'Take Treatment', 'label' : 'Take Treatment', 'role' : 'Patient'}]
       
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
               toga.OptionItem("All Instances", all_instances_box),
               toga.OptionItem("Instance Run", instance_box),
               toga.OptionItem("Logout", logout_box),
               ],
            on_select = self.option_item_changed,
            style=Pack(direction=COLUMN))
       
       self.main_window = toga.MainWindow(title=self.formal_name)
       
       self.option_container = option_container
       self.main_window.content = self.option_container
       
       self.main_window.show()
        
    
    
    async def option_item_changed(self, widget):
        print('[i] You Have Selected Another Option Item!')


    async def login_pressed(self, widget):
        print(f"[i] Login Detected With Username: {self.username_input.value}")
        
        username = self.username_input.value
        password = self.password_input.value
        
        connected = await check_login_from_dcr(self.username_input.value, self.password_input.value)
        
        if isinstance (connected, DcrActiveRepository):
            self.user = DcrUser(self.username_input.value, self.password_input.value)
            self.dcr_ar = connected
            
            self.option_container.content['Logout'].enabled = True
            self.option_container.content['All Instances'].enabled = True
            self.option_container.content['Login'].enabled = False
            self.option_container.content['Instance Run'].enabled = True
            
            self.option_container.value = 'All Instances'
            await self.main_window.info_dialog("Login Success", f"Welcome {username}! You are now logged in.")
        else:
           await self.main_window.error_dialog("Login Failed", "Invalid username or password. Please try again.")
    
    async def delete_all_instances(self, widget):
        print("[i] Delete All Instances")
    
    async def create_new_instance(self, widget):
        print("[i] Create New Instance")
    
    async def show_instance(self, widget):
        print(f"[i] You Want To Show: {widget.id}")
    
    async def delete_instance_by_id(self, widget):
        print(f"[i] You Want To Delete: {widget.id[1:]}")
    
    async def role_changed(self, widget):
        print(f'[i] You Changed The Role To {self.role_selection.value}!')

    async def execute_event(self, widget):
        print(f'[i] You want to execute event: {widget.id}!')
    
    async def logout_pressed(self, widget):
        print('[i] Logout Pressed!')


def main():
    return CloudApp()
