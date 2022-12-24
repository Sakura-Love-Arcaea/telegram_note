import glob
import os
import re
from telegram.ext import *
home = {'home': '/Users/lvjiayao/PycharmProjects/SakuraLoveArcaea_bot_2',
        'L': '/Users/lvjiayao/PycharmProjects/Live_Fast_Die_Young'}

TOKEN = '1716258797:AAF0GwTDIBJdBzC4rllxvypkJrx6GMd44OU'

def test(update):
    print(update.message.text, 'by:', update.message.chat.username)
    with open('recode.txt', 'at') as txt:
        print(update.message.text, 'by:', update.message.chat.username, file=txt)


def read_(update, folder=os.getcwd()):
    if folder != os.getcwd():
        os.chdir(folder)
    with open('text.txt', 'rt', encoding='utf-8') as txt:
        fin = txt.read()
        update.message.reply_text(fin)









def help(update, context):
    test(update)

    update.message.reply_text('{:*^42}\n'
                              '/have -> 有沒有這個文件（對，暫時沒什麼用，因為我不會開文件）\n'
                              '/jump -> 沒有指定資料夾的話會告訴你現在在哪裡，否則跳去指定資料夾\n'
                              '/read -> 讀取當前資料夾裡面\'text.txt\'的內容， 可以指定哪一個資料夾的\n'
                              '/note -> 寫入並告訴你寫入了什麼， 如果內容是clear，則幫你清除裡面的東西\n'
                              '{:*^42}'.format('', ''))


def note(update, context):
    test(update)
    if len(context.args) == 0:
        update.message.reply_text('請東西或者輸入/note clear進行清除喔')
        return

    if context.args[0] == 'clear':
        with open('text.txt', 'wt') as txt:
            txt.write('')
            update.message.reply_text('檔案已經清除')
        return
    with open('text.txt', 'at') as txt:
        for i in context.args:
            print(i, file=txt)
    read_(update)


def read(update, context):
    test(update)
    if len(context.args) != 0:
        if context.args[0] in home.keys():
            read_(update, folder=home[context.args[0]])
        else:
            update.message.reply_text('資料夾不存在')
    else:
        read_(update)






def jump(update, context):
    test(update)
    if len(context.args) != 0:
        print('當前位置：', os.getcwd())
        update.message.reply_text('當前位置：' + str(os.getcwd()))

        try:
            os.chdir(home[context.args[0]])
            update.message.reply_text('已經跳去：' + str(os.getcwd()))
        except:
            update.message.reply_text('沒有這個預設位置喔')
    else:
        update.message.reply_text('當前位置：' + str(os.getcwd()))


def have(update, context):
    test(update)
    if len(context.args) == 0:
        update.message.reply_text('請在後面輸入文件名字，不輸入的話就像現在，把本資料夾符合.txt的給你看\n（指定資料夾的指定檔案還沒做，預設在本資料夾找）')
        text = ''
        update.message.reply_text(os.getcwd())
        update.message.reply_text(glob.glob('*.txt'))
        return

    if context.args[0] in os.listdir(os.getcwd()):
        update.message.reply_text('有喔')
    else:
        update.message.reply_text('沒有喔')


def reply(update, context):
    user_input = update.message.text
    if re.findall('屌|on9|戇鳩|撚|傻閪', user_input):
        update.message.reply_text('講乜撚嘢粗口啊屌你')
    if re.findall('讓我看看', user_input):
        update.message.reply_text(f'不要啊{update.message.chat.username}哥')
    test(update)


bot = Updater(token=TOKEN, use_context=True)
disp = bot.dispatcher

disp.add_handler(CommandHandler("help", help))
disp.add_handler(CommandHandler("jump", jump))
disp.add_handler(CommandHandler("read", read))
disp.add_handler(CommandHandler("note", note))
disp.add_handler(CommandHandler("have", have))
disp.add_handler(MessageHandler(Filters.text, reply))
bot.start_polling()
bot.idle()
