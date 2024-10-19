from telebot import types
from sqlmodel import Session, select
from models import User, Group, GroupMember
from database import engine
from utils import is_admin, get_or_create_user
from texts import (
    CONFIRM_GROUP_DELETE, CONFIRM_MEMBER_DELETE, DELETE_GROUP, DELETE_MEMBER, EDIT_GROUP, EDIT_MEMBER, ENTER_NEW_GROUP_NAME, ENTER_NEW_MEMBER_NAME, GROUP_DELETED_SUCCESSFULLY, GROUP_DELETION_CANCELLED, GROUP_UPDATED_SUCCESSFULLY, GROUPS_MENU, CREATE_GROUP, MEMBER_DELETED_SUCCESSFULLY, MEMBER_DELETION_CANCELLED, MEMBER_UPDATED_SUCCESSFULLY, NO_MEMBERS_IN_GROUP, NO_PERMISSION, RETURN_TO_MAIN_MENU, SELECT_GROUP_TO_DELETE, SELECT_GROUP_TO_DELETE_MEMBER, SELECT_GROUP_TO_EDIT, SELECT_GROUP_TO_EDIT_MEMBER, SELECT_MEMBER_TO_DELETE, SELECT_MEMBER_TO_EDIT, VIEW_GROUPS, ADD_USER_TO_GROUP,
    ENTER_GROUP_NAME, GROUP_CREATED_SUCCESSFULLY, GROUP_ALREADY_EXISTS,
    NO_GROUPS_AVAILABLE, AVAILABLE_GROUPS, SELECT_GROUP_TO_ADD_USER,
    ENTER_NAME_TO_ADD, USER_ADDED_TO_GROUP_SUCCESSFULLY,
    USER_ALREADY_IN_GROUP, USER_NOT_FOUND
)

def groups_menu(message, send_message_once):
    user_id = message.from_user.id
    is_user_admin = is_admin(user_id)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(CREATE_GROUP, callback_data="create_group"))
    keyboard.row(types.InlineKeyboardButton(VIEW_GROUPS, callback_data="view_groups"))
    keyboard.row(types.InlineKeyboardButton(ADD_USER_TO_GROUP, callback_data="add_user_to_group"))
    
    if is_user_admin:
        keyboard.row(types.InlineKeyboardButton(EDIT_GROUP, callback_data="edit_group"))
        keyboard.row(types.InlineKeyboardButton(DELETE_GROUP, callback_data="delete_group"))
    else:
        keyboard.row(types.InlineKeyboardButton(EDIT_GROUP, callback_data="edit_own_group"))
        keyboard.row(types.InlineKeyboardButton(DELETE_GROUP, callback_data="delete_own_group"))
    
    keyboard.row(types.InlineKeyboardButton(EDIT_MEMBER, callback_data="edit_member"))
    keyboard.row(types.InlineKeyboardButton(DELETE_MEMBER, callback_data="delete_member"))
    send_message_once(message.chat.id, GROUPS_MENU, reply_markup=keyboard)

def create_group_prompt(call, send_message_once, bot):
    message = send_message_once(call.message.chat.id, ENTER_GROUP_NAME)
    bot.register_next_step_handler(message, save_new_group, send_message_once)

def save_new_group(message, send_message_once):
    group_name = message.text.strip()
    user_id = message.from_user.id
    with Session(engine) as session:
        user = get_or_create_user(user_id)
        existing_group = session.exec(select(Group).where(Group.name == group_name)).first()
        if existing_group:
            send_message_once(message.chat.id, GROUP_ALREADY_EXISTS.format(group_name=group_name))
        else:
            new_group = Group(name=group_name, created_by_id=user.id)
            session.add(new_group)
            session.commit()
            session.refresh(new_group)
            creator_name = ""
            group_member = GroupMember(group_id=new_group.id, name=creator_name)
            session.add(group_member)
            session.commit()
            send_message_once(message.chat.id, GROUP_CREATED_SUCCESSFULLY.format(group_name=group_name))

def view_groups(call, send_message_once):
    with Session(engine) as session:
        groups = session.exec(select(Group)).all()
    
    if not groups:
        send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
        return

    group_list = AVAILABLE_GROUPS
    for group in groups:
        member_count = session.exec(select(GroupMember).where(GroupMember.group_id == group.id)).all()
        s = ""
        for i in member_count:
            s= s+i.name+"\n"
        
        group_list += f"اسم الموضوع : {group.name}\n الطلاب:{s}\n\n"
    send_message_once(call.message.chat.id, group_list)

