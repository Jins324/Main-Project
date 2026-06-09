#!/usr/bin/env python
"""
Fix database schema issues - add missing learning_needs column
"""
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.db import connection
from core.models import CustomUser

def check_database_schema():
    """Check current database schema"""
    
    print("🔍 CHECKING DATABASE SCHEMA...")
    print("=" * 60)
    
    # Get table schema
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(core_customuser);")
        columns = cursor.fetchall()
        
        print("📋 Current CustomUser table columns:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
    
    print(f"\n📊 Total columns: {len(columns)}")
    
    # Check if learning_needs exists
    column_names = [col[1] for col in columns]
    has_learning_needs = 'learning_needs' in column_names
    
    print(f"\n🔍 learning_needs column exists: {'✅ Yes' if has_learning_needs else '❌ No'}")
    
    return has_learning_needs, columns

def check_model_definition():
    """Check what fields the model expects"""
    
    print(f"\n📋 CHECKING MODEL DEFINITION...")
    print("=" * 60)
    
    # Get model fields
    fields = CustomUser._meta.get_fields()
    
    print("📋 Model fields:")
    for field in fields:
        if hasattr(field, 'name'):
            field_type = field.__class__.__name__
            print(f"   - {field.name} ({field_type})")
    
    print(f"\n📊 Total model fields: {len(fields)}")
    
    # Check if learning_needs is in model
    field_names = [field.name for field in fields if hasattr(field, 'name')]
    has_learning_needs_model = 'learning_needs' in field_names
    
    print(f"\n🔍 learning_needs in model: {'✅ Yes' if has_learning_needs_model else '❌ No'}")
    
    return has_learning_needs_model, field_names

def add_missing_column():
    """Add missing learning_needs column to database"""
    
    print(f"\n🔧 ADDING MISSING COLUMN...")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            # Add learning_needs column as TextField (blank=True, null=True)
            cursor.execute("""
                ALTER TABLE core_customuser 
                ADD COLUMN learning_needs TEXT NULL;
            """)
            
            print("✅ learning_needs column added successfully")
            
            # Verify the column was added
            cursor.execute("PRAGMA table_info(core_customuser);")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            if 'learning_needs' in column_names:
                print("✅ Column verification successful")
                return True
            else:
                print("❌ Column verification failed")
                return False
                
    except Exception as e:
        print(f"❌ Error adding column: {e}")
        return False

def check_main_page_view():
    """Check what the main_page view is trying to access"""
    
    print(f"\n🔍 CHECKING MAIN PAGE VIEW...")
    print("=" * 60)
    
    try:
        # Read the main_page view
        with open('core/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find main_page function
        import re
        main_page_match = re.search(r'def main_page\(request\):(.*?)(?=\n@|\ndef|\nclass|\Z)', content, re.DOTALL)
        
        if main_page_match:
            main_page_code = main_page_match.group(1)
            print("📋 main_page function code:")
            print(main_page_code[:500] + "..." if len(main_page_code) > 500 else main_page_code)
            
            # Check for learning_needs usage
            if 'learning_needs' in main_page_code:
                print("✅ learning_needs is used in main_page")
                
                # Find the specific line
                lines = main_page_code.split('\n')
                for i, line in enumerate(lines):
                    if 'learning_needs' in line:
                        print(f"   Line {i+1}: {line.strip()}")
            else:
                print("❌ learning_needs not found in main_page")
        else:
            print("❌ main_page function not found")
            
    except Exception as e:
        print(f"❌ Error reading views.py: {e}")

def test_main_page_access():
    """Test if main page works after fix"""
    
    print(f"\n🧪 TESTING MAIN PAGE ACCESS...")
    print("=" * 60)
    
    try:
        from django.test.client import Client
        
        client = Client()
        response = client.get('/')
        
        print(f"📄 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            return True
        else:
            print(f"❌ Main page failed: {response.status_code}")
            if response.status_code == 500:
                print("🔍 Server error - checking content...")
                content = response.content.decode('utf-8')
                if 'learning_needs' in content:
                    print("❌ Still has learning_needs error")
                else:
                    print("✅ No learning_needs error in response")
            return False
            
    except Exception as e:
        print(f"❌ Error testing main page: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 DATABASE SCHEMA FIX")
    print("=" * 60)
    
    # Check current schema
    has_column_db, db_columns = check_database_schema()
    
    # Check model definition
    has_column_model, model_fields = check_model_definition()
    
    # Check main page view
    check_main_page_view()
    
    # If column exists in model but not database, add it
    if has_column_model and not has_column_db:
        print(f"\n🎯 ACTION NEEDED: Column in model but missing from database")
        success = add_missing_column()
        
        if success:
            print(f"\n✅ Column added successfully!")
            # Test main page
            test_main_page_access()
        else:
            print(f"\n❌ Failed to add column")
    
    elif not has_column_model and has_column_db:
        print(f"\n⚠️  Column exists in database but not in model")
        print("📋 Consider removing column from database or adding to model")
    
    elif not has_column_model and not has_column_db:
        print(f"\n⚠️  Column missing from both model and database")
        print("📋 Check if learning_needs should be added to model")
    
    else:
        print(f"\n✅ Column exists in both model and database")
        test_main_page_access()
    
    print(f"\n" + "=" * 60)
    print(f"🔧 DATABASE SCHEMA FIX COMPLETE")

if __name__ == "__main__":
    main()
