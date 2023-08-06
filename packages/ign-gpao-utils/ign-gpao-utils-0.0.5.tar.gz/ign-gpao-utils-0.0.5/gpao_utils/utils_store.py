from os.path import expanduser
from gpao_utils import interface_utils as iu
import PySimpleGUI as sg

home = expanduser("~")

class Store:
    def __init__(self, win_letter:str, win_path: str, unix_path: str):
        self._win_letter = win_letter
        self._win_path = win_path
        self._unix_path = unix_path

    def replace_letter(self, dir:str):
        return dir.replace(self._win_letter, self._win_path)

    def to_unix(self, dir: str):
        res = self.replace_letter(dir)
        res = res.replace(self._win_path, self._unix_path)
        res = res.replace("\\", "/")
        return res

    def to_win(self, dir: str):
        res = dir.replace(self._unix_path, self._win_path)
        # res = res.replace("/", "\\")
        return res

def frame_store(i: int, L: list):
    if len(L)!=i :
        raise RuntimeError(f"Not the same number of store in parameters. Number : {i}, List : {L}")
    layout_store = []
    for j in range(i):
        layout_store.append([   sg.Text(f" {j} - Lettre (sur ma machine Windows)", size=(iu.size_text, 1)), sg.InputText(sg.user_settings_get_entry(f"-MAP-STORE{j}-WIN-LETTER", "L:"), key=f"-MAP-STORE{j}-WIN-LETTER", size=(iu.size_text_big,{j})) ])
        layout_store.append([   sg.Text(f" {j} - store Windows ", size=(iu.size_text, 1)), sg.InputText(sg.user_settings_get_entry(f"-MAP-STORE{j}-WIN", f"//store.ign.fr/{L[j]}"), key=f"-MAP-STORE{j}-WIN", size=(iu.size_text_big, 1))])
        layout_store.append([   sg.Text(f" {j} - store Linux ", size=(iu.size_text, 1)), sg.InputText(sg.user_settings_get_entry(f"-MAP-STORE{j}-UNIX", f"/var/data/{L[j]}"), key=f"-MAP-STORE{j}-UNIX", size=(iu.size_text_big, 1)) ])
    return sg.Frame("", layout_store)