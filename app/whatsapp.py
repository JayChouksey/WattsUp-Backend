from fastapi import FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel
import pywhatkit
import time
from typing import Optional
from models import MessageRequest, MessageResponse

message = APIRouter()

@message.post("/send-message/", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def send_whatsapp_message(request: MessageRequest):
    try:
        phone_number = request.phone_number
        if not request.phone_number.startswith("+"):
            if phone_number.startswith("91"):
                phone_number = "+" + phone_number
            else:
                phone_number = "+91" + phone_number
        
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=request.message,
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
