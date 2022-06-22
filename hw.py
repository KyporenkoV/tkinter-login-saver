from tkinter import *
from tkinter import messagebox
import requests
from data_base_workers import udb
from config import cfg

is_auth = False
user_login = udb.get_login()
user_password = udb.get_password()



def send_password_to_tg():
    answer = {
        'chat_id': cfg['tg_chat_id'],
        'text': user_password}
    try:
        requests.post(cfg['tg_main_url'] + cfg['tg_bot_token'] + cfg['tg_method'], json=answer)
        return True
    except EXCEPTION as error:
        print(error)
        return False


def tries(action):
    if action == 'add':
        with open('tries.txt', 'a') as f:
            f.writelines('tries\n')
    elif action == 'reset':
        with open('tries.txt', 'w') as f:
            f.writelines('')
    elif action == 'check':
        with open('tries.txt', 'r') as f:
            lines = f.readlines()
        return len(lines)
    elif action == "create_file":
        with open('tries.txt', 'w') as f:
            f.writelines('')


def app():
    def show_msg_box(event, type, message):
        if type == 'info':
            messagebox.showinfo(title='Information', message=message)
        elif type == 'error':
            messagebox.showerror(title='Error', message=message)
        else:
            print(f'Error message: {message}')

    def clear_password_ent(event):
        f1_ent_password.delete(0, 'end')

    def check_login(login, user_ent):
        if user_ent == login:
            return True
        return False

    def check_password(password, user_ent):
        if user_ent == password:
            return True
        return False

    def text(number):
        try:
            return cfg['msg'][str(number)]
        except EXCEPTION as error:
            print(error)
            return text(0)

    def auth(event):
        global is_auth
        if f1_btn_submit['state'] != 'disabled':
            user_input = f1_ent_login.get()
            if check_login(user_login, user_input):
                if check_password(user_password, f1_ent_password.get()):
                    show_msg_box(event, type='info', message=f"{text(1)} {user_input}")
                    tries('reset')
                    is_auth = True
                    f1_ll_img['image'] = img_unlocked
                    f1_btn_submit['state'] = 'disabled'
                else:
                    if tries('check') < cfg['tries_to_login']:
                        show_msg_box(event, type='error', message=text(3))
                        clear_password_ent(event)
                        tries('add')
                    else:
                        clear_password_ent(event)
                        tries('reset')

                        if send_password_to_tg():
                            show_msg_box(event, type='error', message=text(4))
                        else:
                            show_msg_box(event, type='error', message=text(5))
            else:
                show_msg_box(event, type='error', message=text(3))
                clear_password_ent(event)
        else:
            show_msg_box(event, type='info', message=text(6))
            clear_password_ent(event)

    def get_info_form_db_by_name():
        name = f2_ent_user_entry.get()
        return udb.get_data_by_site_name(name)

    def show_info_from_db(event):
        data = get_info_form_db_by_name()
        if is_auth:
            if data is not None:
                f2_ent_user_entry.delete(0, END)
                f2_ll_info_site_view['text'] = data[0][0]
                f2_ll_info_login_view['text'] = data[0][1]
                f2_ll_info_password_view['text'] = data[0][2]
                f2_ll_info_comment_view['text'] = data[0][3]
            else:
                show_msg_box(event, type='error', message=text(7))
                f2_ent_user_entry.delete(0, END)
        else:
            show_msg_box(event, type='error', message=text(8))
            f2_ent_user_entry.delete(0, END)

    def put_info_into_db(event):
        if is_auth:
            name = f3_ent_name_of_site.get()
            login = f3_ent_login.get()
            password = f3_ent_password.get()
            comment = f3_ent_comment.get()
            if len(name) > 0 and len(login) > 0 and len(password) > 0:
                try:
                    udb.set_data_to_db(site_name=name, login=login, password=password, comment=comment)
                    show_msg_box(event, type='info', message=text(9))
                    clear_frame3_inputs()

                except EXCEPTION as error:
                    print(error)
                    show_msg_box(event, type='error', message=text(10))
            else:
                show_msg_box(event, type='error', message=text(20))
        else:
            show_msg_box(event, type='error', message=text(11))
            f2_ent_user_entry.delete(0, END)

    def clear_frame3_inputs():
        f3_ent_name_of_site.delete(0, END)
        f3_ent_login.delete(0, END)
        f3_ent_password.delete(0, END)
        f3_ent_comment.delete(0, END)

    # ----------------------------------------------------------------------------

    tries('create_file')

    root = Tk()

    root.title(cfg['app_title'])
    root.geometry(cfg['geometry'])
    root.resizable(cfg['resizable_width'], cfg['resizable_height'])

    # -------------------------------------------------------------------------------------`
    # -----------------------         FRAME 1                ------------------------------`
    # -------------------------------------------------------------------------------------
    frm_1 = Frame(root, bg=cfg['bg1'], borderwidth=0)

    f1_ll_title = Label(master=frm_1, text=text(22), font=cfg['label_font_2'], bg=cfg['bg1'])

    f1_ll_login = Label(master=frm_1, text=text(14), font=cfg['label_font_1'], bg=cfg['bg1'])
    f1_ent_login = Entry(master=frm_1, font=cfg['entry_font_1'])

    f1_ll_password = Label(master=frm_1, text=text(15), font=cfg['label_font_1'], bg=cfg['bg1'])
    f1_ent_password = Entry(master=frm_1, font=cfg['entry_font_1'], show='*')

    f1_btn_submit = Button(master=frm_1, text=text(21), font=cfg['btn_font_1'], bg=cfg['bg2'])
    f1_btn_submit.bind("<Button-1>", auth)

    img_locked = PhotoImage(file='locked.png')
    img_unlocked = PhotoImage(file='open.png')
    f1_ll_img = Label(master=frm_1, image=img_locked, bg=cfg['bg1'])

    frm_1.place(x=20, y=20, width=300, height=500)
    f1_ll_title.place(x=20, y=10, width=260, height=30)
    f1_ll_login.place(x=20, y=60, width=60, height=30)
    f1_ent_login.place(x=20, y=90, width=260, height=30)
    f1_ll_password.place(x=20, y=160, width=80, height=30)
    f1_ent_password.place(x=20, y=190, width=260, height=30)
    f1_btn_submit.place(x=50, y=250, width=200, height=40)
    f1_ll_img.place(x=75, y=320, width=150, height=150)

    # -------------------------------------------------------------------------------------
    # -----------------------         FRAME 2                ------------------------------
    # -------------------------------------------------------------------------------------

    frm_2 = Frame(root, bg=cfg['bg1'])
    f2_ll_title = Label(master=frm_2, text=text(24), font=cfg['label_font_2'], bg=cfg['bg1'])

    f2_ent_user_entry = Entry(master=frm_2, font=cfg['entry_font_1'])

    f2_btn_submit = Button(master=frm_2, text=text(19), font=cfg['btn_font_1'], bg=cfg['bg2'])
    f2_btn_submit.bind("<Button-1>", show_info_from_db)

    f2_ll_info_site_title = Label(master=frm_2, text=text(13), bg=cfg['bg1'])
    f2_ll_info_site_view = Label(master=frm_2, text=text(2), justify=cfg['justify'])

    f2_ll_info_login_title = Label(master=frm_2, text=text(14), bg=cfg['bg1'])
    f2_ll_info_login_view = Label(master=frm_2, text=text(2))

    f2_ll_info_password_title = Label(master=frm_2, text=text(15), bg=cfg['bg1'])
    f2_ll_info_password_view = Label(master=frm_2, text=text(2))

    f2_ll_info_comment_title = Label(master=frm_2, text=text(18), bg=cfg['bg1'])
    f2_ll_info_comment_view = Label(master=frm_2, text=text(2))

    # --- place ---
    frm_2.place(x=340, y=20, width=300, height=500)
    f2_ll_title.place(x=10, y=10, width=260, height=30)
    f2_ent_user_entry.place(x=20, y=60, width=260, height=30)
    f2_btn_submit.place(x=50, y=105, width=200, height=40)
    f2_ll_info_site_title.place(x=20, y=160, width=100, height=30)
    f2_ll_info_site_view.place(x=20, y=190, width=260, height=30)
    f2_ll_info_login_title.place(x=20, y=240, width=40, height=30)
    f2_ll_info_login_view.place(x=20, y=270, width=260, height=30)
    f2_ll_info_password_title.place(x=20, y=320, width=60, height=30)
    f2_ll_info_password_view.place(x=20, y=350, width=260, height=30)
    f2_ll_info_comment_title.place(x=20, y=390, width=60, height=30)
    f2_ll_info_comment_view.place(x=20, y=420, width=260, height=60)  # todo розширене поле

    # -------------------------------------------------------------------------------------
    # -----------------------         FRAME 3                ------------------------------
    # -------------------------------------------------------------------------------------

    frm_3 = Frame(root, bg=cfg['bg1'])

    f3_ll_title = Label(master=frm_3, text=text(23), font=cfg['label_font_2'], bg=cfg['bg1'])

    f3_ll_instructions = Label(master=frm_3, text=text(12), justify='left', bg=cfg['bg1'])

    f3_ll_name_of_site = Label(master=frm_3, text=text(13), bg=cfg['bg1'])
    f3_ent_name_of_site = Entry(master=frm_3, font=cfg['entry_font_1'])

    f3_ll_login = Label(master=frm_3, text=text(14), bg=cfg['bg1'])
    f3_ent_login = Entry(master=frm_3, font=cfg['entry_font_1'])

    f3_ll_password = Label(master=frm_3, text=text(15), bg=cfg['bg1'])
    f3_ent_password = Entry(master=frm_3, font=cfg['entry_font_1'])

    f3_ll_comment = Label(master=frm_3, text=text(16), bg=cfg['bg1'])
    f3_ent_comment = Entry(master=frm_3, font=cfg['entry_font_1'])

    f3_btn_submit = Button(master=frm_3, text=text(17), font=cfg['btn_font_1'], bg=cfg['bg2'])

    f3_btn_submit.bind("<Button-1>", put_info_into_db)

    frm_3.place(x=660, y=20, width=300, height=500)
    f3_ll_title.place(x=10, y=10, width=260, height=30)
    f3_ll_instructions.place(x=40, y=40, width=200, height=60)
    f3_ll_name_of_site.place(x=20, y=120, width=90, height=30)
    f3_ent_name_of_site.place(x=20, y=150, width=260, height=30)
    f3_ll_login.place(x=20, y=190, width=40, height=30)
    f3_ent_login.place(x=20, y=220, width=260, height=30)
    f3_ll_password.place(x=20, y=260, width=60, height=30)
    f3_ent_password.place(x=20, y=290, width=260, height=30)
    f3_ll_comment.place(x=20, y=330, width=140, height=30)
    f3_ent_comment.place(x=20, y=360, width=260, height=60)  # todo textaria
    f3_btn_submit.place(x=75, y=440, width=150, height=40)

    root.mainloop()


if __name__ == '__main__':

    app()
