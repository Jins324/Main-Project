#!/usr/bin/env python3
"""
Fix bird_anatomy.html JavaScript issues
"""

import re

# Read the file
with open('c:\\Users\\Bibin\\Downloads\\Kids_Learning_Tool\\core\\templates\\core\\bird_anatomy.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic JavaScript section and replace it
js_start = content.find('{% block extra_js %}')
if js_start != -1:
    # Find the end of the file
    js_end = content.find('</script>', js_start)
    if js_end != -1:
        # Replace the problematic JavaScript section
        new_js = '''<script>
// Go to Dashboard functionality
function goToDashboard() {
    console.log('Navigating to dashboard...');
    try {
        window.location.href = '/child/dashboard/';
    } catch (error) {
        console.error('Navigation error:', error);
        // Fallback navigation
        window.location.assign('/child/dashboard/');
    }
}

// Alternative function name to avoid conflicts
function navigateToDashboard() {
    console.log('Alternative navigation to dashboard...');
    window.location.href = '/child/dashboard/';
}

// Handle button clicks with event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add click listeners to all dashboard buttons
    const dashboardButtons = document.querySelectorAll('button[onclick*="goToDashboard"]');
    dashboardButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Dashboard button clicked');
            window.location.href = '/child/dashboard/';
        });
    });
});
</script>'''
        
        # Replace the problematic section
        before_js = content[:js_start]
        after_js = content[js_end + 9:]  # After </script>
        
        new_content = before_js + new_js + after_js
        
        # Write back to file
        with open('c:\\Users\\Bibin\\Downloads\\Kids_Learning_Tool\\core\\templates\\core\\bird_anatomy.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Fixed bird_anatomy.html JavaScript issues")
    else:
        print("❌ Could not find JavaScript section to fix")
else:
    print("❌ Could not find extra_js block")
