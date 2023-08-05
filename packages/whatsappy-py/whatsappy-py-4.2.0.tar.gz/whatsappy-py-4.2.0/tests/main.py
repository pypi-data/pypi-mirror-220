from whatsappy import Whatsapp

whatsapp = Whatsapp(data_path="C:\\Whatsappy", visible=True)

@whatsapp.event
def on_ready() -> None:
    print("WhatsApp Web está pronto!")

whatsapp.run()

group = whatsapp.open("vou levar 2 de anderson")

group.promote("Douglas")

whatsapp.close()