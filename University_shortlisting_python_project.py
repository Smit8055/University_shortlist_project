
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime, timedelta

class UniversityFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Finder")
        self.root.geometry("900x600")
        
        # Create the university data first
        self.universities = self.create_university_data()
        
        # Set up the interface
        self.setup_interface()

    def create_university_data(self):
        """Create and return the university database"""
        return {
            "Italy": [
                ("University of Bologna", "€2,000 - €6,000/year", "April 30, 2025"),
                ("Sapienza University of Rome", "€1,000 - €6,000/year", "July 15, 2025")
            ],
            "Germany": [
                ("Technical University of Munich", "€72-€147/semester", "May 31, 2025"),
                ("Heidelberg University", "No tuition (€171/semester fee)", "June 15, 2025")
            ],
            "USA": [
                ("Harvard University", "$54,269/year", "January 1, 2025"),
                ("Stanford University", "$58,416/year", "December 5, 2024")
            ],
            "India": [
                ("IIT Bombay", "₹2-3 lakhs/year", "March 31, 2025"),
                ("University of Delhi", "₹15,000-1.5 lakhs/year", "June 30, 2025")
            ]
        }

    def setup_interface(self):
        """Set up all the GUI components"""
        # Search frame
        search_frame = tk.LabelFrame(self.root, text="Search Options", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Country dropdown
        tk.Label(search_frame, text="Select Country:").grid(row=0, column=0, sticky="w")
        self.country_var = tk.StringVar()
        countries = list(self.universities.keys())
        country_dropdown = ttk.Combobox(search_frame, textvariable=self.country_var, values=countries, width=20)
        country_dropdown.grid(row=0, column=1, padx=5, sticky="w")
        
        # Search button
        tk.Button(search_frame, text="Search", command=self.search).grid(row=0, column=2, padx=5)
        
        # Show all button
        tk.Button(search_frame, text="Show All", command=self.show_all).grid(row=0, column=3, padx=5)
        
        # Results frame
        result_frame = tk.LabelFrame(self.root, text="Search Results", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Results treeview
        self.tree = ttk.Treeview(result_frame, columns=("Name", "Tuition", "Deadline", "Country"), show="headings")
        self.tree.heading("Name", text="University Name")
        self.tree.heading("Tuition", text="Tuition Fees")
        self.tree.heading("Deadline", text="Application Deadline")
        self.tree.heading("Country", text="Country")
        self.tree.pack(fill="both", expand=True)
        
        # Details frame
        details_frame = tk.LabelFrame(self.root, text="University Details", padx=10, pady=10)
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Details text area
        self.details_text = scrolledtext.ScrolledText(details_frame, width=80, height=8, wrap=tk.WORD)
        self.details_text.pack()
        
        # View details button
        tk.Button(result_frame, text="View Details", command=self.view_details).pack(side="left", pady=5)
        
        # Save shortlist button
        tk.Button(result_frame, text="Save Shortlist", command=self.save_shortlist).pack(side="right", pady=5)

    def search(self):
        """Search universities by selected country"""
        country = self.country_var.get()
        if not country:
            messagebox.showwarning("Warning", "Please select a country first")
            return
        
        self.show_universities(country)

    def show_all(self):
        """Show all universities from all countries"""
        self.tree.delete(*self.tree.get_children())
        for country, unis in self.universities.items():
            for uni in unis:
                self.tree.insert("", "end", values=(uni[0], uni[1], uni[2], country))
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Showing all {len(self.tree.get_children())} universities")

    def show_universities(self, country):
        """Display universities for a specific country"""
        self.tree.delete(*self.tree.get_children())
        if country in self.universities:
            for uni in self.universities[country]:
                self.tree.insert("", "end", values=(uni[0], uni[1], uni[2], country))
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Showing universities in {country}")

    def view_details(self):
        """Show details of selected university"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a university first")
            return
        
        item = self.tree.item(selected[0])
        name, tuition, deadline, country = item['values']
        
        self.details_text.delete(1.0, tk.END)
        details = f"""University: {name}
Country: {country}
Tuition: {tuition}
Deadline: {deadline}

Application Timeline:
- Start research: {self.calculate_timeline(deadline, -180)}
- Prepare documents: {self.calculate_timeline(deadline, -90)}
- Submit application: {self.calculate_timeline(deadline, -30)}
- Final deadline: {deadline}"""
        
        self.details_text.insert(tk.END, details)

    def calculate_timeline(self, deadline, days_before):
        """Calculate dates before deadline"""
        try:
            deadline_date = datetime.strptime(deadline, "%B %d, %Y")
            return (deadline_date + timedelta(days=days_before)).strftime("%B %d, %Y")
        except:
            return f"{abs(days_before)} days before deadline"

    def save_shortlist(self):
        """Save selected universities to a text file"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select universities to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="my_university_shortlist.txt"
        )
        
        if not file_path:
            return
        
        with open(file_path, "w") as f:
            f.write("MY UNIVERSITY SHORTLIST\n")
            f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            for i, item_id in enumerate(selected, 1):
                uni = self.tree.item(item_id)['values']
                f.write(f"{i}. {uni[0]} ({uni[3]})\n")
                f.write(f"   Tuition: {uni[1]}\n")
                f.write(f"   Deadline: {uni[2]}\n\n")
            
            f.write("Good luck with your applications!\n")
        
        messagebox.showinfo("Success", f"Shortlist saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityFinderApp(root)
    root.mainloop()