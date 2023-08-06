import os
import ttkbootstrap as ttk
from datetime import datetime, timedelta
from SherLocking.file import HiddenConfig


# VARIABLES
CHARACTERS = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ_0123456789'
INTERVALS = {
    '1 Day': 1,
    '1 Week': 7,
    '2 Weeks': 14,
    '3 Weeks': 21,
    '1 Month': 30,
    '2 Months': 60,
    '3 Months': 90,
    '4 Months': 120,
    '5 Months': 150,
    '6 Months': 180,
    '7 Months': 210,
    '8 Months': 240,
    '9 Months': 270,
    '10 Months': 300,
    '11 Months': 330,
    '1 Year': 365,
    'Unlimited': 0
}


def encode(string: str, seed: str) -> str:
    result = ''
    for character, offset in zip(string, seed):
        index_a = CHARACTERS.index(character)
        index_b = CHARACTERS.index(offset)
        index_c = (index_a + index_b) % len(CHARACTERS)
        result += CHARACTERS[index_c]
    return result


def decode(string: str, seed: str) -> str:
    result = ''
    for character, offset in zip(string, seed):
        index_a = CHARACTERS.index(character)
        index_b = CHARACTERS.index(offset)
        index_c = (index_a - index_b) % len(CHARACTERS)
        result += CHARACTERS[index_c]
    return result


class StatusBar(ttk.Frame):
    def __init__(self, master: ttk.Frame, **kwargs):
        super().__init__(master, **kwargs)


class ActivateLicense(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # PROPERTIES
        self.variable = 'USERPROFILE'
        self.directory = os.path.join(os.environ[self.variable], 'desktop') 
        self.config_path = os.path.join(self.directory, 'NTMAF.json')
        self.config_file = HiddenConfig(self.config_path)

        # VARIABLES
        today = self.get_today().strftime('%x')
        intervals = [
            '1 Day', '1 Week', '2 Weeks', '3 Weeks',
            '1 Month', '2 Months', '3 Months', '4 Months', '5 Months', '6 Months',
            '7 Months', '8 Months', '9 Months', '10 Months', '11 Months',
            '1 Year', 'Unlimited'
        ]

        # UI

        date_frame = ttk.LabelFrame(self, text='Date')
        date_frame.pack(expand=True, fill='x', padx=10, pady=10, ipady=5)
        ttk.Label(date_frame, text='Activation date: ').grid(row=0, column=0, padx=20, sticky='w')
        ttk.Label(date_frame, text=today).grid(row=0, column=1, padx=(0, 20), sticky='w')
        ttk.Label(date_frame, text='Activation interval: ').grid(row=1, column=0, padx=20, sticky='w')
        self.interval_combobox = ttk.Combobox(date_frame, values=intervals)
        self.interval_combobox.current(0)
        self.interval_combobox.grid(row=1, column=1, padx=(0, 20), sticky='w')

        info_frame = ttk.LabelFrame(self, text='Info')
        info_frame.pack(expand=True, fill='x', padx=10, pady=(0, 10), ipady=5)
        ttk.Label(info_frame, text='Program seed: ').grid(row=0, column=0, padx=20, sticky='w')
        self.seed_entry = ttk.Entry(info_frame, width=20, state='disabled')
        self.seed_entry.grid(row=0, column=1, padx=(0, 20), sticky='w', pady=5)
        ttk.Label(info_frame, text='Program name: ').grid(row=1, column=0, padx=20, sticky='w')
        self.program_name = ttk.Entry(info_frame, width=20)
        self.program_name.grid(row=1, column=1, padx=(0, 20), sticky='w')

        ttk.Button(self, text='Activate...', bootstyle='success', command=self.activate).pack(fill='x', padx=10, pady=(0, 10))

        # BINDS
        self.wm_protocol('WM_DELETE_WINDOW', self.leave)
        self.program_name.bind('<KeyRelease>', self.update_seed)
    
    def update_seed(self, *_) -> None:
        """Creates a unique seed por each name"""
        string, seed = 'MAFER', ''
        name = self.program_name.get()
        length = len(name)
        for i in range(length): seed += string[i%5]
        seed = encode(name, seed)
        self.seed_entry.config(state='normal')
        self.seed_entry.delete(0, 'end')
        self.seed_entry.insert(0, seed)
        self.seed_entry.config(state='disabled')
    
    def get_today(self) -> datetime:
        """Returns todays date"""
        return datetime.today()

    def leave(self, *_) -> None:
        """Saves the config and exits the app"""
        self.config_file.save()
        self.destroy()

    def activate(self) -> None:
        """Applies the logic to activate a program"""
        info = dict()
        interval = INTERVALS[self.interval_combobox.get()]
        info['installed'] = self.get_today().strftime('%x')
        info['seed'] = self.seed_entry.get()
        if not interval: info['until'] = None
        else:
            info['until'] = self.get_today() + timedelta(days=interval)
            info['until'] = info['until'].strftime('%x')
        code = encode(self.program_name.get(), info['seed'])
        self.config_file.update(code, info)


def activate() -> None:
    window = ActivateLicense(
        themename='darkly',
        resizable=(None, None),
        title='License Activator By Armando Chaparro 17/07/23',
    )

    window.mainloop()


if __name__ == '__main__':
    activate()