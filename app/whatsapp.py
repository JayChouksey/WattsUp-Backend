# send_message.py

from fastapi import HTTPException, status, APIRouter
from models import MessageRequest, MessageResponse
import pywhatkit
import random

message = APIRouter()

# Dashboard link
link = "http://127.0.0.1:5173/dashboard"

# Fun, personalized message templates with placeholders
MESSAGES = [
    f"Hey *{{username}}*! 👋 Your *fan’s* been running like it’s auditioning for *Fast & Furious*. Maybe give it a break? 😅\n\n🔎 *Check your energy dashboard:* {link}",

    f"Yo *{{username}}*! ⚡ Your *geyser's* been partying all night. Let’s not turn your bathroom into a *hot spring*. 🌊\n\n🛠️ *Track your usage here:* {link}",

    f"Hi *{{username}}*! 👋 Your *AC’s* acting like it owns the house. Tell it to chill... just not *too* much. ❄️😂\n\n📊 *See more on your dashboard:* {link}",

    f"What’s up *{{username}}*! 💡 Using the *washing machine* for two socks? Bro… even your *WiFi* uses more sense. 🧦\n\n📈 *Peep your dashboard here:* {link}",

    f"*{{username}}* buddy! 🔌 Your *microwave* is on more than your crush is online. Might wanna take a break. 😜\n\n😂 *More hilarious insights on your dashboard:* {link}"
]

@message.post("/send-message/", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def send_whatsapp_message(request: MessageRequest):
    try:
        phone_number = request.phone_number

        # Add country code if not present
        if not phone_number.startswith("+"):
            if phone_number.startswith("91"):
                phone_number = "+" + phone_number
            else:
                phone_number = "+91" + phone_number

        # Pick and personalize message
        template = random.choice(MESSAGES)
        personalized_message = template.format(username=request.username)

        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=personalized_message,
            wait_time=request.wait_time,
            tab_close=request.close_tab
        )

        return MessageResponse(
            status="success",
            message=f"Message sent successfully to {request.phone_number}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )
