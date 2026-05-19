import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# 🔴 СЮДА ВСТАВЬ СВОЙ API ТОКЕН ОТ BOTFATHER
TOKEN = "8242670749:AAHvWLT3H9sITzwvNvqUAer1aKjBUG685lE"
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Полная машина состояний со всеми 14 шагами опроса
class Questionnaire(StatesGroup):
    gender = State()
    parents_height = State()
    tallest_relative = State()
    age = State()
    current_height = State()
    fast_growth_period = State()
    stagnation_period = State()
    childhood_comparison = State()
    target_height = State()
    weight = State()
    shoe_size = State()
    proportions = State()
    growth_pains = State()
    bedtime = State()
    sleep_duration = State()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🧬 Начать ИИ-Анализ", callback_data="start_quiz"))
    
    welcome = (
        f"Приветствую, {message.from_user.first_name}. На связи **G-Hormone AI** 🧬\n\n"
        "Я — специализированная ИИ-система по оптимизации зон роста. "
        "Чтобы составить твой персональный генетический и эндокринный профиль, "
        "мне нужно задать тебе несколько вопросов.\n\n"
        "Это займет не более 3 минут. Нажми кнопку ниже, чтобы начать."
    )
    await message.answer(welcome, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == "start_quiz")
async def quiz_start(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="👦 Парни", callback_data="gender_male"))
    builder.add(types.InlineKeyboardButton(text="👧 Девушки", callback_data="gender_female"))
    
    await callback.message.answer("1️⃣ **Выбери свой биологический пол:**", reply_markup=builder.as_markup())
    await state.set_state(Questionnaire.gender)
    await callback.answer()

@dp.callback_query(Questionnaire.gender)
async def process_gender(callback: types.CallbackQuery, state: FSMContext):
    gender = "male" if callback.data == "gender_male" else "female"
    await state.update_data(user_gender=gender)
    
    await callback.message.answer(
        "2️⃣ **Укажи рост мамы и папы** в сантиметрах через пробел.\n"
        "Пример: `165 180`"
    )
    await state.set_state(Questionnaire.parents_height)
    await callback.answer()

@dp.message(Questionnaire.parents_height)
async def process_parents(message: types.Message, state: FSMContext):
    await state.update_data(parents_height=message.text)
    await message.answer(
        "3️⃣ **Кто самый высокий родственник в твоем роду и какой у него рост?**\n"
        "Пример: `Прадедушка, 190 см`"
    )
    await state.set_state(Questionnaire.tallest_relative)

@dp.message(Questionnaire.tallest_relative)
async def process_relative(message: types.Message, state: FSMContext):
    await state.update_data(tallest_relative=message.text)
    await message.answer("4️⃣ **Какой у тебя возраст?** (Напиши только число, например: `14`)")
    await state.set_state(Questionnaire.age)

