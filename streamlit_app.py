import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta ,date
import hashlib
import plotly.express as px
import json
import requests
from PIL import Image
import io
import base64
import time



# إعدادات الصفحة
st.set_page_config(
    page_title="نظام إدارة الموارد البشرية ",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# قائمة الوظائف الشائعة في الصوامع والتخزين
JOB_TITLES = [
    "مدير مخازن",
    "مشرف مخازن", 
    "أمين مخزن / أمين مستودع",
    "مساعد أمين مخزن",
    "فني تخزين",
    "كاتب مخازن / مدخل بيانات",
    "مراجع مخازن / أخصائي شئون إدارية",
    "وزان",
    "مهندس ميكانيكا",
    "مهندس كهرباء",
    "فني كهرباء",
    "فني ميكانيكا",
    "فني زراعي",
    "مشغل رافعة",
    "منتقي بضائع",
    "مسؤول تعبئة وتغليف",
    "سائق",
    "سائق لودر",
    "عامل حرفي",
    "عامل تخزين",
    "أمن",
    "نظافة",
    "فني أمن وسلامة",
    "محاسب",
    "مراجع مالي",
    "مدير إداري",
    "موظف استقبال",
    "مندوب مبيعات",
    "مندوب توصيل",
    "أخرى"
]

# استبدل كل الـ CSS اللي في الكود بـ CSS واحد متكامل وواضح

# ====== CSS الأصلي المحسن ======
st.markdown("""
    <style>
    /* استخدام خط عربي نظامي بدون نت */
    html, body, [class*="css"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif' !important;
    }
            
    /* تطبيق RTL على كل الصفحة */
    html, body, [class*="css"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
    }

    /* تعديلات خاصة */
    .main { direction: rtl !important; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3em; 
        font-weight: 600;
        direction: rtl;
    }
    .stTextInput>div>div>input { 
        border-radius: 10px; 
        text-align: right !important;
        direction: rtl;
    }
    .stSelectbox>div>div>div { text-align: right !important; }
    .stNumberInput>div>div>input { text-align: right !important; }
    .stDateInput>div>div>input { text-align: right !important; }
    .stTextArea>div>div>textarea { 
        text-align: right !important; 
        direction: rtl;
    }

    /* الجداول */
    .stDataFrame { direction: rtl; }
    .stDataFrame th { text-align: right !important; }
    .stDataFrame td { text-align: right !important; }

    /* العناوين */
    h1, h2, h3, h4, h5, h6 { 
        color: #2c3e50; 
        font-weight: 700;
        text-align: right !important;
    }

    /* البطاقات */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; 
        border-radius: 15px; 
        color: white;
        text-align: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        direction: rtl;
    }
    .metric-value { font-size: 2.5em; font-weight: bold; margin: 10px 0; }

    /* الحالات */
    .status-active { background-color: #27ae60; color: white; padding: 5px 15px; border-radius: 20px; }
    .status-resigned { background-color: #e74c3c; color: white; padding: 5px 15px; border-radius: 20px; }
    .status-retired { background-color: #f39c12; color: white; padding: 5px 15px; border-radius: 20px; }

    /* Sidebar - نتركه زي ما هو */
    .css-1d391kg { direction: rtl; }
    .css-1d391kg .stRadio > label { 
        flex-direction: row-reverse;
        text-align: right;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        direction: rtl;
    }

    /* Containers */
    .stContainer { direction: rtl; }

    /* Expander */
    .streamlit-expanderHeader {
        direction: rtl;
        text-align: right;
    }

    /* Select boxes alignment */
    div[data-baseweb="select"] > div {
        direction: rtl;
        text-align: right;
    }

    /* Fix for columns */
    .row-widget.stHorizontalBlock {
        direction: rtl;
        flex-direction: row-reverse;
    }

    /* عكس اتجاه الجدول بالكامل */
    .stDataFrame, .stTable {
        direction: rtl !important;
    }
    
    /* عكس ترتيب الأعمدة - مهم جداً */
    .stDataFrame [data-testid="stDataFrameResizable"] {
        direction: rtl;
    }
    
    /* تحسين عام للأزرار */
    .stButton button {
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
   
    /* ========== إخفاء السايدبار تلقائياً في الشاشات الصغيرة ========== */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        
        /* تقليل حجم الخط في الموبايل */
        .stMarkdown h1 {
            font-size: 1.5rem !important;
        }
        .stMarkdown h2 {
            font-size: 1.2rem !important;
        }
        .stMarkdown h3 {
            font-size: 1rem !important;
        }
        
        /* جعل الأعمدة تتراصف فوق بعض في الموبايل */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        
        /* توسيط الأزرار */
        .stButton button {
            width: 100% !important;
            margin-bottom: 5px;
        }
        
        /* تقليل padding */
        .block-container {
            padding: 1rem !important;
        }
        
        /* جعل الجداول قابلة للتمرير */
        .stDataFrame {
            overflow-x: auto !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
# دوال قاعدة البيانات
def get_db_connection():
    return sqlite3.connect('hr_system.db', timeout=30.0)  # <-- زودنا timeout

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if 'show_menu' not in st.session_state:
        st.session_state.show_menu = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = None    


# ==================== دوال الرصيد الذكي للإجازات (محسنة) ====================
def send_whatsapp_message(phone, message):
    """إرسال رسالة WhatsApp باستخدام pywhatkit"""
    from zk import ZK
    from zk.base import ZKHelper
    # التحقق من وجود المكتبة
    if not PYWHATKIT_AVAILABLE:
        st.error("❌ مكتبة pywhatkit غير مثبتة!")
        st.info("💡 لتثبيتها شغل: pip install pywhatkit")
        return False
    
    try:
        import webbrowser
        import os
        
        # تنسيق الرقم
        phone_formatted = str(phone).replace(" ", "").replace("-", "")
        if not phone_formatted.startswith("+"):
            phone_formatted = "+20" + phone_formatted.lstrip("0")
        
        print(f"📱 محاولة إرسال رسالة إلى: {phone_formatted}")
        
        # إرسال الرسالة
        pywhatkit.sendwhatmsg_instantly(
            phone=phone_formatted,
            message=message,
            wait_time=15,
            tab_close=True,
            close_time=5
        )
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إرسال WhatsApp: {e}")
        return False

def send_notification(employee_id, message_type, message, details=None):
    """
    إرسال إشعار داخلي للموظف (بدل WhatsApp - Offline)
    
    Parameters:
        employee_id: ID الموظف
        message_type: نوع الإشعار ('leave_approved', 'leave_rejected', 'overtime_approved', 'general')
        message: نص الإشعار
        details: تفاصيل إضافية (اختياري - dict)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # إضافة تفاصيل للرسالة لو موجودة
        if details:
            extra_info = []
            if 'start_date' in details:
                extra_info.append(f"من: {details['start_date']}")
            if 'end_date' in details:
                extra_info.append(f"إلى: {details['end_date']}")
            if 'days_count' in details:
                extra_info.append(f"المدة: {details['days_count']} أيام")
            if 'remaining_balance' in details:
                extra_info.append(f"الرصيد المتبقي: {details['remaining_balance']} يوم")
            
            if extra_info:
                message += "\n" + " | ".join(extra_info)
        
        # حفظ الإشعار في قاعدة البيانات
        cursor.execute("""
            INSERT INTO notifications (employee_id, type, message, is_read, created_at)
            VALUES (?, ?, ?, 0, datetime('now'))
        """, (employee_id, message_type, message))
        
        notification_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # طباعة في اللوج للتتبع
        print(f"🔔 إشعار #{notification_id} للموظف #{employee_id}: {message[:60]}...")
        
        return notification_id
        
    except Exception as e:
        print(f"❌ خطأ في إرسال الإشعار: {e}")
        return None


def mark_notification_as_read(notification_id):
    """تحديد إشعار كمقروء"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE notifications 
            SET is_read = 1, read_at = datetime('now')
            WHERE id = ?
        """, (notification_id,))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث الإشعار: {e}")
        return False


def get_unread_notifications(employee_id, limit=10):
    """جلب الإشعارات غير المقروءة للموظف"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, type, message, created_at
            FROM notifications
            WHERE employee_id = ? AND is_read = 0
            ORDER BY created_at DESC
            LIMIT ?
        """, (employee_id, limit))
        
        notifications = cursor.fetchall()
        conn.close()
        
        return notifications
        
    except Exception as e:
        print(f"❌ خطأ في جلب الإشعارات: {e}")
        return []


def show_notifications_badge(user):
    """عرض عدد الإشعارات غير المقروءة"""
    
    if not user or not user.get('employee_id'):
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) FROM notifications 
        WHERE employee_id = ? AND is_read = 0
    """, (user['employee_id'],))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    if count > 0:
        st.sidebar.markdown(f"""
            <div style="background-color: #e74c3c; color: white; padding: 10px; 
                        border-radius: 10px; text-align: center; margin-bottom: 10px;">
                🔔 لديك {count} إشعار جديد
            </div>
        """, unsafe_allow_html=True)

def get_or_create_leave_balance(employee_id):
    """
    جلب أو إنشاء رصيد إجازات الموظف للسنة الحالية
    بناءً على قانون العمل المصري 2025
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    current_year = datetime.now().year
    
    try:
        # التحقق من وجود رصيد للسنة الحالية
        cursor.execute("""
            SELECT id, annual_entitled, annual_used, annual_remaining,
                   casual_entitled, casual_used, casual_remaining, year
            FROM leave_balances 
            WHERE employee_id = ? AND year = ?
        """, (employee_id, current_year))
        
        balance = cursor.fetchone()
        
        if not balance:
            # إنشاء رصيد جديد للسنة الحالية
            annual_entitled, years_service = calculate_annual_leave_entitlement(employee_id)
            casual_entitled = calculate_casual_leave_entitlement(employee_id)
            
            cursor.execute("""
                INSERT INTO leave_balances 
                (employee_id, year, annual_entitled, annual_used, annual_remaining,
                 casual_entitled, casual_used, casual_remaining)
                VALUES (?, ?, ?, 0, ?, ?, 0, ?)
            """, (employee_id, current_year, annual_entitled, annual_entitled,
                   casual_entitled, casual_entitled))
            
            conn.commit()
            
            balance = {
                'annual_entitled': annual_entitled,
                'annual_used': 0,
                'annual_remaining': annual_entitled,
                'casual_entitled': casual_entitled,
                'casual_used': 0,
                'casual_remaining': casual_entitled,
                'year': current_year
            }
        else:
            balance = {
                'annual_entitled': balance[1],
                'annual_used': balance[2],
                'annual_remaining': balance[3],
                'casual_entitled': balance[4],
                'casual_used': balance[5],
                'casual_remaining': balance[6],
                'year': balance[7]
            }
        
        return balance
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            st.warning("⏳ قاعدة البيانات مشغولة، جاري المحاولة...")
            time.sleep(1)
            return get_or_create_leave_balance(employee_id)
        raise
    finally:
        conn.close()


def calculate_annual_leave_entitlement(employee_id):
    """
    حساب الأيام المستحقة للإجازة السنوية بناءً على قانون العمل المصري 2025
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # جلب تاريخ التعيين (بدون birth_date لو مش موجود)
        try:
            cursor.execute("SELECT hire_date, birth_date FROM employees WHERE id = ?", (employee_id,))
        except sqlite3.OperationalError:
            cursor.execute("SELECT hire_date, NULL as birth_date FROM employees WHERE id = ?", (employee_id,))
        
        result = cursor.fetchone()
        
        if not result or not result[0]:
            return 15, 0
        
        hire_date_str = result[0]
        
        try:
            hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d')
        except:
            return 15, 0
        
        today = datetime.now()
        years_service = (today - hire_date).days / 365.25
        
        if years_service < 1:
            entitled_days = 15
        elif years_service < 10:
            entitled_days = 21
        else:
            entitled_days = 30
        
        return entitled_days, years_service
    finally:
        conn.close()


def calculate_casual_leave_entitlement(employee_id):
    """
    حساب الأيام المستحقة للإجازة العارضة
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT hire_date FROM employees WHERE id = ?", (employee_id,))
        result = cursor.fetchone()
        
        if not result or not result[0]:
            return 0
        
        hire_date = datetime.strptime(result[0], '%Y-%m-%d')
        today = datetime.now()
        years_service = (today - hire_date).days / 365.25
        
        if years_service >= 1:
            return 7
        else:
            return 0
    finally:
        conn.close()


def restore_leave_balance(employee_id, leave_type_id, days_count):
    """
    استرجاع رصيد الإجازات عند رفض الطلب
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    current_year = datetime.now().year
    
    try:
        cursor.execute("SELECT name FROM leave_types WHERE id = ?", (leave_type_id,))
        leave_type = cursor.fetchone()
        
        if leave_type:
            leave_name = leave_type[0].lower()
            
            cursor.execute("""
                SELECT annual_used, casual_used, annual_entitled, casual_entitled
                FROM leave_balances 
                WHERE employee_id = ? AND year = ?
            """, (employee_id, current_year))
            
            result = cursor.fetchone()
            if result:
                annual_used, casual_used, annual_entitled, casual_entitled = result
                
                if 'عارضة' in leave_name or 'casual' in leave_name:
                    # استرجاع العارضة مع التأكد من عدم التجاوز
                    new_casual_used = max(0, casual_used - days_count)
                    
                    cursor.execute("""
                        UPDATE leave_balances 
                        SET casual_used = ?,
                            casual_remaining = ? - ?
                        WHERE employee_id = ? AND year = ?
                    """, (new_casual_used, casual_entitled, new_casual_used, employee_id, current_year))
                else:
                    # استرجاع السنوية مع التأكد من عدم التجاوز
                    new_annual_used = max(0, annual_used - days_count)
                    
                    cursor.execute("""
                        UPDATE leave_balances 
                        SET annual_used = ?,
                            annual_remaining = ? - ?
                        WHERE employee_id = ? AND year = ?
                    """, (new_annual_used, annual_entitled, new_annual_used, employee_id, current_year))
        
        conn.commit()
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            st.warning("⏳ قاعدة البيانات مشغولة، جاري المحاولة...")
            time.sleep(1)
            restore_leave_balance(employee_id, leave_type_id, days_count)
            return
        raise
    finally:
        conn.close()


def deduct_leave_balance(employee_id, leave_type_id, days_count):
    """
    خصم رصيد الإجازات عند قبول الطلب
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    current_year = datetime.now().year
    
    try:
        cursor.execute("SELECT name FROM leave_types WHERE id = ?", (leave_type_id,))
        leave_type = cursor.fetchone()
        
        if leave_type:
            leave_name = leave_type[0].lower()
            
            if 'عارضة' in leave_name or 'casual' in leave_name:
                cursor.execute("""
                    UPDATE leave_balances 
                    SET casual_used = casual_used + ?,
                        casual_remaining = MAX(0, casual_remaining - ?)
                    WHERE employee_id = ? AND year = ?
                """, (days_count, days_count, employee_id, current_year))
            else:
                cursor.execute("""
                    UPDATE leave_balances 
                    SET annual_used = annual_used + ?,
                        annual_remaining = MAX(0, annual_remaining - ?)
                    WHERE employee_id = ? AND year = ?
                """, (days_count, days_count, employee_id, current_year))
        
        conn.commit()
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            st.warning("⏳ قاعدة البيانات مشغولة، جاري المحاولة...")
            time.sleep(1)
            deduct_leave_balance(employee_id, leave_type_id, days_count)
            return
        raise
    finally:
        conn.close()