def add_user_to_group_prompt(call, send_message_once):
    with Session(engine) as session:
        groups = session.exec(select(Group)).all()
    
    if not groups:
        send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for group in groups:
        keyboard.add(types.InlineKeyboardButton(group.name, callback_data=f"select_group_{group.id}"))
    send_message_once(call.message.chat.id, SELECT_GROUP_TO_ADD_USER, reply_markup=keyboard)

def add_user_to_group(call, send_message_once, bot):
    group_id = int(call.data.split("_")[-1])
    message = send_message_once(call.message.chat.id, ENTER_NAME_TO_ADD)
    bot.register_next_step_handler(message, process_add_user_to_group, group_id, send_message_once)

def process_add_user_to_group(message, group_id, send_message_once):
    name = message.text.strip()
    with Session(engine) as session:
        group = session.get(Group, group_id)
        existing_member = session.exec(select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.name == name)).first()
        if existing_member:
            send_message_once(message.chat.id, USER_ALREADY_IN_GROUP.format(name=name, group_name=group.name))
        else:
            new_member = GroupMember(group_id=group_id, name=name)
            session.add(new_member)
            session.commit()
            send_message_once(message.chat.id, USER_ADDED_TO_GROUP_SUCCESSFULLY.format(name=name, group_name=group.name))

def edit_group_prompt(call, send_message_once):
    user_id = call.from_user.id
    is_user_admin = is_admin(user_id)

    with Session(engine) as session:
        user_local_id = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if is_user_admin:
            groups = session.exec(select(Group)).all()
        else:
            groups = session.exec(select(Group).where(Group.created_by_id == user_local_id.id)).all()
    
    if not groups:
        send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for group in groups:
        keyboard.add(types.InlineKeyboardButton(group.name, callback_data=f"edit_group_{group.id}"))
    keyboard.add(types.InlineKeyboardButton(RETURN_TO_MAIN_MENU, callback_data="groups_menu"))
    send_message_once(call.message.chat.id, SELECT_GROUP_TO_EDIT, reply_markup=keyboard)

def edit_group(call, send_message_once, bot):
    group_id = int(call.data.split("_")[-1])
    message = send_message_once(call.message.chat.id, ENTER_NEW_GROUP_NAME)
    bot.register_next_step_handler(message, process_edit_group, group_id, send_message_once)

def process_edit_group(message, group_id, send_message_once):
    new_name = message.text.strip()
    with Session(engine) as session:
        group = session.get(Group, group_id)
        if group:
            group.name = new_name
            session.commit()
            send_message_once(message.chat.id, GROUP_UPDATED_SUCCESSFULLY.format(new_name=new_name))
        else:
            send_message_once(message.chat.id, NO_GROUPS_AVAILABLE)

def delete_group_prompt(call, send_message_once):
    user_id = call.from_user.id
    is_user_admin = is_admin(user_id)

    with Session(engine) as session:
        user_local_id = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if is_user_admin:
            groups = session.exec(select(Group)).all()
        else:
            groups = session.exec(select(Group).where(Group.created_by_id == user_local_id.id)).all()
    
    if not groups:
        send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for group in groups:
        keyboard.add(types.InlineKeyboardButton(group.name, callback_data=f"delete_group_{group.id}"))
    keyboard.add(types.InlineKeyboardButton(RETURN_TO_MAIN_MENU, callback_data="groups_menu"))
    send_message_once(call.message.chat.id, SELECT_GROUP_TO_DELETE, reply_markup=keyboard)

def delete_group_confirm(call, send_message_once):
    group_id = int(call.data.split("_")[-1])
    user_id = call.from_user.id
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if not user:
            send_message_once(call.message.chat.id, USER_NOT_FOUND)
            return

        group = session.get(Group, group_id)
        if not group:
            send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
            return

        is_user_admin = is_admin(user_id)
        is_group_creator = group.created_by_id == user.id

        if is_user_admin or is_group_creator:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton("نعم", callback_data=f"confirm_delete_group_{group_id}"),
                types.InlineKeyboardButton("لا", callback_data="cancel_delete_group")
            )
            send_message_once(call.message.chat.id, CONFIRM_GROUP_DELETE.format(group_name=group.name), reply_markup=keyboard)
        else:
            send_message_once(call.message.chat.id, NO_PERMISSION)


def delete_group(call, send_message_once):
    group_id = int(call.data.split("_")[-1])
    user_id = call.from_user.id
    is_user_admin = is_admin(user_id)
    
    with Session(engine) as session:
        user_local_id = session.exec(select(User).where(User.telegram_id == user_id)).first()
        group = session.get(Group, group_id)
        members = session.exec(select(GroupMember).where(GroupMember.group_id == group_id)).all()
        if members and (is_user_admin or group.created_by_id == user_local_id.id):
            for i in members:
                session.delete(i)
                session.commit()
        if group and (is_user_admin or group.created_by_id == user_local_id.id):
            session.delete(group)
            session.commit()
            send_message_once(call.message.chat.id, GROUP_DELETED_SUCCESSFULLY.format(group_name=group.name))
        else:
            send_message_once(call.message.chat.id, NO_PERMISSION)

