"""
Age-Based Assessment System for Kids Learning Tool
Provides age-appropriate scoring and assessment adjustments
"""

class AgeBasedAssessment:
    """Age-based assessment system for fair evaluation"""
    
    def __init__(self):
        self.age_groups = {
            'toddler': {
                'age_range': (3, 5),
                'difficulty_multiplier': 1.15,  # 15% bonus
                'effort_bonus': 1.20,          # 20% effort bonus
                'patience_factor': 1.25,        # More patience
                'completion_threshold': 0.70,   # Need 70% completion
                'description': 'Toddler (3-5 years)',
                'characteristics': {
                    'attention_span': 'very_short',  # 2-5 minutes
                    'motor_skills': 'developing',
                    'cognitive_level': 'concrete',
                    'learning_style': 'play_based'
                }
            },
            'preschool': {
                'age_range': (6, 8),
                'difficulty_multiplier': 1.10,  # 10% bonus
                'effort_bonus': 1.15,          # 15% effort bonus
                'patience_factor': 1.15,        # More patience
                'completion_threshold': 0.75,   # Need 75% completion
                'description': 'Preschool (6-8 years)',
                'characteristics': {
                    'attention_span': 'short',     # 5-10 minutes
                    'motor_skills': 'developing',
                    'cognitive_level': 'concrete',
                    'learning_style': 'visual_kinesthetic'
                }
            },
            'elementary': {
                'age_range': (9, 10),
                'difficulty_multiplier': 1.05,  # 5% bonus
                'effort_bonus': 1.05,          # 5% effort bonus
                'patience_factor': 1.05,        # Slightly more patience
                'completion_threshold': 0.85,   # Need 85% completion
                'description': 'Elementary (9-10 years)',
                'characteristics': {
                    'attention_span': 'moderate',   # 10-20 minutes
                    'motor_skills': 'developed',
                    'cognitive_level': 'concrete_to_abstract',
                    'learning_style': 'mixed'
                }
            },
            'preteen': {
                'age_range': (11, 12),
                'difficulty_multiplier': 1.0,   # No bonus
                'effort_bonus': 1.0,           # No effort bonus
                'patience_factor': 1.0,        # Standard expectations
                'completion_threshold': 0.95,   # Need 95% completion
                'description': 'Preteen (11-12 years)',
                'characteristics': {
                    'attention_span': 'developing', # 20-30 minutes
                    'motor_skills': 'developed',
                    'cognitive_level': 'abstract',
                    'learning_style': 'logical'
                }
            },
            'teen': {
                'age_range': (13, 18),
                'difficulty_multiplier': 0.95,  # Slightly higher standards
                'effort_bonus': 0.95,          # Less effort bonus
                'patience_factor': 0.95,        # Higher expectations
                'completion_threshold': 1.0,    # Need full completion
                'description': 'Teen (13-18 years)',
                'characteristics': {
                    'attention_span': 'long',       # 30+ minutes
                    'motor_skills': 'fully_developed',
                    'cognitive_level': 'abstract',
                    'learning_style': 'independent'
                }
            }
        }
    
    def get_age_group(self, age):
        """Get age group configuration for given age"""
        if age is None:
            return self.age_groups['elementary']  # Default fallback
        
        for group_name, group_config in self.age_groups.items():
            min_age, max_age = group_config['age_range']
            if min_age <= age <= max_age:
                return group_config
        
        # Default to teen if age is higher
        return self.age_groups['teen']
    
    def adjust_handwriting_score(self, base_score, age, additional_metrics=None):
        """Adjust handwriting score based on age"""
        age_group = self.get_age_group(age)
        
        # Base adjustment
        adjusted_score = base_score * age_group['difficulty_multiplier']
        
        # Effort bonus for younger children
        if additional_metrics:
            effort_score = self._calculate_effort_bonus(additional_metrics, age_group)
            adjusted_score = max(adjusted_score, adjusted_score + effort_score)
        
        # Motor skills adjustment for younger children
        if age <= 8:  # Toddler and preschool
            motor_adjustment = self._calculate_motor_skills_adjustment(additional_metrics)
            adjusted_score += motor_adjustment
        
        return min(100, max(0, adjusted_score))
    
    def adjust_speech_score(self, base_score, age, additional_metrics=None):
        """Adjust speech score based on age"""
        age_group = self.get_age_group(age)
        
        # Base adjustment
        adjusted_score = base_score * age_group['difficulty_multiplier']
        
        # Speech development adjustments
        if age <= 8:  # Younger children need more patience
            speech_adjustment = self._calculate_speech_development_adjustment(additional_metrics, age_group)
            adjusted_score += speech_adjustment
        
        # Effort bonus
        if additional_metrics:
            effort_score = self._calculate_effort_bonus(additional_metrics, age_group)
            adjusted_score = max(adjusted_score, adjusted_score + effort_score)
        
        return min(100, max(0, adjusted_score))
    
    def adjust_cognitive_score(self, base_score, age, activity_type='general'):
        """Adjust cognitive game scores based on age"""
        age_group = self.get_age_group(age)
        
        # Base adjustment
        adjusted_score = base_score * age_group['difficulty_multiplier']
        
        # Age-specific cognitive adjustments
        if activity_type == 'memory':
            adjusted_score = self._adjust_memory_score(adjusted_score, age_group)
        elif activity_type == 'pattern':
            adjusted_score = self._adjust_pattern_score(adjusted_score, age_group)
        elif activity_type == 'puzzle':
            adjusted_score = self._adjust_puzzle_score(adjusted_score, age_group)
        
        return min(100, max(0, adjusted_score))
    
    def get_completion_threshold(self, age):
        """Get age-appropriate completion threshold"""
        age_group = self.get_age_group(age)
        return age_group['completion_threshold']
    
    def get_age_appropriate_feedback(self, age, score, activity_type):
        """Generate age-appropriate feedback"""
        age_group = self.get_age_group(age)
        
        feedback_templates = {
            'toddler': {
                'excellent': [
                    "Amazing job! You're doing fantastic for your age! 🌟",
                    "Wow! Such great effort from a little superstar! ⭐",
                    "Incredible work! You're learning so fast! 🚀"
                ],
                'good': [
                    "Great try! Keep up the wonderful effort! 💪",
                    "Nice work! You're doing really well! 👏",
                    "Good job! Every try makes you better! 🌈"
                ],
                'improving': [
                    "Keep trying! You're getting better every time! 📈",
                    "Don't worry! Practice makes perfect! 🎯",
                    "You can do it! Just keep trying! 💖"
                ]
            },
            'preschool': {
                'excellent': [
                    "Fantastic work! You're really getting the hang of this! 🎉",
                    "Super job! Your skills are growing so fast! 🌱",
                    "Excellent! You're doing amazing for your age! 🏆"
                ],
                'good': [
                    "Great effort! Keep up the good work! 🌟",
                    "Nice going! You're learning well! 📚",
                    "Good job! Your practice is paying off! 🎯"
                ],
                'improving': [
                    "Keep practicing! You're improving! 📈",
                    "Almost there! A little more practice! 💪",
                    "Don't give up! You're getting closer! 🎪"
                ]
            },
            'elementary': {
                'excellent': [
                    "Outstanding work! Your skills are impressive! 🏅",
                    "Excellent performance! Keep up the great work! 🌟",
                    "Fantastic job! You're mastering this! 🎯"
                ],
                'good': [
                    "Good work! Keep practicing to improve further! 📖",
                    "Nice job! You're on the right track! 🛤️",
                    "Well done! Your effort shows! 🌈"
                ],
                'improving': [
                    "Keep working at it! Progress takes time! 📈",
                    "Practice more! You'll get there! 🎯",
                    "Don't stop trying! Every attempt counts! 💪"
                ]
            },
            'preteen': {
                'excellent': [
                    "Excellent work! Your dedication shows! 🏆",
                    "Outstanding performance! Keep it up! 🌟",
                    "Superb job! You're mastering these skills! 🎯"
                ],
                'good': [
                    "Good effort! Continue to practice! 📚",
                    "Nice work! You're developing well! 📈",
                    "Well done! Keep pushing yourself! 💪"
                ],
                'improving': [
                    "Keep practicing! Improvement comes with effort! 🎯",
                    "Don't give up! You're capable of more! 🌟",
                    "Stay focused! Your hard work will pay off! 💪"
                ]
            },
            'teen': {
                'excellent': [
                    "Excellent performance! Your skills are impressive! 🏅",
                    "Outstanding work! You've mastered this! 🎯",
                    "Superb execution! Keep up the high standards! 🌟"
                ],
                'good': [
                    "Good work! Continue to refine your skills! 📚",
                    "Solid effort! There's room for growth! 📈",
                    "Well done! Your dedication is evident! 💪"
                ],
                'improving': [
                    "Keep practicing! Excellence requires consistency! 🎯",
                    "Don't settle! Push for continuous improvement! 🌟",
                    "Stay focused! Your potential is unlimited! 💪"
                ]
            }
        }
        
        # Determine performance level
        if score >= 90:
            level = 'excellent'
        elif score >= 70:
            level = 'good'
        else:
            level = 'improving'
        
        # Get age group name for feedback
        for group_name, group_config in self.age_groups.items():
            if group_config == age_group:
                age_group_name = group_name
                break
        
        # Get appropriate feedback
        feedback_list = feedback_templates.get(age_group_name, feedback_templates['elementary'])
        import random
        return random.choice(feedback_list.get(level, feedback_list['improving']))
    
    def _calculate_effort_bonus(self, metrics, age_group):
        """Calculate effort bonus based on engagement metrics"""
        bonus = 0
        
        if not metrics:
            return 0
        
        # Time spent bonus (younger kids who try longer get more bonus)
        if 'time_spent' in metrics:
            time_spent = metrics['time_spent']
            if age_group['characteristics']['attention_span'] == 'very_short':
                # Toddlers: bonus for trying more than 2 minutes
                if time_spent > 120:  # More than 2 minutes
                    bonus += 5 * age_group['effort_bonus']
            elif age_group['characteristics']['attention_span'] == 'short':
                # Preschool: bonus for trying more than 5 minutes
                if time_spent > 300:  # More than 5 minutes
                    bonus += 3 * age_group['effort_bonus']
        
        # Attempt count bonus
        if 'attempts' in metrics:
            attempts = metrics['attempts']
            if attempts > 1:  # Multiple attempts show effort
                bonus += min(5, attempts) * age_group['effort_bonus']
        
        return bonus
    
    def _calculate_motor_skills_adjustment(self, metrics):
        """Calculate motor skills adjustment for younger children"""
        adjustment = 0
        
        if not metrics:
            return 0
        
        # Strokes count adjustment (younger kids may have less control)
        if 'strokes_count' in metrics:
            strokes = metrics['strokes_count']
            if strokes > 5:  # Many strokes might indicate effort
                adjustment += 2
        
        # Consistency bonus
        if 'consistency_score' in metrics:
            consistency = metrics['consistency_score']
            if consistency > 0.6:  # Good consistency for young age
                adjustment += 3
        
        return adjustment
    
    def _calculate_speech_development_adjustment(self, metrics, age_group):
        """Calculate speech development adjustment"""
        adjustment = 0
        
        if not metrics:
            return 0
        
        # Word attempts bonus
        if 'word_attempts' in metrics:
            attempts = metrics['word_attempts']
            if attempts > 0:  # Trying to speak is effort
                adjustment += 2 * age_group['effort_bonus']
        
        # Clarity bonus (considering age)
        if 'clarity_score' in metrics:
            clarity = metrics['clarity_score']
            expected_clarity = 0.5 if age_group['characteristics']['attention_span'] == 'very_short' else 0.6
            if clarity >= expected_clarity:
                adjustment += 3 * age_group['effort_bonus']
        
        return adjustment
    
    def _adjust_memory_score(self, score, age_group):
        """Adjust memory game score based on age"""
        # Younger children get more patience in memory games
        if age_group['characteristics']['cognitive_level'] == 'concrete':
            return score * 1.1  # 10% bonus
        return score
    
    def _adjust_pattern_score(self, score, age_group):
        """Adjust pattern recognition score based on age"""
        # Pattern recognition varies by cognitive development
        if age_group['characteristics']['cognitive_level'] == 'concrete':
            return score * 1.08  # 8% bonus
        elif age_group['characteristics']['cognitive_level'] == 'concrete_to_abstract':
            return score * 1.04  # 4% bonus
        return score
    
    def _adjust_puzzle_score(self, score, age_group):
        """Adjust puzzle score based on age"""
        # Puzzle solving depends on motor and cognitive skills
        if age_group['characteristics']['motor_skills'] == 'developing':
            return score * 1.12  # 12% bonus
        elif age_group['characteristics']['motor_skills'] == 'developed':
            return score * 1.05  # 5% bonus
        return score
    
    def get_age_specific_tips(self, age, activity_type, performance_data):
        """Get age-specific learning tips"""
        age_group = self.get_age_group(age)
        
        tips = {
            'handwriting': {
                'toddler': [
                    "Try using thicker crayons or markers - they're easier to hold!",
                    "Practice on large paper first, then smaller sizes.",
                    "Make it fun! Draw shapes and letters together."
                ],
                'preschool': [
                    "Practice tracing letters before writing them freely.",
                    "Use lined paper to help with letter size.",
                    "Take breaks! Young hands get tired quickly."
                ],
                'elementary': [
                    "Focus on letter consistency and spacing.",
                    "Practice writing short sentences about your day.",
                    "Try different writing styles to find what's comfortable."
                ],
                'preteen': [
                    "Work on developing your own handwriting style.",
                    "Practice writing faster while maintaining quality.",
                    "Try calligraphy or artistic lettering for fun."
                ],
                'teen': [
                    "Focus on legibility and efficiency.",
                    "Practice note-taking skills for future education.",
                    "Develop signature and professional writing style."
                ]
            },
            'speech': {
                'toddler': [
                    "Break words into small, easy sounds.",
                    "Use hand gestures and facial expressions!",
                    "Practice with songs and rhymes."
                ],
                'preschool': [
                    "Speak slowly and clearly - one word at a time.",
                    "Practice in front of a mirror.",
                    "Record yourself and listen back!"
                ],
                'elementary': [
                    "Focus on pronunciation of difficult words.",
                    "Practice reading aloud regularly.",
                    "Learn to speak in complete sentences."
                ],
                'preteen': [
                    "Work on public speaking confidence.",
                    "Practice explaining complex ideas clearly.",
                    "Develop your own speaking style."
                ],
                'teen': [
                    "Focus on articulation and clarity.",
                    "Practice debate and discussion skills.",
                    "Develop professional communication abilities."
                ]
            },
            'cognitive': {
                'toddler': [
                    "Start with simple matching games.",
                    "Use colorful, engaging materials.",
                    "Keep sessions short and fun!"
                ],
                'preschool': [
                    "Try memory games with pictures.",
                    "Practice pattern recognition daily.",
                    "Celebrate small victories!"
                ],
                'elementary': [
                    "Challenge yourself with harder levels gradually.",
                    "Focus on strategy, not just speed.",
                    "Learn from mistakes and try again."
                ],
                'preteen': [
                    "Try complex problem-solving games.",
                    "Focus on logical thinking skills.",
                    "Compete with yourself to improve."
                ],
                'teen': [
                    "Tackle advanced strategic challenges.",
                    "Focus on efficiency and optimization.",
                    "Develop critical thinking abilities."
                ]
            }
        }
        
        # Get age group name
        for group_name, group_config in self.age_groups.items():
            if group_config == age_group:
                age_group_name = group_name
                break
        
        activity_tips = tips.get(activity_type, {}).get(age_group_name, [])
        
        # Add performance-specific tips
        if performance_data:
            if performance_data.get('score', 0) < 70:
                activity_tips.append("Remember: progress takes time and patience!")
            elif performance_data.get('score', 0) < 90:
                activity_tips.append("You're doing great! A little more practice will help!")
        
        return activity_tips
