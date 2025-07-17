import tkinter as tk
from tkinter import ttk, messagebox

catalog = [
    (1, "Blue berries",   19.50),
    (2, "Straw berries",  19.50),
    (3, "Kit kat",         9.80),
    (4, "Eggs",           10.50),
    (5, "Bread",          18.00),
    (6, "Milk",           20.00),
    (7, "Meat",           30.00),
    (8, "Rolls",          20.00),
    (9, "Chocolate",      12.00),
    (10, "Yogurt",        11.00),
    (11, "Cheese",        25.00),
    (12, "Butter",        15.00),
    (13, "Cereal",        17.50),
    (14, "Juice",         13.75),
]
product_info = {pid: (name, price) for pid, name, price in catalog}

class ShoppingCartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛍️ Trini’s Fancy Shopping Cart")
        self.geometry("1000x700")
        self.configure(bg="#ffe4e1")
        self.cart = {}

        # --- Header Canvas with Gradient ---
        self.header = tk.Canvas(self, height=100, bd=0, highlightthickness=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.header.bind("<Configure>", self._redraw_header)

        # --- Customer Details ---
        details = tk.Frame(self, bg="#ffc0cb", pady=10, padx=10)
        details.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.name_var  = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        tk.Label(details, text="Name:",  bg="#ffc0cb").grid(row=0, column=0, sticky="e")
        tk.Entry(details, textvariable=self.name_var, width=25).grid(row=0, column=1, padx=5)
        tk.Label(details, text="Email:", bg="#ffc0cb").grid(row=0, column=2, sticky="e")
        tk.Entry(details, textvariable=self.email_var, width=25).grid(row=0, column=3, padx=5)
        tk.Label(details, text="Phone:", bg="#ffc0cb").grid(row=0, column=4, sticky="e")
        tk.Entry(details, textvariable=self.phone_var, width=15).grid(row=0, column=5, padx=5)

        # --- Main Paned Window ---
        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        # Left: Product List
        left = tk.Frame(paned, bg="#ffe4e1")
        paned.add(left, weight=3)
        tk.Label(left, text="Available Products", font=("Helvetica", 16, "bold"), bg="#ffe4e1")\
            .pack(pady=(0,5))
        canvas = tk.Canvas(left, bg="#ffe4e1", bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg="#ffe4e1")
        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=container, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        for pid, name, price in catalog:
            row = tk.Frame(container, bg="#ffe4e1", pady=2)
            row.pack(fill="x", padx=5)
            tk.Label(row, text=f"{pid}", width=3, bg="#ffe4e1").pack(side="left")
            tk.Label(row, text=name, width=20, bg="#ffe4e1").pack(side="left")
            tk.Label(row, text=f"R{price:.2f}", width=8, bg="#ffe4e1").pack(side="left")
            spin = tk.Spinbox(row, from_=1, to=100, width=5)
            spin.pack(side="left", padx=5)
            tk.Button(row, text="Add ➕", bg="#ff69b4", fg="white",
                      command=lambda pid=pid,spin=spin: self._add(pid, int(spin.get()))
            ).pack(side="left", padx=5)

        # Right: Cart
        right = tk.Frame(paned, bg="#ffe4e1")
        paned.add(right, weight=2)
        tk.Label(right, text="Your Cart", font=("Helvetica", 16, "bold"), bg="#ffe4e1")\
            .pack(pady=(0,5))
        cols = ("Name", "Qty", "Unit R", "Subtotal R")
        self.cart_tv = ttk.Treeview(right, columns=cols, show="headings", height=20)
        for c in cols:
            self.cart_tv.heading(c, text=c)
            self.cart_tv.column(c, anchor="center")
        self.cart_tv.pack(fill="both", expand=True, padx=5)
        btnf = tk.Frame(right, bg="#ffe4e1")
        btnf.pack(fill="x", pady=5, padx=5)
        tk.Button(btnf, text="🗑️ Remove Selected", bg="#ff69b4", fg="white",
                  command=self._remove).pack(side="left")
        tk.Button(btnf, text="✅ Checkout", bg="#ff69b4", fg="white",
                  command=self._checkout).pack(side="right")

        # Footer: Total (fixed height)
        footer = tk.Frame(self, bg="#ffc0cb", height=50)
        footer.grid(row=3, column=0, columnspan=2, sticky="nsew")
        footer.grid_propagate(False)
        self.total_var = tk.StringVar(value= "Total: R0.00")
        tk.Label(footer, textvariable=self.total_var, bg="#ffc0cb",
                 font=("Helvetica", 14, "bold")).pack(side="bottom", pady=5)

        # Make grid expand
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._update_cart()

    def _redraw_header(self, event):
        self.header.delete("all")
        w, h = event.width, event.height
        for i in range(h):
            ratio = i / h
            # interpolate from #ff69b4 to #ffb6c1
            r1, g1, b1 = 0xFF, 0x69, 0xB4
            r2, g2, b2 = 0xFF, 0xB6, 0xC1
            nr = int(r1 + (r2 - r1) * ratio)
            ng = int(g1 + (g2 - g1) * ratio)
            nb = int(b1 + (b2 - b1) * ratio)
            self.header.create_line(0, i, w, i, fill=f"#{nr:02x}{ng:02x}{nb:02x}")
        self.header.create_text(w // 2, h // 2,
            text="🛒 Trini’s Fancy Shopping Cart",
            font=("Helvetica", 24, "bold"), fill="white"
        )

    def _add(self, pid, qty):
        self.cart[pid] = self.cart.get(pid, 0) + qty
        self._update_cart()

    def _remove(self):
        sel = self.cart_tv.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select an item to remove.")
            return
        name = self.cart_tv.item(sel[0])["values"][0]
        pid = next(p for p, (n, _) in product_info.items() if n == name)
        del self.cart[pid]
        self._update_cart()

    def _update_cart(self):
        for i in self.cart_tv.get_children():
            self.cart_tv.delete(i)
        total = 0
        for pid, qty in self.cart.items():
            name, price = product_info[pid]
            sub = price * qty
            total += sub
            self.cart_tv.insert("", "end",
                values=(name, qty, f"R{price:.2f}", f"R{sub:.2f}")
            )
        self.total_var.set(f"Total: R{total:.2f}")

    def _checkout(self):
        name  = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        if not (name and email and phone):
            messagebox.showerror("Missing Details", "Fill Name, Email & Phone.")
            return
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Your cart is empty.")
            return
        total = sum(product_info[p][1] * q for p, q in self.cart.items())
        if messagebox.askyesno("Confirm Checkout", f"Total: R{total:.2f}\nProceed?"):
            if messagebox.askyesno("Email Receipt", f"Email receipt to {email}?"):
                messagebox.showinfo("Receipt Sent", f"Receipt emailed to {email}")
            messagebox.showinfo("Thank You", "Order placed!")
            self.cart.clear()
            self._update_cart()

if __name__ == "__main__":
    app = ShoppingCartApp()
    app.mainloop()
