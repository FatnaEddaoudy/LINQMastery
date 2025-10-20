import sys
import json
import os
from PyPDF2 import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text(file_path):
    """Extract text based on file extension"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"

def extract_name_from_cv(text):
    """Extract candidate name from CV using NLP"""
    lines = text.split('\n')[:5]
    
    for line in lines:
        line = line.strip()
        if len(line) < 3 or len(line) > 50:
            continue
            
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
    
    words = text.split()[:20]
    name_pattern = r'^[A-Z][a-z]+\s+[A-Z][a-z]+'
    for i, word in enumerate(words):
        potential_name = ' '.join(words[i:min(i+3, len(words))])
        if re.match(name_pattern, potential_name):
            parts = potential_name.split()[:2]
            return ' '.join(parts)
    
    return None

def extract_skills_with_nlp(text):
    """Extract skills using NLP and contextual understanding with fuzzy matching"""
    
    stop_words = {
        'if', 'for', 'while', 'do', 'then', 'else', 'when', 'where', 'how', 'what', 'who',
        'als', 'voor', 'met', 'van', 'een', 'het', 'de', 'in', 'op', 'aan', 'bij', 'naar',
        'or', 'and', 'not', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'can', 'could', 'will', 'would', 'should', 'may', 'might',
        'go', 'get', 'make', 'take', 'see', 'come', 'know', 'think', 'use', 'find', 'give'
    }
    
    skills_keywords = {
        # Technical/ICT Skills
        'dotnet': ['.NET Core', 'ASP.NET Core', 'Entity Framework', '.NET', 'ASP.NET', 'Blazor', 'MAUI'],
        'programming': ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Go', 'Rust', 'TypeScript', 'Scala', 'Visual Basic', 'VB.NET'],
        'web': ['React', 'Angular', 'Vue', 'Vue.js', 'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot', 'Spring', 'Laravel', 'Next.js', 'Nuxt.js'],
        'mobile': ['React Native', 'Flutter', 'iOS', 'Android', 'Xamarin', 'Ionic', 'Swift UI'],
        'database': ['SQL Server', 'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Cassandra', 'Oracle', 'DynamoDB', 'Firebase', 'Cosmos DB'],
        'cloud': ['AWS', 'Azure', 'GCP', 'Google Cloud', 'Heroku', 'DigitalOcean', 'Vercel', 'Netlify', 'Azure DevOps'],
        'devops': ['Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'CircleCI', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Azure Pipelines'],
        'tools': ['Git', 'GitHub', 'Jira', 'Confluence', 'Webpack', 'Babel', 'npm', 'yarn', 'Maven', 'Gradle', 'Visual Studio', 'VS Code'],
        'testing': ['Jest', 'Mocha', 'Pytest', 'JUnit', 'Selenium', 'Cypress', 'TestNG', 'NUnit', 'xUnit'],
        'data': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn', 'Spark', 'Hadoop', 'Power BI', 'Tableau'],
        
        # Marketing Skills
        'marketing_digital': ['Technische SEO', 'Technical SEO', 'Contentoptimalisatie', 'Content Optimization', 'SEO', 'SEM', 'Google Ads', 'Facebook Ads', 'Social Media Marketing', 'Email Marketing', 'Content Marketing', 'Marketing Automation', 'Google Analytics', 'HubSpot', 'Mailchimp'],
        'marketing_strategy': ['Brand Management', 'Brand Building', 'Campaign Management', 'Marketing Strategy', 'Go-to-Market Strategy', 'Product Marketing', 'Growth Marketing', 'Performance Marketing', 'Influencer Marketing'],
        'marketing_content': ['Copywriting', 'Content Creation', 'Storytelling', 'Video Marketing', 'Graphic Design', 'Adobe Creative Suite', 'Canva', 'Video Editing'],
        'design_ux': ['UX Design', 'UI Design', 'UX/UI Design', 'User Experience', 'Usability', 'User Interface', 'Design', 'Wireframing', 'Prototyping', 'Figma', 'Sketch', 'Adobe XD'],
        'marketing_analytics': ['Marketing Analytics', 'A/B-testen', 'A/B Testing', 'Conversion Optimization', 'CRO', 'Customer Journey Mapping', 'Marketing ROI', 'KPI Tracking', 'Data Analysis', 'Web Analytics', 'Webanalyse'],
        'marketing_tools': ['Google Search Console', 'Search Console', 'SEMrush', 'Screaming Frog', 'Ahrefs', 'Hotjar', 'Google Tag Manager', 'Optimizely', 'Moz'],
        
        # Management & Leadership Skills
        'management': ['Project Management', 'Team Management', 'People Management', 'Change Management', 'Risk Management', 'Budget Management', 'Resource Planning', 'Stakeholder Management'],
        'leadership': ['Leadership', 'Team Leadership', 'Strategic Thinking', 'Decision Making', 'Problem Solving', 'Problem Solver', 'Critical Thinking', 'Innovation', 'Vision Setting'],
        'project_tools': ['Agile', 'Scrum', 'Kanban', 'PRINCE2', 'PMP', 'Asana', 'Trello', 'Monday.com', 'Microsoft Project'],
        
        # Communication & Soft Skills
        'communication': ['Communicatieskills', 'Communication', 'Verbal Communication', 'Written Communication', 'Presentation Skills', 'Public Speaking', 'Negotiation', 'Persuasion', 'Storytelling', 'Schrijfvaardigheid'],
        'collaboration': ['Team Collaboration', 'Cross-functional Collaboration', 'Stakeholder Engagement', 'Relationship Building', 'Networking', 'Interpersonal Skills', 'Collaboration', 'Teamwork'],
        'personal': ['Time Management', 'Organization', 'Planning', 'Multitasking', 'Adaptability', 'Flexibility', 'Self-motivation', 'Initiative', 'Creativity'],
        
        # Sales & Business Development
        'sales': ['Sales', 'B2B Sales', 'B2C Sales', 'Account Management', 'Business Development', 'Lead Generation', 'Sales Strategy', 'CRM', 'Salesforce', 'Pipedrive'],
        'negotiation': ['Contract Negotiation', 'Pricing Strategy', 'Closing Deals', 'Objection Handling', 'Relationship Management'],
        
        # HR & Recruitment
        'hr': ['Human Resources', 'Recruitment', 'Talent Acquisition', 'Onboarding', 'Employee Engagement', 'Performance Management', 'HR Analytics', 'HRIS', 'Workday', 'BambooHR'],
        'hr_development': ['Training and Development', 'Learning and Development', 'Career Development', 'Succession Planning', 'Coaching', 'Mentoring'],
        
        # Finance & Accounting
        'finance': ['Financial Analysis', 'Budgeting', 'Forecasting', 'Financial Planning', 'Financial Reporting', 'Excel', 'SAP', 'QuickBooks', 'Accounting'],
        'analysis': ['Data Analysis', 'Business Analysis', 'Statistical Analysis', 'Reporting', 'Dashboard Creation', 'Excel Advanced', 'SQL', 'Tableau', 'Power BI'],
        
        # Operations & Supply Chain
        'operations': ['Operations Management', 'Process Improvement', 'Lean', 'Six Sigma', 'Supply Chain Management', 'Logistics', 'Inventory Management', 'Quality Control'],
        
        # Customer Success & Support
        'customer': ['Customer Service', 'Customer Success', 'Customer Experience', 'Klantbeleving', 'Client Relations', 'Technical Support', 'Customer Retention', 'Zendesk', 'Intercom'],
        
        # E-commerce & Retail
        'ecommerce': ['E-commerce', 'Online Retail', 'Shopify', 'Magento', 'WooCommerce', 'Amazon', 'eBay', 'Retail'],
        
        # ERP & Business Software
        'erp_dynamics': ['Dynamics 365 Business Central', 'Business Central', 'Microsoft Dynamics 365', 'Dynamics 365', 'Microsoft Dynamics NAV', 'Dynamics NAV', 'NAV', 'Microsoft Dynamics', 'Dynamics CRM', 'Dynamics GP'],
        'erp_systems': ['ERP Systems', 'ERP', 'SAP ERP', 'Oracle ERP', 'NetSuite', 'Odoo', 'Infor', 'Epicor', 'Sage'],
        'business_software': ['Microsoft Office', 'Office 365', 'SharePoint', 'Power Apps', 'Power Automate', 'Power Platform', 'Microsoft Teams'],
        
        # Business Process & Development
        'business_process': ['Business Process Automation', 'Business Process Improvement', 'Process Optimization', 'Workflow Automation', 'Process Mapping', 'Process Analysis'],
        'solution_dev': ['Solution Development', 'Developing Solutions', 'Creating Solutions', 'Solution Architecture', 'Solution Design', 'Software Configuration', 'System Configuration', 'Software Customization'],
        'integration': ['System Integration', 'API Integration', 'Data Integration', 'Cloud Integration', 'Integration Development'],
        
        # Technical Support & Problem Solving
        'technical_support': ['Troubleshooting', 'Technical Troubleshooting', 'Problem Solving', 'Root Cause Analysis', 'Issue Resolution', 'Technical Support', 'System Maintenance'],
        
        # Soft Skills & Attributes  
        'soft_skills': ['Knowledge Sharing', 'Sharing Knowledge', 'Continuous Learning', 'Keep Learning', 'Curiosity', 'Analytical Thinking', 'Attention to Detail', 'Collaboration', 'Teamwork'],
        'sustainability': ['Sustainability', 'Climate Change', 'Environmental Impact', 'Social Impact', 'CSR', 'ESG'],
        
        # Other Business Skills
        'other': ['Strategic Planning', 'Business Strategy', 'Competitive Analysis', 'Market Research', 'Product Development', 'Entrepreneurship', 'Innovation Management', 'REST API', 'GraphQL', 'Microservices', 'TDD', 'CI/CD', 'Linux', 'Unix', 'Windows Server', 'Active Directory']
    }
    
    all_skills = []
    for category in skills_keywords.values():
        all_skills.extend(category)
    
    all_skills.sort(key=len, reverse=True)
    
    found_skills = []
    text_lower = text.lower()
    
    doc = nlp(text)
    
    sentences = [sent.text for sent in doc.sents]
    skill_contexts = [
        # English phrases
        'experience with', 'proficient in', 'skilled in', 'knowledge of', 'expertise in', 
        'familiar with', 'worked with', 'using', 'developed with', 'built with', 'implemented',
        'experience in', 'strong in', 'background in', 'proven track record', 'demonstrated',
        'excellent at', 'excels at', 'ability to', 'capable of', 'responsible for',
        'managed', 'led', 'coordinated', 'organized', 'developed', 'created', 'executed',
        'hands on', 'hands-on', 'go-to person', 'working with', 'work with', 'enjoys',
        'values', 'drive to', 'natural', 'great with', 'solving', 'creating', 'developing',
        'troubleshooting', 'sharing', 'helping', 'translating', 'building',
        'technologies:', 'skills:', 'tools:', 'frameworks:', 'competencies:', 'qualifications:',
        # Dutch phrases
        'ervaring met', 'ervaring in', 'kennis van', 'kennis in', 'bij voorkeur ervaring',
        'ervaring op het gebied van', 'vaardigheden:', 'competenties:', 'tools:', 'technologie:',
        'minimaal', 'oog voor', 'sterke', 'goede kennis', 'zeer goede kennis', 'vaardig in'
    ]
    
    relevant_sentences = []
    for sent in sentences:
        sent_lower = sent.lower()
        if any(context in sent_lower for context in skill_contexts):
            relevant_sentences.append(sent)
    
    search_text = ' '.join(relevant_sentences) if relevant_sentences else text
    search_text_lower = search_text.lower()
    
    for skill in all_skills:
        skill_lower = skill.lower()
        
        if skill_lower in stop_words:
            continue
        
        skill_words = skill_lower.split()
        if len(skill_words) == 1 and skill_words[0] in stop_words:
            continue
        
        # Normalize skill for better matching (handle hyphens and spaces)
        skill_normalized = skill_lower.replace('-', ' ').replace('  ', ' ')
        
        # Try exact match first
        if skill_lower in search_text_lower:
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, search_text_lower):
                found_skills.append(skill)
                continue
        
        # Try normalized match (handles hyphen variations)
        search_normalized = search_text_lower.replace('-', ' ').replace('  ', ' ')
        if skill_normalized in search_normalized:
            pattern = r'\b' + re.escape(skill_normalized) + r'\b'
            if re.search(pattern, search_normalized):
                found_skills.append(skill)
                continue
        
        # Fallback to full text search
        if skill_lower in text_lower:
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
                continue
        
        # Try normalized match in full text
        text_normalized = text_lower.replace('-', ' ').replace('  ', ' ')
        if skill_normalized in text_normalized:
            pattern = r'\b' + re.escape(skill_normalized) + r'\b'
            if re.search(pattern, text_normalized):
                if skill not in found_skills:
                    found_skills.append(skill)
    
    return found_skills

def extract_experience(text):
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(?:experience|exp).*?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            years = match.group(1)
            return f"{years}+ years"
    
    return "Not specified"

def extract_education(text):
    """Extract education information from text"""
    degrees = ['PhD', 'Ph.D', 'Doctorate', 'Master', 'Masters', 'MS', 'M.S', 'MSc', 'MBA', 
               'Bachelor', "Bachelor's", 'Bachelors', 'BS', 'B.S', 'BSc', 'BA', 'B.A', 'degree']
    
    for degree in degrees:
        if degree.lower() in text.lower():
            pattern = rf'{degree}.*?(?:in|of)\s+([A-Z][A-Za-z\s]+?)(?:\.|,|\n|from)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                field = match.group(1).strip()
                return f"{degree} in {field}"
            return f"{degree} degree"
    
    return "Not specified"

def extract_languages(text):
    """Extract language proficiencies from text"""
    languages_map = {
        'dutch': 'Dutch',
        'nederlands': 'Dutch',
        'french': 'French',
        'frans': 'French',
        'english': 'English',
        'engels': 'English',
        'german': 'German',
        'duits': 'German',
        'spanish': 'Spanish',
        'spaans': 'Spanish',
        'italian': 'Italian',
        'italiaans': 'Italian',
        'portuguese': 'Portuguese',
        'portugees': 'Portuguese',
        'chinese': 'Chinese',
        'chinees': 'Chinese',
        'arabic': 'Arabic',
        'arabisch': 'Arabic'
    }
    
    proficiency_levels = {
        'native': 'Native',
        'moedertaal': 'Native',
        'fluent': 'Fluent',
        'vloeiend': 'Fluent',
        'excellent': 'Excellent',
        'zeer goed': 'Excellent',
        'zeer goede': 'Excellent',
        'advanced': 'Advanced',
        'gevorderd': 'Advanced',
        'good': 'Good',
        'goed': 'Good',
        'goede': 'Good',
        'intermediate': 'Intermediate',
        'gemiddeld': 'Intermediate',
        'basic': 'Basic',
        'basis': 'Basic'
    }
    
    found_languages = []
    text_lower = text.lower()
    
    for lang_key, lang_name in languages_map.items():
        if lang_key in text_lower:
            level = None
            
            for level_key, level_name in proficiency_levels.items():
                context_pattern = rf'{level_key}.*?{lang_key}|{lang_key}.*?{level_key}'
                if re.search(context_pattern, text_lower):
                    level = level_name
                    break
            
            lang_result = f"{lang_name} ({level})" if level else lang_name
            
            if lang_result not in found_languages:
                found_languages.append(lang_result)
    
    return found_languages if found_languages else []

def calculate_match_score(job_description, cv_text):
    """Calculate similarity score using enhanced TF-IDF with n-grams for better semantic matching"""
    try:
        # Try spaCy semantic similarity first (if model has word vectors)
        try:
            job_doc = nlp(job_description[:100000])
            cv_doc = nlp(cv_text[:100000])
            
            # Check if model has word vectors
            if job_doc.has_vector and cv_doc.has_vector:
                similarity = job_doc.similarity(cv_doc)
                
                # Only use spaCy if similarity is meaningful (>= 0.05)
                # Low scores indicate poor vector coverage
                if similarity >= 0.05:
                    # Clamp to [0, 1] range then scale to [0, 100]
                    clamped_similarity = max(0, min(1, similarity))
                    score = int(clamped_similarity * 100)
                    return min(100, max(0, score))  # Double clamp for safety
        except:
            pass  # Fall through to TF-IDF
        
        # Enhanced TF-IDF with character n-grams for better semantic matching
        # Character n-grams help match similar words (e.g., "developer" vs "developing")
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2),  # Unigrams and bigrams
            analyzer='word',
            min_df=1,
            lowercase=True
        )
        
        tfidf_matrix = vectorizer.fit_transform([job_description, cv_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Clamp to [0, 1] and scale to percentage
        clamped_similarity = max(0, min(1, similarity))
        return int(clamped_similarity * 100)
        
    except Exception as e:
        print(f"Error calculating similarity: {str(e)}", file=sys.stderr)
        return 0

def format_filename_to_name(filename):
    """Convert filename to readable candidate name"""
    name = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
    name = name.replace('_', ' ').replace('-', ' ')
    name = ' '.join(word.capitalize() for word in name.split())
    return name

def analyze_cv(cv_path, job_description):
    """Analyze a single CV against job description"""
    cv_text = extract_text(cv_path)
    
    if cv_text.startswith("Error") or cv_text == "Unsupported file format":
        return {
            "error": cv_text,
            "fileName": os.path.basename(cv_path)
        }
    
    candidate_name = format_filename_to_name(os.path.basename(cv_path))
    
    match_score = calculate_match_score(job_description, cv_text)
    
    cv_skills = extract_skills_with_nlp(cv_text)
    job_skills = extract_skills_with_nlp(job_description)
    
    matched_skills = [skill for skill in cv_skills if skill in job_skills]
    
    experience = extract_experience(cv_text)
    education = extract_education(cv_text)
    languages = extract_languages(cv_text)
    
    return {
        "fileName": os.path.basename(cv_path),
        "candidateName": candidate_name,
        "matchScore": match_score,
        "skills": cv_skills[:15],
        "matchedSkills": matched_skills,
        "experience": experience,
        "education": education,
        "languages": languages,
        "fullText": cv_text[:500]
    }

def analyze_cv_with_original_name(cv_path, original_name, job_description, job_skills=None):
    """Analyze a single CV against job description using original filename"""
    cv_text = extract_text(cv_path)
    
    if cv_text.startswith("Error") or cv_text == "Unsupported file format":
        return {
            "error": cv_text,
            "fileName": original_name
        }
    
    candidate_name = format_filename_to_name(original_name)
    
    cv_skills = extract_skills_with_nlp(cv_text)
    
    # Use AI-extracted skills if provided, otherwise use NLP extraction
    if not job_skills or len(job_skills) == 0:
        job_skills = extract_skills_with_nlp(job_description)
    
    # Fuzzy match skills (case-insensitive, normalized)
    def normalize_skill(skill):
        return skill.lower().strip().replace('-', ' ').replace('/', ' ')
    
    normalized_job_skills = [normalize_skill(s) for s in job_skills]
    matched_skills = []
    for cv_skill in cv_skills:
        normalized_cv_skill = normalize_skill(cv_skill)
        # Check if CV skill matches any job skill
        if any(normalized_cv_skill == norm_job or norm_job in normalized_cv_skill or normalized_cv_skill in norm_job 
               for norm_job in normalized_job_skills):
            matched_skills.append(cv_skill)
    
    # Calculate match score based on skill overlap
    if len(job_skills) > 0:
        # Primary score: percentage of job skills matched
        skill_match_percentage = (len(matched_skills) / len(job_skills)) * 100
        
        # If NO skills match, score should be very low (0-5%)
        if len(matched_skills) == 0:
            match_score = 0
        else:
            # Secondary score: TF-IDF similarity for context (weighted much lower)
            tfidf_score = calculate_match_score(job_description, cv_text)
            
            # Weighted combination: 90% skill matching + 10% text similarity
            # This ensures skill overlap is the primary driver
            match_score = int((skill_match_percentage * 0.9) + (tfidf_score * 0.1))
    else:
        # Fallback to TF-IDF if no skills extracted
        match_score = calculate_match_score(job_description, cv_text)
    
    experience = extract_experience(cv_text)
    education = extract_education(cv_text)
    languages = extract_languages(cv_text)
    
    return {
        "fileName": original_name,
        "candidateName": candidate_name,
        "matchScore": match_score,
        "skills": cv_skills[:15],
        "matchedSkills": matched_skills,
        "experience": experience,
        "education": education,
        "languages": languages,
        "fullText": cv_text[:500]
    }

def main():
    """Main function to process CVs"""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments. Usage: python cv_matcher.py <job_description> <file_info_json> [ai_skills_json]"}))
        sys.exit(1)
    
    job_description = sys.argv[1]
    file_info_json = sys.argv[2]
    ai_skills_json = sys.argv[3] if len(sys.argv) > 3 else "[]"
    
    try:
        file_info_list = json.loads(file_info_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid file info JSON: {str(e)}"}))
        sys.exit(1)
    
    try:
        ai_extracted_skills = json.loads(ai_skills_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid AI skills JSON: {str(e)}"}))
        sys.exit(1)
    
    # Use AI-extracted skills if provided, otherwise extract with NLP
    if ai_extracted_skills and len(ai_extracted_skills) > 0:
        job_skills = ai_extracted_skills
    else:
        job_skills = extract_skills_with_nlp(job_description)
    
    results = []
    for file_info in file_info_list:
        cv_path = file_info['path']
        original_name = file_info['originalName']
        
        if os.path.exists(cv_path):
            result = analyze_cv_with_original_name(cv_path, original_name, job_description, job_skills)
            results.append(result)
        else:
            results.append({
                "error": f"File not found: {cv_path}",
                "fileName": original_name
            })
    
    output = {
        "jobSkills": job_skills,
        "candidates": results
    }
    
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
