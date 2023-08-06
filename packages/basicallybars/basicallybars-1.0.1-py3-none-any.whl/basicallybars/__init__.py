import math

def lib_get_bar(parsed, full_amount, starts_with, ends_with, quantity_display):
    percent = math.floor(100 * float(parsed)/float(full_amount))
    output = f"[{starts_with}"
    i = 0
    for i in range(1, math.floor(percent/10)+1):
        output = f"{output}="
    for x in range(i, 10):
        output = f"{output} "
    
    if type == "large":
        return f"{output}{ends_with}| {lib_display_quantity(quantity_display, parsed, full_amount)}\n|----------|"
    else:
        return f"{output}{ends_with}] {lib_display_quantity(quantity_display, parsed, full_amount)}"

def lib_display_quantity(mode, parsed, full_amount):
    mode = mode.lower()

    if mode not in ("amount", "percent", "remaining"):
        mode = "amount"

    if mode == "amount":
        return(f" ({parsed}/{full_amount})")
    elif mode == "percent":
        return(f" {math.floor(100 * float(parsed)/float(full_amount))}%")
    elif mode == "remaining":
        return(f" {full_amount-parsed} remaining...")

class progressbar:
    """Creates a new progress bar."""
    def __init__(self, quantity_display="Amount", title="New bar:", starts_with="", ends_with=""):
        self.starts_with = starts_with
        self.ends_with = ends_with
        self.quantity_display = quantity_display
        self.title = title

        self.title_displayed = False
        self.final_call = 0 # 0 means it hasnt reached its goal, 1 means it has but no notif and 2 means notif is done
        
    def display(self, parsed, full_amount):
        """Display/update the progress bar and its progress."""
        if not self.title_displayed and self.title:
            self.title_displayed = True
            print(f"{self.title}")

        if parsed < full_amount:
            print(lib_get_bar(parsed, full_amount, self.starts_with, self.ends_with, self.quantity_display), end='\r', flush=True)
        elif self.final_call == 0:
            print(lib_get_bar(parsed, full_amount, self.starts_with, self.ends_with, self.quantity_display))
            self.final_call = 1

        elif self.final_call == 1:
            print(f"You are calling .display(), even though your bar is finished. ({parsed}/{full_amount})")
            self.final_call = 2
