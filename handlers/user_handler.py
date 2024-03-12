from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

# import pytz
import datetime
import logging
from config_data.config import Config, load_config
from keyboards.user_keyboard import keyboards_start, keyboards_question1, keyboards_question2, keyboards_question3,\
    keyboards_question4
# from services.googlesheets import append_user, append_client
import asyncio
# import requests

router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    get_name = State()
    get_phone = State()
    info_user = State()


user_dict = {}
recomendation_dict ={
    '1А': 'Если из-за работы вы постоянно засиживаетесь допоздна, поменяйте температуру света монитора'
          ' с синего на желтый. Если вы обычно просыпаетесь под будильник на смартфоне, этот шаг поможет'
          ' убрать устройство из кровати. Подойдет как обычный механический, так и радио- или световой'
          ' будильник.',
    '2А': 'Перед сном не следует употреблять жирную и жареную пищу. Она будет долго перевариваться и создаст'
          ' ощущение тяжести в желудке. Откажитесь от крепкого чая и кофе. Они возбуждают нервную систему'
          ' и влияют на качество сна. Также исключите из рациона полуфабрикаты, колбасы и красное мясо,'
          ' соленую рыбу. Любителей сладостей также спешим расстроить: шоколад и любые другие сладкие блюда'
          ' не должны быть в ночном рационе.\n'
          'Продукты, которые можно употреблять перед сном:\n'
          '-Кефир и творог(порция нем больше 200-250г)\n'
          '-Тёплое молоко\n'
          '-Яйца всмятку(не больше двух)\n'
          '-Грейпфрут\n'
          '-Котлета из индейки или курицы\n'
          '-Авокадо\n'
          '-Орехи\n'
          '-Сыр тофу',
    '3B': 'Специалисты не советуют решать проблемы со сном с помощью белого шума — только если при засыпании'
          ' присутствуют посторонние звуки, которые необходимо заглушить. Громкий шепот в тишине, пение птиц,'
          ' шум городской жизни, слышимый за закрытыми окнами ≈ 30-40 дБ. Возможно нарушение сна, движение во'
          ' сне или пробуждение. Наиболее чутко реагируют пожилые люди и маленькие дети.',
    '3C': 'Постарайтесь отказаться от звуков вообще,а если из-за привычки не получается,постепенно снижайте'
          ' громкость до минимума.',
    '4A': 'Сон с пробуждением вреден,поэтом вот несколько советом, чтобы предотвратить эту проблему:\n'
          '-Не ешьте прямо перед тем, как ложиться спать.\n'
          '-Позанимайтесь расслабляющей йогой.\n'
          '-Проветрите комнату.\n'
          '-Спрячьте часы, чтобы не смотреть на них, пока пытаетесь заснуть.\n'
          '-Уберите телефон подальше от кровати.\n'
          '-Перед сном примите горячий душ или ванну.\n'
          '-Спите в носках.',
    '4B': 'Если вы не просыпаетесь ночью, то это говорит о здоровом сне.',
    '1B 2B 3A 4B': 'Основные факторы, влияющие на качество сна в норме. Если вы чувствуете какие-то проблемы со сном,'
                   ' то следует обратиться к специалисту(невролог)'
}


def get_telegram_user(user_id, bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getChat'
    data = {'chat_id': user_id}
    response = requests.post(url, data=data)
    print(response.json())
    return response.json()


@router.message(CommandStart())
async def process_start_command_user(message: Message) -> None:
    logging.info(f'process_start_command_user: {message.chat.id}')
    await message.answer(text=f'Привет!Это бот, который поможет разобраться с тем, какое у тебя качество сна,'
                              f' а так же даст рекомендации для его улучшения.Единственное, что тебе нужно'
                              f' - пройти короткий опрос(отвечай на все вопросы максимально честно,от этого'
                              f' зависит результат), после чего бот выдаст тебе результат на основании твоих ответов.',
                         reply_markup=keyboards_start())


@router.message(F.text == 'Опрос')
async def press_button_the_survey(message: Message) -> None:
    logging.info(f'press_button_the_survey: {message.chat.id}')
    await message.answer(text=f'1. Отказываетесь ли вы  от гаджетов перед сном?',
                         reply_markup=keyboards_question1())


@router.callback_query(F.data.startswith('question1'))
async def question_two(callback: CallbackQuery, state: FSMContext):
    logging.info(f'question_two: {callback.message.chat.id}')

    await state.update_data(survey=[callback.data.split('_')[1]])

    await callback.message.answer(text=f'2. Принимаете ли вы пищу перед сном?',
                                  reply_markup=keyboards_question2())


@router.callback_query(F.data.startswith('question2'))
async def question_three(callback: CallbackQuery, state: FSMContext):
    logging.info(f'question_three: {callback.message.chat.id}')

    user_dict[callback.message.chat.id] = await state.get_data()
    survey_list = user_dict[callback.message.chat.id]['survey']
    survey_list.append(callback.data.split('_')[1])
    await state.update_data(survey=survey_list)

    await callback.message.answer(text=f'3 Достаточно ли тихо у вас в комнате вот время сна?',
                                  reply_markup=keyboards_question3())


@router.callback_query(F.data.startswith('question3'))
async def question_four(callback: CallbackQuery, state: FSMContext):
    logging.info(f'question_three: {callback.message.chat.id}')

    user_dict[callback.message.chat.id] = await state.get_data()
    survey_list = user_dict[callback.message.chat.id]['survey']
    survey_list.append(callback.data.split('_')[1])
    await state.update_data(survey=survey_list)

    await callback.message.answer(text=f'4 Часто ли вы просыпаетесь во время сна?',
                                  reply_markup=keyboards_question4())


@router.callback_query(F.data.startswith('question4'))
async def question_finish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'question_finish: {callback.message.chat.id}')

    user_dict[callback.message.chat.id] = await state.get_data()
    survey_list = user_dict[callback.message.chat.id]['survey']
    survey_list.append(callback.data.split('_')[1])
    print(survey_list)

    await callback.message.answer(text=f'<b>Советы для улучшения вашего качества сна!</b>',
                                  parse_mode='html')
    for serv in survey_list:
        if serv in recomendation_dict:
            await callback.message.answer(text=f'{recomendation_dict[serv]}',
                                          parse_mode='html')
    if ' '.join(survey_list) == '1B 2B 3A 4B':
        await callback.message.answer(text=f'{recomendation_dict["1B 2B 3A 4B"]}',
                                      parse_mode='html')


