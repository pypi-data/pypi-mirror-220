import typing as t
import asyncio
from datetime import datetime

import dearpygui.dearpygui as dpg
from aioconnection.transport.serialport import SerialTransport, serialports_list
from aioconnection import Event, Etype

from dearpyapp import *


# TODO проверять, используется ли в текущем приложении порт, в транспорте реализовать контроль всех портов
# TODO выставить default высоту в зависимости от кол-ва портов
# TODO настройки порта вывести в gui
class PortControlWindow:
    LOG_SIZE = 50

    def __init__(self, transport=None, *, change_callback=None, status_callback=None):
        self.gui = self._Gui()
        self.parent_port_control: t.Optional[PortControl] = None
        self.port_control = PortControl(transport, change_callback=change_callback,
                                        status_callback=status_callback)

    def set_y_scroll(self):  # TODO добавить в общую библиотеку
        gui = self.gui
        scroll_max = dpg.get_y_scroll_max(gui.ports_log)
        scroll = dpg.get_y_scroll(gui.ports_log)
        if scroll == scroll_max:
            dpg.set_y_scroll(gui.ports_log, -1)

    async def scan_ports(self):
        def buttons_callback(s, a, u):
            self.port_changed(dpg.get_item_label(s))

        def show_button(tag):
            if tag:
                dpg.configure_item(tag, show=True)
                ports_buttons_hidden.remove(tag)
            else:
                tag = dpg.add_button(label=changed_port, width=-1, parent=gui.ports,
                                     callback=buttons_callback)
                ports_buttons.update({changed_port: tag})

        def hide_button(tag):
            if tag:
                dpg.configure_item(tag, show=False)
                ports_buttons_hidden.add(tag)

        gui = self.gui
        ports = set()
        ports_buttons = {}
        ports_buttons_hidden = set()
        first_button = False
        while True:
            actual_ports_list = serialports_list()
            actual_ports = set(actual_ports_list)
            new_ports = actual_ports - ports
            deleted_ports = ports - actual_ports

            if new_ports or deleted_ports:
                with dpg_container(gui.ports_log):
                    for ports_group in (new_ports, deleted_ports):
                        is_new_ports = ports_group is new_ports
                        log_text = 'connected' if is_new_ports else 'disconnected'
                        log_color = c.GREEN_23 if is_new_ports else c.RED_23
                        show_hide_button = show_button if is_new_ports else hide_button
                        for changed_port in ports_group:
                            show_hide_button(ports_buttons.get(changed_port))
                            if first_button:
                                with dpg.group(horizontal=True):
                                    dpg.add_button(label=changed_port, width=60,
                                                   callback=buttons_callback)
                                    dpg.add_text(log_text, color=log_color)
                                    dpg.add_text(datetime.now().strftime("%m.%d.%y %H:%M:%S"),
                                                 indent=140)

                log_items = dpg.get_item_children(gui.ports_log, 1)
                if len(log_items) > self.LOG_SIZE:
                    for item in log_items[:-self.LOG_SIZE]:
                        dpg.delete_item(item)
                self.set_y_scroll()

                button_order = [ports_buttons[port] for port in actual_ports_list]
                button_order.extend(list(ports_buttons_hidden))
                dpg.reorder_items(gui.ports, 1, button_order)

            first_button = True
            ports = actual_ports
            await asyncio.sleep(0.3)

    def load_parent_info(self, parent_port_control):
        self_port_control = self.port_control
        self_port_control.transport = parent_port_control.transport
        self_port_control.status_callback = parent_port_control.status_callback
        dpg.set_value(self_port_control.gui.port_input, dpg.get_value(parent_port_control.gui.port_input))
        dpg.set_value(self_port_control.gui.is_active, dpg.get_value(parent_port_control.gui.is_active))
        self.parent_port_control = parent_port_control

    def show(self, s, a, u):
        self.load_parent_info(dpg.get_item_user_data(a))
        dpg.configure_item(self.gui.window, pos=dpg.get_item_rect_min(a), show=True, width=350, height=200)
        dpg.focus_item(self.port_control.gui.port_input)

    def transport_changed(self, parent_port_control):
        if parent_port_control is self.parent_port_control:
            self.load_parent_info(parent_port_control)

    def port_changed(self, value):
        self.port_control.port_changed(value)
        self.parent_port_control.port_changed(value)

    def create_gui(self):
        gui = self.gui

        with dpg.theme(tag=gui.theme_port_ok):
            with dpg.theme_component():
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, c.GREEN_6)
                dpg.add_theme_color(dpg.mvThemeCol_Text, c.GRAY_25)
        with dpg.theme(tag=gui.theme_port_error):
            with dpg.theme_component():
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, c.RED_9)
                dpg.add_theme_color(dpg.mvThemeCol_Text, c.GRAY_25)

        with dpg.theme() as window_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)

        with dpg.theme() as children_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 2)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, 0)
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, c.TRANSPARENT)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c.BLUE_9)
                dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0)

        with dpg.item_handler_registry(tag=gui.port_input_handler_reg):
            dpg.add_item_activated_handler(callback=self.show)

        with dpg.window(tag=gui.window, show=False, no_resize=True, no_move=True, no_title_bar=True):
            dpg.bind_item_theme(gui.window, window_theme)

            self.port_control.create_gui()
            port_input = self.port_control.gui.port_input
            dpg.bind_item_handler_registry(port_input, 0)
            dpg.configure_item(port_input, callback=lambda s, a, u: self.port_changed(a))
            dpg.configure_item(self.port_control.gui.is_active,
                               callback=lambda s, a, u: self.parent_port_control.active_changed(a))

            with dpg.group(horizontal=True, horizontal_spacing=10, indent=5):
                with dpg.group():
                    dpg.add_text('Ports', color=c.BLUE_18)
                    dpg.add_child_window(border=False, width=80, height=-5, tag=gui.ports)
                    dpg.bind_item_theme(gui.ports, children_theme)
                with dpg.group():
                    with dpg.group(horizontal=True):
                        dpg.add_text('Connections Log', color=c.BLUE_18)
                        dpg.add_button(label='Clear',
                                       callback=lambda s, a, u: dpg.delete_item(gui.ports_log, children_only=True))
                    dpg.add_child_window(border=False, width=-1, height=-5, tag=gui.ports_log)
                    dpg.bind_item_theme(gui.ports_log, children_theme)

        get_running_app().loop.create_task(self.scan_ports())

    @dpg_uuid
    class _Gui:
        window: int
        ports: int
        ports_log: int
        port_input_handler_reg: int
        theme_port_ok: int
        theme_port_error: int


