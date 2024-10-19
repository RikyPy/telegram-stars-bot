from telethon import TelegramClient, events, types, functions
from telethon.tl.custom import Message
from telethon.tl.types import User
from telethon.errors.rpcbaseerrors import BadRequestError
from config import API_ID, API_HASH, BOT_TOKEN

client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.Raw(types.UpdateBotPrecheckoutQuery))
async def payment_pre_checkout_handler(e: types.UpdateBotPrecheckoutQuery):
    if e.payload.decode('UTF-8').startswith('Stars Payment'):
        await client(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=e.query_id,
                success=True,
                error=None
            )
        )
    else:
        await client(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=e.query_id,
                success=False,
                error='Error!'
            )
        )

    raise events.StopPropagation


@client.on(events.Raw(types.UpdateNewMessage))
async def payment_received_handler(e):
    if isinstance(e.message.action, types.MessageActionPaymentSentMe):
        payment: types.MessageActionPaymentSentMe = e.message.action
        if payment.payload.decode('UTF-8').startswith('Stars Payment'):
            userid = e.message.peer_id.user_id
            data = payment.payload.decode('UTF-8')
            amount = data[16:]
            print(f"Payment of {amount} Stars from {userid}")
        raise events.StopPropagation

def card(price_label: str, price_amount: int, currency: str, title: str,
                     description: str, payload: str, start_param: str) -> types.InputMediaInvoice:
    price = types.LabeledPrice(label=price_label, amount=price_amount)
    invoice = types.Invoice(
        currency=currency,
        prices=[price],
        name_requested=False,
        phone_requested=False,
        email_requested=False,
        shipping_address_requested=False,
        flexible=False,
        phone_to_provider=False,
        email_to_provider=False
    )
    return types.InputMediaInvoice(
        title=title,
        description=description,
        invoice=invoice,
        payload=payload.encode('UTF-8'),

        provider_data=types.DataJSON('{}'),

        start_param=start_param,

)

print("Online")

@client.on(events.NewMessage())
async def message(e: Message):
    client.parse_mode = 'html'
    sender: User = await e.get_sender()
    stars = 1

    if e.text == "/start":
        await e.respond(f"Hey {sender.first_name}!")
    elif e.text == "/invoice":
        await client.send_message(
            e.chat_id,
            file=card(
                price_label='Stars Payment', price_amount=stars, currency='XTR', title='Stars Payment',
                description=f'Stars Payment of {stars} Star',
                payload=f'Stars Payment - {stars}', start_param='abc'
            )
        )
    elif e.text.startswith("/refund"):
        args = e.text.split(' ')
        if len(args) != 2:
            await e.respond("Transaction id not found")
        else:
            try:
                result = await client(
                    functions.payments.RefundStarsChargeRequest(
                        user_id=sender.id,
                        charge_id=args[1]
                    )
                )
                await e.respond(f"Sucessfully refunded")
            except BadRequestError as exc:
                if exc.message == "CHARGE_ALREADY_REFUNDED":
                    await e.respond("This transaction was already refunded!")
                elif exc.message == "CHARGE_NOT_FOUND":
                    await e.respond("This transaction dosen't exists!")
                else:
                    print(exc)
                    await e.respond("There was an error while processing your refund. Please try again!")

client.run_until_disconnected()