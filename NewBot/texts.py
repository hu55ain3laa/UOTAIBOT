# texts.py

# General messages
WELCOME_MESSAGE = "مرحبًا، {first_name}! 👋\nماذا تريد أن تفعل اليوم؟"

# Menu items
LECTURES_BUTTON = "📚 المحاضرات"
ASSIGNMENTS_BUTTON = "📝 الواجبات"
SUBJECTS_BUTTON = "📋 المواد"
HELP_BUTTON = "❓ المساعدة"
ADMIN_BUTTON = "🛠 الإدارة"

# Lectures
LECTURES_MENU = "قائمة المحاضرات:"
VIEW_LECTURES_BY_SUBJECT = "عرض المحاضرات حسب المادة"
UPLOAD_NEW_LECTURE = "رفع محاضرة جديدة"
NO_SUBJECTS_AVAILABLE = "لا توجد مواد متاحة."
SELECT_SUBJECT_VIEW_LECTURES = "اختر مادة لعرض المحاضرات:"
SUBJECT_NOT_FOUND = "لم يتم العثور على المادة."
NO_LECTURES_AVAILABLE = "لا توجد محاضرات متاحة لـ {subject_name}."
SUBJECT_LECTURES_HEADER = "\n📚 المادة: {subject_name}"
LECTURE_INFO = "المحاضرة {lecture_number}: {title}"
NO_UPLOAD_PERMISSION = "ليس لديك صلاحية لرفع المحاضرات."
NO_SUBJECTS_ADD_FIRST = "لا توجد مواد متاحة. الرجاء إضافة مادة أولاً."
SELECT_SUBJECT_NEW_LECTURE = "اختر مادة للمحاضرة الجديدة:"
ENTER_LECTURE_NUMBER = "الرجاء إدخال رقم المحاضرة."
INVALID_LECTURE_NUMBER = "رقم محاضرة غير صالح. الرجاء إدخال رقم صحيح."
ENTER_LECTURE_TITLE = "الرجاء إدخال عنوان لهذه المحاضرة."
SEND_LECTURE_FILE = "الرجاء إرسال ملف المحاضرة."
LECTURE_ADDED_SUCCESSFULLY = "تمت إضافة المحاضرة '{title}' (المحاضرة {lecture_number} من {subject_name}) بنجاح."
SUBJECT_NOT_FOUND_LECTURE_NOT_SAVED = "لم يتم العثور على المادة. لم يتم حفظ المحاضرة."
SEND_LECTURE_FILE_PROMPT = "الرجاء إرسال ملف للمحاضرة."
EDIT_LECTURE = "تعديل محاضرة"
DELETE_LECTURE = "حذف محاضرة"
SELECT_LECTURE_TO_EDIT = "اختر محاضرة للتعديل:"
SELECT_LECTURE_TO_DELETE = "اختر محاضرة للحذف:"
NO_LECTURES_TO_EDIT = "لا توجد محاضرات متاحة للتعديل."
NO_LECTURES_TO_DELETE = "لا توجد محاضرات متاحة للحذف."
ENTER_NEW_LECTURE_TITLE = "أدخل العنوان الجديد للمحاضرة:"
LECTURE_UPDATED_SUCCESSFULLY = "تم تحديث عنوان المحاضرة إلى '{new_title}'."
CONFIRM_LECTURE_DELETE = "هل أنت متأكد أنك تريد حذف المحاضرة '{lecture_number}: {lecture_title}' من مادة '{subject_name}'؟"
LECTURE_DELETED_SUCCESSFULLY = "تم حذف المحاضرة '{lecture_number}: {lecture_title}' من مادة '{subject_name}'."
LECTURE_DELETION_CANCELLED = "تم إلغاء حذف المحاضرة."

