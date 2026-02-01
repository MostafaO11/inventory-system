"""
نظام إدارة مخزون المطعم - النسخة المتقدمة
Restaurant Inventory Management System - Advanced Version
تم التطوير باستخدام Streamlit و Pandas
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, date

# تحديد مسار ملفات البيانات
BASE_DIR = Path(__file__).parent
INVENTORY_FILE = BASE_DIR / "inventory.csv"
RECIPES_FILE = BASE_DIR / "recipes.csv"
INVENTORY_LOG_FILE = BASE_DIR / "inventory_log.csv"
SALES_LOG_FILE = BASE_DIR / "sales_log.csv"

# إعدادات الصفحة
st.set_page_config(
    page_title="الوحش برجر - نظام إدارة المخزون",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق CSS مخصص للواجهة العربية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif !important;
    }
    
    .main {
        direction: rtl;
        text-align: right;
    }
    
    .stDataFrame {
        direction: ltr;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
    }
    
    .header-title {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .section-header {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        padding: 10px 20px;
        border-radius: 10px;
        color: white;
        font-size: 1.3rem;
        margin: 20px 0 15px 0;
    }
    
    .section-header-purple {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 10px 20px;
        border-radius: 10px;
        color: white;
        font-size: 1.3rem;
        margin: 20px 0 15px 0;
    }
    
    .section-header-orange {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 10px 20px;
        border-radius: 10px;
        color: white;
        font-size: 1.3rem;
        margin: 20px 0 15px 0;
    }
    
    .low-stock {
        background-color: #ffcccc !important;
        color: #cc0000 !important;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: transform 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ========== دوال تحميل وحفظ البيانات ==========

def load_inventory():
    """تحميل بيانات المخزون"""
    if INVENTORY_FILE.exists():
        return pd.read_csv(INVENTORY_FILE, encoding='utf-8-sig')
    else:
        df = pd.DataFrame({
            'Ingredient': ['طماطم', 'بصل', 'ثوم'],
            'Current_Stock': [50, 30, 10],
            'Unit': ['كيلو', 'كيلو', 'كيلو']
        })
        df.to_csv(INVENTORY_FILE, index=False, encoding='utf-8-sig')
        return df


def load_recipes():
    """تحميل بيانات الوصفات"""
    if RECIPES_FILE.exists():
        return pd.read_csv(RECIPES_FILE, encoding='utf-8-sig')
    else:
        df = pd.DataFrame({
            'Dish_Name': ['شاورما دجاج', 'شاورما دجاج'],
            'Ingredient': ['دجاج', 'طماطم'],
            'Quantity_Needed': [0.3, 0.1]
        })
        df.to_csv(RECIPES_FILE, index=False, encoding='utf-8-sig')
        return df


def load_inventory_log():
    """تحميل سجل الوارد"""
    if INVENTORY_LOG_FILE.exists():
        return pd.read_csv(INVENTORY_LOG_FILE, encoding='utf-8-sig')
    else:
        df = pd.DataFrame(columns=['Date', 'Ingredient', 'Quantity_Added', 'Unit', 'Notes'])
        df.to_csv(INVENTORY_LOG_FILE, index=False, encoding='utf-8-sig')
        return df


def save_inventory(df):
    """حفظ بيانات المخزون"""
    df.to_csv(INVENTORY_FILE, index=False, encoding='utf-8-sig')


def save_recipes(df):
    """حفظ بيانات الوصفات"""
    df.to_csv(RECIPES_FILE, index=False, encoding='utf-8-sig')


def save_inventory_log(df):
    """حفظ سجل الوارد"""
    df.to_csv(INVENTORY_LOG_FILE, index=False, encoding='utf-8-sig')


def load_sales_log():
    """تحميل سجل المبيعات"""
    if SALES_LOG_FILE.exists():
        return pd.read_csv(SALES_LOG_FILE, encoding='utf-8-sig')
    else:
        df = pd.DataFrame(columns=['Date', 'Time', 'Dish_Name', 'Quantity', 'Notes'])
        df.to_csv(SALES_LOG_FILE, index=False, encoding='utf-8-sig')
        return df


def save_sales_log(df):
    """حفظ سجل المبيعات"""
    df.to_csv(SALES_LOG_FILE, index=False, encoding='utf-8-sig')


def add_to_sales_log(sales_cart, notes=""):
    """إضافة مبيعات للسجل"""
    log_df = load_sales_log()
    today = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M:%S')
    
    new_rows = []
    for item in sales_cart:
        new_rows.append({
            'Date': today,
            'Time': now_time,
            'Dish_Name': item['dish'],
            'Quantity': item['quantity'],
            'Notes': notes
        })
    
    new_df = pd.DataFrame(new_rows)
    log_df = pd.concat([log_df, new_df], ignore_index=True)
    save_sales_log(log_df)
    return log_df


# ========== دوال المساعدة ==========

def get_dish_names(recipes_df):
    """الحصول على قائمة أسماء الأطباق"""
    return recipes_df['Dish_Name'].unique().tolist()


def calculate_ingredients_needed(recipes_df, dish_name, quantity_sold):
    """حساب المكونات المطلوبة لطبق معين"""
    dish_recipe = recipes_df[recipes_df['Dish_Name'] == dish_name]
    ingredients_needed = {}
    
    for _, row in dish_recipe.iterrows():
        ingredient = row['Ingredient']
        qty_per_dish = row['Quantity_Needed']
        total_needed = qty_per_dish * quantity_sold
        ingredients_needed[ingredient] = total_needed
    
    return ingredients_needed


def check_stock_availability(inventory_df, ingredients_needed):
    """التحقق من توفر المخزون"""
    warnings = []
    
    for ingredient, needed in ingredients_needed.items():
        stock_row = inventory_df[inventory_df['Ingredient'] == ingredient]
        
        if stock_row.empty:
            warnings.append(f"⚠️ المكون '{ingredient}' غير موجود في المخزون!")
        else:
            current_stock = stock_row['Current_Stock'].values[0]
            unit = stock_row['Unit'].values[0]
            
            if current_stock < needed:
                warnings.append(
                    f"⚠️ المخزون غير كافٍ: '{ingredient}' - "
                    f"المتوفر: {current_stock:.2f} {unit} | "
                    f"المطلوب: {needed:.2f} {unit}"
                )
    
    return warnings


def update_stock(inventory_df, ingredients_needed):
    """تحديث المخزون بعد البيع"""
    updated_df = inventory_df.copy()
    
    for ingredient, needed in ingredients_needed.items():
        mask = updated_df['Ingredient'] == ingredient
        if mask.any():
            updated_df.loc[mask, 'Current_Stock'] -= needed
    
    return updated_df


def highlight_low_stock(row, threshold):
    """تمييز المخزون المنخفض"""
    if row['المخزون الحالي'] < threshold:
        return ['background-color: #ffcccc; color: #cc0000; font-weight: bold'] * len(row)
    return [''] * len(row)


def add_to_inventory_log(log_df, items_list, notes=""):
    """إضافة سجلات للوارد"""
    today = datetime.now().strftime('%Y-%m-%d')
    new_rows = []
    
    for item in items_list:
        new_rows.append({
            'Date': today,
            'Ingredient': item['ingredient'],
            'Quantity_Added': item['quantity'],
            'Unit': item['unit'],
            'Notes': notes
        })
    
    new_df = pd.DataFrame(new_rows)
    return pd.concat([log_df, new_df], ignore_index=True)


# ========== صفحة المبيعات ولوحة المعلومات ==========

def render_sales_dashboard():
    """عرض صفحة المبيعات"""
    
    inventory_df = load_inventory()
    recipes_df = load_recipes()
    
    # قسم إدخال المبيعات اليومية
    st.markdown('<div class="section-header">📝 إدخال المبيعات اليومية</div>', unsafe_allow_html=True)
    
    dish_names = get_dish_names(recipes_df)
    
    if not dish_names:
        st.warning("⚠️ لا توجد وصفات! أضف وصفات من تبويب 'إدارة الوصفات'")
    else:
        st.info("💡 أضف الأطباق المباعة واحداً تلو الآخر، ثم راجع القائمة قبل التأكيد")
        
        # تهيئة سلة المبيعات في الجلسة
        if 'sales_cart' not in st.session_state:
            st.session_state.sales_cart = []
        
        col_dish, col_qty, col_add = st.columns([3, 1, 1])
        
        with col_dish:
            selected_dish = st.selectbox(
                "🍴 اختر الطبق",
                options=dish_names,
                key="dish_selector"
            )
        
        with col_qty:
            quantity_sold = st.number_input(
                "📦 الكمية",
                min_value=1,
                max_value=1000,
                value=1,
                step=1,
                key="quantity_input"
            )
        
        with col_add:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ أضف", key="add_to_cart"):
                st.session_state.sales_cart.append({
                    'dish': selected_dish,
                    'quantity': quantity_sold
                })
                st.rerun()
        
        # عرض سلة المبيعات
        if st.session_state.sales_cart:
            st.markdown("---")
            st.markdown("### 🛒 قائمة المبيعات للمراجعة")
            
            # تحويل القائمة لجدول
            cart_df = pd.DataFrame(st.session_state.sales_cart)
            cart_df.columns = ['الطبق', 'الكمية']
            
            st.dataframe(cart_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"**إجمالي الأطباق:** {len(st.session_state.sales_cart)}")
            
            col_confirm, col_clear, col_remove = st.columns(3)
            
            with col_confirm:
                if st.button("✅ تأكيد المبيعات", use_container_width=True, type="primary"):
                    # حساب جميع المكونات المطلوبة
                    all_ingredients_needed = {}
                    
                    for item in st.session_state.sales_cart:
                        dish_ingredients = calculate_ingredients_needed(
                            recipes_df, 
                            item['dish'], 
                            item['quantity']
                        )
                        for ing, qty in dish_ingredients.items():
                            if ing in all_ingredients_needed:
                                all_ingredients_needed[ing] += qty
                            else:
                                all_ingredients_needed[ing] = qty
                    
                    # التحقق من توفر المخزون
                    warnings = check_stock_availability(inventory_df, all_ingredients_needed)
                    
                    if warnings:
                        st.error("❌ لا يمكن إتمام العملية!")
                        for warning in warnings:
                            st.warning(warning)
                    else:
                        # تحديث المخزون
                        updated_inventory = update_stock(inventory_df, all_ingredients_needed)
                        save_inventory(updated_inventory)
                        
                        # تسجيل المبيعات
                        add_to_sales_log(st.session_state.sales_cart)
                        
                        items_count = len(st.session_state.sales_cart)
                        st.session_state.sales_cart = []
                        
                        st.success(f"✅ تم تسجيل {items_count} مبيعات وتحديث المخزون!")
                        st.rerun()
            
            with col_clear:
                if st.button("🗑️ إلغاء الكل", use_container_width=True, key="sales_clear_all"):
                    st.session_state.sales_cart = []
                    st.rerun()
            
            with col_remove:
                if st.button("↩️ حذف آخر طبق", use_container_width=True, key="sales_remove_last"):
                    st.session_state.sales_cart.pop()
                    st.rerun()


# ========== صفحة إدارة الوصفات ==========

def render_recipes_management():
    """عرض صفحة إدارة الوصفات"""
    
    recipes_df = load_recipes()
    inventory_df = load_inventory()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">📖 الوصفات الحالية</div>', unsafe_allow_html=True)
        
        dish_names = get_dish_names(recipes_df)
        
        if dish_names:
            selected_dish = st.selectbox("اختر وصفة للعرض/التعديل/الحذف", dish_names, key="view_recipe")
            
            if selected_dish:
                dish_data = recipes_df[recipes_df['Dish_Name'] == selected_dish]
                display_df = dish_data[['Ingredient', 'Quantity_Needed']].copy()
                display_df.columns = ['المكون', 'الكمية المطلوبة']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                col_edit, col_delete = st.columns(2)
                
                with col_delete:
                    if st.button("🗑️ حذف هذه الوصفة", use_container_width=True, type="secondary"):
                        recipes_df = recipes_df[recipes_df['Dish_Name'] != selected_dish]
                        save_recipes(recipes_df)
                        st.success(f"✅ تم حذف وصفة '{selected_dish}'")
                        st.rerun()
        else:
            st.info("لا توجد وصفات حالياً")
    
    with col2:
        st.markdown('<div class="section-header-purple">➕ إضافة وصفة جديدة</div>', unsafe_allow_html=True)
        
        new_dish_name = st.text_input("اسم الطبق الجديد", key="new_dish_name")
        
        st.markdown("#### المكونات:")
        
        # تهيئة قائمة المكونات في الجلسة
        if 'new_recipe_ingredients' not in st.session_state:
            st.session_state.new_recipe_ingredients = []
        
        available_ingredients = inventory_df['Ingredient'].tolist()
        
        col_ing, col_qty, col_add = st.columns([2, 1, 1])
        
        with col_ing:
            selected_ingredient = st.selectbox("المكون", available_ingredients, key="recipe_ingredient")
        
        with col_qty:
            ingredient_qty = st.number_input("الكمية", min_value=0.01, value=0.1, step=0.01, key="recipe_qty")
        
        with col_add:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ أضف", key="add_ingredient_to_recipe"):
                unit = inventory_df[inventory_df['Ingredient'] == selected_ingredient]['Unit'].values[0]
                st.session_state.new_recipe_ingredients.append({
                    'ingredient': selected_ingredient,
                    'quantity': ingredient_qty,
                    'unit': unit
                })
        
        # عرض المكونات المضافة
        if st.session_state.new_recipe_ingredients:
            st.markdown("**المكونات المضافة:**")
            for i, ing in enumerate(st.session_state.new_recipe_ingredients):
                col_show, col_remove = st.columns([3, 1])
                with col_show:
                    st.write(f"• {ing['ingredient']}: {ing['quantity']} {ing['unit']}")
                with col_remove:
                    if st.button("❌", key=f"remove_ing_{i}"):
                        st.session_state.new_recipe_ingredients.pop(i)
                        st.rerun()
        
        st.markdown("---")
        
        if st.button("💾 حفظ الوصفة الجديدة", use_container_width=True):
            if not new_dish_name:
                st.error("❌ الرجاء إدخال اسم الطبق!")
            elif not st.session_state.new_recipe_ingredients:
                st.error("❌ الرجاء إضافة مكونات للوصفة!")
            elif new_dish_name in dish_names:
                st.error("❌ هذا الطبق موجود بالفعل!")
            else:
                new_rows = []
                for ing in st.session_state.new_recipe_ingredients:
                    new_rows.append({
                        'Dish_Name': new_dish_name,
                        'Ingredient': ing['ingredient'],
                        'Quantity_Needed': ing['quantity']
                    })
                
                new_df = pd.DataFrame(new_rows)
                recipes_df = pd.concat([recipes_df, new_df], ignore_index=True)
                save_recipes(recipes_df)
                
                st.session_state.new_recipe_ingredients = []
                st.success(f"✅ تم إضافة وصفة '{new_dish_name}' بنجاح!")
                st.rerun()
    
    # قسم تعديل وصفة موجودة
    st.markdown("---")
    st.markdown('<div class="section-header-orange">✏️ تعديل وصفة موجودة</div>', unsafe_allow_html=True)
    
    if dish_names:
        edit_dish = st.selectbox("اختر وصفة للتعديل", dish_names, key="edit_recipe_select")
        
        if edit_dish:
            dish_ingredients = recipes_df[recipes_df['Dish_Name'] == edit_dish].copy()
            
            # تغيير اسم الوصفة
            st.markdown("#### ✏️ تغيير اسم الوصفة:")
            col_rename1, col_rename2 = st.columns([3, 1])
            with col_rename1:
                new_dish_name_edit = st.text_input("الاسم الجديد", value=edit_dish, key="rename_dish_input")
            with col_rename2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 تغيير الاسم", key="rename_dish_btn", use_container_width=True):
                    if new_dish_name_edit and new_dish_name_edit != edit_dish:
                        if new_dish_name_edit in dish_names:
                            st.error("❌ هذا الاسم موجود بالفعل!")
                        else:
                            recipes_df.loc[recipes_df['Dish_Name'] == edit_dish, 'Dish_Name'] = new_dish_name_edit
                            save_recipes(recipes_df)
                            st.success(f"✅ تم تغيير الاسم من '{edit_dish}' إلى '{new_dish_name_edit}'!")
                            st.rerun()
            
            st.markdown("---")
            st.markdown("#### 📦 مكونات الوصفة:")
            
            updated_rows = []
            ingredients_to_delete = []
            
            for idx, row in dish_ingredients.iterrows():
                col1, col2, col3 = st.columns([2, 1, 0.5])
                with col1:
                    st.write(f"📦 {row['Ingredient']}")
                with col2:
                    new_qty = st.number_input(
                        "الكمية",
                        min_value=0.01,
                        value=float(row['Quantity_Needed']),
                        step=0.01,
                        key=f"edit_qty_{idx}",
                        label_visibility="collapsed"
                    )
                with col3:
                    if st.button("🗑️", key=f"delete_ing_{idx}", help="حذف هذا المكون"):
                        ingredients_to_delete.append(row['Ingredient'])
                
                if row['Ingredient'] not in ingredients_to_delete:
                    updated_rows.append({
                        'Dish_Name': edit_dish,
                        'Ingredient': row['Ingredient'],
                        'Quantity_Needed': new_qty
                    })
            
            # حذف المكونات المحددة
            if ingredients_to_delete:
                for ing_to_del in ingredients_to_delete:
                    recipes_df = recipes_df[~((recipes_df['Dish_Name'] == edit_dish) & (recipes_df['Ingredient'] == ing_to_del))]
                save_recipes(recipes_df)
                st.success(f"✅ تم حذف {len(ingredients_to_delete)} مكون من الوصفة!")
                st.rerun()
            
            col_save, col_add_ing = st.columns(2)
            
            with col_save:
                if st.button("💾 حفظ التعديلات", use_container_width=True, key="save_recipe_edits"):
                    # حذف الوصفة القديمة وإضافة المحدثة
                    recipes_df = recipes_df[recipes_df['Dish_Name'] != edit_dish]
                    updated_df = pd.DataFrame(updated_rows)
                    recipes_df = pd.concat([recipes_df, updated_df], ignore_index=True)
                    save_recipes(recipes_df)
                    st.success("✅ تم حفظ التعديلات!")
                    st.rerun()
            
            # إضافة مكون جديد للوصفة
            with col_add_ing:
                with st.expander("➕ إضافة مكون جديد للوصفة"):
                    existing_ingredients = dish_ingredients['Ingredient'].tolist()
                    available_to_add = [i for i in available_ingredients if i not in existing_ingredients]
                    
                    if available_to_add:
                        new_ing = st.selectbox("المكون", available_to_add, key="new_ing_for_recipe")
                        new_ing_qty = st.number_input("الكمية", min_value=0.01, value=0.1, step=0.01, key="new_ing_qty_for_recipe")
                        
                        if st.button("➕ إضافة للوصفة", key="add_new_ing_to_recipe"):
                            new_row = pd.DataFrame({
                                'Dish_Name': [edit_dish],
                                'Ingredient': [new_ing],
                                'Quantity_Needed': [new_ing_qty]
                            })
                            recipes_df = pd.concat([recipes_df, new_row], ignore_index=True)
                            save_recipes(recipes_df)
                            st.success(f"✅ تمت إضافة {new_ing} للوصفة!")
                            st.rerun()
                    else:
                        st.info("جميع المكونات المتاحة موجودة في الوصفة")


# ========== صفحة إدارة المخزون ==========

def render_inventory_management():
    """عرض صفحة إدارة المخزون"""
    
    inventory_df = load_inventory()
    log_df = load_inventory_log()
    
    # الشريط الجانبي للإعدادات
    with st.sidebar:
        st.markdown("### ⚙️ الإعدادات")
        low_stock_threshold = st.slider(
            "حد المخزون المنخفض",
            min_value=1,
            max_value=20,
            value=5,
            help="سيتم تمييز المكونات التي يقل مخزونها عن هذا الحد"
        )
    
    # قسم حالة المخزون
    st.markdown('<div class="section-header">📊 حالة المخزون الحالية</div>', unsafe_allow_html=True)
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    total_items = len(inventory_df)
    low_stock_items = len(inventory_df[inventory_df['Current_Stock'] < low_stock_threshold])
    
    with col_stats1:
        st.metric("إجمالي المكونات", total_items)
    with col_stats2:
        st.metric("مخزون منخفض", low_stock_items, delta_color="inverse")
    with col_stats3:
        st.metric("مخزون كافٍ", total_items - low_stock_items)
    
    # عرض جدول المخزون
    styled_inventory = inventory_df.copy()
    styled_inventory.columns = ['المكون', 'المخزون الحالي', 'الوحدة']
    
    styled_df = styled_inventory.style.apply(
        lambda row: highlight_low_stock(row, low_stock_threshold),
        axis=1
    )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    # تنبيهات المخزون المنخفض
    low_stock_df = inventory_df[inventory_df['Current_Stock'] < low_stock_threshold]
    
    if not low_stock_df.empty:
        st.markdown("### ⚠️ تنبيهات المخزون المنخفض")
        for _, row in low_stock_df.iterrows():
            st.warning(
                f"🔴 **{row['Ingredient']}**: المتبقي {row['Current_Stock']:.2f} {row['Unit']} فقط!"
            )
    
    st.markdown("---")
    
    # قسم الإضافة الجماعية
    st.markdown('<div class="section-header">📦 إضافة وارد جديد (دفعة واحدة)</div>', unsafe_allow_html=True)
    
    st.info("💡 أضف المنتجات واحداً تلو الآخر، ثم راجع القائمة قبل التأكيد النهائي")
    
    # تهيئة سلة الإضافة في الجلسة
    if 'bulk_add_items' not in st.session_state:
        st.session_state.bulk_add_items = []
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        all_ingredients = inventory_df['Ingredient'].tolist()
        bulk_ingredient = st.selectbox("المكون", all_ingredients, key="bulk_ingredient")
    
    with col2:
        bulk_quantity = st.number_input("الكمية", min_value=0.1, value=10.0, step=0.5, key="bulk_quantity")
    
    with col3:
        ingredient_unit = inventory_df[inventory_df['Ingredient'] == bulk_ingredient]['Unit'].values[0] if bulk_ingredient else ""
        st.text_input("الوحدة", value=ingredient_unit, disabled=True, key="bulk_unit_display")
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ أضف للقائمة", key="add_to_bulk"):
            st.session_state.bulk_add_items.append({
                'ingredient': bulk_ingredient,
                'quantity': bulk_quantity,
                'unit': ingredient_unit
            })
            st.rerun()
    
    # عرض القائمة المجمعة
    if st.session_state.bulk_add_items:
        st.markdown("---")
        st.markdown("### 📋 قائمة المراجعة قبل التأكيد")
        
        # تحويل القائمة لجدول
        review_df = pd.DataFrame(st.session_state.bulk_add_items)
        review_df.columns = ['المكون', 'الكمية', 'الوحدة']
        
        st.dataframe(review_df, use_container_width=True, hide_index=True)
        
        # إجمالي الكميات
        st.markdown(f"**إجمالي العناصر:** {len(st.session_state.bulk_add_items)}")
        
        # ملاحظات
        bulk_notes = st.text_input("ملاحظات (اختياري)", placeholder="مثال: توريد من المورد أحمد", key="bulk_notes")
        
        col_confirm, col_clear, col_remove_last = st.columns(3)
        
        with col_confirm:
            if st.button("✅ تأكيد وإضافة للمخزون", use_container_width=True, type="primary"):
                # تحديث المخزون
                for item in st.session_state.bulk_add_items:
                    mask = inventory_df['Ingredient'] == item['ingredient']
                    if mask.any():
                        inventory_df.loc[mask, 'Current_Stock'] += item['quantity']
                
                save_inventory(inventory_df)
                
                # تسجيل في السجل
                log_df = add_to_inventory_log(log_df, st.session_state.bulk_add_items, bulk_notes)
                save_inventory_log(log_df)
                
                items_count = len(st.session_state.bulk_add_items)
                st.session_state.bulk_add_items = []
                
                st.success(f"✅ تم إضافة {items_count} عناصر للمخزون وتسجيلها!")
                st.rerun()
        
        with col_clear:
            if st.button("🗑️ إلغاء الكل", use_container_width=True, key="inv_clear_all"):
                st.session_state.bulk_add_items = []
                st.rerun()
        
        with col_remove_last:
            if st.button("↩️ حذف آخر عنصر", use_container_width=True, key="inv_remove_last"):
                st.session_state.bulk_add_items.pop()
                st.rerun()
    
    st.markdown("---")
    
    # قسم إضافة مكون جديد
    st.markdown('<div class="section-header-purple">🆕 إضافة مكون جديد للنظام</div>', unsafe_allow_html=True)
    
    col_new1, col_new2, col_new3, col_new4 = st.columns([2, 1, 1, 1])
    
    with col_new1:
        brand_new_ingredient = st.text_input("اسم المكون الجديد", key="new_ingredient_name")
    
    with col_new2:
        new_stock = st.number_input("الكمية", min_value=0.1, max_value=1000.0, value=10.0, step=0.5, key="new_stock")
    
    with col_new3:
        new_unit = st.selectbox("الوحدة", options=['كيلو', 'لتر', 'قطعة', 'علبة', 'كيس'], key="new_unit")
    
    with col_new4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🆕 إضافة مكون جديد", key="add_new_ingredient_btn"):
            if brand_new_ingredient:
                if brand_new_ingredient not in inventory_df['Ingredient'].values:
                    new_row = pd.DataFrame({
                        'Ingredient': [brand_new_ingredient],
                        'Current_Stock': [new_stock],
                        'Unit': [new_unit]
                    })
                    inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
                    save_inventory(inventory_df)
                    
                    # تسجيل في السجل
                    log_df = add_to_inventory_log(log_df, [{
                        'ingredient': brand_new_ingredient,
                        'quantity': new_stock,
                        'unit': new_unit
                    }], "إضافة مكون جديد")
                    save_inventory_log(log_df)
                    
                    st.success(f"✅ تمت إضافة المكون '{brand_new_ingredient}' بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ هذا المكون موجود بالفعل!")
            else:
                st.error("❌ الرجاء إدخال اسم المكون!")


# ========== صفحة سجل الوارد ==========

def render_inventory_log():
    """عرض صفحة سجل الوارد"""
    
    log_df = load_inventory_log()
    
    st.markdown('<div class="section-header">📜 سجل الوارد للمخزن</div>', unsafe_allow_html=True)
    
    if log_df.empty:
        st.info("لا توجد سجلات حالياً")
    else:
        # فلترة حسب التاريخ
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            unique_dates = log_df['Date'].unique().tolist()
            unique_dates.insert(0, "الكل")
            selected_date = st.selectbox("فلترة حسب التاريخ", unique_dates, key="log_date_filter")
        
        with col_filter2:
            unique_ingredients = log_df['Ingredient'].unique().tolist()
            unique_ingredients.insert(0, "الكل")
            selected_ingredient_filter = st.selectbox("فلترة حسب المكون", unique_ingredients, key="log_ingredient_filter")
        
        # تطبيق الفلترة
        filtered_df = log_df.copy()
        
        if selected_date != "الكل":
            filtered_df = filtered_df[filtered_df['Date'] == selected_date]
        
        if selected_ingredient_filter != "الكل":
            filtered_df = filtered_df[filtered_df['Ingredient'] == selected_ingredient_filter]
        
        # عرض السجل
        display_log = filtered_df.copy()
        display_log.columns = ['التاريخ', 'المكون', 'الكمية', 'الوحدة', 'ملاحظات']
        
        st.dataframe(
            display_log.sort_values('التاريخ', ascending=False),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # إحصائيات
        st.markdown("---")
        st.markdown("### 📊 إحصائيات")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("إجمالي التوريدات", len(filtered_df))
        
        with col_stat2:
            total_qty = filtered_df['Quantity_Added'].sum()
            st.metric("إجمالي الكميات", f"{total_qty:.2f}")
        
        with col_stat3:
            unique_items = filtered_df['Ingredient'].nunique()
            st.metric("عدد المكونات", unique_items)
        
        # ملخص حسب المكون
        if selected_date != "الكل":
            st.markdown(f"### 📦 ملخص توريدات يوم {selected_date}")
            summary = filtered_df.groupby('Ingredient').agg({
                'Quantity_Added': 'sum'
            }).reset_index()
            summary.columns = ['المكون', 'إجمالي الكمية']
            st.dataframe(summary, use_container_width=True, hide_index=True)


# ========== صفحة سجل المبيعات ==========

def render_sales_log():
    """عرض صفحة سجل المبيعات"""
    
    sales_df = load_sales_log()
    
    st.markdown('<div class="section-header-purple">💰 سجل المبيعات</div>', unsafe_allow_html=True)
    
    if sales_df.empty:
        st.info("لا توجد مبيعات مسجلة حالياً")
    else:
        # فلترة حسب التاريخ
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            unique_dates = sales_df['Date'].unique().tolist()
            unique_dates.insert(0, "الكل")
            selected_date = st.selectbox("فلترة حسب التاريخ", unique_dates, key="sales_date_filter")
        
        with col_filter2:
            unique_dishes = sales_df['Dish_Name'].unique().tolist()
            unique_dishes.insert(0, "الكل")
            selected_dish_filter = st.selectbox("فلترة حسب الطبق", unique_dishes, key="sales_dish_filter")
        
        # تطبيق الفلترة
        filtered_df = sales_df.copy()
        
        if selected_date != "الكل":
            filtered_df = filtered_df[filtered_df['Date'] == selected_date]
        
        if selected_dish_filter != "الكل":
            filtered_df = filtered_df[filtered_df['Dish_Name'] == selected_dish_filter]
        
        # عرض السجل
        display_sales = filtered_df.copy()
        display_sales.columns = ['التاريخ', 'الوقت', 'الطبق', 'الكمية', 'ملاحظات']
        
        st.dataframe(
            display_sales.sort_values(['التاريخ', 'الوقت'], ascending=[False, False]),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # إحصائيات
        st.markdown("---")
        st.markdown("### 📊 إحصائيات المبيعات")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("إجمالي الطلبات", len(filtered_df))
        
        with col_stat2:
            total_qty = filtered_df['Quantity'].sum()
            st.metric("إجمالي الأطباق المباعة", int(total_qty))
        
        with col_stat3:
            unique_dishes_count = filtered_df['Dish_Name'].nunique()
            st.metric("أنواع الأطباق", unique_dishes_count)
        
        # ملخص حسب الطبق
        st.markdown("---")
        st.markdown("### 🍔 ملخص المبيعات حسب الطبق")
        
        summary = filtered_df.groupby('Dish_Name').agg({
            'Quantity': 'sum'
        }).reset_index()
        summary.columns = ['الطبق', 'إجمالي الكمية']
        summary = summary.sort_values('إجمالي الكمية', ascending=False)
        st.dataframe(summary, use_container_width=True, hide_index=True)
        
        # ملخص حسب التاريخ (إذا تم اختيار "الكل")
        if selected_date == "الكل":
            st.markdown("---")
            st.markdown("### 📅 ملخص المبيعات حسب اليوم")
            
            daily_summary = filtered_df.groupby('Date').agg({
                'Quantity': 'sum'
            }).reset_index()
            daily_summary.columns = ['التاريخ', 'إجمالي الأطباق']
            daily_summary = daily_summary.sort_values('التاريخ', ascending=False)
            st.dataframe(daily_summary, use_container_width=True, hide_index=True)


# ========== الدالة الرئيسية ==========

def main():
    """الدالة الرئيسية للتطبيق"""
    
    # العنوان الرئيسي
    st.markdown('<h1 class="header-title">🍔 الوحش برجر - نظام إدارة المخزون</h1>', unsafe_allow_html=True)
    
    # التبويبات الرئيسية
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 المبيعات ولوحة المعلومات",
        "📖 إدارة الوصفات",
        "📦 إدارة المخزون",
        "📜 سجل الوارد",
        "💰 سجل المبيعات"
    ])
    
    with tab1:
        render_sales_dashboard()
    
    with tab2:
        render_recipes_management()
    
    with tab3:
        render_inventory_management()
    
    with tab4:
        render_inventory_log()
    
    with tab5:
        render_sales_log()
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; padding: 20px;'>
            <p>🍽️ نظام إدارة مخزون المطعم | النسخة المتقدمة | تم التطوير بواسطة Python & Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
