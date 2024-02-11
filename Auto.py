import os
import pandas as pd
from openpyxl import load_workbook
import win32com.client as win32
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to read all Excel files in a folder and apply column filtration
def process_excel_files(folder_path):
    # Initialize an empty master DataFrame
    master_df = pd.DataFrame()

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Apply column filtration to create a sub DataFrame
            sub_df = df[['Column1', 'Column2', 'Column3']]  # Replace with your column names

            # Concatenate the sub DataFrame to the master DataFrame
            master_df = pd.concat([master_df, sub_df], ignore_index=True)

    return master_df

# Function to write DataFrame to an existing Excel template and refresh pivot table
def write_to_excel(df, template_path):
    # Load the Excel template
    workbook = load_workbook(template_path)

    # Access the first sheet (assuming the pivot table is in the first sheet)
    sheet = workbook.active

    # Write DataFrame to Excel starting from cell A2
    for r in dataframe_to_rows(df, index=False, header=True):
        sheet.append(r)

    # Refresh pivot table
    workbook.refresh_pivot_tables()

    # Save changes to the Excel file
    workbook.save(template_path)

# Function to take a screenshot of the pivot table in the Excel file
def take_screenshot(template_path, screenshot_path):
    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(template_path)
    ws = wb.Sheets(1)  # Assuming pivot table is in the first sheet

    # Take a screenshot of the pivot table
    ws.Shapes("PivotTable1").Copy()

    # Paste the screenshot into a new Excel instance
    wb2 = excel.Workbooks.Add()
    ws2 = wb2.Sheets(1)
    ws2.Paste()

    # Save the screenshot as an image
    ws2.Shapes(1).CopyPicture()

    # Paste the image into Paint and save it
    paint = win32.Dispatch('Paint.Application')
    paint.ActiveDocument.Open()
    paint.ActiveDocument.Selection.Paste()
    paint.ActiveDocument.SaveAs(screenshot_path)

    # Close all instances of Excel and Paint
    wb.Close(False)
    wb2.Close(False)
    excel.Quit()
    paint.Application.Quit()

# Function to compose and send email with attachments
def send_email(sender_email, sender_password, receiver_emails, attachment_paths):
    # Create a multipart message
    msg = MIMEMultipart()

    # Set email parameters
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = 'Excel Automation Report ' + datetime.now().strftime("%Y-%m-%d")

    # Add message body
    body = "Please find attached the Excel automation report."
    msg.attach(MIMEText(body, 'plain'))

    # Add attachments
    for attachment_path in attachment_paths:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + os.path.basename(attachment_path))
        msg.attach(part)

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_emails, text)
    server.quit()

# Main function
def main():
    # Initialize Tkinter
    root = tk.Tk()
    root.title("Excel Automation")

    # Function to handle folder selection
    def select_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_var.set(folder_path)

    # Function to handle template selection
    def select_template():
        template_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if template_path:
            template_var.set(template_path)

    # Function to handle email sending
    def send_email_command():
        try:
            # Process Excel files and create master DataFrame
            master_df = process_excel_files(folder_var.get())

            # Write master DataFrame to Excel template and refresh pivot table
            write_to_excel(master_df, template_var.get())

            # Take screenshot of pivot table
            screenshot_path = os.path.join(output_var.get(), 'pivot_table_screenshot.png')
            take_screenshot(template_var.get(), screenshot_path)

            # Save master DataFrame to CSV
            csv_path = os.path.join(output_var.get(), 'master_dataframe.csv')
            master_df.to_csv(csv_path, index=False)

            # Send email with attachments
            attachment_paths = [template_var.get(), csv_path, screenshot_path]
            send_email(sender_var.get(), password_var.get(), receiver_var.get().split(','), attachment_paths)

            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create and place widgets
    folder_label = tk.Label(root, text="Folder Path:")
    folder_label.grid(row=0, column=0, padx=5, pady=5)
    folder_var = tk.StringVar()
    folder_entry = tk.Entry(root, textvariable=folder_var)
    folder_entry.grid(row=0, column=1, padx=5, pady=5)
    folder_button = tk.Button(root, text="Select Folder", command=select_folder)
    folder_button.grid(row=0, column=2, padx=5, pady=5)

    template_label = tk.Label(root, text="Template Path:")
    template_label.grid(row=1, column=0, padx=5, pady=5)
    template_var = tk.StringVar()
    template_entry = tk.Entry(root, textvariable=template_var)
    template_entry.grid(row=1, column=1, padx=5, pady=5)
    template_button = tk.Button(root, text="Select Template", command=select_template)
    template_button.grid(row=1, column=2, padx=5, pady=5)

    sender_label = tk.Label(root, text="Sender Email:")
    sender_label.grid(row=2, column=0, padx=5, pady=5)
    sender_var = tk.StringVar()
    sender_entry = tk.Entry(root, textvariable=sender_var)
    sender_entry.grid(row=2, column=1, padx=5, pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=3, column=0, padx=5, pady=5)
    password_var = tk.StringVar()
    password_entry = tk.Entry(root, textvariable=password_var, show="*")
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    receiver_label = tk.Label(root, text="Receiver Emails (comma-separated):")
    receiver_label.grid(row=4, column=0, padx=5, pady=5)
    receiver_var = tk.StringVar()
    receiver_entry = tk.Entry(root, textvariable=receiver_var)
    receiver_entry.grid(row=4, column=1, padx=5, pady=5)

    output_label = tk.Label(root, text="Output Folder:")
    output_label.grid(row=5, column=0, padx=5, pady=5)
    output_var = tk.StringVar()
    output_entry = tk.Entry(root, textvariable=output_var)
    output_entry.grid(row=5, column=1, padx=5, pady=5)

    send_button = tk.Button(root, text="Send Email", command=send_email_command)
    send_button.grid(row=6, column=1, padx=5, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

