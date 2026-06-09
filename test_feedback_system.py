#!/usr/bin/env python
"""
Test script for the feedback system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import CustomUser, Feedback
from django.test import Client
from django.urls import reverse

def test_feedback_system():
    """Test the feedback system functionality"""
    print("🧪 Testing Feedback System...")
    print("=" * 50)
    
    # Check if Feedback model exists
    try:
        feedback_count = Feedback.objects.count()
        print(f"✅ Feedback model exists - {feedback_count} feedback records")
    except Exception as e:
        print(f"❌ Feedback model error: {e}")
        return False
    
    # Check parent-child relationships
    parents = CustomUser.objects.filter(is_parent=True)
    children = CustomUser.objects.filter(is_parent=False)
    
    print(f"✅ Found {parents.count()} parent accounts")
    print(f"✅ Found {children.count()} child accounts")
    
    # Test URL patterns
    try:
        feedback_url = reverse('feedback_center')
        print(f"✅ Feedback center URL: {feedback_url}")
    except Exception as e:
        print(f"❌ URL error: {e}")
        return False
    
    # Test parent-child linking
    for parent in parents:
        linked_children = parent.children.all()
        if linked_children.exists():
            print(f"✅ Parent {parent.username} has {linked_children.count()} linked children")
        else:
            print(f"⚠️  Parent {parent.username} has no linked children")
    
    # Create test feedback if none exists
    if feedback_count == 0 and children.exists() and parents.exists():
        try:
            child = children.first()
            parent = parents.first()
            
            # Link child to parent if not linked
            if not child.parent_account:
                child.parent_account = parent
                child.save()
                print(f"✅ Linked {child.username} to {parent.username}")
            
            # Create test feedback
            feedback = Feedback.objects.create(
                child=child,
                parent=parent,
                feedback_type='general_message',
                title='Test Message',
                message='This is a test message from the system.',
                priority='medium'
            )
            print(f"✅ Created test feedback: {feedback}")
        except Exception as e:
            print(f"❌ Error creating test feedback: {e}")
    
    # Test API endpoints
    client = Client()
    
    # Test feedback stats API
    try:
        response = client.get('/api/feedback-stats/')
        if response.status_code == 302:  # Redirect to login (expected)
            print("✅ Feedback stats API requires authentication (correct)")
        elif response.status_code == 200:
            print("✅ Feedback stats API working")
        else:
            print(f"⚠️  Feedback stats API status: {response.status_code}")
    except Exception as e:
        print(f"❌ Feedback stats API error: {e}")
    
    print("\n🎯 Feedback System Status:")
    print("=" * 30)
    
    if parents.exists() and children.exists():
        print("✅ Basic setup complete")
        print("✅ Ready for testing with browser")
        print("\n📱 Test URLs:")
        print(f"   Feedback Center: http://127.0.0.1:8000{feedback_url}")
        print(f"   Parent Dashboard: http://127.0.0.1:8000/parent/dashboard/")
        print(f"   Child Dashboard: http://127.0.0.1:8000/child/dashboard/")
        
        if parents.exists():
            parent = parents.first()
            print(f"\n👤 Test Parent Account: {parent.username}")
        
        if children.exists():
            child = children.first()
            print(f"👶 Test Child Account: {child.username}")
        
        print("\n🔧 Next Steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Login as parent and check dashboard")
        print("3. Login as child and send message")
        print("4. Check parent dashboard for new message")
        
    else:
        print("⚠️  Need to create parent and child accounts first")
        print("Run: python manage.py createsuperuser")
    
    return True

if __name__ == '__main__':
    test_feedback_system()
