from fastapi import APIRouter, Request, BackgroundTasks
import smtplib
from email.mime.text import MIMEText

router = APIRouter()

@router.post("/contact")
async def contact_us(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    name = data.get("name", "")
    email = data.get("email", "")
    message = data.get("message", "")
    subject = f"פנייה חדשה מהאתר AquaSafe"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    recipients = ["noa4000@gmail.com", "lihicohen122@gmail.com"]
    def send_email(name, email, message):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = email
        msg["To"] = ", ".join(recipients)
        try:
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login("aquasafehelp@outlook.co.il", "AU5UV-5N7DX-8PHBW-BMSQA-369PY")
                server.sendmail(email, recipients, msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")
    background_tasks.add_task(send_email, name, email, message)
    return {"message": "Message sent"}