# Assignments
ASSIGNMENTS_MENU = "قائمة الواجبات:"
VIEW_UPCOMING_ASSIGNMENTS = "عرض الواجبات القادمة"
CREATE_NEW_ASSIGNMENT = "إنشاء واجب جديد"
NO_UPCOMING_ASSIGNMENTS = "لا توجد واجبات قادمة للأسبوع القادم."
ASSIGNMENT_INFO = "الواجب: {title}\nالموعد النهائي: {due_date}\nالوصف: {description}"
NO_ASSIGNMENT_PERMISSION = "ليس لديك صلاحية لإنشاء واجبات."
ENTER_ASSIGNMENT_TITLE = "الرجاء إدخال عنوان الواجب."
ENTER_ASSIGNMENT_DESCRIPTION = "الرجاء إدخال وصف الواجب."
ENTER_ASSIGNMENT_DUE_DATE = "الرجاء إدخال الموعد النهائي للواجب (MM-DD)"
SEND_ASSIGNMENT_FILE = "الرجاء إرسال ملف الواجب (اختياري). أرسل /skip إذا لم يكن هناك ملف."
INVALID_DATE_FORMAT = "صيغة تاريخ غير صالحة. الرجاء استخدام MM-DD أو MM-DD+7 للأسبوع القادم."
INVALID_INPUT_ASSIGNMENT_SAVED = "إدخال غير صالح. تم حفظ الواجب بدون ملف."
ASSIGNMENT_CREATED_SUCCESSFULLY = "تم إنشاء الواجب '{title}' بنجاح للموعد {due_date}."
EDIT_ASSIGNMENT = "تعديل الواجب"
DELETE_ASSIGNMENT = "حذف الواجب"
SELECT_ASSIGNMENT_TO_EDIT = "اختر الواجب للتعديل:"
SELECT_ASSIGNMENT_TO_DELETE = "اختر الواجب للحذف:"
NO_ASSIGNMENTS_TO_EDIT = "لا توجد واجبات متاحة للتعديل."
NO_ASSIGNMENTS_TO_DELETE = "لا توجد واجبات متاحة للحذف."
ENTER_NEW_ASSIGNMENT_TITLE = "أدخل العنوان الجديد للواجب:"
ENTER_NEW_ASSIGNMENT_DESCRIPTION = "أدخل الوصف الجديد للواجب:"
ENTER_NEW_ASSIGNMENT_DUE_DATE = "أدخل الموعد النهائي الجديد للواجب (MM-DD))."
ASSIGNMENT_UPDATED_SUCCESSFULLY = "تم تحديث الواجب بنجاح."
CONFIRM_ASSIGNMENT_DELETE = "هل أنت متأكد أنك تريد حذف الواجب '{title}' (الموعد النهائي: {due_date})؟"
ASSIGNMENT_DELETED_SUCCESSFULLY = "تم حذف الواجب '{title}' (الموعد النهائي: {due_date}) بنجاح."
ASSIGNMENT_DELETION_CANCELLED = "تم إلغاء حذف الواجب."
ARABIC_DAY_NAMES = [
    "الاثنين",
    "الثلاثاء",
    "الأربعاء",
    "الخميس",
    "الجمعة",
    "السبت",
    "الأحد"
]

# Subjects
SUBJECTS_MENU = "قائمة المواد:"
VIEW_ALL_SUBJECTS = "عرض جميع المواد"
ADD_NEW_SUBJECT = "إضافة مادة جديدة"
EDIT_SUBJECT = "تعديل مادة"
DELETE_SUBJECT = "حذف مادة"
NO_SUBJECT_MANAGEMENT_PERMISSION = "يمكن للمشرفين فقط إدارة المواد."
NO_SUBJECTS_AVAILABLE = "لا توجد مواد متاحة."
AVAILABLE_SUBJECTS = "المواد المتاحة:\n"
ENTER_NEW_SUBJECT_NAME = "الرجاء إدخال اسم المادة الجديدة:"
SUBJECT_ALREADY_EXISTS = "المادة '{subject_name}' موجودة بالفعل."
SUBJECT_ADDED_SUCCESSFULLY = "تمت إضافة المادة '{subject_name}' بنجاح."
NO_SUBJECTS_TO_EDIT = "لا توجد مواد متاحة للتعديل."
SELECT_SUBJECT_TO_EDIT = "اختر مادة للتعديل:"
ENTER_NEW_SUBJECT_NAME_EDIT = "أدخل الاسم الجديد للمادة:"
SUBJECT_UPDATED_SUCCESSFULLY = "تم تحديث اسم المادة إلى '{new_name}'."
NO_SUBJECTS_TO_DELETE = "لا توجد مواد متاحة للحذف."
SELECT_SUBJECT_TO_DELETE = "اختر مادة للحذف:"
CONFIRM_SUBJECT_DELETE = "هل أنت متأكد أنك تريد حذف المادة '{subject_name}'؟"
SUBJECT_DELETED_SUCCESSFULLY = "تم حذف المادة '{subject_name}'."
SUBJECT_DELETION_CANCELLED = "تم إلغاء حذف المادة."

