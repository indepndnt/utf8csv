from utf8csv import language, logs, registry, config


def load_gui() -> int:
    """Import Tkinter and load the GUI to set options and view logs"""
    # imports inside the function so they don't slow down other uses of the program
    import tkinter as tk
    from tkinter.ttk import LabelFrame, Checkbutton, Button, Scrollbar

    class Window(tk.Tk):
        def __init__(self) -> None:
            super().__init__()
            self.settings = config.get_settings()
            self.title("Utf8csv")
            self.iconbitmap(default=str(self.settings.icon_bitmap))
            self.columnconfigure(0, weight=1, minsize=490)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)
            self.rowconfigure(2, weight=0)
            self.minsize(500, 240)

            self.import_default = tk.BooleanVar()
            self.import_default.set(registry.is_set_import_default_encoding())
            self.strip_bom = tk.BooleanVar()
            self.strip_bom.set(self.settings.strip_bom)

            self.create_options_frame()
            self.create_log_frame()
            self.create_close_button()

        def set_import_default(self):
            if self.import_default.get():
                registry.set_import_default_encoding()
            else:
                registry.unset_import_default_encoding()

        def set_strip_bom(self):
            self.settings.strip_bom = self.strip_bom.get()
            self.settings.save()

        def create_options_frame(self):
            frm_options = LabelFrame(
                self, borderwidth=3, relief="groove", text=language.text(language.OPTION_LABEL), height=120
            )
            chk_excel_option = Checkbutton(
                frm_options,
                text=language.text(language.EXCEL_OPT),
                variable=self.import_default,
                command=self.set_import_default,
            )
            chk_excel_option.grid(row=0, sticky="ew")
            chk_strip_option = Checkbutton(
                frm_options, text=language.text(language.STRIP_OPT), variable=self.strip_bom, command=self.set_strip_bom
            )
            chk_strip_option.grid(row=1, sticky="ew")
            frm_options.grid(in_=self, row=0, sticky="nsew", padx=2, pady=2)
            frm_options.grid_propagate(0)

        def create_log_frame(self):
            others, log_text = logs.read_logs()
            frm_logs = LabelFrame(
                self, borderwidth=3, relief="groove", text=language.text(language.LOGS_LABEL), height=80
            )
            # stretch textbox in frame
            frm_logs.grid_rowconfigure(0, weight=1)
            frm_logs.grid_columnconfigure(0, weight=1)
            # create the text widget
            # height={#lines} state=tk.DISABLED for no interaction
            txt_logs = tk.Text(frm_logs, takefocus=0, undo=False)
            txt_logs.insert(1.0, log_text)
            txt_logs.see("end")
            txt_logs.grid(row=0, column=0, sticky="nsew")
            # create the scrollbar
            scroll = Scrollbar(frm_logs, command=txt_logs.yview)
            scroll.grid(row=0, column=1, sticky="nsew")
            txt_logs["yscrollcommand"] = scroll.set
            txt_logs["state"] = "disabled"
            frm_logs.grid(in_=self, row=1, sticky="nsew", padx=2, pady=2)
            frm_logs.grid_propagate(0)

        def create_close_button(self):
            btn_close = Button(self, text=language.text(language.CLOSE), command=self.quit)
            btn_close.grid(in_=self, row=2, sticky="se", padx=20, pady=6)

    app = Window()
    app.mainloop()
    return 0