class PortControl:
    popup: PortControlWindow = None

    @dpg_uuid
    class Gui:
        port_input: int
        is_active: int
        status: int
        status_tooltip: int
        status_tooltip_text: int

    def __init__(self, transport=None, *, change_callback=None, status_callback=None,
                 gui: Gui = None):
        self.gui: PortControl.Gui = gui
        self.change_callback = change_callback
        self.status_callback = status_callback
        self._transport: SerialTransport = transport

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, transport):
        if self._transport == transport:
            return
        if self._transport:
            self._transport.get_protocol().unsubscribe(self.update_port_status)
        if transport:
            transport.get_protocol().subscribe(self.update_port_status)
            dpg.set_value(self.gui.port_input, transport.port)
            dpg.set_value(self.gui.is_active, transport.is_active())
        self._transport = transport
        self.update_port_status()
        self.__class__.popup.transport_changed(self)

    def update_port_status(self, event: Event = None):
        event_type = event.type if event else None
        if not self._transport or event_type not in (None, Etype.CONNECT_FAILED, Etype.CONNECTED):
            return

        gui = self.gui
        if not dpg.does_item_exist(gui.port_input):
            if self._transport:
                self._transport.get_protocol().unsubscribe(self.update_port_status)
            self._transport = None
            return

        is_active = self._transport.is_active()
        is_connect_failed = event_type == Etype.CONNECT_FAILED
        port_status = '' if not dpg.get_value(gui.port_input) else \
                      'Closed' if not is_active else \
                      'Error' if is_connect_failed or self._transport.is_closing() else \
                      'Opened'
        theme = 0 if not dpg.get_value(gui.port_input) or not is_active else \
                self.popup.gui.theme_port_error if is_connect_failed or self._transport.is_closing() else \
                self.popup.gui.theme_port_ok
        dpg.bind_item_theme(gui.port_input, theme)
        dpg.set_value(gui.status, port_status)
        status_text = self.status_callback() if self.status_callback else ''
        if is_active and is_connect_failed and event.data:
            status_text += str(event.data)
        if status_text:
            dpg.configure_item(gui.status_tooltip, show=True)
            dpg.set_value(gui.status_tooltip_text, status_text)
        else:
            dpg.configure_item(gui.status_tooltip, show=False)

    def port_changed(self, value):
        dpg.set_value(self.gui.port_input, value)
        if self._transport is not None:
            self._transport.port = value
            self.notify()

    def active_changed(self, value):
        dpg.set_value(self.gui.is_active, value)
        if self._transport is not None:
            (self._transport.open if value else self._transport.close)()
            self.notify()

    def notify(self):
        self.update_port_status()
        if self.change_callback:
            self.change_callback()

    def create_gui(self):
        if (gui := self.gui) is None:
            gui = self.gui = PortControl.Gui()
            with dpg.group(horizontal=True, horizontal_spacing=2):
                dpg.add_input_text(tag=gui.port_input)
                dpg.add_checkbox(tag=gui.is_active)
                dpg.add_text(tag=gui.status)

        dpg.configure_item(gui.port_input, hint='Port Name', width=70, user_data=self, on_enter=False)
        dpg.configure_item(gui.is_active, callback=lambda s, a, u: self.active_changed(a))
        with dpg.tooltip(gui.port_input, show=False, tag=gui.status_tooltip):
            dpg.add_text(tag=gui.status_tooltip_text)

        cls = self.__class__
        if cls.popup is None:
            cls.popup = PortControlWindow()
            cls.popup.create_gui()

        dpg.bind_item_handler_registry(gui.port_input, cls.popup.gui.port_input_handler_reg)
        # TODO WTF
        transport = self._transport
        self._transport = None
        self.transport = transport

