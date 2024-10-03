from pyrogram.types import InlineKeyboardButton

# Text content from handlers.py

START_MESSAGE = "مرحبًا ، أي شيء تريد القيام به؟"
USER_START_MESSAGE = "مرحبًا! إليك ما يمكنك فعله:"
ERROR_MESSAGE = "حدث خطأ. يرجى المحاولة مرة أخرى لاحقًا."
NO_PERMISSION_MESSAGE = "ليس لديك إذن لإضافة مهام."
ADD_TASK_INSTRUCTIONS = "الرجاء إدخال تفاصيل {task_type} بالتنسيق التالي:\nالعنوان | الوصف | تاريخ الاستحقاق (YYYY-MM-DD)\nيمكنك أيضًا إرفاق صورة مع التفاصيل في التعليق."
MISSING_CAPTION = "الرجاء إرفاق التفاصيل في تعليق الصورة."
TASK_ADDED_SUCCESS = "{task_type} تمت إضافته بنجاح!"
NO_TASKS_NEXT_WEEK = "لا توجد مهام للأسبوع القادم!"
EDIT_TASK_INSTRUCTIONS = "الرجاء إدخال تفاصيل {task_type} الجديدة بالتنسيق التالي:\nالعنوان | الوصف | تاريخ الاستحقاق (YYYY-MM-DD)\nيمكنك أيضًا إرفاق صورة جديدة مع التفاصيل في التعليق."
TASK_NOT_EXIST = "المهمة غير موجودة."
NO_PERMISSION_DELETE = "ليس لديك إذن لحذف المهام."
TASK_DELETED_SUCCESS = "{task_type} تم حذفه بنجاح!"
MAKE_ADMIN_REPLY_REQUIRED = "يرجى الرد على رسالة المستخدم لجعله مشرفًا."
MAKE_ADMIN_SUCCESS = "المستخدم {target_username} أصبح الآن مشرفًا."
ADMIN_ONLY_COMMAND = "عذرًا، فقط المشرفون يمكنهم استخدام هذا الأمر."
PROVIDE_ADMIN_PASSWORD = "يرجى تقديم كلمة مرور المشرف."
ADMIN_PASSWORD_SUCCESS = "تهانينا! أنت الآن مشرف."
ADMIN_PASSWORD_FAIL = "كلمة المرور غير صحيحة. لا يمكنك أن تصبح مشرفًا."
DEFAULT_RESPONSE = "مرحبًا! إذا كنت تريد إضافة أو عرض المهام، يرجى استخدام الأوامر المتاحة."
TASK_UPDATED_SUCCESS = "تم التعديل بنجاح"
# Keyboard layouts
ADMIN_KEYBOARD = [
    [InlineKeyboardButton("إضافة واجب", callback_data="add_homework"),
     InlineKeyboardButton("إضافة مهمة", callback_data="add_assignment")],
    [InlineKeyboardButton("عرض الأسبوع القادم", callback_data="view_next_week")]
]

USER_KEYBOARD = [
    [InlineKeyboardButton("عرض الأسبوع القادم", callback_data="view_next_week")]
]

# Add other constant strings and keyboard layouts as needed