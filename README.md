<div dir="rtl">

# API مدیریت کتابخانه (Library Management API)

یک API ساده برای مدیریت کتاب‌های کتابخانه، ساخته‌شده با FastAPI. کتاب‌ها داخل حافظه‌ی برنامه نگهداری می‌شوند و از دیتابیس استفاده نشده است.

## قابلیت‌ها

| متد | آدرس | توضیح |
|---|---|---|
| `GET` | `/books` | دریافت لیست همه‌ی کتاب‌ها |
| `POST` | `/books` | اضافه کردن یک کتاب جدید |
| `GET` | `/books/{book_id}` | دریافت اطلاعات یک کتاب با شناسه‌ی آن |
| `PATCH` | `/books/{book_id}` | تغییر بخشی از اطلاعات یک کتاب |
| `DELETE` | `/books/{book_id}` | حذف یک کتاب با شناسه‌ی آن |

## فیلدهای کتاب

| فیلد | نوع | اجباری |
|---|---|---|
| `title` | متن | بله |
| `author` | متن | بله |
| `publication_year` | عدد | خیر |
| `publisher` | متن | خیر |

شناسه‌ی هر کتاب (`id`) را برنامه خودش می‌سازد، از عدد ۱ شروع می‌شود و برای هر کتاب جدید یکی بیشتر می‌شود.

## تکنولوژی‌ها

- Python نسخه‌ی ۳.۱۰ یا بالاتر
- FastAPI
- Pydantic
- Uvicorn

## نصب و اجرا (ویندوز، PowerShell)

</div>

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

<div dir="rtl">

بعد از اجرا، آدرس زیر را در مرورگر باز کنید تا بتوانید همه‌ی مسیرها را امتحان کنید:

http://127.0.0.1:8000/docs

## نمونه‌ی درخواست‌ها

### اضافه کردن کتاب

یک درخواست `POST` به آدرس `/books` با این بدنه‌ی JSON بفرستید:

</div>

```json
{
  "title": "The Little Prince",
  "author": "Antoine de Saint-Exupery",
  "publication_year": 1943,
  "publisher": "Reynal & Hitchcock"
}
```

<div dir="rtl">

### تغییر فقط عنوان کتاب

یک درخواست `PATCH` به آدرس `/books/1` بفرستید. فقط فیلدهایی که می‌فرستید تغییر می‌کنند:

</div>

```json
{
  "title": "The Little Prince - Updated Edition"
}
```

<div dir="rtl">

### دریافت و حذف کتاب

- `GET /books/1` اطلاعات کتابی که شناسه‌اش ۱ است را برمی‌گرداند.
- `DELETE /books/1` همان کتاب را حذف می‌کند.

اگر کتابی با شناسه‌ی داده‌شده وجود نداشته باشد، پاسخ `404` با پیام `Book not found` برمی‌گردد.

## ذخیره‌سازی داده‌ها

کتاب‌ها داخل یک دیکشنری پایتون در حافظه نگهداری می‌شوند و از دیتابیس استفاده نشده است. با بستن یا ری‌استارت شدن برنامه، همه‌ی داده‌ها پاک می‌شوند.

## ساختار پروژه

</div>

```text
library-management-api/
├── main.py            # کد برنامه و مسیرهای API
├── requirements.txt   # کتابخانه‌های مورد نیاز
├── README.md          # توضیحات پروژه
└── .gitignore
```
