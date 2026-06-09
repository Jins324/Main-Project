#!/usr/bin/env python
"""
Demo: How Age-Based Assessment Gets Child's Age
Shows the complete flow from database to age-adjusted scoring
"""

import os
import sys
import django

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import CustomUser
from core.enhanced_scoring import EnhancedScoringSystem
from age_based_assessment import AgeBasedAssessment

def demonstrate_age_detection():
    """Demonstrate exactly how the system gets and uses child's age"""
    
    print("🔍 HOW AGE-BASED ASSESSMENT GETS CHILD'S AGE")
    print("=" * 60)
    
    # Step 1: Show database model structure
    print("\n📊 STEP 1: DATABASE MODEL - CustomUser")
    print("-" * 40)
    print("The system stores age in the CustomUser model:")
    print("  Field: age = models.PositiveIntegerField(default=5, null=True, blank=True)")
    print("  Location: core/models.py line 7")
    print("  Type: PositiveIntegerField (stores integer age)")
    print("  Default: 5 years old if not specified")
    
    # Step 2: Show how age is accessed
    print("\n🔑 STEP 2: AGE ACCESS IN VIEWS")
    print("-" * 40)
    print("When a logged-in user performs an activity:")
    print("  Code: request.user.age")
    print("  Example: request.user.age returns 7 for a 7-year-old")
    print("  Used in: handwriting_views.py line 326")
    print("  Used in: robust_audio_to_text_views.py line 322")
    
    # Step 3: Create test users to demonstrate
    print("\n👥 STEP 3: CREATING TEST USERS")
    print("-" * 40)
    
    test_ages = [4, 7, 10, 13, 16]
    test_users = []
    
    for age in test_ages:
        username = f"testchild_{age}"
        try:
            user = CustomUser.objects.get(username=username)
            print(f"  ✅ Found existing user: {username} (age {user.age})")
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(
                username=username,
                email=f'test{age}@example.com',
                password='test123',
                age=age,
                is_parent=False
            )
            print(f"  🆕 Created new user: {username} (age {user.age})")
        
        test_users.append(user)
    
    # Step 4: Show age group determination
    print("\n🎯 STEP 4: AGE GROUP DETERMINATION")
    print("-" * 40)
    
    age_assessment = AgeBasedAssessment()
    
    for user in test_users:
        age_group = age_assessment.get_age_group(user.age)
        print(f"  User {user.username} (age {user.age}) → {age_group['description']}")
        print(f"    Difficulty Multiplier: {age_group['difficulty_multiplier']}")
        print(f"    Effort Bonus: {age_group['effort_bonus']}")
        print(f"    Completion Threshold: {age_group['completion_threshold']}")
    
    # Step 5: Show real scoring example
    print("\n📝 STEP 5: REAL SCORING EXAMPLE")
    print("-" * 40)
    
    scoring_system = EnhancedScoringSystem()
    
    # Same handwriting performance for all ages
    base_ml_result = {'score': 70, 'confidence': 0.8}
    time_taken = 10
    strokes_count = 3
    
    print(f"Same handwriting performance for all children:")
    print(f"  Base ML Score: 70")
    print(f"  Time Taken: 10 seconds")
    print(f"  Strokes Count: 3")
    print()
    
    for user in test_users:
        # This is exactly how the system works in real code
        result = scoring_system.calculate_handwriting_score(
            base_ml_result, 
            time_taken, 
            strokes_count, 
            child_age=user.age  # ← This is where age is used!
        )
        
        bonus = (result['final_score'] - 70) / 70 * 100
        print(f"  {user.username} (age {user.age}): {result['final_score']:.1f} points ({bonus:+.1f}% bonus)")
    
    # Step 6: Show database storage
    print("\n💾 STEP 6: DATABASE STORAGE")
    print("-" * 40)
    print("The system stores both original and age-adjusted scores:")
    print("  Metadata fields:")
    print("    'base_score': 70.0")
    print("    'age_adjusted_score': 97.3")
    print("    'age_group': 'Toddler (3-5 years)'")
    print("    'age_feedback': 'Amazing job! You\\'re doing fantastic!'")
    
    # Step 7: Show the complete flow
    print("\n🔄 STEP 7: COMPLETE FLOW")
    print("-" * 40)
    print("1. Child logs in → Django creates session")
    print("2. Child performs activity → request.user is available")
    print("3. System reads age → request.user.age (e.g., 7)")
    print("4. Age group determined → 'Preschool (6-8 years)'")
    print("5. Multipliers applied → 10% difficulty + 15% effort bonus")
    print("6. Score calculated → Base 70 × 1.10 × 1.15 = 88.55")
    print("7. Feedback generated → Age-appropriate message")
    print("8. Results stored → Both base and adjusted scores saved")
    
    print("\n" + "=" * 60)
    print("✅ AGE DETECTION AND USAGE FULLY DEMONSTRATED!")
    print("=" * 60)
    
    print("\n🎯 KEY POINTS:")
    print("  • Age stored in CustomUser.age field (database)")
    print("  • Accessed via request.user.age (Django session)")
    print("  • Automatically applied to all scoring calculations")
    print("  • Younger children get significant bonuses")
    print("  • Age-appropriate feedback generated")
    print("  • Both original and adjusted scores stored")

if __name__ == "__main__":
    demonstrate_age_detection()