# ==================== صفحة تسجيل الدخول ====================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; padding: 2em 0;'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/921/921347.png", width=100)
        st.title("👔 نظام إدارة الموارد البشرية")
        st.markdown("### تسجيل الدخول")

        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")

            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submitted = st.form_submit_button("تسجيل الدخول", use_container_width=True)

            if submitted and username and password:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.id, u.employee_id, u.role, e.full_name, e.department_id, d.name as dept_name
                    FROM users u
                    LEFT JOIN employees e ON u.employee_id = e.id
                    LEFT JOIN departments d ON e.department_id = d.id
                    WHERE u.username = ? AND u.password_hash = ? AND u.is_active = 1
                """, (username, hash_password(password)))
                user = cursor.fetchone()
                conn.close()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        'id': user[0], 'employee_id': user[1], 'role': user[2],
                        'full_name': user[3], 'department_id': user[4], 'dept_name': user[5]
                    }
                    st.success("✅ تم تسجيل الدخول!")
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")

        with st.expander("🔑 بيانات تجريبية"):
            st.markdown("**Admin:** `admin` / `admin123`<br>**HR:** `hr1` / `hr123`<br>**Manager:** `manager1` / `mgr123`<br>**Employee:** `emp[الكود]` / `123456`", unsafe_allow_html=True)

# ==================== صفحات الموظف العادي ====================
def show_employee_leaves(user):
    """عرض إجازات الموظف بتصميم محسن مع الرصيد الذكي"""
    st.title("📋 إجازاتي")

    # جلب الرصيد الذكي
    balance = get_or_create_leave_balance(user['employee_id'])
    annual_entitled, years_service = calculate_annual_leave_entitlement(user['employee_id'])
    casual_entitled = calculate_casual_leave_entitlement(user['employee_id'])

    # عرض بطاقات الرصيد
    st.markdown("### 📊 رصيد إجازاتك")

    col1, col2, col3 = st.columns(3)

    with col1:
        # تحديد لون البطاقة حسب سنوات الخدمة
        if years_service < 1:
            card_color = "#e74c3c"  # أحمر للعقد
            status_text = "عقد (أول سنة)"
        elif years_service < 10:
            card_color = "#27ae60"  # أخضر
            status_text = "دائم (1-10 سنة)"
        else:
            card_color = "#9b59b6"  # بنفسجي
            status_text = "قديم (+10 سنوات)"

        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {card_color} 0%, {card_color}dd 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <div style="font-size: 0.9em; opacity: 0.9;">{status_text}</div>
                <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">
                    {balance['annual_remaining']} / {balance['annual_entitled']}
                </div>
                <div style="font-size: 1em;">إجازة سنوية (يوم)</div>
                <div style="font-size: 0.8em; margin-top: 5px; opacity: 0.9;">
                    مستخدم: {balance['annual_used']} | متبقي: {balance['annual_remaining']}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        casual_color = "#3498db" if balance['casual_entitled'] > 0 else "#95a5a6"
        casual_text = f"{balance['casual_remaining']} / {balance['casual_entitled']}" if balance['casual_entitled'] > 0 else "غير مستحق"

        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {casual_color} 0%, {casual_color}dd 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <div style="font-size: 0.9em; opacity: 0.9;">إجازات عارضة</div>
                <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">
                    {casual_text}
                </div>
                <div style="font-size: 1em;">عارضة (يوم)</div>
                {'<div style="font-size: 0.8em; margin-top: 5px; opacity: 0.9;">متاحة بعد أول سنة</div>' if balance['casual_entitled'] == 0 else f'<div style="font-size: 0.8em; margin-top: 5px; opacity: 0.9;">مستخدم: {balance["casual_used"]} | متبقي: {balance["casual_remaining"]}</div>'}
            </div>
        """, unsafe_allow_html=True)

    with col3:
        total_remaining = balance['annual_remaining'] + balance['casual_remaining']
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <div style="font-size: 0.9em; opacity: 0.9;">إجمالي الرصيد</div>
                <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">
                    {total_remaining}
                </div>
                <div style="font-size: 1em;">يوم متبقي</div>
                <div style="font-size: 0.8em; margin-top: 5px; opacity: 0.9;">
                    سنة {datetime.now().year}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # معلومات سنوات الخدمة
    st.markdown(f"""
        <div style="background-color: #ecf0f1; padding: 10px 20px; border-radius: 10px; margin: 15px 0; text-align: center;">
            📅 <strong>سنوات خدمتك:</strong> {years_service:.1f} سنة 
            <span style="color: #7f8c8d; margin: 0 10px;">|</span>
            🎯 <strong>المرحلة:</strong> {"أول سنة (15 يوم)" if years_service < 1 else "1-10 سنوات (21 يوم)" if years_service < 10 else "+10 سنوات (30 يوم)"}
        </div>
    """, unsafe_allow_html=True)

    conn = get_db_connection()

    # جلب الإجازات
    leaves = pd.read_sql_query("""
        SELECT lt.name as leave_type, lr.start_date, lr.end_date, 
               lr.days_count, lr.reason, lr.status, lr.requested_at,
               CASE 
                   WHEN lr.status = 'approved' THEN '✅ مقبولة'
                   WHEN lr.status = 'rejected' THEN '❌ مرفوضة'
                   ELSE '⏳ معلقة'
               END as status_display,
               CASE 
                   WHEN lr.status = 'approved' THEN '#27ae60'
                   WHEN lr.status = 'rejected' THEN '#e74c3c'
                   ELSE '#f39c12'
               END as status_color
        FROM leave_requests lr
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        WHERE lr.employee_id = ?
        ORDER BY lr.requested_at DESC
    """, conn, params=(user['employee_id'],))

    conn.close()

    if leaves.empty:
        st.info("📭 لم تقم بتقديم أي طلبات إجازة بعد")
        st.markdown("💡 اضغط على 'طلب إجازة جديدة' من القائمة لتقديم طلب")
    else:
        # إحصائيات
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("إجمالي الطلبات", len(leaves))
        with col2:
            approved = len(leaves[leaves['status'] == 'approved'])
            st.metric("✅ المقبولة", approved)
        with col3:
            pending = len(leaves[leaves['status'] == 'pending'])
            st.metric("⏳ المعلقة", pending)
        with col4:
            rejected = len(leaves[leaves['status'] == 'rejected'])
            st.metric("❌ المرفوضة", rejected)

        st.markdown("---")
        st.subheader("📋 تاريخ طلباتك")

        # عرض الإجازات في cards
        for _, row in leaves.iterrows():
            with st.container():
                # Card design
                st.markdown(f"""
                    <div style="border-right: 5px solid {row['status_color']}; 
                                background-color: #f8f9fa; 
                                padding: 15px; 
                                border-radius: 10px; 
                                margin-bottom: 15px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{row['leave_type']}</h4>
                                <div style="color: #666; margin-bottom: 5px;">
                                    📅 <strong>من:</strong> {row['start_date']} | <strong>إلى:</strong> {row['end_date']}
                                </div>
                                <div style="color: #666; margin-bottom: 5px;">
                                    ⏱️ <strong>المدة:</strong> {row['days_count']} أيام
                                </div>
                                <div style="color: #888; font-size: 0.9em;">
                                    📝 {row['reason']}
                                </div>
                            </div>
                            <div style="text-align: center; margin-right: 20px;">
                                <div style="background-color: {row['status_color']}; 
                                            color: white; 
                                            padding: 8px 20px; 
                                            border-radius: 20px; 
                                            font-weight: bold;">
                                    {row['status_display']}
                                </div>
                                <div style="color: #999; font-size: 0.8em; margin-top: 5px;">
                                    {row['requested_at'][:10]}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # زر طلب إجازة جديدة
        st.markdown("---")
        if st.button("➕ طلب إجازة جديدة", type="primary", use_container_width=True):
            st.session_state.page = "➕ طلب إجازة جديدة"
            st.rerun()
def show_new_leave(user):
    """طلب إجازة جديدة للموظف"""
    st.title("➕ طلب إجازة جديدة")

    conn = get_db_connection()
    leave_types = pd.read_sql_query("SELECT id, name, max_days_per_year FROM leave_types", conn)

    # جلب رصيد الإجازات الحالي
    balance = get_or_create_leave_balance(user['employee_id'])
    
    st.info(f"📊 رصيد إجازاتك السنوية: {balance['annual_remaining']} يوم متبقي من {balance['annual_entitled']}")

    with st.form("new_leave_form"):
        col1, col2 = st.columns(2)

        with col1:
            leave_type = st.selectbox("نوع الإجازة", options=leave_types['name'])
            start_date = st.date_input("تاريخ البداية", min_value=datetime.now().date())

        with col2:
            days = st.number_input("عدد الأيام", min_value=1, max_value=30, value=1)
            end_date = st.date_input("تاريخ النهاية", 
                                    value=start_date + timedelta(days=days-1),
                                    min_value=start_date)

        reason = st.text_area("السبب", placeholder="اكتب سبب الإجازة هنا...")

        submitted = st.form_submit_button("تقديم الطلب", type="primary")

        if submitted:
            if not reason.strip():
                st.error("❌ يرجى كتابة سبب الإجازة")
                return

            # التحقق من الرصيد
            leave_type_id = leave_types[leave_types['name'] == leave_type]['id'].values[0]
            
            if 'عارضة' in leave_type.lower():
                if days > balance['casual_remaining']:
                    st.error(f"❌ رصيدك في الإجازات العارضة غير كافي. متبقي: {balance['casual_remaining']} يوم")
                    return
            else:
                if days > balance['annual_remaining']:
                    st.error(f"❌ رصيدك في الإجازات السنوية غير كافي. متبقي: {balance['annual_remaining']} يوم")
                    return

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leave_requests (employee_id, leave_type_id, start_date, end_date, days_count, reason)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user['employee_id'], int(leave_type_id), start_date, end_date, days, reason))
            conn.commit()
            conn.close()

            st.success("✅ تم تقديم طلب الإجازة بنجاح!")
            st.balloons()
            st.info("⏳ سيتم مراجعة طلبك من قبل HR")


# ==================== إدارة الإجازات (للـ Admin/HR) ====================
def show_leaves_management(user):
    """صفحة إدارة الإجازات للـ Admin و HR"""
    st.title("📋 إدارة طلبات الإجازات")

    # ========== تحديث الرصيد لكل الموظفين ==========
    # عشان نتأكد إن الرصيد محدث قبل ما نعرض الطلبات
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # جلب كل الموظفين اللي عندهم طلبات معلقة
    pending_employees = cursor.execute("""
        SELECT DISTINCT employee_id FROM leave_requests WHERE status = 'pending'
    """).fetchall()
    
    for (emp_id,) in pending_employees:
        get_or_create_leave_balance(emp_id)  # ده بيحدث الرصيد تلقائياً
    
    conn.close()

    conn = get_db_connection()

    # فلاتر
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("حالة الطلب", ["الكل", "معلق", "مقبول", "مرفوض"])
    with col2:
        dept_filter = st.selectbox("الإدارة", ["الكل"] + [d[0] for d in conn.execute("SELECT name FROM departments").fetchall()])
    with col3:
        date_filter = st.date_input("من تاريخ", value=None)

    # بناء الاستعلام
    query = """
        SELECT 
            lr.id,
            e.code as emp_code,
            e.full_name as emp_name,
            d.name as department,
            lt.name as leave_type,
            lr.start_date,
            lr.end_date,
            lr.days_count,
            lr.reason,
            lr.status,
            lr.requested_at,
            lr.leave_type_id,
            lr.employee_id
        FROM leave_requests lr
        JOIN employees e ON lr.employee_id = e.id
        JOIN departments d ON e.department_id = d.id
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        WHERE 1=1
    """

    params = []

    if status_filter == "معلق":
        query += " AND lr.status = 'pending'"
    elif status_filter == "مقبول":
        query += " AND lr.status = 'approved'"
    elif status_filter == "مرفوض":
        query += " AND lr.status = 'rejected'"

    if dept_filter != "الكل":
        query += " AND d.name = ?"
        params.append(dept_filter)

    if date_filter:
        query += " AND lr.start_date >= ?"
        params.append(date_filter.strftime('%Y-%m-%d'))

    query += " ORDER BY lr.requested_at DESC"

    leaves = pd.read_sql_query(query, conn, params=params)
    conn.close()

    # إحصائيات
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي الطلبات", len(leaves))
    with col2:
        pending = len(leaves[leaves['status'] == 'pending']) if not leaves.empty else 0
        st.metric("معلق", pending)
    with col3:
        approved = len(leaves[leaves['status'] == 'approved']) if not leaves.empty else 0
        st.metric("مقبول", approved)
    with col4:
        rejected = len(leaves[leaves['status'] == 'rejected']) if not leaves.empty else 0
        st.metric("مرفوض", rejected)

    st.markdown("---")

    # عرض الطلبات
    if not leaves.empty:
        for _, row in leaves.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

                with col1:
                    st.markdown(f"**{row['emp_name']}**")
                    st.markdown(f"🆔 كود: {row['emp_code']} | 📍 {row['department']}")

                with col2:
                    st.markdown(f"**{row['leave_type']}**")
                    st.markdown(f"📅 {row['start_date']} → {row['end_date']}")
                    st.markdown(f"⏱️ {row['days_count']} أيام")
                    st.caption(f"📝 {row['reason']}")
                    
                    # عرض الرصيد الحالي للموظف
                    emp_balance = get_or_create_leave_balance(row['employee_id'])
                    if 'عارضة' in row['leave_type']:
                        remaining = emp_balance['casual_remaining']
                        entitled = emp_balance['casual_entitled']
                        balance_text = f"عارضة: {remaining}/{entitled}"
                        balance_color = "#3498db" if remaining > 0 else "#e74c3c"
                    else:
                        remaining = emp_balance['annual_remaining']
                        entitled = emp_balance['annual_entitled']
                        balance_text = f"سنوية: {remaining}/{entitled}"
                        balance_color = "#27ae60" if remaining >= row['days_count'] else "#e74c3c"
                    
                    st.markdown(f"""
                        <div style="background-color: {balance_color}; color: white; padding: 5px 10px; 
                                    border-radius: 15px; font-size: 0.85em; display: inline-block; margin-top: 5px;">
                            📊 الرصيد: {balance_text}
                        </div>
                    """, unsafe_allow_html=True)    



            #    with col2:
            #        st.markdown(f"**{row['leave_type']}**")
            #        st.markdown(f"📅 {row['start_date']} → {row['end_date']}")
            #        st.markdown(f"⏱️ {row['days_count']} أيام")
            #        st.caption(f"📝 {row['reason']}")

                with col3:
                    if row['status'] == 'pending':
                        st.markdown("<span style='background-color: #f39c12; color: white; padding: 5px 15px; border-radius: 20px;'>⏳ معلق</span>", unsafe_allow_html=True)
                    elif row['status'] == 'approved':
                        st.markdown("<span style='background-color: #27ae60; color: white; padding: 5px 15px; border-radius: 20px;'>✅ مقبول</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='background-color: #e74c3c; color: white; padding: 5px 15px; border-radius: 20px;'>❌ مرفوض</span>", unsafe_allow_html=True)

                with col4:
                    if row['status'] == 'pending' and user['role'] in ['admin', 'hr']:
                        if st.button("✅ قبول", key=f"app_{row['id']}", use_container_width=True):
                            approve_leave(row['id'], user['id'], row['employee_id'], row['leave_type_id'], row['days_count'])
                            st.rerun()
                        if st.button("❌ رفض", key=f"rej_{row['id']}", use_container_width=True):
                            reject_leave(row['id'], user['id'])
                            st.rerun()

                st.markdown("---")
    else:
        st.info("📭 لا توجد طلبات إجازات مطابقة للفلاتر")


def approve_leave(leave_id, approver_id, employee_id, leave_type_id, days_count):
    """قبول طلب إجازة - مع التحقق من الرصيد وإرسال إشعار WhatsApp"""
    
    # ========== جلب بيانات الطلب ==========
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # جلب تفاصيل الطلب (start_date, end_date)
    cursor.execute("""
        SELECT start_date, end_date, reason 
        FROM leave_requests 
        WHERE id = ?
    """, (leave_id,))
    leave_details = cursor.fetchone()
    
    if not leave_details:
        st.error("❌ لم يتم العثور على تفاصيل الطلب")
        conn.close()
        return False
    
    start_date, end_date, reason = leave_details
    
    # جلب نوع الإجازة
    cursor.execute("SELECT name FROM leave_types WHERE id = ?", (leave_type_id,))
    leave_type_result = cursor.fetchone()
    leave_type_name = leave_type_result[0] if leave_type_result else ""
    
    conn.close()
    
    # ========== التحقق من الرصيد المتبقي ==========
    current_balance = get_or_create_leave_balance(employee_id)
    
    # تحديد نوع الإجازة والرصيد المتبقي الفعلي
    if 'عارضة' in leave_type_name.lower():
        remaining = current_balance['casual_remaining']
        leave_type_display = "العارضة"
    else:
        remaining = current_balance['annual_remaining']
        leave_type_display = "السنوية"
    
    # ========== التحقق: هل الرصيد كافي؟ ==========
    if days_count > remaining:
        st.error(f"❌ لا يمكن قبول الطلب!")
        st.error(f"📊 رصيد الموظف في الإجازات {leave_type_display}: {remaining} يوم")
        st.error(f"📊 الطلب المقدم: {days_count} يوم")
        st.warning(f"⚠️ النقص: {days_count - remaining} يوم")
        
        # رفض تلقائي
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE leave_requests 
            SET status = 'rejected', approved_by = ?, approved_at = datetime('now')
            WHERE id = ?
        """, (approver_id, leave_id))
        conn.commit()
        conn.close()
        
        st.error("❌ تم رفض الطلب تلقائياً بسبب عدم كفاية الرصيد")
        return False
    
    # ========== الرصيد كافي، نكمل القبول ==========
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE leave_requests 
            SET status = 'approved', approved_by = ?, approved_at = datetime('now')
            WHERE id = ?
        """, (approver_id, leave_id))
        
        conn.commit()
        
        # خصم الرصيد
        deduct_leave_balance(employee_id, leave_type_id, days_count)
        
        st.success(f"✅ تم قبول طلب الإجازة!")
        st.success(f"📊 تم خصم {days_count} أيام من رصيد الإجازات {leave_type_display}")
        st.info(f"📊 الرصيد المتبقي: {remaining - days_count} أيام")
        
        # ===== إرسال إشعار داخلي (بدل WhatsApp) =====
        try:
            # جلب بيانات الموظف
            cursor.execute("SELECT full_name FROM employees WHERE id = ?", (employee_id,))
            emp_name = cursor.fetchone()[0]
        
            # تجهيز تفاصيل الإشعار
            details = {
                'start_date': start_date,
                'end_date': end_date,
                'days_count': days_count,
                'remaining_balance': remaining - days_count
            }
        
            message = f"✅ تم قبول طلب إجازتك يا {emp_name}!"
        
            send_notification(
                employee_id=employee_id,
                message_type='leave_approved',
                message=message,
                details=details
            )
        
            st.info("🔔 تم إرسال إشعار داخلي للموظف")
        
        except Exception as e:
            st.warning(f"⚠️ لم يتم إرسال الإشعار: {e}")

    except Exception as e:
        conn.rollback()
        st.error(f"❌ خطأ في قاعدة البيانات: {e}")
        return False
    finally:
        conn.close()
    # ==========================================
def reject_leave(leave_id, approver_id):
    """رفض طلب إجازة - يسترجع الرصيد"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # جلب معلومات الطلب قبل الرفض
    cursor.execute("SELECT employee_id, leave_type_id, days_count FROM leave_requests WHERE id = ?", (leave_id,))
    leave_info = cursor.fetchone()

    cursor.execute("""
        UPDATE leave_requests 
        SET status = 'rejected', approved_by = ?, approved_at = datetime('now')
        WHERE id = ?
    """, (approver_id, leave_id))
    conn.commit()
    conn.close()

    # استرجاع الرصيد
    if leave_info:
        restore_leave_balance(leave_info[0], leave_info[1], leave_info[2])

    st.error("❌ تم رفض طلب الإجازة")
    st.info("📱 تم إرسال إشعار للموظف واسترجاع الرصيد")