# Admin
ADMIN_MENU = "لوحة الإدارة:"
LIST_USERS = "قائمة المستخدمين"
ADD_ADMIN = "إضافة مشرف"
REMOVE_ADMIN = "إزالة مشرف"
NO_ADMIN_PERMISSION = "ليس لديك صلاحية للوصول إلى لوحة الإدارة."
MAKE_ADMIN_USAGE = "الاستخدام: /makeadmin <كلمة المرور>"
INCORRECT_PASSWORD = "كلمة مرور غير صحيحة."
ALREADY_ADMIN = "أنت بالفعل مشرف."
NOW_ADMIN = "أنت الآن مشرف."
ADDED_AS_ADMIN = "تمت إضافتك كمشرف."
NO_PERMISSION_LIST_USERS = "ليس لديك صلاحية لعرض قائمة المستخدمين."
USER_LIST_HEADER = "قائمة المستخدمين:\n"
USER_INFO = "المعرف: {id}، معرف تيليجرام: {telegram_id}، مشرف: {is_admin}"
NO_PERMISSION_MODIFY_ADMIN = "ليس لديك صلاحية لتعديل حالة المشرف."
ENTER_TELEGRAM_ID = "الرجاء إدخال معرف تيليجرام للمستخدم لـ {action} كمشرف."
INVALID_TELEGRAM_ID = "معرف تيليجرام غير صالح. الرجاء إدخال رقم صالح."
USER_NOT_FOUND = "لم يتم العثور على المستخدم بمعرف تيليجرام {target_id}."
ADMIN_STATUS_CHANGED = "تم {action} المستخدم بمعرف تيليجرام {target_id} {status} مشرف."
USERNAME_USAGE = "الاستخدام: /username <معرف_تيليجرام>"
USERNAME_RESULT = """معلومات المستخدم للمعرف {id}:
اسم المستخدم: @{username}
الاسم الأول: {first_name}
الاسم الأخير: {last_name}"""
USER_NOT_FOUND = "لم يتم العثور على المستخدم بهذا المعرف."
TELEGRAM_API_ERROR = "حدث خطأ أثناء جلب معلومات المستخدم. الرجاء المحاولة مرة أخرى لاحقًا."
NO_ADMIN_PERMISSION = "عذرًا، هذا الأمر متاح للمشرفين فقط."

# PDF Utilities strings
PDF_UTILS_BUTTON = "📄 أدوات PDF"
PDF_UTILS_MENU = "قائمة أدوات PDF:"
PHOTO_TO_PDF = "تحويل صور إلى PDF"
SEND_PHOTOS_FOR_PDF = "الرجاء إرسال الصور التي تريد تحويلها إلى PDF. عندما تنتهي، اضغط على 'إنهاء إنشاء PDF'."
PDF_CREATION_ERROR = "حدث خطأ أثناء إنشاء ملف PDF: {error}"
PDF_CREATED_SUCCESSFULLY = "تم إنشاء ملف PDF بنجاح! إليك الملف المحول."
PHOTO_ADDED_TO_PDF = "تمت إضافة الصورة. يمكنك إرسال المزيد من الصور أو الضغط على 'إنهاء إنشاء PDF' عند الانتهاء."
FINISH_PDF_CREATION = "إنهاء إنشاء PDF"
CANCEL_PDF_CREATION = "إلغاء إنشاء PDF"
PDF_CREATION_CANCELLED = "تم إلغاء إنشاء ملف PDF."
NO_PHOTOS_FOR_PDF = "لم يتم إرسال أي صور. الرجاء إرسال صورة واحدة على الأقل لإنشاء ملف PDF."


