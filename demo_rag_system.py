# demo_rag_system.py
"""
Complete demo script that shows the Alumni RAG system in action
Run this after setting up the sample data
"""

import time
import json
import asyncio
from datetime import datetime
from setup_sample_data import setup_mongodb_with_sample_data
from chatbot import AlumniRAGService

class AlumniRAGDemo:
    def __init__(self):
        print("🤖 Initializing Alumni RAG System...")
        self.rag_service = AlumniRAGService()
        
    def run_demo_queries(self):
        """Run a series of demo queries to show system capabilities"""
        
        # Demo queries that showcase different capabilities
        demo_queries = [
            {
                "category": "🏢 Company-based Search",
                "queries": [
                    "Who works at Google?",
                    "Show me all alumni working at Microsoft or Amazon",
                    "Which companies do our alumni work at?"
                ]
            },
            {
                "category": "📅 Graduation Year Search", 
                "queries": [
                    "Who graduated in 2020?",
                    "Show me recent graduates from 2021 and 2022",
                    "Find alumni who graduated before 2019"
                ]
            },
            {
                "category": "💻 Skills and Technology Search",
                "queries": [
                    "Who has Python skills?",
                    "Find machine learning experts",
                    "Show me frontend developers",
                    "Who knows blockchain technology?"
                ]
            },
            {
                "category": "🌍 Location-based Search",
                "queries": [
                    "Which alumni are in Bangalore?",
                    "Show me alumni working in the USA",
                    "Find someone in Europe"
                ]
            },
            {
                "category": "🎯 Profession/Role Search",
                "queries": [
                    "Who are the software engineers?",
                    "Find data scientists in our network",
                    "Show me product managers",
                    "Who works in AI research?"
                ]
            },
            {
                "category": "💰 Salary and Experience Search",
                "queries": [
                    "Who has the highest salary?",
                    "Show me senior alumni with 5+ years experience",
                    "Find entry-level alumni"
                ]
            },
            {
                "category": "🏆 Achievement-based Search",
                "queries": [
                    "Who has published research papers?",
                    "Show me award winners",
                    "Find alumni with certifications"
                ]
            },
            {
                "category": "🤝 Complex Conversational Queries",
                "queries": [
                    "I'm interested in machine learning. Can you recommend some alumni I should connect with?",
                    "I want to work at a startup. Do we have any alumni who might help?",
                    "Who can help me with career advice for data science?",
                    "Find alumni who might be good mentors for a new graduate"
                ]
            }
        ]
        
        session_id = "demo_session"
        print(f"\n🎬 Starting Interactive Demo")
        print("=" * 60)
        
        for category_info in demo_queries:
            print(f"\n{category_info['category']}")
            print("-" * 40)
            
            for query in category_info['queries']:
                print(f"\n❓ Query: {query}")
                print("🤔 Thinking...")
                
                start_time = time.time()
                response = self.rag_service.query_alumni(query, session_id)
                end_time = time.time()
                
                if response.get('success'):
                    print(f"🤖 Answer: {response['answer']}")
                    print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
                else:
                    print(f"❌ Error: {response.get('error')}")
                
                print("-" * 40)
                time.sleep(1)  # Brief pause for readability
    
    def demonstrate_conversation_continuity(self):
        """Show how the system maintains conversation context"""
        print(f"\n💬 Conversation Continuity Demo")
        print("=" * 40)
        
        session_id = "conversation_demo"
        
        conversation_flow = [
            "Who works at Google?",
            "What skills do they have?",  # Should refer to Google employees from previous question
            "Are any of them in machine learning?",
            "What about their graduation years?",
            "Can you summarize what we've discussed about these alumni?"
        ]
        
        for i, query in enumerate(conversation_flow, 1):
            print(f"\nStep {i}: {query}")
            response = self.rag_service.query_alumni(query, session_id)
            
            if response.get('success'):
                print(f"🤖: {response['answer']}")
            else:
                print(f"❌ Error: {response.get('error')}")
            
            time.sleep(2)
    
    def demonstrate_real_time_addition(self):
        """Show how new alumni are immediately searchable"""
        print(f"\n➕ Real-time Addition Demo")
        print("=" * 40)
        
        # Add a new alumni
        new_alumni = {
            "name": "Priyanka Verma",
            "profession": "AI Ethics Researcher", 
            "company": "OpenAI",
            "graduation_year": 2023,
            "degree": "PhD",
            "department": "Computer Science",
            "skills": ["AI Ethics", "Machine Learning", "Python", "Research", "Policy"],
            "email": "priyanka.verma@openai.com",
            "phone": "+1-555-999-8888",
            "location": "San Francisco, CA, USA",
            "current_salary": "$180,000",
            "experience_years": 0,
            "linkedin": "https://linkedin.com/in/priyanka-verma-ai-ethics",
            "achievements": ["PhD in AI Ethics", "Published 15 papers", "UN AI Advisory Panel"],
        }
        
        print("🔄 Adding new alumni: Priyanka Verma (AI Ethics Researcher at OpenAI)...")
        alumni_id = self.rag_service.add_alumni_and_embed(new_alumni)
        print(f"✅ Added with ID: {alumni_id}")
        
        # Immediately search for the new alumni
        print("\n🔍 Searching for the newly added alumni...")
        time.sleep(2)  # Give a moment for embedding to process
        
        queries = [
            "Who works at OpenAI?",
            "Find AI Ethics experts",
            "Show me PhD graduates from 2023",
            "Who can help with AI policy?"
        ]
        
        for query in queries:
            print(f"\n❓ {query}")
            response = self.rag_service.query_alumni(query, "realtime_demo")
            
            if response.get('success'):
                print(f"🤖 {response['answer']}")
            else:
                print(f"❌ Error: {response.get('error')}")
    
    def show_system_statistics(self):
        """Display system statistics and health"""
        print(f"\n📊 System Statistics")
        print("=" * 30)
        
        health = self.rag_service.health_check()
        
        print(f"🗄️  MongoDB Status: {health['mongodb']}")
        print(f"🔍 Vector Store Status: {health['vectorstore']}")
        print(f"📚 Total Alumni Records: {health['total_documents']}")
        print(f"💬 Active Conversations: {health['active_sessions']}")
        
        # Show some sample queries that work well
        print(f"\n💡 Try these queries:")
        sample_queries = [
            "Find software engineers in Bangalore",
            "Who graduated in 2020 and works in AI?",
            "Show me alumni with the highest salaries",
            "Find someone who can help with React development",
            "Who has experience with startups?",
            "Show me alumni working abroad",
            "Find machine learning researchers",
            "Who can mentor a new graduate?"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"{i:2d}. {query}")