def show_employee_summary(user):
    """عرض ملخص منظم للموظف العادي"""
    st.title(f"👋 مرحباً، {user['full_name']}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # بياناتي الأساسية
    cursor.execute("""
        SELECT 
            e.id, e.code, e.full_name, e.department_id, e.job_title,
            e.national_id, e.phone, e.hire_date, e.employment_type,
            e.is_active, e.status_id, e.status_date, e.status_reason,
            e.years_of_service, e.governorate, e.city, e.street,
            e.postal_code, e.education, e.marital_status, 
            e.num_children,           -- ✅ index 20
            e.emergency_contact,      -- ✅ index 21
            e.notes, e.birth_date,
            d.name as dept_name, 
            es.name as status_name
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        JOIN employee_statuses es ON e.status_id = es.id
        WHERE e.id = ?
    """, (user['employee_id'],))
    emp = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]

    if not emp:
        st.error("❌ لم يتم العثور على بيانات الموظف")
        conn.close()
        return

    # ✅ الترتيب الصحيح حسب صورة قاعدة البيانات
    # emp[0-23] = e.* | emp[24] = dept_name | emp[25] = status_name
    emp_dict = dict(zip(columns, emp))
    emp_data = {
        'id': emp_dict.get('id'),
        'code': emp_dict.get('code'),
        'full_name': emp_dict.get('full_name'),
        'department_id': emp_dict.get('department_id'),
        'job_title': emp_dict.get('job_title') or 'غير محدد',
        'national_id': emp_dict.get('national_id') or 'غير مسجل',
        'phone': emp_dict.get('phone') or 'غير مسجل',
        'hire_date': emp_dict.get('hire_date') or 'غير مسجل',
        'employment_type': emp_dict.get('employment_type') or 'غير محدد',
        'is_active': emp_dict.get('is_active'),
        'status_id': emp_dict.get('status_id'),
        'status_date': emp_dict.get('status_date'),
        'status_reason': emp_dict.get('status_reason'),
        'years_of_service': emp_dict.get('years_of_service') if emp_dict.get('years_of_service') is not None else 0,
        'governorate': str(emp_dict.get('governorate')) if emp_dict.get('governorate') else 'غير مسجل',
        'city': str(emp_dict.get('city')) if emp_dict.get('city') else '',
        'street': str(emp_dict.get('street')) if emp_dict.get('street') else '',
        'postal_code': str(emp_dict.get('postal_code')) if emp_dict.get('postal_code') else '',
        'education': str(emp_dict.get('education')) if emp_dict.get('education') else 'غير مسجل',
        'marital_status': str(emp_dict.get('marital_status')) if emp_dict.get('marital_status') else 'غير مسجل',
        'num_children': emp_dict.get('num_children') if emp_dict.get('num_children') is not None else 0,
        'emergency_contact': str(emp_dict.get('emergency_contact')) if emp_dict.get('emergency_contact') is not None else 'غير مسجل',
        'notes': str(emp_dict.get('notes')) if emp_dict.get('notes') else '',
        'birth_date': emp_dict.get('birth_date'),
        'department': emp_dict.get('dept_name') or 'غير مسجل',
        'status': emp_dict.get('status_name') or 'غير مسجل'
    }
    
    # ==== القسم الأول: البطاقة الشخصية ====
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0; text-align: center;">🪪 البطاقة الشخصية</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px;">
                <div style="font-size: 2em; font-weight: bold; color: #667eea;">{emp_data['code']}</div>
                <div style="color: #666; font-size: 0.9em;">كود الموظف</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px;">
                <div style="font-size: 1.2em; font-weight: bold; color: #27ae60;">{emp_data['department']}</div>
                <div style="color: #666; font-size: 0.9em;">الإدارة</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        status_color = "#27ae60" if "نشط" in emp_data['status'] else "#e74c3c"
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px;">
                <div style="font-size: 1.2em; font-weight: bold; color: {status_color};">{emp_data['status']}</div>
                <div style="color: #666; font-size: 0.9em;">الحالة</div>
            </div>
        """, unsafe_allow_html=True)

    # ==== القسم الثاني: البيانات الشخصية ====
    st.markdown("""
        <div style="background-color: #ecf0f1; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin: 0; color: #2c3e50;">📋 البيانات الشخصية</h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 10px; border-right: 4px solid #3498db;">
                <table style="width: 100%;">
        """, unsafe_allow_html=True)
        
        info_items = [
            ("👤 الاسم", emp_data['full_name']),
            ("🎂 الرقم القومي", emp_data['national_id']),
            ("📱 رقم التليفون", emp_data['phone']),
            ("💼 الوظيفة", emp_data['job_title']),
        ]
        
        for label, value in info_items:
            st.markdown(f"""
                <tr>
                    <td style="padding: 8px; color: #7f8c8d; width: 40%;">{label}</td>
                    <td style="padding: 8px; font-weight: 600; color: #2c3e50;">{value}</td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 10px; border-right: 4px solid #e74c3c;">
                <table style="width: 100%;">
        """, unsafe_allow_html=True)
        
        info_items2 = [
            ("📅 تاريخ التعيين", emp_data['hire_date']),
            ("⚖️ الحالة الوظيفية", emp_data['employment_type']),
            ("🎓 المؤهل الدراسي", emp_data['education']),
            ("💍 الحالة الاجتماعية", f"{emp_data['marital_status']} ({emp_data['num_children']} أطفال)"),
        ]
        
        for label, value in info_items2:
            st.markdown(f"""
                <tr>
                    <td style="padding: 8px; color: #7f8c8d; width: 40%;">{label}</td>
                    <td style="padding: 8px; font-weight: 600; color: #2c3e50;">{value}</td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table></div>", unsafe_allow_html=True)

    # ==== القسم الثالث: العنوان ====
    if emp_data['governorate'] != 'غير مسجل':
        st.markdown("""
            <div style="background-color: #ecf0f1; padding: 15px; border-radius: 10px; margin: 20px 0;">
                <h3 style="margin: 0; color: #2c3e50;">🏠 العنوان</h3>
            </div>
        """, unsafe_allow_html=True)
        
        address_parts = [emp_data['governorate'], emp_data['city'], emp_data['street']]
        full_address = " - ".join([str(p) for p in address_parts if p is not None and str(p) != 'غير مسجل'])
        
        st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; border-right: 4px solid #f39c12;">
                <div style="font-size: 1.1em; color: #2c3e50; line-height: 1.6;">
                    📍 {full_address if full_address else 'غير مسجل'}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ==== القسم الرابع: الإحصائيات ====
    st.markdown("""
        <div style="background-color: #ecf0f1; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin: 0; color: #2c3e50;">📊 إحصائياتي</h3>
        </div>
    """, unsafe_allow_html=True)

    # عدد أيام الحضور هذا الشهر
    cursor.execute("""
        SELECT COUNT(DISTINCT punch_date) 
        FROM attendance_logs 
        WHERE employee_id = ? AND strftime('%Y-%m', punch_date) = strftime('%Y-%m', 'now')
    """, (user['employee_id'],))
    attendance_days = cursor.fetchone()[0] or 0

    # عدد الإجازات المقبولة
    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(days_count), 0)
        FROM leave_requests 
        WHERE employee_id = ? AND status = 'approved'
    """, (user['employee_id'],))
    leaves = cursor.fetchone()
    leaves_count = leaves[0] or 0
    leaves_days = leaves[1] or 0

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <div style="font-size: 2.5em; font-weight: bold;">{attendance_days}</div>
                <div style="font-size: 0.9em; opacity: 0.9;">أيام الحضور هذا الشهر</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3498db 0%, #5dade2 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <div style="font-size: 2.5em; font-weight: bold;">{leaves_count}</div>
                <div style="font-size: 0.9em; opacity: 0.9;">عدد الإجازات المقبولة</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #9b59b6 0%, #bb8fce 100%); 
                        padding: 20px; border-radius: 15px; color: white; text-align: center;">
                <div style="font-size: 2.5em; font-weight: bold;">{leaves_days}</div>
                <div style="font-size: 0.9em; opacity: 0.9;">إجمالي أيام الإجازات</div>
            </div>
        """, unsafe_allow_html=True)

    conn.close()

    # ==== روابط سريعة ====
    st.markdown("""
        <div style="background-color: #ecf0f1; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin: 0; color: #2c3e50;">⚡ روابط سريعة</h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 إجازاتي", use_container_width=True, type="primary", key="quick_leaves"):
            st.session_state.current_page = "📋 إجازاتي"
            st.session_state.show_menu = False
            st.rerun()
            
    with col2:
        if st.button("➕ طلب إجازة", use_container_width=True, type="primary", key="quick_new_leave"):
            st.session_state.current_page = "➕ طلب إجازة جديدة"
            st.session_state.show_menu = False
            st.rerun()
            
    with col3:
        if st.button("⏰ سجل الحضور", use_container_width=True, type="primary", key="quick_attendance"):
            st.session_state.current_page = "📊 ملخصي"
            st.session_state.show_menu = False
            st.rerun()

def show_dashboard(user):
    st.title("📊 لوحة التحكم")

    conn = get_db_connection()
    cursor = conn.cursor()

    # إحصائيات
    cursor.execute("SELECT COUNT(*) FROM employees WHERE is_active = 1 AND status_id = 1")
    active_emp = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM employees WHERE status_id = 2")  # مستقيل
    resigned = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM employees WHERE status_id = 3")  # معاش
    retired = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leave_requests WHERE status = 'pending'")
    pending_leaves = cursor.fetchone()[0]

    conn.close()

    # بطاقات
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("الموظفين النشطين", active_emp, "#27ae60"),
        ("مستقيلين", resigned, "#e74c3c"),
        ("متقاعدين", retired, "#f39c12"),
        ("إجازات معلقة", pending_leaves, "#9b59b6")
    ]

    for col, (label, value, color) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f'<div class="metric-card" style="background: {color};"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # رسوم بيانية
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 توزيع الموظفين")
        conn = get_db_connection()
        df = pd.read_sql_query("""
            SELECT es.name as status, COUNT(e.id) as count, es.color
            FROM employee_statuses es
            LEFT JOIN employees e ON es.id = e.status_id AND e.is_active = 1
            GROUP BY es.id
            HAVING count > 0
        """, conn)
        conn.close()

        if not df.empty:
            fig = px.pie(df, values='count', names='status', color='status', color_discrete_map=dict(zip(df['status'], df['color'])))
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📊 الإدارات")
        conn = get_db_connection()
        df = pd.read_sql_query("""
            SELECT d.name, COUNT(e.id) as count 
            FROM departments d 
            LEFT JOIN employees e ON d.id = e.department_id AND e.status_id = 1
            GROUP BY d.id 
            ORDER BY count DESC 
            LIMIT 8
        """, conn)
        conn.close()

        if not df.empty:
            fig = px.bar(df, x='name', y='count', labels={'name': 'الإدارة', 'count': 'العدد'})
            st.plotly_chart(fig, use_container_width=True)

def show_employee_notifications(user):
    """صفحة إشعارات الموظف"""
    st.title("🔔 إشعاراتي")
    
    # جلب الإشعارات
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, message, is_read, created_at
        FROM notifications
        WHERE employee_id = ?
        ORDER BY is_read ASC, created_at DESC
        LIMIT 50
    """, (user['employee_id'],))
    notifications = cursor.fetchall()
    conn.close()
    
    if not notifications:
        st.info("📭 لا توجد إشعارات")
        return
    
    # فصل المقروءة عن غير المقروءة
    unread = [n for n in notifications if n[3] == 0]
    read = [n for n in notifications if n[3] == 1]
    
    # ===== Badge كبير في الأعلى =====
    if unread:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                        color: white; padding: 20px; border-radius: 15px; 
                        text-align: center; margin-bottom: 20px;">
                <div style="font-size: 2.5em;">🔴</div>
                <div style="font-size: 1.5em; font-weight: bold;">
                    لديك {len(unread)} إشعار جديد
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # الإحصائيات
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📬 الكل", len(notifications))
    with col2:
        st.metric("🔴 جديدة", len(unread), delta=f"{len(unread)} غير مقروءة" if unread else None)
    with col3:
        st.metric("✅ مقروءة", len(read))
    
    st.markdown("---")
    
    # عرض الإشعارات غير المقروءة
    if unread:
        st.markdown("### 🔴 إشعارات جديدة (غير مقروءة)")
        
        for notif in unread:
            notif_id, notif_type, message, is_read, created_at = notif
            
            # ألوان حسب النوع
            colors = {
                'leave_approved': ('#d4edda', '#27ae60', '✅'),
                'leave_rejected': ('#f8d7da', '#e74c3c', '❌'),
                'overtime_approved': ('#d1ecf1', '#3498db', '⏰'),
                'general': ('#fff3cd', '#f39c12', '📢')
            }
            bg_color, border_color, icon = colors.get(notif_type, ('#fff3cd', '#f39c12', '📢'))
            
            with st.container():
                col_msg, col_btn = st.columns([4, 1])
                
                with col_msg:
                    st.markdown(f"""
                        <div style="background-color: {bg_color}; padding: 15px; 
                                    border-radius: 10px; border-right: 5px solid {border_color};
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div style="font-size: 1.3em; margin-bottom: 5px;">
                                {icon}
                            </div>
                            <div style="font-weight: bold; color: #2c3e50; margin-bottom: 5px;">
                                {message}
                            </div>
                            <div style="color: #7f8c8d; font-size: 0.85em;">
                                🕐 {created_at}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_btn:
                    # زر "قرأتها" بشكل أنيق
                    if st.button("✅ قرأتها", key=f"read_{notif_id}", 
                                use_container_width=True, type="primary"):
                        mark_notification_as_read(notif_id)
                        st.success("✓ تم")
                        st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # عرض المقروءة
    if read:
        with st.expander(f"📂 الإشعارات المقروءة ({len(read)})", expanded=False):
            for notif in read:
                notif_id, notif_type, message, is_read, created_at = notif
                
                st.markdown(f"""
                    <div style="background-color: #ecf0f1; padding: 10px; 
                                border-radius: 5px; margin-bottom: 5px; opacity: 0.6;">
                        <div style="color: #7f8c8d;">
                            {message}
                        </div>
                        <div style="color: #95a5a6; font-size: 0.75em;">
                            🕐 {created_at} | ✅ تم القراءة
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            # ==================== إدارة الموظفين (CRUD كامل) ====================
def show_employees_management(user):
    st.title("👥 إدارة الموظفين")

    tab1, tab2, tab3 = st.tabs(["📋 قائمة الموظفين", "➕ إضافة موظف", "🔄 حركات الموظفين"])

    # تبويب 1: قائمة الموظفين
    with tab1:
        conn = get_db_connection()

        # فلترة
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 البحث بالاسم أو الكود")
        with col2:
            status_filter = st.selectbox("الحالة", ["الكل", "نشط", "مستقيل", "معاش", "مفصول"])
        with col3:
            dept_filter = st.selectbox("الإدارة", ["الكل"] + [d[0] for d in conn.execute("SELECT name FROM departments").fetchall()])

        # الاستعلام
        query = """
            SELECT 
                e.id,
                e.code,
                e.full_name, 
                d.name as department,
                e.job_title,
                es.name as status,
                es.color as status_color,
                e.national_id,
                e.phone,
                e.hire_date,
                e.employment_type
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            JOIN employee_statuses es ON e.status_id = es.id
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (e.full_name LIKE ? OR e.code LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])

        if status_filter != "الكل":
            query += " AND es.name = ?"
            params.append(status_filter)

        if dept_filter != "الكل":
            query += " AND d.name = ?"
            params.append(dept_filter)

        query += " ORDER BY e.code"

        df = pd.read_sql_query(query, conn, params=params)

        if not df.empty:
            # حذف الأعمدة المؤقتة
            display_df = df.drop(['id', 'status_color'], axis=1, errors='ignore').copy()

            # ترجمة أسماء الأعمدة للعربي
            column_names_ar = {
                'code': 'كود الموظف',
                'full_name': 'اسم الموظف',
                'department': 'الإدارة',
                'job_title': 'الوظيفة',
                'status': 'الحالة',
                'national_id': 'الرقم القومي',
                'phone': 'رقم التليفون',
                'hire_date': 'تاريخ التعيين',
                'employment_type': 'الحالة الوظيفية'
            }
            display_df.rename(columns=column_names_ar, inplace=True)

            st.dataframe(display_df, use_container_width=True, hide_index=True)

                        

            # تعديل/حذف
            st.markdown("---")
            st.subheader("✏️ تعديل بيانات موظف")

            emp_options = [f"{row['code']} - {row['full_name']}" for _, row in df.iterrows()]
            selected = st.selectbox("اختر موظف", emp_options, key="edit_emp_select")

            if selected:
                try:
                    emp_code = int(selected.split(" - ")[0])
                    # إعادة قراءة البيانات من قاعدة البيانات مباشرة
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT e.*, d.name as department, es.name as status_name 
                        FROM employees e
                        JOIN departments d ON e.department_id = d.id
                        JOIN employee_statuses es ON e.status_id = es.id
                        WHERE e.code = ?
                    """, (emp_code,))
                    emp_row = cursor.fetchone()
                    conn.close()

                    if emp_row:
                        # تحويل للـ dict عشان يسهل الاستخدام
                        emp_data = {
                            'id': emp_row[0] or '',
                            'code': emp_row[1],
                            'full_name': emp_row[2] or '',
                            'department': emp_row[-2] or '',
                            'status_name': emp_row[-1] or '',
                            'phone': emp_row[6] or '',
                            'job_title': emp_row[4] or '',
                            'governorate': emp_row[10] if len(emp_row) > 10 else '',
                            'city': emp_row[11] ,
                            'street': emp_row[12],
                            'education': emp_row[13],
                        #    'marital_status': emp_row[14],
                        #    'num_children': emp_row[15],
                        #    'emergency_contact': emp_row[16],
                        #    'birth_date': emp_row[17],
                            'marital_status': str(emp_row[19]) if emp_row[19] else '',
                            'num_children': emp_row[20] if emp_row[20] else 0,
                            'emergency_contact': str(emp_row[21]) if emp_row[21] else '',
                            'birth_date': emp_row[23]
                            
                        }
                    else:
                        st.error("❌ لم يتم العثور على بيانات الموظف")
                        return
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
                    return

                # جلب كل بيانات الموظف من قاعدة البيانات
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.*, d.name as dept_name 
                    FROM employees e 
                    JOIN departments d ON e.department_id = d.id 
                    WHERE e.code = ?
                """, (emp_code,))
                emp_full = cursor.fetchone()
                conn.close()

                if not emp_full:
                    st.error("❌ لم يتم العثور على بيانات الموظف الكاملة")
                    return
                
                 # تحويل للـ dict - emp_full يحتوي على e.* (0-23) + dept_name (24)
                 
                emp_dict = {
                    'id': emp_full[0], 
                    'code': emp_full[1], 
                    'full_name': emp_full[2],
                    'department_id': emp_full[3], 
                    'job_title': emp_full[4],
                    'national_id': emp_full[5], 
                    'phone': emp_full[6],
                    'hire_date': emp_full[7], 
                    'employment_type': emp_full[8],
                    'status_id': emp_full[9],
                    'governorate': str(emp_full[14]) if emp_full[14] else '',
                    'city': str(emp_full[15]) if emp_full[15] else '',
                    'street': str(emp_full[16]) if emp_full[16] else '',
                    'education': str(emp_full[18]) if emp_full[18] else '',
                    'marital_status': str(emp_full[19]) if emp_full[19] else '',
                    'num_children': emp_full[20] if emp_full[20] else 0,
                    'emergency_contact': str(emp_full[21]) if len(emp_full) > 21 and emp_full[21] else 'غير مسجل',
                    'notes': str(emp_full[22]) if emp_full[22] else '',
                    'birth_date': emp_full[23],
                    'dept_name': emp_full[24] if len(emp_full) > 24 else '',
                    'status': emp_full[25] if len(emp_full) > 25 else 'غير مسجل'  # من JOIN
                }
                

                with st.form("edit_employee"):
                    st.subheader("📋 البيانات الشخصية")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        new_name = st.text_input("الاسم الرباعي *", value=emp_dict['full_name'])
                        new_national_id = st.text_input("الرقم القومي *", value=emp_dict['national_id'] if emp_dict['national_id'] else "")
                        new_phone = st.text_input("رقم التليفون", value=emp_dict['phone'] if emp_dict['phone'] else "")
                        governorates = [
                            "القاهرة", "الإسكندرية", "الجيزة", "القليوبية", "المنوفية", 
                            "الغربية", "الشرقية", "الدقهلية", "كفر الشيخ", "البحيرة",
                            "دمياط", "بورسعيد", "الإسماعيلية", "السويس", "شمال سيناء",
                            "جنوب سيناء", "البحر الأحمر", "الفيوم", "بني سويف", "المنيا",
                            "أسيوط", "سوهاج", "قنا", "الأقصر", "أسوان", "الوادي الجديد", "مطروح"
                        ]
                        current_gov = str(emp_dict.get('governorate', ''))
                        gov_index = governorates.index(current_gov) if current_gov in governorates else 0
                        new_governorate = st.selectbox("المحافظة", governorates, index=gov_index)
                        
                        marital_options = ["أعزب", "متزوج", "مطلق", "أرمل"]
                        current_marital = str(emp_dict.get('marital_status', ''))
                        marital_index = marital_options.index(current_marital) if current_marital in marital_options else 0
                        new_marital_status = st.selectbox("الحالة الاجتماعية", marital_options, index=marital_index)
                        
                        num_children_val = int(emp_dict.get('num_children')) if emp_dict.get('num_children') else 0
                        new_num_children = st.number_input("عدد الأطفال", min_value=0, max_value=20, 
                                                          value=num_children_val, key="children_input")

                    #    current_gov = str(emp_dict.get('governorate', ''))
                    #    gov_index = governorates.index(current_gov) if current_gov in governorates else 0
                    #    new_governorate = st.selectbox("المحافظة", governorates, index=gov_index)
                        
                        
                    #    marital_options = ["أعزب", "متزوج", "مطلق", "أرمل"]
                    #    current_marital = str(emp_dict.get('marital_status', ''))
                    #    marital_index = marital_options.index(current_marital) if current_marital in marital_options else 0
                    #    new_marital_status = st.selectbox("الحالة الاجتماعية", marital_options, index=marital_index)
                    #    try:
                    #        num_children_val = int(st.session_state.edit_children) if st.session_state.get('edit_children') else 0
                    #    except (ValueError, TypeError):
                    #        num_children_val = 0
                        
                    #    new_num_children = st.number_input("عدد الأطفال", min_value=0, max_value=20, 
                    #                                      value=num_children_val, key="children_input")
                        
                        
##                        num_children_val = 0
##                        if pd.notna(emp_data.get('num_children')):
##                            try:
##                                num_children_val = int(emp_data['num_children'])
##                            except:
##                                pass
##                        new_num_children = st.number_input("عدد الأطفال", min_value=0, max_value=20, value=num_children_val)

                    with col2:
                        # جلب الإدارات
                        conn = get_db_connection()
                        depts = conn.execute("SELECT id, name FROM departments ORDER BY name").fetchall()
                        conn.close()

                        dept_names = [d[1] for d in depts]
                        current_dept = emp_dict['dept_name'] if emp_dict['dept_name'] else dept_names[0]
                        new_dept = st.selectbox("الإدارة *", dept_names, index=dept_names.index(current_dept) if current_dept in dept_names else 0)

                        # تعديل: حقل الوظيفة أصبح اختيار من متعدد
                        current_job = emp_dict['job_title'] if emp_dict['job_title'] else JOB_TITLES[0]
                        new_job = st.selectbox("الوظيفة *", JOB_TITLES, index=JOB_TITLES.index(current_job) if current_job in JOB_TITLES else 0)

                        new_emp_type = st.selectbox("الحالة الوظيفية", 
                                                   ["دائم", "عقد", "إعارة", "بدون مرتب"],
                                                   index=["دائم", "عقد", "إعارة", "بدون مرتب"].index(emp_dict['employment_type']) if emp_dict['employment_type'] in ["دائم", "عقد", "إعارة", "بدون مرتب"] else 0)
                        new_city = st.text_input("المدينة / المركز", value=str(emp_dict.get('city', '')))
                        new_emergency_contact = st.text_input("رقم الطوارئ", 
                                                              value=str(emp_dict.get('emergency_contact', '')), 
                                                              placeholder="رقم شخص للاتصال في حالة الطوارئ", 
                                                              key="emergency_input")
                        birth_date_val = pd.to_datetime(emp_dict['birth_date']) if emp_dict['birth_date'] else datetime.now()
                        new_birth_date = st.date_input("تاريخ الميلاد", value=birth_date_val)

                    with col3:
                        hire_date_val = pd.to_datetime(emp_dict['hire_date']) if emp_dict['hire_date'] else datetime.now()
                        new_hire_date = st.date_input("تاريخ التعيين", value=hire_date_val)
                        education_options = ["دكتوراه", "ماجستير", "بكالوريوس", "دبلوم عالي", "دبلوم", 
                                               "ثانوي عام", "إعدادية", "ابتدائية", "بدون مؤهل"]
                        current_edu = str(emp_dict.get('education', ''))
                        edu_index = education_options.index(current_edu) if current_edu in education_options else 0
                        new_education = st.selectbox("المؤهل الدراسي", education_options, index=edu_index)
                        # جلب الحالات
                        conn = get_db_connection()
                        statuses = conn.execute("SELECT name FROM employee_statuses ORDER BY id").fetchall()
                        conn.close()

                        status_names = [s[0] for s in statuses]
                        current_status = emp_data['status_name']
                        new_status = st.selectbox("حالة الموظف", status_names, 
                                                 index=status_names.index(current_status) if current_status in status_names else 0)
                        new_street = st.text_area("العنوان التفصيلي", 
                                                  value=str(emp_dict.get('street', '')),
                                                  placeholder="اسم الشارع، رقم العمارة، الدور...", height=100)
                        status_reason = st.text_input("سبب التغيير (اختياري)", placeholder="مثال: نقل لفرع آخر")

                    st.markdown("---")
                    st.subheader("📝 ملاحظات إضافية")
                    new_notes = st.text_area("ملاحظات", placeholder="أي ملاحظات إضافية...", height=100)

                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                    with col_btn1:
                        if st.form_submit_button("💾 حفظ التعديلات", type="primary"):
                            conn = get_db_connection()
                            cursor = conn.cursor()

                            # جلب IDs
                            cursor.execute("SELECT id FROM employee_statuses WHERE name = ?", (new_status,))
                            new_status_id = cursor.fetchone()[0]

                            cursor.execute("SELECT id FROM departments WHERE name = ?", (new_dept,))
                            new_dept_id = cursor.fetchone()[0]

                            # تحديث كل البيانات
                            cursor.execute("""
                                UPDATE employees 
                                SET full_name = ?, national_id = ?, phone = ?, 
                                    department_id = ?, job_title = ?, employment_type = ?,
                                    hire_date = ?, status_id = ?, status_date = ?, status_reason = ?,
                                    governorate = ?, city = ?, street = ?, education = ?, marital_status = ?,
                                    emergency_contact = ?, num_children = ?, birth_date = ?
                                WHERE code = ?
                            """, (
                                new_name, new_national_id, new_phone,
                                new_dept_id, new_job, new_emp_type,
                                new_hire_date.strftime('%Y-%m-%d'), new_status_id, 
                                datetime.now().strftime('%Y-%m-%d'), status_reason, 
                                new_governorate, new_city, new_street, new_education, 
                                new_marital_status, new_emergency_contact, new_num_children,
                                new_birth_date.strftime('%Y-%m-%d') if new_birth_date else None, 
                                emp_code
                            ))

                            # تسجيل الحركة
                            cursor.execute("""
                                INSERT INTO employee_movements (employee_id, movement_type, old_value, new_value, notes, created_by)
                                        VALUES ((SELECT id FROM employees WHERE code = ?), 'status_change', ?, ?, ?, ?)
                                    """, (emp_code, str(emp_data.get('status', '')), new_status, status_reason, user['id']))

                            conn.commit()
                            st.success("✅ تم التحديث!")
                            time.sleep(0.5)
                            st.rerun()

                    with col_btn2:
                        if st.form_submit_button("🗑️ حذف الموظف"):
                            cursor = conn.cursor()
                            cursor.execute("UPDATE employees SET is_active = 0 WHERE code = ?", (emp_code,))
                            conn.commit()
                            st.warning("⚠️ تم حذف الموظف!")
                            st.rerun()
        else:
            st.info("لا توجد نتائج")

        conn.close()

    # تبويب 2: إضافة موظف
    with tab2:
        with st.form("add_employee"):
            st.subheader("➕ إضافة موظف جديد")

            # البيانات الأساسية
            col1, col2 = st.columns(2)
            with col1:
                code = st.text_input("الكود *", placeholder="مثال: 9999")
                name = st.text_input("الاسم الرباعي *")
                national_id = st.text_input("الرقم القومي *")
                phone = st.text_input("رقم التليفون")
                birth_date = st.date_input("تاريخ الميلاد", value=datetime(1990, 1, 1))

            with col2:
                conn = get_db_connection()
                depts = conn.execute("SELECT name FROM departments").fetchall()
                conn.close()

                department = st.selectbox("الإدارة *", [d[0] for d in depts])
                
                # تعديل: حقل الوظيفة أصبح اختيار من متعدد
                job_title = st.selectbox("الوظيفة *", JOB_TITLES)
                
                hire_date = st.date_input("تاريخ التعيين", value=datetime.now())
                employment_type = st.selectbox("الحالة الوظيفية", ["دائم", "عقد", "إعارة", "بدون مرتب"])

            # بيانات العنوان
            st.markdown("---")
            st.subheader("🏠 بيانات العنوان")

            col_addr1, col_addr2 = st.columns(2)
            with col_addr1:
                governorate = st.selectbox("المحافظة", [
                    "القاهرة", "الإسكندرية", "الجيزة", "القليوبية", "المنوفية", 
                    "الغربية", "الشرقية", "الدقهلية", "كفر الشيخ", "البحيرة",
                    "دمياط", "بورسعيد", "الإسماعيلية", "السويس", "شمال سيناء",
                    "جنوب سيناء", "البحر الأحمر", "الفيوم", "بني سويف", "المنيا",
                    "أسيوط", "سوهاج", "قنا", "الأقصر", "أسوان", "الوادي الجديد",
                    "مطروح"
                ])
                city = st.text_input("المدينة / المركز")
                
            with col_addr2:
                street = st.text_area("العنوان التفصيلي", placeholder="اسم الشارع، رقم العمارة، الدور...")
                

            # بيانات إضافية
            st.markdown("---")
            st.subheader("📋 بيانات إضافية")

            col_extra1, col_extra2 = st.columns(2)
            with col_extra1:
                education = st.selectbox("المؤهل الدراسي", [
                    "دكتوراه", "ماجستير", "بكالوريوس", "دبلوم عالي", "دبلوم", 
                    "ثانوي عام", "إعدادية", "ابتدائية", "بدون مؤهل"
                ])
                marital_status = st.selectbox("الحالة الاجتماعية", [
                    "أعزب", "متزوج", "مطلق", "أرمل"
                ])
                
            with col_extra2:
                num_children = st.number_input("عدد الأطفال", min_value=0, max_value=20, value=0)
                emergency_contact = st.text_input("رقم الطوارئ", placeholder="رقم شخص يمكن الاتصال به في حالة الطوارئ")

            notes = st.text_area("ملاحظات إضافية", placeholder="أي معلومات إضافية عن الموظف...")

            if st.form_submit_button("➕ إضافة الموظف", type="primary"):
                if code and name and national_id and department and job_title:
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    # جلب ID الإدارة
                    cursor.execute("SELECT id FROM departments WHERE name = ?", (department,))
                    dept_id = cursor.fetchone()[0]

                    try:
                        cursor.execute("""
                            INSERT INTO employees 
                            (code, full_name, department_id, job_title, national_id, phone, 
                             hire_date, employment_type, status_id, is_active,
                             governorate, city, street, education, 
                             marital_status, num_children, emergency_contact, notes, birth_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (int(code), name, dept_id, job_title, national_id, phone, 
                              hire_date.strftime('%Y-%m-%d'), employment_type,
                              governorate, city, street, education,
                              marital_status, num_children, emergency_contact, notes, birth_date))

                        emp_id = cursor.lastrowid

                        # إنشاء حساب للموظف
                        username = f"emp{code}"
                        password_hash = hash_password('123456')
                        cursor.execute("INSERT INTO users (employee_id, username, password_hash, role) VALUES (?, ?, ?, 'employee')",
                                      (emp_id, username, password_hash))

                        # تسجيل الحركة
                        cursor.execute("INSERT INTO employee_movements (employee_id, movement_type, new_value, notes, created_by) VALUES (?, 'hiring', ?, ?, ?)",
                                      (emp_id, department, notes, user['id']))

                        conn.commit()
                        st.success("✅ تم إضافة الموظف بنجاح!")
                        st.balloons()

                        # عرض بيانات الدخول في صندوق منفصل
                        st.markdown("---")
                        st.subheader("🔑 بيانات الدخول للموظف الجديد:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**اسم المستخدم:** `{username}`")
                        with col2:
                            st.markdown(f"**كلمة المرور:** `123456`")
                        st.markdown("---")

                        # إشعار واتساب
                        st.info("📱 تم إرسال إشعار واتساب للموظف (محاكاة)")

                    except sqlite3.IntegrityError:
                        st.error("❌ الكود أو الرقم القومي موجود مسبقاً!")
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
                    finally:
                        conn.close()


                else:
                    st.error("❌ يرجى ملء جميع الحقول المطلوبة (*)")

    # تبويب 3: حركات الموظفين
    with tab3:
        st.subheader("📜 سجل حركات الموظفين")

        # فلاتر
        col1, col2, col3 = st.columns(3)
        with col1:
            show_all = st.checkbox("عرض كل الحركات", value=True)
        with col2:
            movement_filter = st.selectbox("نوع الحركة", ["الكل", "تعيين جديد", "تغيير حالة", "استقالة", "تقاعد"])
        with col3:
            search_emp = st.text_input("🔍 بحث باسم الموظف")

        conn = get_db_connection()

        # بناء الاستعلام
        query = """
            SELECT 
                e.code as "الكود",
                e.full_name as "الموظف", 
                em.movement_type as "نوع الحركة",
                em.old_value as "القيمة القديمة", 
                em.new_value as "القيمة الجديدة",
                em.movement_date as "التاريخ",
                em.notes as "ملاحظات",
                COALESCE(u.username, 'النظام') as "بواسطة"
            FROM employee_movements em
            JOIN employees e ON em.employee_id = e.id
            LEFT JOIN users u ON em.created_by = u.id
            WHERE 1=1
        """

        params = []

        if not show_all:
            query += " AND em.movement_date = date('now')"

        if movement_filter != "الكل":
            filter_map = {
                "تعيين جديد": "hiring",
                "تغيير حالة": "status_change",
                "استقالة": "resignation",
                "تقاعد": "retirement"
            }
            query += " AND em.movement_type = ?"
            params.append(filter_map.get(movement_filter, movement_filter))

        if search_emp:
            query += " AND e.full_name LIKE ?"
            params.append(f"%{search_emp}%")

        query += " ORDER BY em.created_at DESC LIMIT 200"

        movements = pd.read_sql_query(query, conn, params=params)
        conn.close()

        if not movements.empty:
            # ترجمة أنواع الحركات للعربي
            movement_types = {
                'hiring': 'تعيين جديد 👤',
                'status_change': 'تغيير حالة 🔄',
                'promotion': 'ترقية 📈',
                'transfer': 'نقل 📍',
                'resignation': 'استقالة 📤',
                'retirement': 'تقاعد 🎖️'
            }
            movements['نوع الحركة'] = movements['نوع الحركة'].map(movement_types).fillna(movements['نوع الحركة'])

            # عرض الإحصائيات
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("إجمالي الحركات", len(movements))
            with col2:
                today_count = len(movements[movements['التاريخ'] == datetime.now().strftime('%Y-%m-%d')])
                st.metric("حركات اليوم", today_count)
            with col3:
                st.metric("أنواع مختلفة", movements['نوع الحركة'].nunique())

            # عرض الجدول مع ترتيب الأعمدة من اليمين
            st.markdown("### 📋 تفاصيل الحركات")

            # ترتيب الأعمدة حسب الأولوية (من اليمين للشمال)
            column_order = ["الكود", "الموظف", "نوع الحركة", "القيمة الجديدة", "القيمة القديمة", "التاريخ", "ملاحظات", "بواسطة"]
            movements = movements[[col for col in column_order if col in movements.columns]]

            st.dataframe(
                movements, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "الكود": st.column_config.NumberColumn("الكود", width="small"),
                    "الموظف": st.column_config.TextColumn("اسم الموظف", width="medium"),
                    "نوع الحركة": st.column_config.TextColumn("الحركة", width="medium"),
                    "التاريخ": st.column_config.DateColumn("التاريخ", width="small"),
                }
            )

            # أزرار التصدير
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                csv = movements.to_csv(index=False).encode('utf-8-sig')
                st.download_button("⬇️ تصدير CSV", csv, "movements.csv", "text/csv", use_container_width=True)
            with col_exp2:
                # to_excel needs a buffer, not like to_csv
                import io
                excel_buffer = io.BytesIO()
                movements.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                st.download_button("⬇️ تصدير Excel", excel_buffer, "movements.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        else:
            st.info("📭 لا توجد حركات مسجلة")
            st.markdown("**💡 ملاحظة:** الحركات تُسجل تلقائياً عند:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("- ✅ إضافة موظف جديد")
                st.markdown("- 🔄 تغيير حالة الموظف")
            with col2:
                st.markdown("- 📈 الترقيات")
                st.markdown("- 📍 النقل بين الإدارات")


# ====================تقرير الحضور ==========================

def show_advanced_attendance_report(user):
    """تقرير حضور متقدم للـ HR"""
    st.title("📊 تقرير الحضور والانصراف المتقدم")
    
    # الفلاتر
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        report_date = st.date_input("📅 التاريخ", value=datetime.now())
    with col2:
        conn = get_db_connection()
        depts = [d[0] for d in conn.execute("SELECT name FROM departments").fetchall()]
        conn.close()
        dept_filter = st.selectbox("الإدارة", ["الكل"] + depts)
    with col3:
        view_type = st.selectbox("عرض", ["الكل", "الحاضرين فقط", "الغائبين فقط"])
    with col4:
        export_format = st.selectbox("تصدير", ["لا شيء", "Excel"])
    
    conn = get_db_connection()
    
    # جلب الموظفين
    query_emp = """
        SELECT e.id, e.code, e.full_name, d.name as department, e.job_title
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE e.is_active = 1 AND e.status_id = 1
    """
    params = []
    if dept_filter != "الكل":
        query_emp += " AND d.name = ?"
        params.append(dept_filter)
    
    employees = pd.read_sql_query(query_emp, conn, params=params)
    
    # جلب البصمات
    date_str = report_date.strftime('%Y-%m-%d')
    attendance = pd.read_sql_query("""
        SELECT employee_id, punch_time, punch_type
        FROM attendance_logs
        WHERE punch_date = ?
    """, conn, params=(date_str,))
    
    # جلب المأموريات المسجلة
    missions = pd.read_sql_query("""
        SELECT employee_id, new_value as mission_type, notes
        FROM employee_movements
        WHERE movement_type = 'attendance_mission' AND movement_date = ?
    """, conn, params=(date_str,))
    
    conn.close()
    
    # بناء التقرير
    report_data = []
    
    for _, emp in employees.iterrows():
        emp_attendance = attendance[attendance['employee_id'] == emp['id']]
        emp_mission = missions[missions['employee_id'] == emp['id']]
        
        check_in = emp_attendance[emp_attendance['punch_type'] == 'IN']['punch_time'].min() if not emp_attendance.empty else None
        check_out = emp_attendance[emp_attendance['punch_type'] == 'OUT']['punch_time'].max() if not emp_attendance.empty else None
        
        # حساب الساعات
        hours_worked = 0
        if check_in and check_out:
            try:
                from datetime import datetime as dt
                t1 = dt.strptime(str(check_in), '%H:%M:%S')
                t2 = dt.strptime(str(check_out), '%H:%M:%S')
                hours_worked = round((t2 - t1).seconds / 3600, 2)
            except:
                pass
        
        # تحديد الحالة
        if not emp_attendance.empty:
            status = '✅ حاضر'
            status_color = '#d4edda'
        elif not emp_mission.empty:
            mission = emp_mission.iloc[0]
            status = f'📋 {mission["mission_type"]}'
            status_color = '#fff3cd'
        else:
            status = '❌ غائب'
            status_color = '#f8d7da'
        
        report_data.append({
            'كود': int(emp['code']),
            'الاسم': emp['full_name'],
            'الإدارة': emp['department'],
            'الوظيفة': emp['job_title'],
            'الحالة': status,
            'الدخول': str(check_in) if check_in else '-',
            'الخروج': str(check_out) if check_out else '-',
            'ساعات': hours_worked if hours_worked > 0 else '-',
            'employee_id': emp['id']
        })
    
    df_report = pd.DataFrame(report_data)
    
    # تصفية
    if view_type == "الحاضرين فقط":
        df_report = df_report[df_report['الحالة'].str.contains('حاضر')]
    elif view_type == "الغائبين فقط":
        df_report = df_report[df_report['الحالة'].str.contains('غائب')]
    
    # إحصائيات
    present = len(df_report[df_report['الحالة'].str.contains('حاضر')])
    absent = len(df_report[df_report['الحالة'].str.contains('غائب')])
    mission_count = len(df_report[df_report['الحالة'].str.contains('مأمورية|إجازة|عمل')])
    total = len(df_report)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 إجمالي", total)
    with col2:
        st.metric("✅ الحاضرين", present)
    with col3:
        st.metric("❌ الغائبين", absent)
    with col4:
        st.metric("📋 المأموريات", mission_count)
    
    # عرض الجدول
    st.markdown("---")
    
    if not df_report.empty:
        display_df = df_report.drop('employee_id', axis=1)
        
        # تلوين
        def highlight_status(val):
            if 'حاضر' in val:
                return 'background-color: #d4edda;'
            elif 'غائب' in val:
                return 'background-color: #f8d7da;'
            else:
                return 'background-color: #fff3cd;'
        
        styled_df = display_df.style.applymap(highlight_status, subset=['الحالة'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # ===== تسجيل المأموريات للغائبين =====
        if user['role'] in ['admin', 'hr']:
            absent_employees = df_report[df_report['الحالة'].str.contains('غائب')]
            
            if not absent_employees.empty:
                st.markdown("---")
                st.subheader("📝 تسجيل مأمورية / سبب غياب")
                
                with st.form("mission_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        selected_absent = st.selectbox(
                            "الموظف الغائب",
                            [f"{row['كود']} - {row['الاسم']}" for _, row in absent_employees.iterrows()]
                        )
        
                    with col2:
                        mission_type = st.selectbox("النوع", [
                            "مأمورية رسمية",
                            "إجازة مرضية",
                            "إجازة استثنائية", 
                            "إجازة بدون مرتب",
                            "عمل من المنزل",
                            "تأخير بسبب مرور",
                            "غياب بدون إذن"
                        ])
                    
                    mission_notes = st.text_area("ملاحظات", placeholder="تفاصيل إضافية...")
                    
                    if st.form_submit_button("💾 حفظ", type="primary"):
                        emp_code_mission = int(selected_absent.split(" - ")[0])
                        emp_row = df_report[df_report['كود'] == emp_code_mission].iloc[0]
                        
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        try:
                            # تسجيل الحركة
                            cursor.execute("""
                                INSERT INTO employee_movements 
                                (employee_id, movement_type, new_value, notes, created_by, movement_date)
                                VALUES (?, 'attendance_mission', ?, ?, ?, ?)
                            """, (
                                int(emp_row['employee_id']),
                                mission_type,
                                mission_notes,
                                user['id'],
                                date_str
                            ))
                            
                            # لو مأمورية رسمية أو عمل من المنزل، نضيف بصمة وهمية
                            if mission_type in ["مأمورية رسمية", "عمل من المنزل"]:
                                cursor.execute("""
                                    INSERT INTO attendance_logs (employee_id, punch_date, punch_time, punch_type)
                                    VALUES (?, ?, '09:00:00', 'IN')
                                """, (int(emp_row['employee_id']), date_str))
                                cursor.execute("""
                                    INSERT INTO attendance_logs (employee_id, punch_date, punch_time, punch_type)
                                    VALUES (?, ?, '17:00:00', 'OUT')
                                """, (int(emp_row['employee_id']), date_str))
                            
                            conn.commit()
                            st.success(f"✅ تم تسجيل {mission_type}")
                            st.rerun()
                            
                        except Exception as e:
                            conn.rollback()
                            st.error(f"❌ خطأ: {e}")
                        finally:
                            conn.close()
    else:
        st.info("لا توجد بيانات")
    
    # تصدير
    if export_format == "Excel" and not df_report.empty:
        import io
        excel_buffer = io.BytesIO()
        df_report.drop('employee_id', axis=1).to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            "⬇️ تحميل Excel",
            excel_buffer,
            f"attendance_{date_str}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ==================== ربط ZKTeco مباشرة ====================
def show_zkteco_integration(user):
    
    
    #الكود القديم
    st.title("📟 ربط جهاز البصمة ZKTeco")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ إعدادات الاتصال")
        with st.form("zkteco_config"):
            device_ip = st.text_input("IP الجهاز", value="192.168.1.201")
            port = st.number_input("البورت", value=4370, min_value=1, max_value=65535)
            timeout = st.number_input("Timeout (ثواني)", value=30, min_value=10, max_value=120)

            col_test, col_save = st.columns(2)
            with col_test:
                if st.form_submit_button("🔗 اختبار الاتصال"):
                    test_connection(device_ip, port, timeout)

            with col_save:
                if st.form_submit_button("💾 حفظ الإعدادات"):
                    # حفظ في ملف config
                    save_config(device_ip, port, timeout)
                    st.success("✅ تم حفظ الإعدادات!")

    with col2:
        st.subheader("📥 سحب البيانات")
        
        # خيارات السحب
        fetch_option = st.radio("طريقة السحب", [
            "سحب كل البصمات", 
            "سحب من تاريخ محدد",
            "سحب اليوم فقط"
        ])
        
        if fetch_option == "سحب من تاريخ محدد":
            from_date = st.date_input("من تاريخ", value=datetime.now() - timedelta(days=7))
            to_date = st.date_input("إلى تاريخ", value=datetime.now())
        
        batch_size = st.slider("حجم الدفعة", 10, 100, 50, 
                              help="عدد البصمات في كل دفعة")
        
        if st.button("🔄 سحب البصمات الآن", type="primary", use_container_width=True):
            fetch_attendance_real(device_ip, port, timeout, fetch_option, batch_size)

    # عرض البصمات
    show_attendance_logs()


def test_connection(ip, port, timeout):
    """اختبار الاتصال بالجهاز"""
    try:
        from zk import ZK
        
        with st.spinner("جاري الاتصال بالجهاز..."):
            zk = ZK(ip, port=port, timeout=timeout)
            conn = zk.connect()
            
            if conn:
                device_info = conn.get_device_info()
                st.success(f"✅ تم الاتصال بنجاح!")
                st.info(f"""
                📊 معلومات الجهاز:
                - الموديل: {device_info.device_name}
                - الإصدار: {device_info.firmware_version}
                - عدد المستخدمين: {conn.get_user_count()}
                - عدد البصمات: {conn.get_attendance_count()}
                """)
                conn.disconnect()
            else:
                st.error("❌ فشل الاتصال بالجهاز")
                
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {e}")
        st.info("💡 تأكد من:")
        st.markdown("""
        - الجهاز شغال ومتصل بالشبكة
        - IP صحيح
        - البورت 4370 مفتوح في الجدار الناري
        - الجهاز مش مقفول بـ IP مختلف
        """)


def fetch_attendance_real(ip, port, timeout, fetch_option, batch_size):
    """سحب البصمات الحقيقية من الجهاز"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        zk = ZK(ip, port=port, timeout=timeout)
        conn = zk.connect()
        
        if not conn:
            st.error("❌ فشل الاتصال بالجهاز")
            return
        
        # جلب معلومات الجهاز
        attendance_count = conn.get_attendance_count()
        st.info(f"📊 إجمالي البصمات في الجهاز: {attendance_count}")
        
        # تحديد نطاق السحب
        if fetch_option == "سحب اليوم فقط":
            today = datetime.now().strftime('%Y-%m-%d')
            attendances = conn.get_attendance()
            # تصفية بصمات اليوم فقط
            attendances = [a for a in attendances if a.timestamp.strftime('%Y-%m-%d') == today]
            
        elif fetch_option == "سحب من تاريخ محدد":
            # هنا محتاج تعديل في مكتبة pyzk أو سحب الكل وتصفيتها
            attendances = conn.get_attendance()
            # تصفية حسب التاريخ
            from_date = st.session_state.get('from_date', datetime.now() - timedelta(days=7))
            to_date = st.session_state.get('to_date', datetime.now())
            attendances = [a for a in attendances if from_date <= a.timestamp.date() <= to_date]
            
        else:  # سحب كل البصمات
            # سحب على دفعات
            attendances = []
            offset = 0
            
            while offset < attendance_count:
                status_text.text(f"⏳ جاري سحب الدفعة {offset//batch_size + 1}...")
                
                batch = conn.get_attendance(limit=batch_size, offset=offset)
                if not batch:
                    break
                    
                attendances.extend(batch)
                offset += len(batch)
                
                # تحديث شريط التقدم
                progress = min(offset / attendance_count, 1.0)
                progress_bar.progress(progress)
                
                # بريك بسيط
                if offset < attendance_count:
                    time.sleep(0.5)
        
        conn.disconnect()
        
        # حفظ في قاعدة البيانات
        save_attendance_to_db(attendances)
        
        st.success(f"✅ تم سحب {len(attendances)} بصمة بنجاح!")
        
    except Exception as e:
        st.error(f"❌ خطأ في السحب: {e}")
        import traceback
        st.error(traceback.format_exc())


def save_attendance_to_db(attendances):
    """حفظ البصمات في قاعدة البيانات"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for att in attendances:
        try:
            # البحث عن الموظف بكود البصمة (user_id)
            cursor.execute("SELECT id FROM employees WHERE code = ?", (int(att.user_id),))
            emp = cursor.fetchone()
            
            if not emp:
                skipped += 1
                continue
            
            emp_id = emp[0]
            punch_date = att.timestamp.strftime('%Y-%m-%d')
            punch_time = att.timestamp.strftime('%H:%M:%S')
            
            # تحديد نوع البصمة (IN/OUT) - افتراضي IN لو الصبح
            hour = att.timestamp.hour
            punch_type = 'IN' if hour < 12 else 'OUT'
            
            # التحقق من عدم التكرار
            cursor.execute("""
                SELECT id FROM attendance_logs 
                WHERE employee_id = ? AND punch_date = ? AND punch_time = ?
            """, (emp_id, punch_date, punch_time))
            
            if cursor.fetchone():
                continue  # موجود قبل كده
            
            # إدخال البصمة
            cursor.execute("""
                INSERT INTO attendance_logs (employee_id, punch_date, punch_time, punch_type)
                VALUES (?, ?, ?, ?)
            """, (emp_id, punch_date, punch_time, punch_type))
            
            imported += 1
            
        except Exception as e:
            st.warning(f"⚠️ تخطي بصمة للموظف {att.user_id}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    if skipped > 0:
        st.info(f"ℹ️ تم تخطي {skipped} بصمة (موظفين غير مسجلين)")


def save_config(ip, port, timeout):
    """حفظ إعدادات الجهاز"""
    import json
    config = {
        'ip': ip,
        'port': port,
        'timeout': timeout
    }
    with open('zkteco_config.json', 'w') as f:
        json.dump(config, f)


def show_attendance_logs():
    """عرض سجلات البصمات"""
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        show_date = st.date_input("عرض بصمات تاريخ", value=datetime.now())
    with col2:
        dept_filter = st.selectbox("تصفية بالإدارة", ["الكل"] + 
                                  [d[0] for d in get_db_connection().execute("SELECT name FROM departments").fetchall()])
    
    conn = get_db_connection()
    
    query = """
        SELECT e.code, e.full_name, d.name as department, 
               al.punch_date, al.punch_time, al.punch_type
        FROM attendance_logs al
        JOIN employees e ON al.employee_id = e.id
        JOIN departments d ON e.department_id = d.id
        WHERE al.punch_date = ?
    """
    params = [show_date.strftime('%Y-%m-%d')]
    
    if dept_filter != "الكل":
        query += " AND d.name = ?"
        params.append(dept_filter)
    
    query += " ORDER BY al.punch_time DESC"
    
    logs = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    if not logs.empty:
        st.dataframe(logs, use_container_width=True, hide_index=True)
        
        # إحصائيات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي البصمات", len(logs))
        with col2:
            check_ins = len(logs[logs['punch_type'] == 'IN'])
            st.metric("دخول", check_ins)
        with col3:
            check_outs = len(logs[logs['punch_type'] == 'OUT'])
            st.metric("خروج", check_outs)
    else:
        st.info("لا توجد بصمات في هذا التاريخ")

        # ==================== إشعارات واتساب ====================
def show_notifications(user):
    st.title("📱 إشعارات واتساب")

    st.markdown("""
    ### إعدادات إشعارات واتساب

    يمكن إرسال إشعارات تلقائية للموظفين عبر واتساب في الحالات التالية:
    - ✅ قبول الإجازة
    - ❌ رفض الإجازة
    - 📅 تذكير بموعد العودة من الإجازة
    - ⏰ تأخر عن الحضور
    - 💰 صرف الراتب
    """)

    with st.form("whatsapp_config"):
        st.subheader("⚙️ إعدادات API")
        api_key = st.text_input("API Key", type="password", value="demo_key_12345")
        phone_number = st.text_input("رقم الهاتف المرسل (مع كود الدولة)", value="00201024519625")

        st.subheader("📋 قوالب الرسائل")

        col1, col2 = st.columns(2)
        with col1:
            leave_approved = st.text_area("قبول الإجازة", 
                value="مرحباً {name}، تم قبول طلب إجازتك من {start} إلى {end}. عدد الأيام: {days}. بالتوفيق! 👍")
        with col2:
            leave_rejected = st.text_area("رفض الإجازة",
                value="مرحباً {name}، نأسف لإبلاغك برفض طلب إجازتك. السبب: {reason}. للاستفسار تواصل مع HR.")

        if st.form_submit_button("💾 حفظ الإعدادات"):
            st.success("✅ تم حفظ إعدادات واتساب!")

    st.markdown("---")
    st.subheader("📤 إرسال رسالة يدوية")

    conn = get_db_connection()
    employees = pd.read_sql_query("SELECT code, full_name, phone FROM employees WHERE status_id = 1", conn)
    conn.close()

    if not employees.empty:
        emp_options = [f"{row['code']} - {row['full_name']}" for _, row in employees.iterrows()]
        selected_emp = st.selectbox("اختر موظف", emp_options)

        if selected_emp:
            try:
                emp_code = int(selected_emp.split(" - ")[0])
                emp_filtered = employees[employees['code'] == emp_code]
                if not emp_filtered.empty:
                    phone = emp_filtered['phone'].values[0]
                else:
                    st.error("لم يتم العثور على الموظف")
                    return
            except:
                st.error("خطأ في اختيار الموظف")
                return

        message = st.text_area("نص الرسالة", value="مرحباً، هذا اختبار من نظام HR.")

        if st.button("📱 إرسال الرسالة", type="primary"):
            with st.spinner("جاري الإرسال... (افتح WhatsApp Web)"):
                try:
                    import pywhatkit
                    import time
                    
                    # تنسيق الرقم (لازم يكون مع كود الدولة)
                    phone_formatted = str(phone).replace(" ", "").replace("-", "")
                    if not phone_formatted.startswith("+"):
                        phone_formatted = "+20" + phone_formatted.lstrip("0")
                    
                    # إرسال الرسالة
                    pywhatkit.sendwhatmsg_to_instantly(
                        phone=phone_formatted,
                        message=message,
                        wait_time=15  # وقت الانتظار عشان يفتح WhatsApp Web
                    )
                    
                    st.success(f"✅ تم إرسال الرسالة إلى {phone_formatted}!")
                    st.info("📱 تم فتح WhatsApp Web، الرسالة هتتبعت تلقائياً")
                    
                except Exception as e:
                    st.error(f"❌ خطأ في الإرسال: {e}")
                    st.info("💡 تأكد إن:")
                    st.markdown("- WhatsApp Web شغال على جهازك")
                    st.markdown("- الرقم صحيح مع كود الدولة (+20)")
                    st.markdown("- فيه اتصال إنترنت")

def import_from_zkteco_attendance():
    """استيراد البصمات من ZKTeco Attendance Arabic مع دعم الورديات"""
    
    import os
    import pandas as pd
    
    # البحث عن قاعدة البيانات في أماكن مختلفة
    possible_paths = [
        r"C:\Program Files\ZKTeco Attendance Arabic\database\attenda.db",
        r"C:\Program Files (x86)\ZKTeco Attendance Arabic\database\attenda.db",
        r"C:\ZKTeco Attendance Arabic\database\attenda.db",
        os.path.expanduser(r"~\Documents\ZKTeco Attendance Arabic\database\attenda.db"),
        r"D:\ZKTeco Attendance Arabic\database\attenda.db",
    ]
    
    zkteco_db = None
    for path in possible_paths:
        if os.path.exists(path):
            zkteco_db = path
            break
    
    if not zkteco_db:
        st.error("❌ لم يتم العثور على قاعدة بيانات ZKTeco")
        st.info("💡 المسارات التي تم البحث فيها:")
        for path in possible_paths:
            st.code(path)
        return False
    
    st.success(f"✅ تم العثور على قاعدة البيانات: {zkteco_db}")
    
    try:
        conn_zk = sqlite3.connect(zkteco_db)
        
        # ========== جلب البصمات ==========
        # جدول Checkinout هو الأساسي في ZKTeco
        query = """
            SELECT 
                c.Userid as employee_code,
                c.CheckTime as punch_datetime,
                c.CheckType as punch_type,
                c.Sensorid as device_id
            FROM Checkinout c
            WHERE c.CheckTime >= datetime('now', '-30 days')
            ORDER BY c.CheckTime DESC
            LIMIT 5000
        """
        
        attendance_data = pd.read_sql_query(query, conn_zk)
        conn_zk.close()
        
        if attendance_data.empty:
            st.warning("⚠️ لا توجد بيانات حضور في الـ 30 يوم الماضية")
            return False
        
        st.info(f"📊 تم العثور على {len(attendance_data)} سجل حضور")
        
        # ========== معالجة واستيراد البيانات ==========
        conn_hr = get_db_connection()
        cursor_hr = conn_hr.cursor()
        
        imported = 0
        skipped = 0
        errors = []
        
        progress_bar = st.progress(0)
        
        for idx, row in attendance_data.iterrows():
            try:
                progress = (idx + 1) / len(attendance_data)
                progress_bar.progress(min(progress, 1.0))
                
                # البحث عن الموظف
                cursor_hr.execute(
                    "SELECT id FROM employees WHERE code = ?", 
                    (int(row['employee_code']),)
                )
                emp = cursor_hr.fetchone()
                
                if not emp:
                    skipped += 1
                    continue
                
                emp_id = emp[0]
                
                # تفكيك التاريخ والوقت
                punch_datetime = pd.to_datetime(row['punch_datetime'])
                punch_date = punch_datetime.strftime('%Y-%m-%d')
                punch_time = punch_datetime.strftime('%H:%M:%S')
                
                # تحديد نوع البصمة
                # في ZKTeco: 0 = دخول, 1 = خروج, 2 = دخول ثاني, 3 = خروج ثاني
                check_type = int(row['punch_type']) if str(row['punch_type']).isdigit() else 0
                
                if check_type in [0, 2]:  # دخول
                    punch_type = 'IN'
                else:  # خروج
                    punch_type = 'OUT'
                
                # التحقق من عدم التكرار
                cursor_hr.execute("""
                    SELECT id FROM attendance_logs 
                    WHERE employee_id = ? AND punch_date = ? AND punch_time = ?
                """, (emp_id, punch_date, punch_time))
                
                if cursor_hr.fetchone():
                    continue
                
                # إدخال البصمة
                cursor_hr.execute("""
                    INSERT INTO attendance_logs 
                    (employee_id, punch_date, punch_time, punch_type, device_id, created_at)
                    VALUES (?, ?, ?, ?, ?, datetime('now'))
                """, (
                    emp_id, 
                    punch_date, 
                    punch_time, 
                    punch_type, 
                    str(row['device_id']) if pd.notna(row['device_id']) else 'ZKTeco'
                ))
                
                imported += 1
                
            except Exception as e:
                errors.append(str(e))
                continue
        
        conn_hr.commit()
        conn_hr.close()
        progress_bar.empty()
        
        # ========== عرض النتائج ==========
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ تم الاستيراد", imported)
        with col2:
            st.metric("⏭️ تم تخطيهم", skipped)
        with col3:
            st.metric("❌ أخطاء", len(errors))
        
        if imported > 0:
            st.success(f"🎉 تم استيراد {imported} بصمة بنجاح!")
            st.balloons()
        
        if errors and len(errors) < 10:
            with st.expander("📋 تفاصيل الأخطاء"):
                for err in errors[:10]:
                    st.error(err)
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في الاستيراد: {e}")
        import traceback
        st.code(traceback.format_exc())
        return False




# ==================== تقارير PDF ====================


def show_reports(user):
    st.title("📄 التقارير والطباعة")

    tab1, tab2, tab3 = st.tabs(["📊 تقرير الحضور", "📋 تقرير الإجازات", "👥 تقرير الموظفين"])

    with tab1:
        st.subheader("📊 تقرير الحضور والانصراف")

        col1, col2 = st.columns(2)
        with col1:
            report_month = st.selectbox("الشهر", range(1, 13), format_func=lambda x: f"{x:02d}")
        with col2:
            report_year = st.selectbox("السنة", range(2023, 2027), index=2)

        if st.button("📄 توليد تقرير PDF", type="primary"):
            with st.spinner("جاري إنشاء التقرير..."):
                # محاكاة إنشاء PDF
                st.success("✅ تم إنشاء التقرير!")

                # عرض بيانات التقرير
                conn = get_db_connection()
                report_data = pd.read_sql_query(f"""
                    SELECT e.full_name, d.name as department,
                           COUNT(DISTINCT al.punch_date) as days_present,
                           SUM(CASE WHEN al.punch_type = 'IN' THEN 1 ELSE 0 END) as check_ins
                    FROM employees e
                    JOIN departments d ON e.department_id = d.id
                    LEFT JOIN attendance_logs al ON e.id = al.employee_id 
                        AND strftime('%Y-%m', al.punch_date) = '{report_year:04d}-{report_month:02d}'
                    WHERE e.status_id = 1
                    GROUP BY e.id
                """, conn)
                conn.close()

                st.dataframe(report_data, use_container_width=True)

                # زر تحميل (محاكاة)
                st.download_button(
                    label="⬇️ تحميل التقرير PDF",
                    data=b"PDF content placeholder",
                    file_name=f"attendance_report_{report_year}_{report_month}.pdf",
                    mime="application/pdf"
                )

    with tab2:
        st.subheader("📋 تقرير الإجازات")

        if st.button("📄 توليد تقرير الإجازات", type="primary"):
            conn = get_db_connection()
            leaves = pd.read_sql_query("""
                SELECT e.full_name, d.name as department, lt.name as leave_type,
                       lr.start_date, lr.end_date, lr.days_count, lr.status
                FROM leave_requests lr
                JOIN employees e ON lr.employee_id = e.id
                JOIN departments d ON e.department_id = d.id
                JOIN leave_types lt ON lr.leave_type_id = lt.id
                ORDER BY lr.requested_at DESC
            """, conn)
            conn.close()

            st.dataframe(leaves, use_container_width=True)

            st.download_button(
                label="⬇️ تحميل Excel",
                data=leaves.to_csv(index=False).encode('utf-8-sig'),
                file_name="leaves_report.csv",
                mime="text/csv"
            )

    with tab3:
        st.subheader("👥 تقرير الموظفين")

        if st.button("📄 توليد كشف الموظفين", type="primary"):
            conn = get_db_connection()
            employees = pd.read_sql_query("""
                SELECT e.code, e.full_name, d.name as department, e.job_title,
                       es.name as status, e.phone, e.hire_date
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                JOIN employee_statuses es ON e.status_id = es.id
                WHERE e.is_active = 1
                ORDER BY e.code
            """, conn)
            conn.close()

            st.dataframe(employees, use_container_width=True)

            st.download_button(
                label="⬇️ تحميل Excel",
                data=employees.to_csv(index=False).encode('utf-8-sig'),
                file_name="employees_report.csv",
                mime="text/csv"
            )
def show_all_employees_leaves(user):
    """صفحة لـ HR يشوف فيها رصيد إجازات كل الموظفين"""
    st.title("📊 رصيد إجازات جميع الموظفين")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # فلاتر البحث
    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("🔍 بحث بالاسم")
    with col2:
        dept_filter = st.selectbox("الإدارة", ["الكل"] + [d[0] for d in cursor.execute("SELECT name FROM departments").fetchall()])
    with col3:
        status_filter = st.selectbox("الحالة", ["الكل", "نشط", "مستقيل", "معاش"])
    
    # بناء الاستعلام
    query = """
        SELECT 
            e.id,
            e.code,
            e.full_name,
            d.name as department,
            es.name as status,
            e.hire_date
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        JOIN employee_statuses es ON e.status_id = es.id
        WHERE e.is_active = 1
    """
    params = []
    
    if search_name:
        query += " AND e.full_name LIKE ?"
        params.append(f"%{search_name}%")
    
    if dept_filter != "الكل":
        query += " AND d.name = ?"
        params.append(dept_filter)
    
    if status_filter != "الكل":
        query += " AND es.name = ?"
        params.append(status_filter)
    
    query += " ORDER BY e.code"
    
    employees = pd.read_sql_query(query, conn, params=params)
    
    if employees.empty:
        st.info("لا يوجد موظفين مطابقين للفلاتر")
        conn.close()
        return
    
    st.markdown(f"### 📋 عدد الموظفين: {len(employees)}")
    
    # عرض كل موظف ورصيده
    for _, emp in employees.iterrows():
        with st.container():
            # جلب رصيد الإجازات
            balance = get_or_create_leave_balance(emp['id'])
            annual_entitled, years_service = calculate_annual_leave_entitlement(emp['id'])
            casual_entitled = calculate_casual_leave_entitlement(emp['id'])
            
            # تحديد لون البطاقة حسب الرصيد
            if balance['annual_remaining'] < 5:
                card_color = "#e74c3c"  # أحمر للرصيد القليل
                status_icon = "🔴"
            elif balance['annual_remaining'] < 15:
                card_color = "#f39c12"  # برتقالي
                status_icon = "🟡"
            else:
                card_color = "#27ae60"  # أخضر
                status_icon = "🟢"
            
            # عرض البطاقة
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; 
                                border-right: 5px solid {card_color};">
                        <div style="font-weight: bold; font-size: 1.1em; color: #2c3e50;">
                            {status_icon} {emp['full_name']}
                        </div>
                        <div style="color: #7f8c8d; font-size: 0.9em;">
                            🆔 كود: {int(emp['code'])} | 📍 {emp['department']}
                        </div>
                        <div style="color: #95a5a6; font-size: 0.8em; margin-top: 5px;">
                            📅 {years_service:.1f} سنة خدمة | الحالة: {emp['status']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {card_color} 0%, {card_color}dd 100%); 
                                padding: 15px; border-radius: 10px; color: white; text-align: center;">
                        <div style="font-size: 1.8em; font-weight: bold;">
                            {balance['annual_remaining']}/{balance['annual_entitled']}
                        </div>
                        <div style="font-size: 0.8em;">سنوية</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                casual_color = "#3498db" if casual_entitled > 0 else "#95a5a6"
                casual_text = f"{balance['casual_remaining']}/{casual_entitled}" if casual_entitled > 0 else "-"
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {casual_color} 0%, {casual_color}dd 100%); 
                                padding: 15px; border-radius: 10px; color: white; text-align: center;">
                        <div style="font-size: 1.8em; font-weight: bold;">{casual_text}</div>
                        <div style="font-size: 0.8em;">عارضة</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                total = balance['annual_remaining'] + balance['casual_remaining']
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #9b59b6 0%, #bb8fce 100%); 
                                padding: 15px; border-radius: 10px; color: white; text-align: center;">
                        <div style="font-size: 1.8em; font-weight: bold;">{total}</div>
                        <div style="font-size: 0.8em;">إجمالي</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col5:
                # زر عرض تفاصيل أكتر
                if st.button("📋 التفاصيل", key=f"details_{emp['id']}"):
                    st.session_state.selected_emp = emp['id']
                    st.session_state.selected_emp_name = emp['full_name']
                    st.rerun()
            
            st.markdown("---")
    
    # لو فيه موظف مختار، اعرض تفاصيله
    if 'selected_emp' in st.session_state:
        show_employee_leaves_details(st.session_state.selected_emp, 
                                     st.session_state.selected_emp_name, 
                                     user)
    
    conn.close()


def show_employee_leaves_details(emp_id, emp_name, user):
    """عرض تفاصيل إجازات موظف محدد"""
    st.markdown(f"### 📋 تفاصيل إجازات: {emp_name}")
    
    conn = get_db_connection()
    
    # جلب كل الإجازات
    leaves = pd.read_sql_query("""
        SELECT lt.name as leave_type, lr.start_date, lr.end_date, 
               lr.days_count, lr.reason, lr.status, lr.requested_at,
               CASE 
                   WHEN lr.status = 'approved' THEN '✅ مقبولة'
                   WHEN lr.status = 'rejected' THEN '❌ مرفوضة'
                   ELSE '⏳ معلقة'
               END as status_display
        FROM leave_requests lr
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        WHERE lr.employee_id = ?
        ORDER BY lr.requested_at DESC
    """, conn, params=(emp_id,))
    
    conn.close()
    
    if not leaves.empty:
        # إحصائيات
        col1, col2, col3 = st.columns(3)
        with col1:
            approved = len(leaves[leaves['status'] == 'approved'])
            st.metric("✅ المقبولة", approved)
        with col2:
            pending = len(leaves[leaves['status'] == 'pending'])
            st.metric("⏳ المعلقة", pending)
        with col3:
            rejected = len(leaves[leaves['status'] == 'rejected'])
            st.metric("❌ المرفوضة", rejected)
        
        # عرض الجدول
        st.dataframe(leaves[['leave_type', 'start_date', 'end_date', 'days_count', 
                            'status_display', 'reason']], 
                    use_container_width=True, hide_index=True)
    else:
        st.info("📭 لا توجد طلبات إجازات لهذا الموظف")
    
    if st.button("🔙 رجوع للقائمة"):
        del st.session_state.selected_emp
        del st.session_state.selected_emp_name
        st.rerun()

def get_unread_notifications_count(employee_id):
    """جلب عدد الإشعارات غير المقروءة"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM notifications
            WHERE employee_id = ? AND is_read = 0
        """, (employee_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
        
    except Exception as e:
        print(f"❌ خطأ في عد الإشعارات: {e}")
        return 0
    

# ==================== التطبيق الرئيسي ====================
def main():
    init_session()
    
    # ✅ Initialize all session state variables first
    if 'show_menu' not in st.session_state:
        st.session_state.show_menu = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = None

    if not st.session_state.logged_in:
        login_page()
        return

    user = st.session_state.user

    # ✅ CSS محسّن - نخفي زر القائمة في الديسكتوب فقط
    st.markdown("""
    <style>
    @media (min-width: 769px) {
        div[data-testid="stHorizontalBlock"]:has(button[key="menu_toggle_btn"]) {
            display: none !important;
        }
    }
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ✅ زر القائمة (في الموبايل فقط)
    menu_col, _ = st.columns([1, 4])
    with menu_col:
        if st.button("☰ القائمة", key="menu_toggle_btn"):
            st.session_state.show_menu = not st.session_state.show_menu
            st.rerun()

    # ✅ القائمة المنسدلة (تظهر لما تكون مفتوحة)
    if st.session_state.show_menu:
        st.markdown("---")
        st.markdown("### 📋 القائمة")
        
        # خيارات القائمة حسب الصلاحيات
        if user['role'] == 'admin':
            menu_options = [
                "📊 لوحة التحكم", "👥 إدارة الموظفين", "📊 رصيد الإجازات",
                "📊 تقرير الحضور", "📟 ربط ZKTeco", 
                "📄 التقارير", "📋 طلبات الإجازات"
            ]
        elif user['role'] == 'hr':
            menu_options = [
                "📊 لوحة التحكم", "👥 إدارة الموظفين", "📊 رصيد الإجازات",
                "📊 تقرير الحضور", "📟 ربط ZKTeco", 
                "📄 التقارير", "📋 طلبات الإجازات"
            ]
        elif user['role'] == 'manager':
            menu_options = ["📊 لوحة التحكم", "👥 فريقي", "📋 طلبات الإجازات"]
        else:  # employee
            # جلب عدد الإشعارات غير المقروءة
            unread_count = get_unread_notifications_count(user['employee_id']) if user.get('employee_id') else 0
    
            # إعداد نص الإشعارات مع الـ Badge
            if unread_count > 0:
                notifications_text = f"🔔 إشعاراتي 🔴 {unread_count}"  # <-- النقطة الحمراء هنا!
            else:
                notifications_text = "🔔 إشعاراتي"
    
            menu_options = [
                "📊 ملخصي",
                "📋 إجازاتي",
                "➕ طلب إجازة جديدة",
                notifications_text,  # <-- متغير بدل نص ثابت
            ]
        # شبكة الأزرار
        cols = st.columns(2)
        for idx, option in enumerate(menu_options):
            with cols[idx % 2]:
                btn_type = "primary" if option == st.session_state.current_page else "secondary"
                if st.button(option, key=f"menu_opt_{idx}", use_container_width=True, type=btn_type):
                    # ✅ لو الاختيار فيه "🔔 إشعاراتي" (مع أو من غير badge)، نحفظ الاسم الأساسي
                    if "🔔 إشعاراتي" in option:
                        st.session_state.current_page = "🔔 إشعاراتي"
                    else:
                        st.session_state.current_page = option
                    st.session_state.show_menu = False
                    st.rerun()

        # أزرار التحكم
        col_close, col_logout = st.columns(2)
        with col_close:
            if st.button("❌ إغلاق القائمة", use_container_width=True, key="close_menu"):
                st.session_state.show_menu = False
                st.rerun()
        with col_logout:
            if st.button("🚪 تسجيل الخروج", use_container_width=True, key="logout_from_menu"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.show_menu = False
                st.rerun()
        
        st.markdown("---")

    # ✅ Sidebar الأصلي - نحطه هنا عشان يكون في مكان ثابت
    try:
        with st.sidebar:
            st.title(f"مرحباً، {user['full_name']}")
            st.markdown(f"**الدور:** {user['role']}")
            st.markdown("---")

            # تحديد خيارات Sidebar حسب الصلاحيات
            if user['role'] == 'admin':
                sidebar_options = [
                    "📊 لوحة التحكم", "👥 إدارة الموظفين", "📊 رصيد الإجازات",
                    "📊 تقرير الحضور", "📟 ربط ZKTeco", 
                    "📄 التقارير", "📋 طلبات الإجازات"
                ]
            elif user['role'] == 'hr':
                sidebar_options = [
                    "📊 لوحة التحكم", "👥 إدارة الموظفين", "📊 رصيد الإجازات",
                    "📊 تقرير الحضور", "📟 ربط ZKTeco", 
                    "📄 التقارير", "📋 طلبات الإجازات"
                ]
            elif user['role'] == 'manager':
                sidebar_options = ["📊 لوحة التحكم", "👥 فريقي", "📋 طلبات الإجازات"]
            else:
                sidebar_options = ["📊 ملخصي", "📋 إجازاتي", "➕ طلب إجازة جديدة", "🔔 إشعاراتي"]

            # Radio buttons للتنقل
            current_idx = sidebar_options.index(st.session_state.current_page) if st.session_state.current_page in sidebar_options else 0
            page = st.radio("القائمة", sidebar_options, index=current_idx, key="sidebar_radio")
            
            if page != st.session_state.current_page:
                st.session_state.current_page = page
                st.rerun()

            st.divider()
            
            # إشعارات للموظف
            if user['role'] == 'employee' and user.get('employee_id'):
                unread_count = get_unread_notifications_count(user['employee_id'])
                if unread_count > 0:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                                    color: white; padding: 12px; border-radius: 12px; 
                                    text-align: center; margin: 15px 0;">
                            <div style="font-size: 1.2em; font-weight: bold;">
                                🔔 {unread_count} إشعار جديد
                            </div>
                            <div style="font-size: 0.8em; opacity: 0.9; margin-top: 5px;">
                                اضغط على "🔔 إشعاراتي" لعرضها
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                        <style>
                        @keyframes pulse {
                            0% { transform: scale(1); }
                            50% { transform: scale(1.05); }
                            100% { transform: scale(1); }
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    if st.button("🔔 عرض الإشعارات", use_container_width=True):
                        st.session_state.current_page = "🔔 إشعاراتي"
                        st.rerun()

            # زر الخروج
            if st.button("🚪 تسجيل الخروج", use_container_width=True, key="sidebar_logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
    except Exception as e:
        st.error(f"Error in sidebar: {e}")

    # ✅ عرض الصفحة الحالية
    page = st.session_state.current_page
    
    if page == "📊 لوحة التحكم":
        if user['role'] in ['admin', 'hr', 'manager']:
            show_dashboard(user)
        else:
            show_employee_summary(user)
    elif page == "📊 ملخصي":
        show_employee_summary(user)
    elif page in ["👥 إدارة الموظفين", "👥 فريقي"]:
        show_employees_management(user)
    elif page == "📟 ربط ZKTeco":
        show_zkteco_integration(user)
    elif page == "📱 إشعارات واتساب":
        show_notifications(user)
    elif page == "📄 التقارير":
        show_reports(user)
    elif page == "📋 طلبات الإجازات":
        show_leaves_management(user)
    elif page == "📋 إجازاتي":
        show_employee_leaves(user)
    elif page == "➕ طلب إجازة جديدة":
        show_new_leave(user)
    elif page == "📊 رصيد الإجازات":
        show_all_employees_leaves(user)
    elif page == "📊 تقرير الحضور":
        show_advanced_attendance_report(user)
    elif page == "🔔 إشعاراتي":
        show_employee_notifications(user)

if __name__ == "__main__":
    main()
