# __init__.py
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from . import general, lectures, assignments, subjects, admin, pdf_utils, groups
from utils import prevent_duplicate_message, prevent_duplicate_callback
from texts import FINISH_PDF_CREATION, CANCEL_PDF_CREATION

def register_handlers(bot: TeleBot, send_message_once):
    # General handlers
    @bot.message_handler(commands=['start'])
    @prevent_duplicate_message
    def start(message: Message):
        general.start(message, send_message_once)
    
    @bot.message_handler(commands=['username'])
    @prevent_duplicate_message
    def username_handler(message: Message):
        admin.get_username_by_id(message, send_message_once, bot)

    # Lecture handlers
    @bot.message_handler(func=lambda message: message.text == "📚 المحاضرات")
    @prevent_duplicate_message
    def lectures_menu(message: Message):
        lectures.lectures_menu(message, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "view_lectures_subjects")
    @prevent_duplicate_callback
    def view_lectures_subjects(call: CallbackQuery):
        lectures.view_lectures_subjects(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("view_lectures_"))
    @prevent_duplicate_callback
    def view_lectures(call: CallbackQuery):
        lectures.view_lectures(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "upload_lecture")
    @prevent_duplicate_callback
    def upload_lecture_prompt(call: CallbackQuery):
        lectures.upload_lecture_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("select_subject_"))
    @prevent_duplicate_callback
    def process_lecture_subject(call: CallbackQuery):
        lectures.process_lecture_subject(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "edit_lecture")
    @prevent_duplicate_callback
    def edit_lecture_prompt(call: CallbackQuery):
        lectures.edit_lecture_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_lecture_"))
    @prevent_duplicate_callback
    def edit_lecture(call: CallbackQuery):
        lectures.edit_lecture(call, send_message_once, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_lecture")
    @prevent_duplicate_callback
    def delete_lecture_prompt(call: CallbackQuery):
        lectures.delete_lecture_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_lecture_"))
    @prevent_duplicate_callback
    def delete_lecture_confirm(call: CallbackQuery):
        lectures.delete_lecture_confirm(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete_lecture_"))
    @prevent_duplicate_callback
    def delete_lecture(call: CallbackQuery):
        lectures.delete_lecture(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "cancel_delete_lecture")
    @prevent_duplicate_callback
    def cancel_delete_lecture(call: CallbackQuery):
        lectures.cancel_delete_lecture(call, send_message_once)

    # Assignment handlers
    @bot.message_handler(func=lambda message: message.text == "📝 الواجبات")
    @prevent_duplicate_message
    def assignments_menu(message: Message):
        assignments.assignments_menu(message, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "view_assignments")
    @prevent_duplicate_callback
    def view_assignments(call: CallbackQuery):
        assignments.view_assignments(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "create_assignment")
    @prevent_duplicate_callback
    def create_assignment_prompt(call: CallbackQuery):
        assignments.create_assignment_prompt(call, send_message_once)
    
    @bot.callback_query_handler(func=lambda call: call.data == "edit_assignment")
    @prevent_duplicate_callback
    def edit_assignment_prompt(call: CallbackQuery):
        assignments.edit_assignment_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_assignment_"))
    @prevent_duplicate_callback
    def edit_assignment(call: CallbackQuery):
        assignments.edit_assignment(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_assignment")
    @prevent_duplicate_callback
    def delete_assignment_prompt(call: CallbackQuery):
        assignments.delete_assignment_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_assignment_"))
    @prevent_duplicate_callback
    def delete_assignment_confirm(call: CallbackQuery):
        assignments.delete_assignment_confirm(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete_assignment_"))
    @prevent_duplicate_callback
    def delete_assignment(call: CallbackQuery):
        assignments.delete_assignment(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "cancel_delete_assignment")
    @prevent_duplicate_callback
    def cancel_delete_assignment(call: CallbackQuery):
        assignments.cancel_delete_assignment(call, send_message_once)

    # Subject handlers
    @bot.message_handler(func=lambda message: message.text == "📋 المواد")
    @prevent_duplicate_message
    def subjects_menu(message: Message):
        subjects.subjects_menu(message, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "view_subjects")
    @prevent_duplicate_callback
    def view_subjects(call: CallbackQuery):
        subjects.view_subjects(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "add_subject")
    @prevent_duplicate_callback
    def add_subject_prompt(call: CallbackQuery):
        subjects.add_subject_prompt(call, send_message_once, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "edit_subject")
    @prevent_duplicate_callback
    def edit_subject_prompt(call: CallbackQuery):
        subjects.edit_subject_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_subject_"))
    @prevent_duplicate_callback
    def edit_subject(call: CallbackQuery):
        subjects.edit_subject(call, send_message_once, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_subject")
    @prevent_duplicate_callback
    def delete_subject_prompt(call: CallbackQuery):
        subjects.delete_subject_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_subject_"))
    @prevent_duplicate_callback
    def delete_subject_confirm(call: CallbackQuery):
        subjects.delete_subject_confirm(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete1_"))
    @prevent_duplicate_callback
    def delete_subject(call: CallbackQuery):
        subjects.delete_subject(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "cancel_delete")
    @prevent_duplicate_callback
    def cancel_delete(call: CallbackQuery):
        subjects.cancel_delete(call, send_message_once)

    # Admin handlers
    @bot.message_handler(func=lambda message: message.text == "🛠 الإدارة")
    @prevent_duplicate_message
    def admin_menu(message: Message):
        admin.admin_menu(message, send_message_once)

    @bot.message_handler(commands=['makeadmin'])
    @prevent_duplicate_message
    def make_admin(message: Message):
        admin.make_admin(message, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "list_users")
    @prevent_duplicate_callback
    def list_users(call: CallbackQuery):
        admin.list_users(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data in ["add_admin", "remove_admin"])
    @prevent_duplicate_callback
    def admin_action_prompt(call: CallbackQuery):
        admin.admin_action_prompt(call, send_message_once)
    

    # PDF utilities handlers
    @bot.message_handler(func=lambda message: message.text == "📄 أدوات PDF")
    @prevent_duplicate_message
    def pdf_utils_menu_handler(message: Message):
        pdf_utils.pdf_utils_menu(message, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "photo_to_pdf")
    @prevent_duplicate_callback
    def photo_to_pdf_prompt_handler(call: CallbackQuery):
        pdf_utils.photo_to_pdf_prompt(call, send_message_once)

    @bot.message_handler(content_types=['photo'])
    def photo_handler(message: Message):
        pdf_utils.handle_photo_for_pdf(message, bot, send_message_once)

    @bot.message_handler(func=lambda message: message.text in [FINISH_PDF_CREATION, CANCEL_PDF_CREATION])
    def pdf_creation_control_handler(message: Message):
        pdf_utils.handle_photo_for_pdf(message, bot, send_message_once)
# Group handlers
    @bot.message_handler(func=lambda message: message.text == "👥 المجموعات")
    @prevent_duplicate_message
    def groups_menu_handler(message: Message):
        groups.groups_menu(message, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "create_group")
    @prevent_duplicate_callback
    def create_group_handler(call: CallbackQuery):
        groups.create_group_prompt(call, send_message_once, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "view_groups")
    @prevent_duplicate_callback
    def view_groups_handler(call: CallbackQuery):
        groups.view_groups(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "add_user_to_group")
    @prevent_duplicate_callback
    def add_user_to_group_handler(call: CallbackQuery):
        groups.add_user_to_group_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("select_group_"))
    @prevent_duplicate_callback
    def select_group_handler(call: CallbackQuery):
        groups.add_user_to_group(call, send_message_once, bot)
        
    @bot.callback_query_handler(func=lambda call: call.data == "edit_group")
    @prevent_duplicate_callback
    def edit_group_prompt_handler(call: CallbackQuery):
        groups.edit_group_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_group_"))
    @prevent_duplicate_callback
    def edit_group_handler(call: CallbackQuery):
        groups.edit_group(call, send_message_once, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_group")
    @prevent_duplicate_callback
    def delete_group_prompt_handler(call: CallbackQuery):
        groups.delete_group_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_group_"))
    @prevent_duplicate_callback
    def delete_group_confirm_handler(call: CallbackQuery):
        groups.delete_group_confirm(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete_group_"))
    @prevent_duplicate_callback
    def delete_group_handler(call: CallbackQuery):
        groups.delete_group(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "cancel_delete_group")
    @prevent_duplicate_callback
    def cancel_delete_group_handler(call: CallbackQuery):
        groups.cancel_delete_group(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "edit_member")
    @prevent_duplicate_callback
    def edit_member_prompt_handler(call: CallbackQuery):
        groups.edit_member_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_member_group_"))
    @prevent_duplicate_callback
    def select_member_to_edit_handler(call: CallbackQuery):
        groups.select_member_to_edit(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_member_"))
    @prevent_duplicate_callback
    def edit_member_handler(call: CallbackQuery):
        groups.edit_member(call, send_message_once, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_member")
    @prevent_duplicate_callback
    def delete_member_prompt_handler(call: CallbackQuery):
        groups.delete_member_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_member_group_"))
    @prevent_duplicate_callback
    def select_member_to_delete_handler(call: CallbackQuery):
        groups.select_member_to_delete(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_member_"))
    @prevent_duplicate_callback
    def delete_member_confirm_handler(call: CallbackQuery):
        groups.delete_member_confirm(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete_member_"))
    @prevent_duplicate_callback
    def delete_member_handler(call: CallbackQuery):
        groups.delete_member(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "cancel_delete_member")
    @prevent_duplicate_callback
    def cancel_delete_member_handler(call: CallbackQuery):
        groups.cancel_delete_member(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "edit_own_group")
    @prevent_duplicate_callback
    def edit_own_group_handler(call: CallbackQuery):
        groups.edit_group_prompt(call, send_message_once)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_own_group")
    @prevent_duplicate_callback
    def delete_own_group_handler(call: CallbackQuery):
        groups.delete_group_prompt(call, send_message_once)

    # Handle lecture and assignment steps
    @bot.message_handler(func=lambda message: True, content_types=['text', 'document'])
    def handle_steps(message: Message):
        # First, try to handle lecture steps
        if lectures.handle_lecture_steps(message, send_message_once):
            return
        
        # If it's not a lecture step, try to handle assignment steps
        if assignments.handle_assignment_steps(message, send_message_once):
            return
        
        # If it's not an assignment step, try to handle edit assignment steps
        if assignments.handle_edit_assignment_steps(message, send_message_once):
            return