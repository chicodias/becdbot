from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from pendulum import today, datetime, now
import random
import os
import argparse

LINK_GRUPO = os.getenv('LINK_GRUPO')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Já em funcionamento.")


def fwd(update, context):
    is_reply = update.message.reply_to_message
    fwd_name = '@becdbotfwd'
    
    if is_reply:  # encaminha para o fwd
        context.bot.forwardMessage(fwd_name, update.effective_chat.id, is_reply.message_id)
    else:  # encaminha para o grupo
        max_id = 10
        max_tries = max_id*5
        tries = 0
        while True:
            message_id = random.randint(0, max_id)
            try:
                if tries <= max_tries: 
                    context.bot.forwardMessage(update.effective_chat.id, fwd_name, message_id)
                    break
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Ai cansei aqui, manda de novo...")
            except:
                pass 


def aulas(update, context):
    
    hoje = today('America/Sao_Paulo')
    aulas = datetime(2021, 8, 16)
    diff = aulas.diff(hoje).in_days()
    
    if hoje < aulas:
        frases = [
            'Caalma, caraio. As aulas vão começar em',
            'Porra, bixo. As aulas começam em',
            'Infelizmente já teremos aulas em',
            'Poorrraaaa, não me lembra que as aulas começam em'
        ]
        frase = random.choice(frases)
        msg = f'{frase} {diff} dias'
    
    elif hoje > aulas:
        msg = "Infelizmente, as aulas já começaram. Manda /semestre pra saber quando o semestre vai dar a folguinha."

    else:
        msg = "É hj que começa tudo de novo pohaaAaaAa fodeu :'("
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def semestre(update, context):
    hoje = today('America/Sao_Paulo')
    # mini ferias
    aulas = datetime(2021, 12, 21)
    diff = aulas.diff(hoje).in_days()
    # ferias ferias
    aulas2 = datetime(2022, 1, 14)
    diff2 = aulas2.diff(hoje).in_days()
    
    volta = datetime(2021, 8, 17)
    if hoje >= volta:
        frases = [
            'Por favor, eu não aguento mais {} dias. Até o fim em janeiro, {} dias.',
            'Tenhamos fé, ainda faltam {} dias para o recesso, e {} dias para o fim de tudo',
            'Sinto muito em lhe informar que restam {} dias para as mini férias, e {} dias para o término do semestre',
            'Desculpe, faltam {} dias para o final do semestre este ano e mais {} dias pro final real oficial'
        ]
        frase = random.choice(frases)
        msg = frase.format(diff, diff2)

    else:
        msg = "De alguma maneira, as aulas ainda não começaram. Manda /aulas pra saber quando elas voltarão."
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def maquera(update, context):
    context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id='@becdbotfwd', message_id=2)


def trancar(update, context):
    if random.random() < 0.2:
        txt = "Desculpe, não tá rolando trancar o curso não."
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        return
    else:
        txt = "Vamos iniciar seu processo de trancamento!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

        l = [
            "Enviando emojis ofensivos para a grad...",
            "Passando trote para a PPUSP...",
            "Devolvendo bandeija com restos de comida...",
            "Ligando para a Cibele...",
            "Avisando o governador...",
            "Denunciando a turma por cola...",
            "Chamando engenheiros de Cientistas de Dados....",
            "Usando drogas na universidade....",
            "Incendiando empréstimos da biblioteca...",
            "Falando que estuda na federal...",
            "Instalando Microsoft Excel...",
            "Fechando a comanda no Podrão...."
        ]

        while True:
            if random.random() < 0.80:
                if len(l) > 0:
                    x = random.choice(l)
                    l.remove(x)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=x)
                else:
                    try:
                        mins = 3
                        date_unban = now().add(minutes=mins).int_timestamp
                        txt = "Tudo bem, concluindo trancamento..."
                        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
                        txt = """[@{}](tg://user?id={}) conseguiu trancar o curso e foi embora!
                        """.format(update.effective_user.first_name, update.effective_user.id)
                        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
                        
                        msg = f"Trancamento concluído, haha. Aguarda {mins} minutos e entra no grupo novamente: {LINK_GRUPO}"
                        
                        context.bot.kick_chat_member(chat_id=update.effective_chat.id,
                                                    user_id=update.effective_user.id,
                                                    until_date=date_unban)
                        context.bot.send_message(chat_id=update.effective_user.id, text=msg)
                    except:
                        print("Não foi possível trancar o curso")
                    return
            else:
                txt = "Lamento, seu trancamento falhou."
                context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
                break

def feriado(update, context):
    feriados = holidays.CountryHoliday('BRA', prov=None, state='SP', years = date.today().year)
    weekDays = ("segunda. Tá safe!",
            "terça. Bora emendar clan!!1!",
            "quarta, bem no meio da semana...",
            "quinta. E vamos de emenda fml!!",
            "sexta. Feriadou!",
            "sabado. Sem palavras para essa atrocidade.",
            "domingo. Do que adianta um feriado num domingo?")

    proximos = list(filter(lambda data: data > date.today(), feriados.keys()))
    if len(proximos) > 0:
        txt = f"Proximo feriado dia{proximos[0].day}/{proximos[0].month} cai numa {weekDays[date.weekday(proximos[0])]}"
    else:
        txt = "Sem mais feriados este ano, foi mal."
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)


def send_welcome(update, context, new_member):
    welcome_message = """Bem-vinde, [@{}](tg://user?id={})!
    """.format(new_member.first_name, new_member.id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_message,
                             parse_mode='Markdown')


def empty_message(update, context):
    """
        Handles empty messages:
            - User enters the group
            - User leaves the group
    """
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            # Bot added to group
            if new_member.username != 'becdbot':
                return send_welcome(update, context, new_member)


if __name__ == '__main__':

    appname = 'becdbot'
    parser = argparse.ArgumentParser(description='BECD Bot')
    parser.add_argument('--local',
                        dest='is_local',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Local run')
    args = parser.parse_args()
    BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
    
    updater = Updater(token=BOT_API_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('aulas', aulas))
    dp.add_handler(CommandHandler('maquera', maquera))
    dp.add_handler(CommandHandler('fwd', fwd))
    dp.add_handler(CommandHandler('semestre', semestre))
    dp.add_handler(CommandHandler('trancar', trancar))
    dp.add_handler(MessageHandler(Filters.status_update, empty_message))

    if not args.is_local:
        PORT = os.getenv('PORT')

        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=BOT_API_TOKEN,
                              webhook_url=f"https://{appname}.herokuapp.com/{BOT_API_TOKEN}"
                              )
    else:
        updater.start_polling()

    updater.idle()
