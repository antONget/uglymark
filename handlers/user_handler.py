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


# def get_telegram_user(user_id, bot_token):
#     url = f'https://api.telegram.org/bot{bot_token}/getChat'
#     data = {'chat_id': user_id}
#     response = requests.post(url, data=data)
#     print(response.json())
#     return response.json()


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
async def question_finish(callback: CallbackQuery, state: FSMContext, bot: Bot):
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
    await bot.send_message(chat_id=949984586,
                           text=f'Пользователь {callback.message.from_user.username}\n'
                                f'прошел опрос - {" ".join(survey_list)}')


@router.message(F.text == 'Рекомендации')
async def press_button_recomendation(message: Message) -> None:
    logging.info(f'press_button_recomendation: {message.chat.id}')
    # 1
    await message.answer(text=f'<blockquote>Правило №1. Режим сна:</blockquote>\n'
                              f'Главное, о чем стоит всегда помнить – это режим, и он должен быть во всем. Согласитесь,'
                              f' если вы ходите в тренажерный зал по три раза в неделю несколько месяцев подряд,'
                              f' то и четвертый раз позаниматься на тренажерах для вас не составит труда. А вот если'
                              f' пропустить хотя бы одну тренировку, то и ноги не бегут, и колени не так легко'
                              f' приседают. С чем это связано? Наш организм – это механизм, и работать он должен как'
                              f' часы, а если одна стрелка часов не двигается, то и остальные будут стоять на месте.'
                              f' Да, первое время, это трудно, но старайтесь ложиться спать и просыпаться всегда в'
                              f' одно и то же время. И даже на выходных, особенно на выходных! Поспав лишние два часа'
                              f' в субботу, вы оказали для своего организма такой же стресс, как если бы преодолели'
                              f' два часовых пояса. По причине того, что вы поздно засыпаете и просыпаетесь в выходные,'
                              f' в воскресенье вам трудно уснуть, а утром в понедельник вы совсем разбиты.',
                         parse_mode='html')
    # 2
    await message.answer(text=f'<blockquote>Правило №2. Физическая активность:</blockquote>\n'
                              f'Для качественного не только сна, но и для жизни в целом, нужно быть активным.'
                              f' Чтобы сон наступал быстрее, важно быть достаточно подвижным в течение всего дня.'
                              f' Человек ест пищу, благодаря этому в организм поступает энергия, а любая энергия'
                              f' должна иметь выход. И мы сейчас не призываем вас начать готовиться к марафону,'
                              f' что на самом деле неплохо, но попробуйте иногда отказываться от лифта и автомобиля,'
                              f' делайте 5-10 приседаний утром, а перед сном прогуляйтесь около дома. Поверьте,'
                              f' так вы начнете засыпать намного быстрее.',
                         parse_mode='html')
    # 3
    await message.answer(text=f'<blockquote>Правило №3. Питание:</blockquote>\n'
                              f'Кажется, информация об этом звучала из каждого утюга, но для тех, кто пропустил,'
                              f' повторяем: последний прием пищи должен быть за 3-4 часа до сна. И постарайтесь'
                              f' не переедать: во время сна организм должен отдыхать, а не тратить силы на'
                              f' переваривание бабушкиных пирожков, хотя, согласимся, они очень вкусные!',
                         parse_mode='html')
    # 4
    await message.answer(text=f'<blockquote>Правило №4. Гигиена спального места:</blockquote>\n'
                              f'Чтобы от вас не улетело одеяло, и простыня не убежала (а без них, сами понимаете, не'
                              f' очень удобно спать), необходимо следить за чистотой спального места. Пот, пыль, грязь'
                              f' и посторонние запахи мешают нам заснуть. Меняйте постельное белье не реже чем раз в'
                              f' 10 дней и как можно скорее приобретите защитный чехол для подушки и матраса.',
                         parse_mode='html')
    # 5
    await message.answer(text=f'<blockquote>Правило №5. Температура в спальне:</blockquote>\n'
                              f'Начнем с того, почти все люди спят в одежде для сна: пижамах, сорочках, футболках.'
                              f' Все это дополнительно согревает наше тело. К этому же добавляем одеяло и тепло,'
                              f' исходящее от партнера или кота. Если учесть то, что в среднем температура воздуха в'
                              f' комнатах около 27 градусов тепла, и прибавить к этому тепло от одежды и одеяла, то'
                              f' нам во сне действительно жарко! Из-за этого мы скидываем с себя одеяло, ворочаемся'
                              f' и никак не попадаем в глубокую фазу сна. Идеальная температура спальни от +16 до +19'
                              f' С. Выбирая одеяла, отдавайте предпочтения моделям с эффектом терморегуляции.'
                              f' Под таким одеялом не жарко летом, и не холодно зимой.',
                         parse_mode='html')
    # 6
    await message.answer(text=f'<blockquote>Правило №6. Воздух:</blockquote>\n'
                              f'А помните, как хорошо в детстве вы спали в деревне, после дождя с грозой? И ничего,'
                              f' что кровать неудобная, а подушка слишком жесткая, сон наступал моментально, а на утро'
                              f' с первыми петухами вы просыпались максимально отдохнувшими. Все дело в воздухе, точнее'
                              f' в его чистоте. Чем чище воздух – тем лучше нашим легким, тем больше поступает'
                              f' кислорода в организм. Циркуляция крови происходит быстрее, и энергии в нас больше.'
                              f' Сейчас с учетом того, что мы живем в больших городах, достичь чистоты воздуха в'
                              f' квартире очень трудно. Проветривание помогает не на 100%, ведь через открытое окно в'
                              f' дом могут поступать пыль, выхлопные газы и посторонние запахи. Лучше пользоваться'
                              f' мойками для воздуха или увлажнителями. Воздух в спальне должен быть чистым и в меру'
                              f' влажным.',
                         parse_mode='html')
    # 7
    await message.answer(text=f'<blockquote>Правило №7. Освещение:</blockquote>\n'
                              f'Спать нужно в абсолютной темноте, только так в нашем организме начинает вырабатываться'
                              f' мелатонин – гормон счастья, красоты и долголетия. И обратите внимание, что даже'
                              f' огоньки выключенного телевизора, роутера или короткие оповещения на мобильном'
                              f' телефоне снижают выработку этого гормона. Они раздражают наш мозг, в который даже'
                              f' во время сна поступают сигналы об окружающей среде.',
                         parse_mode='html')
    # 8
    await message.answer(text=f'<blockquote>Правило №8. Звуки:</blockquote>\n'
                              f'Спать нужно в абсолютной тишине, причина та же: нам кажется, что мы спим, но наш мозг'
                              f' работает, он слышит, как кто-то «чирикает», и анализирует эту информацию. А вот'
                              f' послушать непосредственно перед сном расслабляющую музыку – можно, она поможет'
                              f' организму успокоиться и аккуратно настроит вас на отдых.',
                         parse_mode='html')
    # 9
    await message.answer(text=f'<blockquote>Правило №9. Мелатонин или во сколько засыпать:</blockquote>\n'
                              f'Еще раз и более подробно про мелатонин. Это гормон, который вырабатывается в нашем'
                              f' организме именно в темное время суток, поэтому мы и хотим спать, когда становится'
                              f' темнее. Меньше всего этого гормона вырабатывается в светлое время, с 8 до 18 часов,'
                              f' зато мы сами максимально продуктивны в этот период. После наша активность становится'
                              f' ниже, а мелатонина вырабатывается больше. Почему? Все просто, этот гормон, если'
                              f' по-простому, наше естественное снотворное. Важно не проморгать его, в прямом смысле'
                              f' слова. Старайтесь засыпать не позже 23:00, так вы запасетесь мелатонином на будущее.'
                              f' Он спасет вас от стрессов, преждевременного старения и от многих болезней, даже'
                              f' онкологических. Недостаток мелатонина – прямой путь к депрессии и бессоннице в'
                              f' пожилом возрасте.',
                         parse_mode='html')
    # 10
    await message.answer(text=f'<blockquote>Правило №10. На чем вы спите:</blockquote>\n'
                              f'Чтобы ваше тело окончательно расслабилось в конце дня, ему должно быть комфортно.'
                              f' Высота подушки должна подходить под длину плеча, а матрас – поддерживать позвоночник'
                              f' в правильном положении.',
                         parse_mode='html')