def main():
    """Main demo function"""
    print("🎓 Alumni RAG System Complete Demo")
    print("=" * 50)
    
    # Step 1: Set up sample data
    print("Step 1: Setting up sample data in MongoDB...")
    success = setup_mongodb_with_sample_data()
    
    if not success:
        print("❌ Failed to set up sample data. Please check MongoDB connection.")
        return
    
    print("✅ Sample data ready!")
    print("\nWaiting 3 seconds for system to initialize...")
    time.sleep(3)
    
    try:
        # Step 2: Initialize RAG system
        demo = AlumniRAGDemo()
        
        # Step 3: Show system stats
        demo.show_system_statistics()
        
        # Give user option to run different demos
        print(f"\n🎮 Demo Options:")
        print("1. Quick Query Demo (recommended)")
        print("2. Full Demo (all categories)")
        print("3. Conversation Demo") 
        print("4. Real-time Addition Demo")
        print("5. All Demos")
        
        choice = input("\nEnter your choice (1-5) or press Enter for quick demo: ").strip()
        
        if choice == "1" or choice == "":
            # Quick demo with most impressive queries
            print(f"\n🚀 Running Quick Demo...")
            quick_queries = [
                "Who works at Google?",
                "Find machine learning experts", 
                "Show me alumni in Bangalore",
                "Who graduated in 2020?",
                "Find someone who can help with Python development"
            ]
            
            for query in quick_queries:
                print(f"\n❓ {query}")
                response = demo.rag_service.query_alumni(query, "quick_demo")
                
                if response.get('success'):
                    print(f"🤖 {response['answer']}")
                else:
                    print(f"❌ Error: {response.get('error')}")
                
                time.sleep(1)
                
        elif choice == "2":
            # Run full demo with all categories
            demo.run_demo_queries()
            
        elif choice == "3":
            # Run conversation continuity demo
            demo.demonstrate_conversation_continuity()
            
        elif choice == "4":
            # Run real-time addition demo
            demo.demonstrate_real_time_addition()
            
        elif choice == "5":
            # Run all demos sequentially
            demo.run_demo_queries()
            demo.demonstrate_conversation_continuity()
            demo.demonstrate_real_time_addition()
            
        else:
            print("⚠️ Invalid choice. Running quick demo by default.")
            quick_queries = [
                "Who works at Google?",
                "Find machine learning experts", 
                "Show me alumni in Bangalore",
                "Who graduated in 2020?",
                "Find someone who can help with Python development"
            ]
            
            for query in quick_queries:
                print(f"\n❓ {query}")
                response = demo.rag_service.query_alumni(query, "quick_demo")
                
                if response.get('success'):
                    print(f"🤖 {response['answer']}")
                else:
                    print(f"❌ Error: {response.get('error')}")
                
                time.sleep(1)
    
    except Exception as e:
        print(f"❌ Unexpected error occurred: {str(e)}")
    
    print("\n🎉 Demo finished. Thank you for trying the Alumni RAG System!")

if __name__ == "__main__":
    main()