# Group-related messages
GROUPS_BUTTON = "👥 المجموعات"
GROUPS_MENU = "قائمة المجموعات:"
CREATE_GROUP = "إنشاء مجموعة جديدة"
VIEW_GROUPS = "عرض المجموعات"
ADD_USER_TO_GROUP = "إضافة مستخدم إلى مجموعة"
ENTER_GROUP_NAME = "الرجاء إدخال اسم العنوان:"
GROUP_CREATED_SUCCESSFULLY = "تم إنشاء المجموعة '{group_name}' بنجاح."
GROUP_ALREADY_EXISTS = "المجموعة '{group_name}' موجودة بالفعل."
NO_GROUPS_AVAILABLE = "لا توجد مجموعات متاحة."
AVAILABLE_GROUPS = "المجموعات المتاحة:\n"
SELECT_GROUP_TO_ADD_USER = "اختر مجموعة لإضافة مستخدم إليها:"
ENTER_NAME_TO_ADD = "أدخل اسم المستخدم الذي تريد إضافته:"
USER_ADDED_TO_GROUP_SUCCESSFULLY = "تمت إضافة المستخدم '{name}' إلى المجموعة '{group_name}' بنجاح."
USER_ALREADY_IN_GROUP = "المستخدم '{name}' موجود بالفعل في المجموعة '{group_name}'."
USER_NOT_FOUND = "لم يتم العثور على المستخدم. تأكد من إدخال الاسم بشكل صحيح."
EDIT_MEMBER = "تعديل اسم عضو"
DELETE_MEMBER = "حذف عضو"
SELECT_GROUP_TO_EDIT_MEMBER = "اختر المجموعة التي تريد تعديل أحد أعضائها:"
SELECT_MEMBER_TO_EDIT = "اختر العضو الذي تريد تعديل اسمه:"
ENTER_NEW_MEMBER_NAME = "أدخل الاسم الجديد للعضو:"
MEMBER_UPDATED_SUCCESSFULLY = "تم تحديث اسم العضو إلى '{new_name}' بنجاح."
SELECT_GROUP_TO_DELETE_MEMBER = "اختر المجموعة التي تريد حذف أحد أعضائها:"
SELECT_MEMBER_TO_DELETE = "اختر العضو الذي تريد حذفه:"
CONFIRM_MEMBER_DELETE = "هل أنت متأكد أنك تريد حذف العضو '{member_name}'؟"
MEMBER_DELETED_SUCCESSFULLY = "تم حذف العضو '{member_name}' بنجاح."
MEMBER_DELETION_CANCELLED = "تم إلغاء حذف العضو."
NO_MEMBERS_IN_GROUP = "لا يوجد أعضاء في هذه المجموعة."
EDIT_GROUP = "تعديل مجموعة"
DELETE_GROUP = "حذف مجموعة"
SELECT_GROUP_TO_EDIT = "اختر المجموعة التي تريد تعديلها:"
ENTER_NEW_GROUP_NAME = "أدخل الاسم الجديد للعنوان:"
GROUP_UPDATED_SUCCESSFULLY = "تم تحديث اسم المجموعة إلى '{new_name}' بنجاح."
SELECT_GROUP_TO_DELETE = "اختر المجموعة التي تريد حذفها:"
CONFIRM_GROUP_DELETE = "هل أنت متأكد أنك تريد حذف المجموعة '{group_name}'؟"
GROUP_DELETED_SUCCESSFULLY = "تم حذف المجموعة '{group_name}' بنجاح."
GROUP_DELETION_CANCELLED = "تم إلغاء حذف المجموعة."
NO_PERMISSION = "عذرًا، ليس لديك صلاحية للقيام بهذا الإجراء."
RETURN_TO_MAIN_MENU = "العودة"
# Error messages
USER_NOT_FOUND_ERROR = "لم يتم العثور على المستخدم. الرجاء المحاولة مرة أخرى."
SUBJECT_NOT_FOUND_ERROR = "لم يتم العثور على المادة."
GENERAL_ERROR_MESSAGE = "عذرًا، حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى لاحقًا."
DATABASE_ERROR_MESSAGE = "عذرًا، حدث خطأ في قاعدة البيانات. يرجى المحاولة مرة أخرى لاحقًا."
TELEGRAM_API_ERROR_MESSAGE = "عذرًا، حدث خطأ في واجهة برمجة تطبيقات تيليجرام. يرجى المحاولة مرة أخرى لاحقًا."