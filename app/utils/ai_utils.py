import os
import json
import time
import logging
import re
from groq import Groq
import markdown2
from typing import Tuple

logger = logging.getLogger(__name__)

def detect_language(code_text: str) -> str:
    """
    Detect the programming language based on code patterns and syntax.
    Returns the detected language or 'unknown' if unclear.
    """
    code_lower = code_text.lower()
    
    # Python indicators
    python_indicators = [
        'def ', 'import ', 'from ', 'if __name__', 'print(', 'range(', 
        'len(', 'append(', 'split(', 'strip()', 'lower()', 'upper()',
        'for ', 'in ', 'while ', 'try:', 'except:', 'finally:', 'with ',
        'class ', 'self.', 'lambda ', 'map(', 'filter(', 'list(', 'dict(',
        'set(', 'tuple(', 'enumerate(', 'zip(', 'sorted(', 'reversed('
    ]
    
    # JavaScript indicators
    js_indicators = [
        'function ', 'var ', 'let ', 'const ', 'console.log(', 'alert(',
        'document.', 'window.', 'addEventListener(', 'querySelector(',
        'getElementById(', 'innerHTML', 'style.', 'classList.',
        'fetch(', 'then(', 'catch(', 'async ', 'await ', 'Promise(',
        'setTimeout(', 'setInterval(', 'parseInt(', 'parseFloat(',
        'JSON.parse(', 'JSON.stringify(', 'localStorage.', 'sessionStorage.'
    ]
    
    # PHP indicators
    php_indicators = [
        '<?php', '<?=', 'echo ', 'print ', 'var_dump(', 'print_r(',
        '$', 'function ', 'class ', 'public ', 'private ', 'protected ',
        'static ', 'const ', 'namespace ', 'use ', 'require ', 'include ',
        'require_once ', 'include_once ', 'array(', 'count(', 'strlen(',
        'substr(', 'strpos(', 'explode(', 'implode(', 'trim(', 'strtolower(',
        'strtoupper(', 'ucfirst(', 'ucwords(', 'htmlspecialchars(',
        'mysqli_', 'pdo_', 'mysql_', 'session_start(', 'header(',
        'isset(', 'empty(', 'is_array(', 'is_string(', 'is_numeric('
    ]
    
    # Java indicators
    java_indicators = [
        'public class', 'public static void main', 'System.out.println',
        'import java.', 'package ', 'public ', 'private ', 'protected ',
        'static ', 'final ', 'class ', 'interface ', 'extends ', 'implements ',
        'new ', 'String ', 'int ', 'double ', 'boolean ', 'char ', 'byte ',
        'short ', 'long ', 'float ', 'void ', 'return ', 'if (', 'else ',
        'for (', 'while (', 'do {', 'switch (', 'case ', 'default:',
        'try {', 'catch (', 'finally {', 'throw ', 'throws ',
        'ArrayList<', 'HashMap<', 'LinkedList<', 'HashSet<', 'TreeSet<'
    ]
    
    # C++ indicators
    cpp_indicators = [
        '#include <', '#include "', 'using namespace std;', 'cout <<',
        'cin >>', 'endl;', 'int main()', 'class ', 'public:', 'private:',
        'protected:', 'virtual ', 'template<', 'typename ', 'const ',
        'static ', 'extern ', 'inline ', 'friend ', 'operator ', 'new ',
        'delete ', 'this->', 'std::', 'vector<', 'map<', 'set<', 'string ',
        'auto ', 'nullptr', 'override', 'final', 'noexcept', 'constexpr'
    ]
    
    # C indicators
    c_indicators = [
        '#include <', '#include "', '#define ', '#ifdef ', '#ifndef ',
        '#endif', '#pragma ', 'int main(', 'printf(', 'scanf(', 'malloc(',
        'free(', 'calloc(', 'realloc(', 'strcpy(', 'strcat(', 'strcmp(',
        'strlen(', 'strtok(', 'sprintf(', 'sscanf(', 'fopen(', 'fclose(',
        'fread(', 'fwrite(', 'fgets(', 'fputs(', 'struct ', 'union ',
        'enum ', 'typedef ', 'extern ', 'static ', 'register ', 'volatile '
    ]
    
    # Count matches for each language
    scores = {
        'python': sum(1 for indicator in python_indicators if indicator in code_lower),
        'javascript': sum(1 for indicator in js_indicators if indicator in code_lower),
        'php': sum(1 for indicator in php_indicators if indicator in code_lower),
        'java': sum(1 for indicator in java_indicators if indicator in code_lower),
        'cpp': sum(1 for indicator in cpp_indicators if indicator in code_lower),
        'c': sum(1 for indicator in c_indicators if indicator in code_lower)
    }
    
    # Get the language with the highest score
    if scores:
        detected_language = max(scores, key=scores.get)
        # Only return detected language if it has a reasonable number of matches
        if scores[detected_language] >= 2:
            return detected_language
    
    return 'unknown'