def cancel_delete_group(call, send_message_once):
    send_message_once(call.message.chat.id, GROUP_DELETION_CANCELLED)
    
def edit_member_prompt(call, send_message_once):
    user_id = call.from_user.id
    is_user_admin = is_admin(user_id)

    with Session(engine) as session:
        user_local_id = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if is_user_admin:
            groups = session.exec(select(Group)).all()
        else:
            groups = session.exec(select(Group).where(Group.created_by_id == user_local_id.id)).all()
    if not groups:
        send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for group in groups:
        keyboard.add(types.InlineKeyboardButton(group.name, callback_data=f"edit_member_group_{group.id}"))
    send_message_once(call.message.chat.id, SELECT_GROUP_TO_EDIT_MEMBER, reply_markup=keyboard)

def select_member_to_edit(call, send_message_once):
    group_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        members = session.exec(select(GroupMember).where(GroupMember.group_id == group_id)).all()
    
    if not members:
        send_message_once(call.message.chat.id, NO_MEMBERS_IN_GROUP)
        return

    keyboard = types.InlineKeyboardMarkup()
    for member in members:
        keyboard.add(types.InlineKeyboardButton(member.name, callback_data=f"edit_member_{member.id}"))
    send_message_once(call.message.chat.id, SELECT_MEMBER_TO_EDIT, reply_markup=keyboard)

def edit_member(call, send_message_once, bot):
    member_id = int(call.data.split("_")[-1])
    message = send_message_once(call.message.chat.id, ENTER_NEW_MEMBER_NAME)
    bot.register_next_step_handler(message, process_edit_member, member_id, send_message_once)

def process_edit_member(message, member_id, send_message_once):
    new_name = message.text.strip()
    with Session(engine) as session:
        member = session.get(GroupMember, member_id)
        if member:
            member.name = new_name
            session.commit()
            send_message_once(message.chat.id, MEMBER_UPDATED_SUCCESSFULLY.format(new_name=new_name))
        else:
            send_message_once(message.chat.id, USER_NOT_FOUND)

def delete_member_prompt(call, send_message_once):
    user_id = call.from_user.id
    is_user_admin = is_admin(user_id)

    with Session(engine) as session:
        user_local_id = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if is_user_admin:
            groups = session.exec(select(Group)).all()
        else:
            groups = session.exec(select(Group).where(Group.created_by_id == user_local_id.id)).all()
    
    if not groups:
        send_message_once(call.message.chat.id, NO_GROUPS_AVAILABLE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for group in groups:
        keyboard.add(types.InlineKeyboardButton(group.name, callback_data=f"delete_member_group_{group.id}"))
    send_message_once(call.message.chat.id, SELECT_GROUP_TO_DELETE_MEMBER, reply_markup=keyboard)

def select_member_to_delete(call, send_message_once):
    group_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        members = session.exec(select(GroupMember).where(GroupMember.group_id == group_id)).all()
    
    if not members:
        send_message_once(call.message.chat.id, NO_MEMBERS_IN_GROUP)
        return

    keyboard = types.InlineKeyboardMarkup()
    for member in members:
        keyboard.add(types.InlineKeyboardButton(member.name, callback_data=f"delete_member_{member.id}"))
    send_message_once(call.message.chat.id, SELECT_MEMBER_TO_DELETE, reply_markup=keyboard)

def delete_member_confirm(call, send_message_once):
    member_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        member = session.get(GroupMember, member_id)
        if member:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton("نعم", callback_data=f"confirm_delete_member_{member_id}"),
                types.InlineKeyboardButton("لا", callback_data="cancel_delete_member")
            )
            send_message_once(call.message.chat.id, CONFIRM_MEMBER_DELETE.format(member_name=member.name), reply_markup=keyboard)
        else:
            send_message_once(call.message.chat.id, USER_NOT_FOUND)

def delete_member(call, send_message_once):
    member_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        member = session.get(GroupMember, member_id)
        if member:
            session.delete(member)
            session.commit()
            send_message_once(call.message.chat.id, MEMBER_DELETED_SUCCESSFULLY.format(member_name=member.name))
        else:
            send_message_once(call.message.chat.id, USER_NOT_FOUND)

def cancel_delete_member(call, send_message_once):
    send_message_once(call.message.chat.id, MEMBER_DELETION_CANCELLED)