@dp.message(Questionnaire.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("5️⃣ **Какой у тебя рост сейчас?** Введи число в сантиметрах (например: `170`)")
    await state.set_state(Questionnaire.current_height)

@dp.message(Questionnaire.current_height)
async def process_height(message: types.Message, state: FSMContext):
    await state.update_data(current_height=message.text)
    await message.answer("6️⃣ **В какой период ты рос быстрее всего?** (например: *в 13 лет*)")
    await state.set_state(Questionnaire.fast_growth_period)

@dp.message(Questionnaire.fast_growth_period)
async def process_fast_growth(message: types.Message, state: FSMContext):
    await state.update_data(fast_growth_period=message.text)
    await message.answer("7️⃣ **Были ли периоды, когда ты почти не рос (несколько месяцев или дольше)?**")
    await state.set_state(Questionnaire.stagnation_period)

@dp.message(Questionnaire.stagnation_period)
async def process_stagnation(message: types.Message, state: FSMContext):
    await state.update_data(stagnation_period=message.text)
    await message.answer("8️⃣ **Каким ты был в детстве по сравнению со сверстниками?** (Выше, ниже, как все?)")
    await state.set_state(Questionnaire.childhood_comparison)

@dp.message(Questionnaire.childhood_comparison)
async def process_childhood(message: types.Message, state: FSMContext):
    await state.update_data(childhood_comparison=message.text)
    await message.answer("9️⃣ **Какого роста ты бы хотел достичь?** (Например: `195`)")
    await state.set_state(Questionnaire.target_height)

@dp.message(Questionnaire.target_height)
async def process_target(message: types.Message, state: FSMContext):
    await state.update_data(target_height=message.text)
    await message.answer("🔟 **Сколько ты сейчас весишь?** (Введи число в кг, например: `60`)")
    await state.set_state(Questionnaire.weight)

@dp.message(Questionnaire.weight)
async def process_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer("1️⃣1️⃣ **Твой размер обуви:** (Например: `42`)")
    await state.set_state(Questionnaire.shoe_size)

@dp.message(Questionnaire.shoe_size)
async def process_shoe(message: types.Message, state: FSMContext):
    await state.update_data(shoe_size=message.text)
    await message.answer("1️⃣2️⃣ **Замечал ли ты, что твои руки или ноги выглядят непропорционально к телу?**")
    await state.set_state(Questionnaire.proportions)

@dp.message(Questionnaire.proportions)
async def process_proportions(message: types.Message, state: FSMContext):
    await state.update_data(proportions=message.text)
    await message.answer("1️⃣3️⃣ **Как часто у тебя бывают боли в ногах или ощущение 'тянущего роста'?**")
    await state.set_state(Questionnaire.growth_pains)

@dp.message(Questionnaire.growth_pains)
async def process_pains(message: types.Message, state: FSMContext):
    await state.update_data(growth_pains=message.text)
    await message.answer("1️⃣4️⃣ **Во сколько ты обычно засыпаешь и сколько часов спишь?** (Пример: `23:00, 8 часов`)")
    await state.set_state(Questionnaire.sleep_duration)

@dp.message(Questionnaire.sleep_duration)
async def final_result(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
    age = user_data.get('age', '14')
    height = user_data.get('current_height', '170')
    target = user_data.get('target_height', '195')
    relative = user_data.get('tallest_relative', 'прадедушка')
    
    result_text = (
        f"📊 **Твой потенциал роста 🏔️**\n\n"
        f"Ваш текущий рост — **{height} см в {age} лет** — уже превышает средние показатели для вашего возраста, и это хороший знак. "
        f"Учитывая динамику развития, можно предположить, что вы находитесь в активной фазе роста. "
        f"Ваш родственник ({relative}), как самый высокий в роду, указывает на наличие генетического потенциала, который может проявиться и у вас. "
        f"Физические изменения говорят о том, что пубертатный период у вас протекает активно, что связано с возможностями роста. "
        f"Ваш сон глубокий и продолжительный, что является важным фактором для выработки гормона роста. "
        f"Даже если вы не занимаетесь спортом, ваш организм все еще имеет значительный потенциал для достижения цели в **{target} см**.\n\n"
        
        f"🔹 **Ваш потенциальный генетический рост**\n"
        f"🔒 Доступно в полной версии\n\n"
        
        f"🔹 **Шансы достичь этого роста**\n"
        f"Шансы достичь этого роста высокие. Учитывая ваш возраст, активные пубертатные изменения и генетический потенциал, у вас есть все предпосылки для дальнейшего роста.\n\n"
        
        f"🔹 **Что всё это время мешало вам расти**\n"
        f"🔒 Доступно в полной версии\n\n"
        
        f"🔹 **На чём стоит сфокусироваться прямо сейчас**\n"
        f"🔒 Доступно в полной версии\n\n"
        
        f"🔹 **Насколько ваша генетика поддерживает рост**\n"
        f"Ваша генетика имеет хороший потенциал для роста, особенно учитывая данные ваших родственников. "
        f"В платной версии мы разберем, как активировать скрытые ДНК-маркеры...\n"
        f"🔒 Оставшаяся часть доступна в полной версии\n\n"
        
        f"🔹 **Ваш рост относительно сверстников**\n"
        f"🔒 Доступно в полной версии\n\n"
        
        f"🔹 **Почему стандартные советы не работали именно у вас**\n"
        f"🔒 Доступно в полной версии\n\n"
        
        f"🔹 **Сколько роста вы потенциально теряете каждый год без корректировки**\n"
        f"🔒 Доступно в полной версии\n\n"
        
        f"🔹 **Что в вашем профиле сильнее всего отличает вас от среднего подростка**\n"
        f"🔒 Доступно в полной версии"
    )
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🔓 Открыть полную версию (Premium)", callback_data="buy_premium"))
    
    await message.answer(result_text, parse_mode="Markdown", reply_markup=builder.as_markup())
    await state.clear()

@dp.callback_query(lambda c: c.data == "buy_premium")
async def process_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "💳 **Оформление Premium доступа к G-Hormone AI**\n\n"
        "Стоимость полной версии анализа и Протокола 195: **290 рублей**.\n\n"
        "Для оплаты нажмите на команду /pay"
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
