import tkinter as tk
import random
from PIL import Image, ImageTk #ไลบรารีสำหรับจัดการและประมวลผลภาพ


class TurnBasedGame:
    def __init__(self, root): #โครงสร้าง ตั้งค่า
        self.root = root
        self.root.title("Turn-Based Game")
        root.configure(bg="lightblue")
        self.player_hp = 100
        self.player_def = 5
        self.default_def = 5
        self.enemy_hp = 100
        self.enemy_def = 5
        self.player_counter_mode = False
        self.enemy_counter_mode = False
        self.attack_limit = 10
        self.defend_limit = 3
        self.counter_limit = 2
        self.ulti_limit = 1
        self.turn = "player"



        self.info = tk.Label(root, text="GAME START!",bg='lightgray') #สร้าง Label widget สำหรับแสดงข้อความ
        self.info.config(font=("",22))
        self.info.pack(fill='x' )

        frame_buttons = tk.Frame(root,bg='lightblue')
        frame_buttons.pack(pady=40)


        self.attack_button = tk.Button(frame_buttons, text="Attack!", command=self.player_attack,font=("", 16), bg='red', fg='white',border=5)
        self.attack_button.pack(side="left", padx=10)

        self.defend_button = tk.Button(frame_buttons, text="Defend!", command=self.player_defend, font=("", 16), bg='blue', fg='white',border=5)
        self.defend_button.pack(side="left", padx=10)

        self.counter_button = tk.Button(frame_buttons, text="Counter!", command=self.player_counter, font=("", 16),  bg='purple', fg='white',border=5)
        self.counter_button.pack(side="left", padx=10)

        self.ultimate_button = tk.Button(frame_buttons, text="Ultimate!", command=self.player_ultimate, font=("", 16), bg='orange', fg='white',border=5)
        self.ultimate_button.pack(side="left", padx=10)

        frame_hp = tk.Frame(root,bg='lightblue')
        frame_hp.pack(pady=10 , fill='x')
        

        self.player_hp_label = tk.Label(frame_hp, text=f"Player HP: {self.player_hp}",font=("", 16),bg='lightgreen',fg='green')
        self.player_hp_label.grid(row=0, column=0, padx=10, sticky="nsew")

        self.enemy_hp_label = tk.Label(frame_hp, text=f"Enemy HP: {self.enemy_hp}",font=("", 16),bg='lightgreen',fg='green')
        self.enemy_hp_label.grid(row=0, column=1, padx=10, sticky="nsew")

        frame_hp.columnconfigure(0, weight=1, uniform="equal")
        frame_hp.columnconfigure(1, weight=1, uniform="equal")

        frame_act = tk.Frame(root,bg='lightblue')
        frame_act.pack(pady=10 , fill='x')

        self.player_act_label = tk.Label(frame_act, text=f"",font=("", 16),bg='pink',fg='black')
        self.player_act_label.grid(row=0, column=0, padx=10, sticky="nsew")

        self.enemy_act_label = tk.Label(frame_act, text=f"",font=("", 16),bg='pink',fg='black')
        self.enemy_act_label.grid(row=0, column=1, padx=10, sticky="nsew")

        frame_act.columnconfigure(0, weight=1, uniform="equal")
        frame_act.columnconfigure(1, weight=1, uniform="equal")
        
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game, font=("Arial", 14), bg="red", fg="white", border=5)

        self.enemy_action_limit = {'atk': 10, 'def': 5, 'counter': 3, 'ulti': 1}

    def player_attack(self):
        if self.turn != "player":
            return
        self.attack_limit -= 1
        if self.attack_limit == 0:
            self.attack_button.config(state=tk.DISABLED)
        self.player_action = "attack"
        self.player_select_done()

    def player_defend(self):
        if self.turn != "player":
            return
        self.defend_limit -= 1
        if self.defend_limit == 0:
            self.defend_button.config(state=tk.DISABLED)
        self.player_action = "defend"
        self.player_select_done()

    def player_counter(self):
        if self.turn != "player":
            return
        self.counter_limit -= 1
        if self.counter_limit == 0:
            self.counter_button.config(state=tk.DISABLED)
        self.player_action = "counter"
        self.player_select_done()

    def player_ultimate(self):
        if self.turn != "player":
            return
        self.ulti_limit -= 1
        if self.ulti_limit == 0:
            self.ultimate_button.config(state=tk.DISABLED)
        self.player_action = "ultimate"
        self.player_select_done()

    def player_select_done(self):
        self.turn = "enemy"
        self.enemy_choose_action()

    def enemy_choose_action(self):
        available_actions = [action for action, count in self.enemy_action_limit.items() if count > 0]
        if available_actions:
            self.enemy_action = random.choice(available_actions)
            self.enemy_action_limit[self.enemy_action] -= 1
        else:
            self.enemy_action = None
        self.root.after(1000, self.resolve_turn)

    def resolve_turn(self):
        self.info.config(text=f"Player chose {self.player_action} | Enemy chose {self.enemy_action}")
        if self.player_action == "counter":
            self.player_counter_mode = True
            self.player_act_label.config(text="Counter! ")
        if self.enemy_action == "counter":
            self.enemy_counter_mode = True
            self.enemy_act_label.config(text="Counter! ")
        if self.player_action == "defend":
            self.player_def *= 3
            self.player_act_label.config(text="Defend! ")
        if self.enemy_action == "def":
            self.enemy_def *= 3
            self.enemy_act_label.config(text="Defend! ")

        # --- Player's Action ---
        if self.player_action == "attack":
            self.do_attack(attacker="player", defender="enemy")
        elif self.player_action == "ultimate":
            self.do_ultimate(attacker="player", defender="enemy")

        # --- Enemy's Action ---
        if self.enemy_action == "atk":
            self.do_attack(attacker="enemy", defender="player")
        elif self.enemy_action == "ulti":
            self.do_ultimate(attacker="enemy", defender="player")

        # --- End Turn ---
        self.enemy_def = self.default_def
        self.player_def = self.default_def
        self.enemy_counter_mode = False
        self.player_counter_mode = False
        self.update_hp()
        self.check_winner()

        if self.player_hp > 0 and self.enemy_hp > 0:
            self.turn = "player"

    def do_attack(self, attacker, defender):
        damage = random.randint(10, 20)
        if attacker == "player":
            if self.enemy_counter_mode:
                damage *= 2
                damage -= self.player_def
                self.player_hp -= damage
                self.player_act_label.config(text="Enemy Counter! " + str(damage)+ " dmg")
            elif damage < self.enemy_def:
                damage = 0
                self.player_act_label.config(text="Block!" + str(damage)+ " dmg")
            else:
                damage -= self.enemy_def
                self.enemy_hp -= damage
                print("Player attacks", damage)
                self.player_act_label.config(text="Player attacks " + str(damage)+ " dmg")
        else:
            if self.player_counter_mode:
                damage *= 2
                damage -= self.enemy_def
                self.enemy_hp -= damage
                print("Player counter! Enemy takes", damage)
                self.enemy_act_label.config(text="Player Counter! " + str(damage)+ " dmg")
            elif damage < self.player_def:
                damage = 0
                print("Block!")
                self.enemy_act_label.config(text="Block! " + str(damage)+ " dmg")
            else:
                damage -= self.player_def
                self.player_hp -= damage
                print("Enemy attacks", damage)
                self.enemy_act_label.config(text="Enemy attacks " + str(damage)+ " dmg")

    def do_ultimate(self, attacker, defender):
        damage = random.randint(30, 40)
        if attacker == "player":
            if self.enemy_counter_mode:
                damage *= 2
                damage -= self.player_def
                self.player_hp -= damage
                self.enemy_counter_mode = False
                print("Enemy counter! Player takes", damage)
                self.player_act_label.config(text="Enemy Counter " + str(damage)+ " dmg")
            elif damage < self.enemy_def:
                damage = 0
            else:
                damage -= self.enemy_def
                self.enemy_hp -= damage
                print("Player uses Ultimate", damage)
                self.player_act_label.config(text="Player Ultimate! " + str(damage)+ " dmg")
        else:
            if self.player_counter_mode:
                damage *= 2
                damage -= self.enemy_def
                self.enemy_hp -= damage
                self.player_counter_mode = False
                print("Player counter! Enemy takes", damage)
                self.enemy_act_label.config(text="Player Counter! " + str(damage)+ " dmg")
            elif damage < self.player_def:
                damage = 0
            else:
                damage -= self.player_def
                self.player_hp -= damage
                print("Enemy uses Ultimate", damage)
                self.enemy_act_label.config(text="Enemy Ultimate " + str(damage)+ " dmg")


    def update_hp(self):
        self.player_hp_label.config(text=f"Player HP: {self.player_hp}")
        self.enemy_hp_label.config(text=f"Enemy HP: {self.enemy_hp}")

    def check_winner(self):
        if self.player_hp <= 0:
            self.info.config(text="You LOSE :C")
            self.disable_buttons()
            self.restart_button.pack(side='bottom',pady=20)
        elif self.enemy_hp <= 0:
            self.info.config(text="You WIN!")
            self.disable_buttons()
            self.restart_button.pack(side='bottom',pady=20)

    def disable_buttons(self):
        self.attack_button.config(state="disabled")
        self.defend_button.config(state="disabled")
        self.counter_button.config(state="disabled")
        self.ultimate_button.config(state="disabled")

    def restart_game(self):
    # รีเซ็ตค่าทั้งหมด
        self.player_hp = 100
        self.enemy_hp = 100
        self.player_def = 5
        self.enemy_def = 5
        self.default_def = 5
        self.player_counter_mode = False
        self.enemy_counter_mode = False
        self.attack_limit = 10
        self.defend_limit = 3
        self.counter_limit = 2
        self.ulti_limit = 1
        self.enemy_action_limit = {'atk': 10, 'def': 5, 'counter': 3, 'ulti': 1}
        self.turn = "player"

        # รีเซ็ตปุ่ม
        self.attack_button.config(state="normal")
        self.defend_button.config(state="normal")
        self.counter_button.config(state="normal")
        self.ultimate_button.config(state="normal")

        # รีเซ็ตข้อความ
        self.info.config(text="GAME RESTARTED!")
        self.player_act_label.config(text="")
        self.enemy_act_label.config(text="")

        # รีเซ็ต HP
        self.update_hp()

        # ซ่อนปุ่มรีสตาร์ท
        self.restart_button.pack_forget()

