#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Don't forget to enable inline mode with @BotFather
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

#https://pastebin.com/raw/VsmWHrLe
import random, logging, pycurl, os
from dotenv import load_dotenv
from io import BytesIO 
load_dotenv()

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class Exception404(Exception):
    pass

def leurl(ur: str):
    a_obj = BytesIO() 
    rl = pycurl.Curl()
    rl.setopt(pycurl.SSL_VERIFYPEER, 0)   
    rl.setopt(pycurl.SSL_VERIFYHOST, 0)
    rl.setopt(pycurl.URL, ur)
    rl.setopt(rl.WRITEDATA, a_obj)
    rl.perform()
    if rl.getinfo(pycurl.HTTP_CODE) == 404:
        raise Exception404
    rl.close()
    return a_obj.getvalue()


def popula(rl: str):
        
        try:
            saida = leurl(rl)
        except(Exception404):
            raise Exception404
        if len(saida) == 0:
            return
        cita8=saida.decode("utf-8")
        
        global lc,pc
        lc = {}
        pc = []
        citacoes = cita8.split("\n")
        for cita in citacoes:
            separa = cita.split(":")
            citada = separa[1].split("#")
            texto = citada[1]
            pcs = citada[0].split(";")
            autor = separa[0]
            if autor in lc:
                for chiave in pcs:
                    if chiave in lc[autor]:
                        lc[autor][chiave].append(texto)
                    else:
                        lc[autor][chiave] = {}
                        lc[autor][chiave].append(texto)
            else:
                lc[autor] = {}
                for chiave in pcs:
                    lc[autor][chiave] = []
                    lc[autor][chiave].append(texto)
        for aut in lc.keys():
            for palavras in lc[aut].keys():
                pc.append([aut, palavras])


# Define a few command handlers. These usually take the two arguments update and
# context.


async def rele(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    try:
        update.message.edit_date
    except AttributeError:
            return
    try:
        popula(update.message.text.replace("/rele","").strip())
        await update.message.reply_text("Releitura com sucesso!")
    except Exception404:
        await update.message.reply_text("Falha na releitura!")
    


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    try:
        update.message.edit_date
    except AttributeError:
            return
    possibs = []
    citaut = [] 
    for chav in pc:
        if chav[1].lower() in update.message.text.lower().split(): #falou alguma palavra-chave
            for aut in lc.keys():
                if chav[1] in lc[aut].keys():
                    possibs.append([aut,chav[1]])#guarda todos os autores que citaram a palavra
    for autor in lc.keys():
        if autor in update.message.text.split(): #falou algum autor
            citaut.append(autor)
    #limpeza de autores nao citados (caso algum)
    if len(citaut) > 0:
        for possib in possibs:
            if possib[0] not in citaut:
                possibs.pop(possib)
    if len(possibs) > 0:
        pick = possibs[random.randrange(len(possibs))]
        frase = lc[pick[0]][pick[1]][random.randrange(len(lc[pick[0]][pick[1]]))]
        citacoes = []
        for possib in possibs:
            citacoes.append(possib[1].lower())
        for entrada in update.message.text.split():
                if entrada.lower() in citacoes:
                    frase = frase.replace(entrada.casefold(),"<b>"+entrada+"</b>")
        if len(citaut) > 0:
            pick[0]=pick[0].replace(pick[0],"<b>"+pick[0]+"</b>")
        await update.message.reply_text(f"<i>\""+frase+"\"</i>"+" - "+pick[0], parse_mode=ParseMode.HTML)

def main() -> None:
    """Run the bot."""
    try:
        popula("https://pastebin.com/raw/VsmWHrLe")
    except IOError:
        logger.log(1,"Erro de leitura")
    
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["BOT_TOKEN"]).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("rele", rele))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
        
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
