from types import FunctionType
from contextlib import contextmanager
from collections import ChainMap
import typing as t

import dearpygui.dearpygui as dpg
import dearpygui._dearpygui as internal_dpg
from recordclass import make_dataclass, dataobject


_T = t.TypeVar('_T')

_top_container_name = 'mvWindowAppItem'
_container_name_lookup = {
    dpg.mvWindowAppItem: _top_container_name,
    dpg.mvChildWindow: 'mvChildWindow',
    dpg.mvGroup: 'mvGroup',
    dpg.mvTab: 'mvTab',
}

_not_container_name_lookup = {
    dpg.mvImage: 'mvImage',
    dpg.mvInputText: 'mvInputText',
    dpg.mvText: 'mvText',
    dpg.mvCombo: 'mvCombo',
    dpg.mvListbox: 'mvListbox',
    dpg.mvCollapsingHeader: 'mvCollapsingHeader',
    dpg.mvTabBar: 'mvTabBar',
    dpg.mvTab: 'mvTab',
    dpg.mvMenuBar: 'mvMenuBar',
    dpg.mvMenu: 'mvMenu',
    dpg.mvMenuItem: 'mvMenuItem',
    dpg.mvDragFloat: 'mvDragFloat',
    dpg.mvInputFloat: 'mvInputFloat',
    dpg.mvSliderFloat: 'mvSliderFloat',
    dpg.mvDragInt: 'mvDragInt',
    dpg.mvInputInt: 'mvInputInt',
    dpg.mvSliderInt: 'mvSliderInt',
    dpg.mvCheckbox: 'mvCheckbox',
    dpg.mvButton: 'mvButton',
    dpg.mvRadioButton: 'mvRadioButton',
    dpg.mvImageButton: 'mvImageButton',
    dpg.mvColorButton: 'mvColorButton',
    dpg.mvProgressBar: 'mvProgressBar',
    dpg.mvTable: 'mvTable',
    dpg.mvDatePicker: 'mvDatePicker',
    dpg.mvTimePicker: 'mvTimePicker',
    dpg.mvTreeNode: 'mvTreeNode',
    dpg.mvPlot: 'mvPlot',
    dpg.mvSimplePlot: 'mvSimplePlot',
    dpg.mvSeparator: 'mvSeparator',
    dpg.mvSpacer: 'mvSpacer',
    dpg.mvColorEdit: 'mvColorEdit',
    dpg.mvColorPicker: 'mvColorPicker',
    dpg.mvTooltip: 'mvTooltip',
}

_item_type_lookup = {v: k for k, v in ChainMap(_container_name_lookup,
                                               _not_container_name_lookup).items()}


@contextmanager
def dpg_container(tag):
    try:
        dpg.push_container_stack(tag)
        yield tag
    finally:
        dpg.pop_container_stack()


def dpg_get_item_container(item, container_type: int = dpg.mvWindowAppItem) -> t.Optional[int]:
    container_name = _container_name_lookup.get(container_type)
    assert container_name is not None
    first_iter = True
    while True:
        item_name = dpg_get_item_name(item)
        if not first_iter and item_name == container_name:
            return item
        elif item_name == _top_container_name:
            return
        first_iter = False
        item = dpg.get_item_parent(item)


def dpg_get_item_name(item) -> str:
    return internal_dpg.get_item_info(item)["type"].rsplit('::')[1]


def dpg_get_item_type(item) -> int:
    item_type = _item_type_lookup.get(dpg_get_item_name(item))
    assert item_type is not None
    return item_type


def dpg_get_item_by_pos(items: t.Union[list, tuple], mouse_pos, horizontal: bool = False, *,
                        return_index=False):
    index_start = 0
    index_end = len(items)
    while True:
        index = index_start + (index_end - index_start) // 2
        if index == index_start:
            break
        item = items[index]
        item = item if isinstance(item, (str, int)) else item[0]
        # TODO если в таблице включен клиппер, то get_item_pos возвращает 0, если элемент вне видимости
        if mouse_pos[not horizontal] >= dpg.get_item_pos(item)[not horizontal]:
            index_start = index
        else:
            index_end = index
    return (items[index_start], index_start) if return_index else items[index_start]


def dpg_set_y_scroll(item, window, offset: float = 0.85):
    scroll_pos = dpg.get_y_scroll(window)
    win_size = dpg.get_item_rect_size(window)[1]
    btn_size = dpg.get_item_rect_size(item)[1]
    if (pos := dpg.get_item_pos(item)[1]) > scroll_pos + win_size - btn_size:
        dpg.set_y_scroll(window, pos - win_size * (1 - offset) + btn_size)
    elif pos < scroll_pos:
        dpg.set_y_scroll(window, max(0, int(pos - win_size * offset)))


