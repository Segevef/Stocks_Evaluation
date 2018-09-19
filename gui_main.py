import tkinter as tk
from tkinter import *
import ticker_spider as ts
from PIL import ImageTk, Image
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from pandastable import Table


stock_data = dict()


class StockEvaluation(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill=BOTH, expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, CompetitionPage, FinancialPage, AnalystsPage, EstimatePage, HoldersDescriptionPage, DescriptionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")

    def get_page(self, page_class):
        return self.frames[page_class]


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.master.title("Main Page")
        # self.pack(fill=BOTH, expand=True)
        # self.style = Style()
        # self.style.theme_use("default")

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Stock Evaluation")
        head_line.pack(side=TOP, padx=5, pady=5)

        # Search frame - below top
        frame_search = Frame(self, borderwidth=1)
        frame_search.pack(side=TOP, fill=X)

        entry_symbol = Entry(frame_search)
        entry_symbol.pack(side=LEFT, fill=Y, padx=5, expand=False)

        def on_search_click():
            symbol_txt = entry_symbol.get()
            # Error message - if empty or symbol not found
            global stock_data
            stock_data = ts.analyze_ticker(symbol_txt)

            financial_button = Button(frame_bottom, text="Financial",
                                      command=lambda: controller.show_frame(FinancialPage))
            financial_button.pack(side=LEFT, padx=2, pady=2)
            estimate_button = Button(frame_bottom, text="Estimate",
                                     command=lambda: controller.show_frame(EstimatePage))
            estimate_button.pack(side=LEFT, padx=2, pady=2)
            analysis_button = Button(frame_bottom, text="Analysts",
                                     command=lambda: controller.show_frame(AnalystsPage))
            analysis_button.pack(side=LEFT, padx=2, pady=2)
            holders_button = Button(frame_bottom, text="Holders",
                                    command=lambda: controller.show_frame(HoldersDescriptionPage))
            holders_button.pack(side=LEFT, padx=2, pady=2)
            desc_button = Button(frame_bottom, text="Description",
                                 command=lambda: controller.show_frame(DescriptionPage))
            desc_button.pack(side=LEFT, padx=2, pady=2)

            # Table frame - data
            frame_table = Frame(self, relief=SUNKEN, borderwidth=3)
            frame_table.pack(side=TOP, fill=BOTH, expand=True)
            count_rows = 0
            count_columns = 0
            if stock_data is not None:

                def delete_keys_from_finviz():
                    if stock_data['finviz_table'].get('Index'): del stock_data['finviz_table']['Index']
                    if stock_data['finviz_table'].get('Book/sh'): del stock_data['finviz_table']['Book/sh']
                    if stock_data['finviz_table'].get('Dividend'): del stock_data['finviz_table']['Dividend']
                    if stock_data['finviz_table'].get('Optionable'): del stock_data['finviz_table']['Optionable']
                    if stock_data['finviz_table'].get('Shortable'): del stock_data['finviz_table']['Shortable']
                    if stock_data['finviz_table'].get('Quick Ratio'): del stock_data['finviz_table']['Quick Ratio']
                    if stock_data['finviz_table'].get('Current Ratio'): del stock_data['finviz_table']['Current Ratio']
                    if stock_data['finviz_table'].get('LT Debt/Eq'): del stock_data['finviz_table']['LT Debt/Eq']
                    if stock_data['finviz_table'].get('SMA20'): del stock_data['finviz_table']['SMA20']
                    if stock_data['finviz_table'].get('SMA50'): del stock_data['finviz_table']['SMA50']
                    if stock_data['finviz_table'].get('Insider Own'): del stock_data['finviz_table']['Insider Own']
                    if stock_data['finviz_table'].get('Insider Trans'): del stock_data['finviz_table']['Insider Trans']
                    if stock_data['finviz_table'].get('Inst Own'): del stock_data['finviz_table']['Inst Own']
                    if stock_data['finviz_table'].get('Inst Trans'): del stock_data['finviz_table']['Inst Trans']
                    if stock_data['finviz_table'].get('Payout'): del stock_data['finviz_table']['Payout']
                    if stock_data['finviz_table'].get('SMA200'): del stock_data['finviz_table']['SMA200']
                    if stock_data['finviz_table'].get('Shs Outstand'): del stock_data['finviz_table']['Shs Outstand']
                    if stock_data['finviz_table'].get('Shs Float'): del stock_data['finviz_table']['Shs Float']
                    if stock_data['finviz_table'].get('Short Ratio'): del stock_data['finviz_table']['Short Ratio']
                    if stock_data['finviz_table'].get('RSI (14)'): del stock_data['finviz_table']['RSI (14)']
                    if stock_data['finviz_table'].get('Rel Volume'): del stock_data['finviz_table']['Rel Volume']
                    if stock_data['finviz_table'].get('Volume'): del stock_data['finviz_table']['Volume']
                    if stock_data['finviz_table'].get('Beta'): del stock_data['finviz_table']['Beta']
                    if stock_data['finviz_table'].get('Prev Close'): del stock_data['finviz_table']['Prev Close']
                    if stock_data['finviz_table'].get('Change'): del stock_data['finviz_table']['Change']

                delete_keys_from_finviz()

                for key in stock_data['finviz_table'].keys():
                    # Label and Entry - like finviz table with extra data
                    label = Label(frame_table, text=key, padx=1, pady=1, width=14, anchor='w')
                    entry = Label(frame_table, text=stock_data['finviz_table'].get(key),
                                  padx=1, pady=1, width=10)
                    # Place table on grid
                    label.grid(row=count_rows, column=count_columns, padx=5, pady=1)
                    entry.grid(row=count_rows, column=count_columns+1, padx=5, pady=1)
                    count_rows = count_rows + 1
                    if count_rows % 15 == 0:
                        count_columns = count_columns + 2
                        count_rows = 0

        search_button = Button(frame_search, text="Search Symbol", command=on_search_click)
        search_button.pack(side=LEFT, padx=5, pady=5)

        # Bottom frame
        # Right side
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=2, pady=2)
        comp_button = Button(frame_bottom, text="Evaluate Competitors",
                             command=lambda: controller.show_frame(CompetitionPage))
        comp_button.pack(side=RIGHT, padx=2, pady=2)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=2, pady=2)
        # Left side appears after search


class CompetitionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Competitors From The Same Sector")
        head_line.pack(side=TOP, padx=5, pady=5)


        # Bottom frame
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)
        back_button = Button(frame_bottom, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=RIGHT)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=5, pady=5)


class FinancialPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Financial")
        head_line.pack(side=TOP, padx=5, pady=5)

        # Bottom frame - Right side
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)
        back_button = Button(frame_bottom, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=RIGHT)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=5, pady=5)
        # Left side
        financial_button = Button(frame_bottom, text="Financial",
                                  command=lambda: controller.show_frame(FinancialPage))
        financial_button.pack(side=LEFT, padx=2, pady=2)
        estimate_button = Button(frame_bottom, text="Estimate",
                                 command=lambda: controller.show_frame(EstimatePage))
        estimate_button.pack(side=LEFT, padx=2, pady=2)
        analysis_button = Button(frame_bottom, text="Analysts",
                                 command=lambda: controller.show_frame(AnalystsPage))
        analysis_button.pack(side=LEFT, padx=2, pady=2)
        holders_button = Button(frame_bottom, text="Holders",
                                command=lambda: controller.show_frame(HoldersDescriptionPage))
        holders_button.pack(side=LEFT, padx=2, pady=2)
        desc_button = Button(frame_bottom, text="Description",
                                command=lambda: controller.show_frame(DescriptionPage))
        desc_button.pack(side=LEFT, padx=2, pady=2)

    def on_show_frame(self, event):

        # Table frame - data
        frame_table = Frame(self, relief=SUNKEN, borderwidth=3)
        frame_table.pack(side=TOP, fill=BOTH, expand=True)

        if stock_data:
            self.table = pt = Table(frame_table, dataframe=stock_data['financial'].reset_index(),
                                    showtoolbar=True, showstatusbar=True)
            pt.show()


class EstimatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Estimate By Analysts")
        head_line.pack(side=TOP, padx=5, pady=5)

        # Bottom frame
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)
        back_button = Button(frame_bottom, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=RIGHT)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=5, pady=5)
        # Left side
        financial_button = Button(frame_bottom, text="Financial",
                                  command=lambda: controller.show_frame(FinancialPage))
        financial_button.pack(side=LEFT, padx=2, pady=2)
        estimate_button = Button(frame_bottom, text="Estimate",
                                 command=lambda: controller.show_frame(EstimatePage))
        estimate_button.pack(side=LEFT, padx=2, pady=2)
        analysis_button = Button(frame_bottom, text="Analysts",
                                 command=lambda: controller.show_frame(AnalystsPage))
        analysis_button.pack(side=LEFT, padx=2, pady=2)
        holders_button = Button(frame_bottom, text="Holders",
                                command=lambda: controller.show_frame(HoldersDescriptionPage))
        holders_button.pack(side=LEFT, padx=2, pady=2)
        desc_button = Button(frame_bottom, text="Description",
                                command=lambda: controller.show_frame(DescriptionPage))
        desc_button.pack(side=LEFT, padx=2, pady=2)

    def on_show_frame(self, event):

        # Table frame - data
        frame_table = Frame(self, relief=SUNKEN, borderwidth=3)
        frame_table.pack(side=TOP, fill=BOTH, expand=True)

        if stock_data:
            self.table = pt = Table(frame_table, dataframe=stock_data['estimates'],
                                    showtoolbar=True, showstatusbar=True)
            pt.show()


class AnalystsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Analysts")
        head_line.pack(side=TOP, padx=5, pady=5)

        # Bottom frame
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)
        back_button = Button(frame_bottom, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=RIGHT)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=5, pady=5)
        # Left side
        financial_button = Button(frame_bottom, text="Financial",
                                  command=lambda: controller.show_frame(FinancialPage))
        financial_button.pack(side=LEFT, padx=2, pady=2)
        estimate_button = Button(frame_bottom, text="Estimate",
                                 command=lambda: controller.show_frame(EstimatePage))
        estimate_button.pack(side=LEFT, padx=2, pady=2)
        analysis_button = Button(frame_bottom, text="Analysts",
                                 command=lambda: controller.show_frame(AnalystsPage))
        analysis_button.pack(side=LEFT, padx=2, pady=2)
        holders_button = Button(frame_bottom, text="Holders",
                                command=lambda: controller.show_frame(HoldersDescriptionPage))
        holders_button.pack(side=LEFT, padx=2, pady=2)
        desc_button = Button(frame_bottom, text="Description",
                                command=lambda: controller.show_frame(DescriptionPage))
        desc_button.pack(side=LEFT, padx=2, pady=2)

    def on_show_frame(self, event):

        # Table frame - data
        frame_table = Frame(self, relief=SUNKEN, borderwidth=3)
        frame_table.pack(side=TOP, fill=BOTH, expand=True)
        frame_table1 = Frame(self, relief=SUNKEN, borderwidth=3)
        frame_table1.pack(side=TOP, fill=BOTH, expand=True)
        frame_table2 = Frame(self, relief=SUNKEN, borderwidth=3)
        frame_table2.pack(side=TOP, fill=BOTH, expand=True)

        if stock_data:
            self.table = pt = Table(frame_table, dataframe=stock_data['analysis'],
                                    showtoolbar=True, showstatusbar=True)
            pt.show()


class HoldersDescriptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Company Description & Stock Holders")
        head_line.pack(side=TOP, padx=5, pady=5)

        # Bottom frame
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)
        back_button = Button(frame_bottom, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=RIGHT)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=5, pady=5)
        # Left side
        financial_button = Button(frame_bottom, text="Financial",
                                  command=lambda: controller.show_frame(FinancialPage))
        financial_button.pack(side=LEFT, padx=2, pady=2)
        estimate_button = Button(frame_bottom, text="Estimate",
                                 command=lambda: controller.show_frame(EstimatePage))
        estimate_button.pack(side=LEFT, padx=2, pady=2)
        analysis_button = Button(frame_bottom, text="Analysts",
                                 command=lambda: controller.show_frame(AnalystsPage))
        analysis_button.pack(side=LEFT, padx=2, pady=2)
        holders_button = Button(frame_bottom, text="Holders",
                                command=lambda: controller.show_frame(HoldersDescriptionPage))
        holders_button.pack(side=LEFT, padx=2, pady=2)
        desc_button = Button(frame_bottom, text="Description",
                                command=lambda: controller.show_frame(DescriptionPage))
        desc_button.pack(side=LEFT, padx=2, pady=2)

    def on_show_frame(self, event):

        # Table frame - data
        frame_table = Frame(self, relief=SUNKEN, borderwidth=3)
        frame_table.pack(side=TOP, fill=BOTH, expand=True)

        if stock_data:
            self.table = pt = Table(frame_table, dataframe=stock_data['holders'].reset_index(),
                                    showtoolbar=True, showstatusbar=True)
            pt.show()


class DescriptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Top frame
        frame_top = Frame(self, relief=RAISED, borderwidth=1)
        frame_top.pack(side=TOP, fill=BOTH, expand=False)

        head_line = Label(frame_top, text="Company Description")
        head_line.pack(side=TOP, padx=5, pady=5)

        # Bottom frame - Right side
        frame_bottom = Frame(self, relief=RAISED, borderwidth=1)
        frame_bottom.pack(side=BOTTOM, fill=X)

        close_button = Button(frame_bottom, text="Exit", command=quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)
        back_button = Button(frame_bottom, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=RIGHT)
        export_button = Button(frame_bottom, text="Export to XLSX")
        export_button.pack(side=RIGHT, padx=5, pady=5)
        # Left side
        financial_button = Button(frame_bottom, text="Financial",
                                  command=lambda: controller.show_frame(FinancialPage))
        financial_button.pack(side=LEFT, padx=2, pady=2)
        estimate_button = Button(frame_bottom, text="Estimate",
                                 command=lambda: controller.show_frame(EstimatePage))
        estimate_button.pack(side=LEFT, padx=2, pady=2)
        analysis_button = Button(frame_bottom, text="Analysts",
                                 command=lambda: controller.show_frame(AnalystsPage))
        analysis_button.pack(side=LEFT, padx=2, pady=2)
        holders_button = Button(frame_bottom, text="Holders",
                                command=lambda: controller.show_frame(HoldersDescriptionPage))
        holders_button.pack(side=LEFT, padx=2, pady=2)
        desc_button = Button(frame_bottom, text="Description",
                                command=lambda: controller.show_frame(DescriptionPage))
        desc_button.pack(side=LEFT, padx=2, pady=2)

    def on_show_frame(self, event):

        # Text widget - description
        frame_center = Frame(self, relief=RAISED, borderwidth=1)
        frame_center.pack(side=TOP, fill=X)

        if stock_data:
            text_widget = Text(frame_center, relief=SUNKEN, borderwidth=3, height=20, width=35)
            text_widget.pack(side=TOP, fill=BOTH, expand=True)
            text_widget.insert(END, stock_data['description'])


def quit():
    sys.exit()


def main():
    app = StockEvaluation()
    app.wm_title("Stock Evaluation")
    # app.wm_iconbitmap()
    app.geometry("900x550+300+100")
    app.mainloop()


if __name__ == '__main__':
    main()