def analyze_code_with_groq(code_text: str, language: str, max_retries: int = 3):
    """
    Analyze code with Groq AI with retry logic for handling API errors.
    """
    # First, detect the actual language of the code
    detected_language = detect_language(code_text)
    
    # Check for language mismatch
    language_mismatch = False
    language_warning = ""
    
    if detected_language != 'unknown' and detected_language != language.lower():
        language_mismatch = True
        language_warning = f"⚠️ **Language Mismatch Detected:** The code appears to be {detected_language.upper()} but you selected {language.upper()}. Analysis will be performed for the detected language ({detected_language.upper()})."
        analysis_language = detected_language
        logger.info(f"Language mismatch detected: user selected '{language}', detected '{detected_language}'")
    else:
        analysis_language = language
        logger.info(f"Analyzing code with language: '{analysis_language}'")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY environment variable missing")
        raise Exception("GROQ_API_KEY not found in environment variables")
    
    client = Groq(api_key=api_key)
    prompt = f"""
    Analyze the following {analysis_language} code and provide a structured review with the following format:

    Code:
    {code_text}

    Please format your response as follows:
    ---
    FEEDBACK:
    ## Overview
    <Brief overview of the code>

    ## Code Quality Assessment
    - **Strengths:**
      - <strength 1>
      - <strength 2>
      - <strength 3>
    
    - **Areas for Improvement:**
      - <improvement 1>
      - <improvement 2>
      - <improvement 3>

    ## Best Practices
    - **Followed:**
      - <good practice 1>
      - <good practice 2>
    
    - **Recommendations:**
      - <recommendation 1>
      - <recommendation 2>
      - <recommendation 3>

    ## Security Considerations
    - <security point 1>
    - <security point 2>
    - <security point 3>

    ## Performance Tips
    - <performance tip 1>
    - <performance tip 2>
    - <performance tip 3>

    ## Code Structure
    - <structure point 1>
    - <structure point 2>
    - <structure point 3>
    ---
    SCORE: <number>
    ---
    COMMENTS:
    <Inline commented code here>
    ---
    """
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Sending request to Groq API (Attempt {attempt + 1}/{max_retries})...")
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                  {
                    "role": "user",
                    "content": prompt
                  }
                ],
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                reasoning_effort="medium",
                stream=True,
                stop=None
            )

            content = ""
            for chunk in completion:
                content += chunk.choices[0].delta.content or ""
            
            # Parse the response for FEEDBACK, SCORE, COMMENTS using robust regex & string splitting
            feedback, score, comments = '', 75, ''
            try:
                # 1. Parse Score
                score_match = re.search(r'SCORE:\s*\*?\*?\s*(\d+)', content, re.IGNORECASE)
                if score_match:
                    raw_val = int(score_match.group(1))
                    score = raw_val * 10 if raw_val <= 10 else min(raw_val, 100)
                
                # 2. Parse Feedback
                if 'FEEDBACK:' in content:
                    fb_parts = content.split('FEEDBACK:', 1)
                    after_fb = fb_parts[1]
                    end_idx = len(after_fb)
                    for marker in ['SCORE:', 'COMMENTS:', '--- SCORE']:
                        idx = after_fb.find(marker)
                        if idx != -1 and idx < end_idx:
                            end_idx = idx
                    feedback = after_fb[:end_idx].strip()
                    feedback = re.sub(r'^\s*---\s*', '', feedback)
                    feedback = re.sub(r'\s*---\s*$', '', feedback).strip()
                else:
                    # Remove trailing SCORE and COMMENTS sections if raw output returned
                    feedback_clean = content
                    for marker in ['SCORE:', 'COMMENTS:', '--- SCORE']:
                        idx = feedback_clean.find(marker)
                        if idx != -1:
                            feedback_clean = feedback_clean[:idx]
                    feedback = feedback_clean.strip()
                    feedback = re.sub(r'^\s*---\s*', '', feedback)
                    feedback = re.sub(r'\s*---\s*$', '', feedback).strip()
                
                # 3. Parse Comments
                if 'COMMENTS:' in content:
                    c_parts = content.split('COMMENTS:', 1)
                    c_after = c_parts[1]
                    c_end = len(c_after)
                    idx = c_after.find('---')
                    if idx != -1:
                        c_end = idx
                    comments = c_after[:c_end].strip()
            except Exception as parse_err:
                logger.warning(f"Error parsing Groq output structured sections: {parse_err}")
                feedback = content.strip()
                score = 75
                comments = ''
            
            # Add language mismatch warning if applicable
            if language_mismatch:
                feedback = f"{language_warning}\n\n{feedback}"
            
            feedback_html = markdown2.markdown(feedback)
            logger.info("Successfully received and parsed AI review response from Groq")
            return feedback_html, score, comments
            
        except Exception as e:
            err_msg = str(e)
            err_lower = err_msg.lower()
            logger.error(f"Groq API error on attempt {attempt + 1}: {err_msg}")
            
            if "413" in err_lower or "too large" in err_lower:
                raise Exception("Code payload is too large for AI review. Please submit a smaller snippet.")
            elif "429" in err_lower or ("quota" in err_lower and "exceeded" in err_lower):
                raise Exception("Groq AI service quota exceeded. Please try again later or contact support.")
            elif "401" in err_lower or "unauthorized" in err_lower or "api key" in err_lower:
                raise Exception("Access denied to Groq AI. Please check your API key and permissions.")
            elif "503" in err_lower or "unavailable" in err_lower or "overloaded" in err_lower:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1
                    logger.warning(f"Groq service unavailable, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.warning("Groq service unavailable after max retries; falling back to basic analysis")
                    feedback, score, comments = basic_code_analysis(code_text, analysis_language)
                    if language_mismatch:
                        feedback = f"{language_warning}\n\n{feedback}"
                    feedback_html = markdown2.markdown(feedback)
                    return feedback_html, score, comments
            else:
                raise Exception(f"Unexpected error occurred: {err_msg}")

def detect_plagiarism_hints(code_text: str) -> str:
    """
    Basic plagiarism detection using pattern matching.
    This is a simplified version - in production you'd use more sophisticated methods.
    """
    # Common patterns that might indicate copied code
    patterns = [
        "public static void main",
        "def main():",
        "if __name__ == '__main__':",
        "console.log(",
        "print(",
        "System.out.println"
    ]
    
    hints = []
    for pattern in patterns:
        if pattern in code_text:
            hints.append(f"Contains common pattern: {pattern}")
    
    if hints:
        return " | ".join(hints)
    return "No obvious patterns detected"

def basic_code_analysis(code_text: str, language: str) -> Tuple[str, int, str]:
    """
    Basic code analysis when AI service is unavailable.
    Provides simple metrics and suggestions based on code patterns.
    """
    lines = code_text.split('\n')
    total_lines = len(lines)
    comment_lines = sum(1 for line in lines if line.strip().startswith(('#', '//', '/*', '*/')))
    empty_lines = sum(1 for line in lines if not line.strip())
    code_lines = total_lines - comment_lines - empty_lines
    
    # Basic scoring based on code structure
    score = 50  # Base score
    
    # Adjust score based on code characteristics
    if comment_lines > 0 and code_lines > 0:
        comment_ratio = comment_lines / code_lines
        if 0.1 <= comment_ratio <= 0.3:
            score += 10  # Good comment ratio
        elif comment_ratio > 0.3:
            score += 5   # Too many comments
        else:
            score -= 5   # Too few comments
    
    if code_lines > 0:
        avg_line_length = sum(len(line) for line in lines if line.strip() and not line.strip().startswith(('#', '//', '/*', '*/'))) / code_lines
        if avg_line_length <= 80:
            score += 10  # Good line length
        elif avg_line_length > 120:
            score -= 10  # Lines too long
    
    # Check for common issues
    issues = []
    suggestions = []
    
    if language.lower() == 'python':
        if 'import *' in code_text:
            issues.append("Avoid wildcard imports")
            score -= 5
        if 'print(' in code_text and 'def ' in code_text:
            suggestions.append("Consider using logging instead of print statements in functions")
        if len(code_text) > 1000 and 'def ' not in code_text:
            suggestions.append("Consider breaking code into functions")
        if 'eval(' in code_text:
            issues.append("Avoid using eval() - security risk")
            score -= 15
        if 'exec(' in code_text:
            issues.append("Avoid using exec() - security risk")
            score -= 15
    
    elif language.lower() == 'javascript':
        if 'console.log(' in code_text and 'function ' in code_text:
            suggestions.append("Consider using proper logging instead of console.log in functions")
        if 'var ' in code_text:
            suggestions.append("Consider using 'let' or 'const' instead of 'var'")
            score -= 5
        if 'eval(' in code_text:
            issues.append("Avoid using eval() - security risk")
            score -= 15
        if 'innerHTML' in code_text and 'document.' in code_text:
            suggestions.append("Consider using textContent instead of innerHTML for security")
    
    elif language.lower() == 'php':
        if 'mysql_' in code_text:
            issues.append("mysql_* functions are deprecated, use PDO or mysqli")
            score -= 10
        if 'echo $_' in code_text or 'print $_' in code_text:
            issues.append("Sanitize user input before output")
            score -= 10
        if 'include $_' in code_text or 'require $_' in code_text:
            issues.append("Avoid dynamic includes with user input - security risk")
            score -= 15
        if '<?=' in code_text and 'htmlspecialchars' not in code_text:
            suggestions.append("Use htmlspecialchars() when outputting data")
    
    elif language.lower() == 'java':
        if 'System.out.println' in code_text and 'public static void main' in code_text:
            suggestions.append("Consider using proper logging framework instead of System.out.println")
        if 'catch (Exception e)' in code_text:
            suggestions.append("Catch specific exceptions instead of generic Exception")
        if 'new String(' in code_text:
            suggestions.append("Use string literals instead of new String()")
    
    elif language.lower() in ['cpp', 'c']:
        if 'using namespace std;' in code_text and language.lower() == 'cpp':
            suggestions.append("Consider avoiding 'using namespace std;' in header files")
        if 'malloc(' in code_text and 'free(' not in code_text:
            issues.append("Memory allocated but not freed")
            score -= 10
        if 'printf(' in code_text and 'scanf(' in code_text:
            suggestions.append("Consider using C++ streams (cout/cin) instead of printf/scanf")
    
    # Generate feedback
    feedback_parts = [
        f"## Overview",
        f"This is a basic analysis of your {language} code with {code_lines} lines of executable code.",
        "",
        f"## Code Quality Assessment",
        f"- **Strengths:**",
        f"  - Code has {comment_lines} comment lines for documentation",
        f"  - Average line length is {avg_line_length:.1f} characters",
        f"  - Good code-to-comment ratio" if 0.1 <= comment_lines/code_lines <= 0.3 else f"  - Code structure is well-organized",
        "",
        f"- **Areas for Improvement:**",
    ]
    
    if issues:
        for issue in issues:
            feedback_parts.append(f"  - {issue}")
    else:
        feedback_parts.append("  - No major issues detected")
    
    feedback_parts.extend([
        "",
        f"## Best Practices",
        f"- **Followed:**",
        f"  - Proper code formatting",
        f"  - Consistent indentation",
    ])
    
    if suggestions:
        feedback_parts.extend([
            f"- **Recommendations:**",
        ])
        for suggestion in suggestions:
            feedback_parts.append(f"  - {suggestion}")
    else:
        feedback_parts.append(f"  - Code follows most best practices")
    
    feedback_parts.extend([
        "",
        f"## Code Statistics",
        f"- Total lines: {total_lines}",
        f"- Code lines: {code_lines}",
        f"- Comment lines: {comment_lines}",
        f"- Empty lines: {empty_lines}",
        f"- Average line length: {avg_line_length:.1f} characters",
        "",
        f"**Score: {score}/100**",
        "",
        "*Note: This is a basic analysis. For detailed AI-powered review, please try again when the service is available.*"
    ])
    
    feedback = "\n".join(feedback_parts)
    comments = f"Basic analysis completed for {language} code ({code_lines} lines of code)"
    
    return feedback, score, comments

def generate_inline_comments(code_text: str, language: str, max_retries: int = 3) -> str:
    """
    Generate inline comments for code using Groq AI with retry logic.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY unavailable for generating inline comments")
        return "Comments could not be generated - API key not available"
    
    client = Groq(api_key=api_key)
    prompt = f"""
    Add helpful inline comments to this {language} code. 
    Explain what each section does in simple terms.
    Return only the commented code:

    {code_text}
    """
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Generating inline comments via Groq (Attempt {attempt + 1}/{max_retries})...")
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                  {
                    "role": "user",
                    "content": prompt
                  }
                ],
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                reasoning_effort="medium",
                stream=True,
                stop=None
            )
            
            content = ""
            for chunk in completion:
                content += chunk.choices[0].delta.content or ""
            return content
            
        except Exception as e:
            err_msg = str(e)
            err_lower = err_msg.lower()
            logger.error(f"Error generating inline comments (attempt {attempt + 1}): {err_msg}")
            
            if "503" in err_lower or "unavailable" in err_lower or "overloaded" in err_lower:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1
                    time.sleep(wait_time)
                    continue
                else:
                    return f"Comments could not be generated - Groq AI service is currently unavailable. Please try again in a few minutes. (Attempt {attempt + 1}/{max_retries})"
            elif "429" in err_lower or ("quota" in err_lower and "exceeded" in err_lower):
                return "Comments could not be generated - Groq AI service quota exceeded. Please try again later."
            else:
                return f"Comments could not be generated - Unexpected error: {err_msg}" 