class AnimatedGIF:
    def __init__(self, label, gif_file, size=None):
        self.label = label
        self.frames = [] #เก็บทุกเฟรมของ GIF
        self.index = 0 #ใช้สำหรับหมุนวนไปแต่ละเฟรม
        self.size = size

        # โหลดภาพด้วย PIL
        img = Image.open(gif_file) #เปิดไฟล์ภาพ
        try:
            while True:
                frame = img.copy() #คัดลอกเฟรม
                if self.size:
                    frame = frame.resize(self.size, Image.LANCZOS) #อัลกอริทึมสำหรับการปรับขนาด
                tk_frame = ImageTk.PhotoImage(frame) #แปลงเป็นรูปแบบที่ Tkinter ใช้ได้
                self.frames.append(tk_frame)
                img.seek(len(self.frames))  # ไปยังเฟรมถัดไป
        except EOFError:
            pass  # หมดเฟรมแล้ว

        self.animate()

    def animate(self):
        if self.frames:
            frame = self.frames[self.index]
            self.label.config(image=frame)
            self.label.image = frame  # ต้องเก็บอ้างอิงไว้ไม่งั้นภาพหาย
            self.index = (self.index + 1) % len(self.frames) #ทำให้หมุนวนไปเรื่อย ๆ
            self.label.after(100, self.animate)  # เปลี่ยนเฟรมทุก 100ms

root = tk.Tk()
game = TurnBasedGame(root)
root.geometry('700x600')
root.maxsize(width=700, height=600)
root.minsize('700','600')


frame_gif = tk.Frame(root, bg='black')
frame_gif.pack(pady=10,fill='x')

gif_label1 = tk.Label(frame_gif, bg='black')
gif_label2 = tk.Label(frame_gif, bg='black')

anim = AnimatedGIF(gif_label1, "images/zenulti.gif", size=(200, 200)) #ปรับขนาด
anim = AnimatedGIF(gif_label2, "images/madara.gif", size=(200, 200))

gif_label1.pack(side="left", padx=10, expand=True)

middle_space = tk.Label(frame_gif, width=1, bg='black') 
middle_space.pack(side="left")

gif_label2.pack(side="left", padx=10, expand=True)

root.mainloop()
