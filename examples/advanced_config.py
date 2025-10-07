#!/usr/bin/env python3
"""
Advanced Mozart AI Configuration Example

This example shows how to configure Mozart AI V10 for specialized
review scenarios with custom settings.
"""

import os
from pathlib import Path

def create_custom_env_config():
    """
    Create a custom environment configuration for specialized reviews.
    """
    
    # Example: Security-focused configuration
    security_config = """
# Security-Focused Mozart AI Configuration

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Specialized Model Selection for Security Reviews
OPENAI_MODEL=gpt-4o
DEEPSEEK_MODEL=deepseek-coder

# Security-Focused Reviewer Names
REVIEWER_A_NAME=Security Auditor
REVIEWER_A_PROVIDER=openai
REVIEWER_A_MODEL=gpt-4o

REVIEWER_B_NAME=Penetration Tester
REVIEWER_B_PROVIDER=deepseek
REVIEWER_B_MODEL=deepseek-coder

# Judge for final security assessment
JUDGE_PROVIDER=openai
JUDGE_MODEL=gpt-4o

# Extended timeout for thorough security analysis
TIMEOUT_SECONDS=120

# Detailed logging for security reviews
LOG_LEVEL=DEBUG

# Custom agent name
AGENT_NAME=Mozart Security Audit
"""

    # Example: Performance-focused configuration
    performance_config = """
# Performance-Focused Mozart AI Configuration

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Performance Optimization Models
OPENAI_MODEL=gpt-4o
DEEPSEEK_MODEL=deepseek-coder

# Performance-Focused Reviewer Names
REVIEWER_A_NAME=Performance Engineer
REVIEWER_A_PROVIDER=openai
REVIEWER_A_MODEL=gpt-4o

REVIEWER_B_NAME=Optimization Specialist
REVIEWER_B_PROVIDER=deepseek
REVIEWER_B_MODEL=deepseek-coder

# Performance analysis settings
TIMEOUT_SECONDS=90
LOG_LEVEL=INFO
AGENT_NAME=Mozart Performance Analyzer
"""

    return security_config, performance_config

def demonstrate_criteria_combinations():
    """
    Show different criteria combinations for specialized reviews.
    """
    
    review_scenarios = {
        "Security Audit": [
            "security", "error handling", "logic", "correctness"
        ],
        "Performance Review": [
            "performance", "scalability", "logic", "design"
        ],
        "Code Quality Assessment": [
            "clarity", "maintainability", "documentation", "design"
        ],
        "Comprehensive Review": [
            "correctness", "security", "performance", "clarity", 
            "maintainability", "logic", "error handling", "testing",
            "scalability", "documentation", "design"
        ],
        "Quick Sanity Check": [
            "correctness", "logic", "clarity"
        ],
        "Production Readiness": [
            "correctness", "security", "error handling", "testing", "scalability"
        ]
    }
    
    print("=== Mozart AI Advanced Configuration Examples ===\n")
    
    print("🔧 Configuration Scenarios:")
    security_config, performance_config = create_custom_env_config()
    
    print("\n1. Security-Focused Configuration:")
    print("   - Specialized reviewer names (Security Auditor, Penetration Tester)")
    print("   - Extended timeout for thorough analysis")
    print("   - Debug logging for detailed security insights")
    
    print("\n2. Performance-Focused Configuration:")
    print("   - Performance-specialized reviewer names")
    print("   - Optimized timeout settings")
    print("   - Custom agent branding")
    
    print("\n📋 Review Scenario Criteria Combinations:")
    for scenario, criteria in review_scenarios.items():
        print(f"\n• {scenario}:")
        print(f"  Criteria: {', '.join(criteria)}")
        print(f"  Count: {len(criteria)} of 11 available")
        
        # Suggest mode based on criteria count
        if len(criteria) <= 3:
            mode_suggestion = "Fast Mode (quick competitive review)"
        elif len(criteria) >= 8:
            mode_suggestion = "Full Mode (comprehensive with judge)"
        else:
            mode_suggestion = "Either mode (balanced analysis)"
        
        print(f"  Suggested Mode: {mode_suggestion}")

def advanced_usage_tips():
    """
    Provide advanced tips for using Mozart AI effectively.
    """
    
    print("\n🎯 Advanced Usage Tips:")
    
    tips = [
        {
            "title": "API Key Management",
            "description": "Use environment variables or secure vaults for API keys in production",
            "example": "Set OPENAI_API_KEY in your system environment for security"
        },
        {
            "title": "Custom Model Selection",
            "description": "Different models excel at different types of analysis",
            "example": "Use gpt-4o for complex reasoning, deepseek-coder for technical accuracy"
        },
        {
            "title": "Timeout Optimization",
            "description": "Adjust timeouts based on code complexity and review depth",
            "example": "60s for quick reviews, 120s+ for comprehensive security audits"
        },
        {
            "title": "Criteria Selection Strategy",
            "description": "Choose criteria that align with your specific code review goals",
            "example": "Security + Error Handling + Logic for authentication code"
        },
        {
            "title": "Mode Selection",
            "description": "Fast Mode for quick feedback, Full Mode for critical code",
            "example": "Use Full Mode for production deployment code reviews"
        },
        {
            "title": "Result Integration",
            "description": "Export JSON results for integration with CI/CD pipelines",
            "example": "Parse JSON output for automated quality gates"
        }
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"\n{i}. {tip['title']}:")
        print(f"   {tip['description']}")
        print(f"   Example: {tip['example']}")

def main():
    """
    Main function demonstrating advanced Mozart AI configuration.
    """
    demonstrate_criteria_combinations()
    advanced_usage_tips()
    
    print(f"\n🚀 Next Steps:")
    print("1. Copy .env.mozart.example to .env.mozart")
    print("2. Configure with your API keys and preferred settings")
    print("3. Run: python mozart_monitorV10.py")
    print("4. Select appropriate criteria for your review type")
    print("5. Choose Fast or Full mode based on your needs")
    print("6. Export results in your preferred format")

if __name__ == "__main__":
    main()