def dpg_show_popup(item, window):
    state = dpg.get_item_state(item)
    dpg.configure_item(window, show=True, pos=(state['rect_min'][0], state['rect_max'][1]))


# TODO переделать под датакласс
def dpg_uuid(cls: _T, return_values=False) -> _T:
    def wrap(*args):
        values = []
        for name, class_ in cls.__annotations__.items():
            if isinstance(class_, FunctionType) and class_.__qualname__ == wrap.__qualname__:
                value = class_()
            else:
                is_named_tuple = class_.__base__ is tuple and hasattr(class_, '_fields')
                try:
                    class_.__annotations__
                except AttributeError:
                    if is_named_tuple:
                        value = class_(*(dpg.generate_uuid() for _ in range(len(getattr(class_, '_fields')))))
                    else:
                        value = dpg.generate_uuid()
                else:
                    if is_named_tuple:
                        value = class_(*dpg_uuid(class_, return_values=True)())
                    else:
                        value = dpg_uuid(class_, )()

            values.append(value)

        if return_values:
            return values
        else:
            factory = cls if cls.__base__ is dataobject else \
                make_dataclass(cls.__name__, cls.__annotations__.keys(), fast_new=True)
            return factory(*values)
    return wrap


# TODO поддержка dataclass, tuple, list
# TODO делать перевод значения в соответсвующий класс типа int str и т.д.
# TODO возможность выгружать в существующий объект, а не создавать новый
# TODO переделка под dpg.get_values для оптимизации
# TODO периодически проверять, не изменил ли viewport свой размер, или просто по евенту перемещения окна сделать
def dpg_get_values(gui_obj):
    cls = getattr(gui_obj, '__class__')
    values = []
    for tag, cls_ in cls.__annotations__.items():
        gui_obj_ = getattr(gui_obj, tag)
        is_named_tuple = cls_.__base__ is tuple and hasattr(cls_, '_fields')
        try:
            cls_.__annotations__
        except AttributeError:
            if is_named_tuple:
                value = cls_(*(dpg.get_value(getattr(gui_obj_, tag_)) for tag_ in cls_))
            else:
                value = cls_(dpg.get_value(gui_obj_))
        else:
            value = dpg_get_values(gui_obj_)
        values.append(value)
    return cls(*values)


def dpg_set_values(gui_obj, val_obj):
    cls = getattr(val_obj, '__class__')
    for tag, cls_ in cls.__annotations__.items():
        gui_obj_ = getattr(gui_obj, tag)
        val_obj_ = getattr(val_obj, tag)
        is_named_tuple = cls_.__base__ is tuple and hasattr(cls_, '_fields')
        try:
            cls_.__annotations__
        except AttributeError:
            if is_named_tuple:
                for tag_ in cls_:
                    dpg.set_value(getattr(gui_obj_, tag_), getattr(val_obj_, tag_))
            else:
                dpg.set_value(gui_obj_, val_obj_)
        else:
            dpg_set_values(gui_obj_, val_obj_)


def _get_wrapped_text(text, wrap, font):
    text_size = start_index = 0
    wrapped_text = []
    for char_index, char in enumerate(text):
        text_size += dpg.get_text_size(char, font=font)[0]
        if char == '\n' or (wrap and text_size > wrap):
            wrapped_text.append(text[start_index: char_index])
            start_index = char_index + 1 if char == '\n' else char_index
            text_size = 0
    wrapped_text.append(text[start_index:])
    return '\n'.join(wrapped_text)


def dpg_get_text_from_cell(cell, wrap=-1, font=0):
    if (item_type := dpg_get_item_type(cell)) == dpg.mvText:
        text = dpg.get_value(cell)
        width, height = dpg.get_text_size(text, font=font, wrap_width=wrap)
    elif item_type != dpg.mvGroup:
        return None, 0, 0
    else:
        width, height = dpg.get_item_rect_size(cell)
        cell_items = dpg.get_item_children(cell, slot=1)
        for index, item in enumerate(cell_items):
            text = dpg.get_value(item) if dpg_get_item_type(item) == dpg.mvText else \
                ''.join(dpg.get_value(text_item) for text_item in dpg.get_item_children(item, slot=1))
            cell_items[index] = text
        text = '\n'.join(cell_items)
    if wrap >= 0:
        text = _get_wrapped_text(text, wrap, font)
        width_, height_ = dpg.get_text_size(text, font=font)
        if text.endswith('\n'):
            height_ += dpg.get_text_size(' ', font=font)[1]
        width = max(width_, width)
        height = max(height_, height)
    return text, width, height
