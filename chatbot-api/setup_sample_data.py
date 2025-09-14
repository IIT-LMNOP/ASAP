# setup_sample_data.py
import pymongo
from datetime import datetime, timedelta
import random
from typing import List, Dict

# Sample data for realistic alumni database
SAMPLE_ALUMNI_DATA = [
    {
        "name": "Arjun Sharma",
        "profession": "Software Engineer",
        "company": "Google",
        "graduation_year": 2019,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["Python", "JavaScript", "React", "Machine Learning", "Docker"],
        "email": "arjun.sharma@gmail.com",
        "phone": "+91-9876543210",
        "location": "Bangalore, Karnataka",
        "current_salary": "₹25,00,000",
        "experience_years": 4,
        "linkedin": "https://linkedin.com/in/arjun-sharma",
        "achievements": ["Google Code Jam Finalist", "Published research paper on ML"],
        "created_at": datetime.now() - timedelta(days=100)
    },
    {
        "name": "Priya Patel",
        "profession": "Data Scientist",
        "company": "Microsoft",
        "graduation_year": 2020,
        "degree": "Master of Science",
        "department": "Data Science",
        "skills": ["Python", "R", "SQL", "TensorFlow", "Statistics", "Power BI"],
        "email": "priya.patel@outlook.com",
        "phone": "+91-8765432109",
        "location": "Hyderabad, Telangana",
        "current_salary": "₹22,00,000",
        "experience_years": 3,
        "linkedin": "https://linkedin.com/in/priya-patel",
        "achievements": ["Microsoft AI Challenge Winner", "Kaggle Expert"],
        "created_at": datetime.now() - timedelta(days=95)
    },
    {
        "name": "Rahul Krishnan",
        "profession": "Product Manager",
        "company": "Amazon",
        "graduation_year": 2018,
        "degree": "Bachelor of Technology",
        "department": "Information Technology",
        "skills": ["Product Strategy", "Analytics", "SQL", "Python", "Leadership", "Agile"],
        "email": "rahul.krishnan@amazon.com",
        "phone": "+91-7654321098",
        "location": "Chennai, Tamil Nadu",
        "current_salary": "₹28,00,000",
        "experience_years": 5,
        "linkedin": "https://linkedin.com/in/rahul-krishnan",
        "achievements": ["Launched 3 successful products", "MBA from IIM Bangalore"],
        "created_at": datetime.now() - timedelta(days=90)
    },
    {
        "name": "Sneha Gupta",
        "profession": "AI Research Scientist",
        "company": "DeepMind",
        "graduation_year": 2017,
        "degree": "PhD",
        "department": "Computer Science",
        "skills": ["Deep Learning", "PyTorch", "Research", "NLP", "Computer Vision", "Python"],
        "email": "sneha.gupta@deepmind.com",
        "phone": "+44-7123456789",
        "location": "London, UK",
        "current_salary": "£85,000",
        "experience_years": 6,
        "linkedin": "https://linkedin.com/in/sneha-gupta-ai",
        "achievements": ["10+ research papers", "NIPS Best Paper Award", "PhD from Stanford"],
        "created_at": datetime.now() - timedelta(days=85)
    },
    {
        "name": "Vikram Singh",
        "profession": "DevOps Engineer",
        "company": "Netflix",
        "graduation_year": 2021,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["Kubernetes", "Docker", "AWS", "Python", "Jenkins", "Terraform"],
        "email": "vikram.singh@netflix.com",
        "phone": "+1-555-123-4567",
        "location": "San Francisco, CA, USA",
        "current_salary": "$120,000",
        "experience_years": 2,
        "linkedin": "https://linkedin.com/in/vikram-singh-devops",
        "achievements": ["AWS Certified Solutions Architect", "Open Source Contributor"],
        "created_at": datetime.now() - timedelta(days=80)
    },
    {
        "name": "Anita Reddy",
        "profession": "UX Designer",
        "company": "Adobe",
        "graduation_year": 2020,
        "degree": "Bachelor of Design",
        "department": "Design",
        "skills": ["UI/UX Design", "Figma", "Sketch", "User Research", "Prototyping", "Adobe Creative Suite"],
        "email": "anita.reddy@adobe.com",
        "phone": "+91-6543210987",
        "location": "Pune, Maharashtra",
        "current_salary": "₹18,00,000",
        "experience_years": 3,
        "linkedin": "https://linkedin.com/in/anita-reddy-ux",
        "achievements": ["Adobe Design Circle Member", "Won National Design Competition"],
        "created_at": datetime.now() - timedelta(days=75)
    },
    {
        "name": "Karthik Menon",
        "profession": "Cybersecurity Analyst",
        "company": "Palo Alto Networks",
        "graduation_year": 2019,
        "degree": "Master of Technology",
        "department": "Cybersecurity",
        "skills": ["Ethical Hacking", "Network Security", "Python", "Incident Response", "SIEM", "Penetration Testing"],
        "email": "karthik.menon@paloaltonetworks.com",
        "phone": "+91-5432109876",
        "location": "Mumbai, Maharashtra",
        "current_salary": "₹24,00,000",
        "experience_years": 4,
        "linkedin": "https://linkedin.com/in/karthik-menon-security",
        "achievements": ["CISSP Certified", "Bug Bounty Hunter", "Spoke at DefCon"],
        "created_at": datetime.now() - timedelta(days=70)
    },
    {
        "name": "Meera Iyer",
        "profession": "Blockchain Developer",
        "company": "Coinbase",
        "graduation_year": 2021,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["Solidity", "Web3", "JavaScript", "Python", "Smart Contracts", "DeFi"],
        "email": "meera.iyer@coinbase.com",
        "phone": "+1-555-987-6543",
        "location": "New York, NY, USA",
        "current_salary": "$110,000",
        "experience_years": 2,
        "linkedin": "https://linkedin.com/in/meera-iyer-blockchain",
        "achievements": ["Ethereum Developer Certification", "Built DeFi protocol with $1M TVL"],
        "created_at": datetime.now() - timedelta(days=65)
    },
    {
        "name": "Rohan Joshi",
        "profession": "Mobile App Developer",
        "company": "Swiggy",
        "graduation_year": 2020,
        "degree": "Bachelor of Technology",
        "department": "Information Technology",
        "skills": ["Flutter", "React Native", "iOS", "Android", "Firebase", "Node.js"],
        "email": "rohan.joshi@swiggy.in",
        "phone": "+91-4321098765",
        "location": "Bangalore, Karnataka",
        "current_salary": "₹20,00,000",
        "experience_years": 3,
        "linkedin": "https://linkedin.com/in/rohan-joshi-mobile",
        "achievements": ["App with 1M+ downloads", "Google Play Store Featured Developer"],
        "created_at": datetime.now() - timedelta(days=60)
    },
    {
        "name": "Kavya Nair",
        "profession": "Machine Learning Engineer",
        "company": "Tesla",
        "graduation_year": 2018,
        "degree": "Master of Science",
        "department": "Artificial Intelligence",
        "skills": ["PyTorch", "Computer Vision", "Python", "CUDA", "MLOps", "Autonomous Systems"],
        "email": "kavya.nair@tesla.com",
        "phone": "+1-555-456-7890",
        "location": "Austin, TX, USA",
        "current_salary": "$140,000",
        "experience_years": 5,
        "linkedin": "https://linkedin.com/in/kavya-nair-ml",
        "achievements": ["Self-driving car patents", "CVPR paper author", "Tesla AI Team Lead"],
        "created_at": datetime.now() - timedelta(days=55)
    },
    {
        "name": "Amit Agarwal",
        "profession": "Cloud Solutions Architect",
        "company": "Amazon Web Services",
        "graduation_year": 2017,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["AWS", "Azure", "Kubernetes", "Microservices", "Python", "Serverless"],
        "email": "amit.agarwal@aws.amazon.com",
        "phone": "+91-3210987654",
        "location": "Delhi, India",
        "current_salary": "₹32,00,000",
        "experience_years": 6,
        "linkedin": "https://linkedin.com/in/amit-agarwal-cloud",
        "achievements": ["AWS Solutions Architect Professional", "Cloud migration expert", "Tech speaker"],
        "created_at": datetime.now() - timedelta(days=50)
    },
    {
        "name": "Divya Pillai",
        "profession": "Frontend Developer",
        "company": "Airbnb",
        "graduation_year": 2021,
        "degree": "Bachelor of Technology",
        "department": "Information Technology",
        "skills": ["React", "TypeScript", "Next.js", "CSS", "JavaScript", "GraphQL"],
        "email": "divya.pillai@airbnb.com",
        "phone": "+1-555-234-5678",
        "location": "San Francisco, CA, USA",
        "current_salary": "$115,000",
        "experience_years": 2,
        "linkedin": "https://linkedin.com/in/divya-pillai-frontend",
        "achievements": ["React Conf Speaker", "Open source maintainer", "Design system creator"],
        "created_at": datetime.now() - timedelta(days=45)
    },
    {
        "name": "Sanjay Kumar",
        "profession": "Backend Developer",
        "company": "Flipkart",
        "graduation_year": 2019,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["Java", "Spring Boot", "MongoDB", "Redis", "Kafka", "Microservices"],
        "email": "sanjay.kumar@flipkart.com",
        "phone": "+91-2109876543",
        "location": "Bangalore, Karnataka",
        "current_salary": "₹26,00,000",
        "experience_years": 4,
        "linkedin": "https://linkedin.com/in/sanjay-kumar-backend",
        "achievements": ["Built scalable systems for 100M+ users", "Java certification", "Tech blogger"],
        "created_at": datetime.now() - timedelta(days=40)
    },
    {
        "name": "Riya Shah",
        "profession": "Data Analyst",
        "company": "Zomato",
        "graduation_year": 2022,
        "degree": "Bachelor of Science",
        "department": "Statistics",
        "skills": ["Python", "SQL", "Tableau", "Excel", "Statistics", "A/B Testing"],
        "email": "riya.shah@zomato.com",
        "phone": "+91-1098765432",
        "location": "Gurgaon, Haryana",
        "current_salary": "₹12,00,000",
        "experience_years": 1,
        "linkedin": "https://linkedin.com/in/riya-shah-data",
        "achievements": ["Improved delivery efficiency by 20%", "Tableau Desktop Specialist"],
        "created_at": datetime.now() - timedelta(days=35)
    },
    {
        "name": "Akash Verma",
        "profession": "Game Developer",
        "company": "Ubisoft",
        "graduation_year": 2020,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["Unity", "C#", "Unreal Engine", "C++", "3D Graphics", "Game Design"],
        "email": "akash.verma@ubisoft.com",
        "phone": "+33-1-23-45-67-89",
        "location": "Paris, France",
        "current_salary": "€55,000",
        "experience_years": 3,
        "linkedin": "https://linkedin.com/in/akash-verma-gamedev",
        "achievements": ["Shipped 2 AAA games", "Unity Certified Developer", "Game Jam Winner"],
        "created_at": datetime.now() - timedelta(days=30)
    },
    {
        "name": "Pooja Desai",
        "profession": "Quality Assurance Engineer",
        "company": "Spotify",
        "graduation_year": 2021,
        "degree": "Bachelor of Technology",
        "department": "Information Technology",
        "skills": ["Selenium", "Python", "API Testing", "Automation", "JIRA", "Postman"],
        "email": "pooja.desai@spotify.com",
        "phone": "+46-70-123-4567",
        "location": "Stockholm, Sweden",
        "current_salary": "500,000 SEK",
        "experience_years": 2,
        "linkedin": "https://linkedin.com/in/pooja-desai-qa",
        "achievements": ["Automated 80% of test cases", "ISTQB Certified", "Bug bounty participant"],
        "created_at": datetime.now() - timedelta(days=25)
    },
    {
        "name": "Nikhil Pandey",
        "profession": "Site Reliability Engineer",
        "company": "Uber",
        "graduation_year": 2018,
        "degree": "Bachelor of Technology",
        "department": "Computer Science",
        "skills": ["Go", "Kubernetes", "Monitoring", "Linux", "Docker", "Prometheus"],
        "email": "nikhil.pandey@uber.com",
        "phone": "+1-555-345-6789",
        "location": "Seattle, WA, USA",
        "current_salary": "$135,000",
        "experience_years": 5,
        "linkedin": "https://linkedin.com/in/nikhil-pandey-sre",
        "achievements": ["Reduced downtime by 99.9%", "Kubernetes Certified Administrator", "On-call hero"],
        "created_at": datetime.now() - timedelta(days=20)
    },
    {
        "name": "Shruti Agrawal",
        "profession": "Business Analyst",
        "company": "McKinsey & Company",
        "graduation_year": 2019,
        "degree": "Master of Business Administration",
        "department": "Business Administration",
        "skills": ["Business Strategy", "Excel", "PowerPoint", "SQL", "Market Research", "Financial Modeling"],
        "email": "shruti.agrawal@mckinsey.com",
        "phone": "+91-9087654321",
        "location": "Mumbai, Maharashtra",
        "current_salary": "₹45,00,000",
        "experience_years": 4,
        "linkedin": "https://linkedin.com/in/shruti-agrawal-ba",
        "achievements": ["Led digital transformation projects", "CFA Level II", "Top performer 2 years"],
        "created_at": datetime.now() - timedelta(days=15)
    },
    {
        "name": "Rajesh Bhatia",
        "profession": "Technical Writer",
        "company": "Atlassian",
        "graduation_year": 2020,
        "degree": "Bachelor of Arts",
        "department": "English Literature",
        "skills": ["Technical Writing", "Documentation", "Markdown", "Git", "API Documentation", "Content Strategy"],
        "email": "rajesh.bhatia@atlassian.com",
        "phone": "+61-4-1234-5678",
        "location": "Sydney, Australia",
        "current_salary": "AUD 95,000",
        "experience_years": 3,
        "linkedin": "https://linkedin.com/in/rajesh-bhatia-writer",
        "achievements": ["Rewrote entire product documentation", "Technical writing certification", "Content award winner"],
        "created_at": datetime.now() - timedelta(days=10)
    },
    {
        "name": "Nisha Chopra",
        "profession": "Digital Marketing Manager",
        "company": "HubSpot",
        "graduation_year": 2021,
        "degree": "Bachelor of Business Administration",
        "department": "Marketing",
        "skills": ["Digital Marketing", "SEO", "Google Analytics", "Content Marketing", "Social Media", "HubSpot"],
        "email": "nisha.chopra@hubspot.com",
        "phone": "+1-555-567-8901",
        "location": "Boston, MA, USA",
        "current_salary": "$75,000",
        "experience_years": 2,
        "linkedin": "https://linkedin.com/in/nisha-chopra-marketing",
        "achievements": ["Increased lead generation by 150%", "Google Ads Certified", "Content viral campaigns"],
        "created_at": datetime.now() - timedelta(days=5)
    }
]

def setup_mongodb_with_sample_data():
    """Set up MongoDB with sample alumni data"""
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Create database and collection
        db = client["alumni_db"]
        collection = db["alumni"]
        
        # Clear existing data (optional)
        print("Clearing existing data...")
        collection.delete_many({})
        
        # Insert sample data
        print(f"Inserting {len(SAMPLE_ALUMNI_DATA)} alumni records...")
        result = collection.insert_many(SAMPLE_ALUMNI_DATA)
        
        print(f"✅ Successfully inserted {len(result.inserted_ids)} alumni records")
        
        # Create indexes for better performance
        print("Creating indexes...")
        collection.create_index("name")
        collection.create_index("graduation_year")
        collection.create_index("company")
        collection.create_index("department")
        collection.create_index("skills")
        
        # Display some stats
        total_docs = collection.count_documents({})
        print(f"📊 Total documents in database: {total_docs}")
        
        # Show sample data
        print("\n📋 Sample records:")
        for doc in collection.find().limit(3):
            print(f"- {doc['name']}, {doc['profession']} at {doc['company']} (Class of {doc['graduation_year']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up MongoDB: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Alumni Database with Sample Data...")
    print("=" * 50)
    
    success = setup_mongodb_with_sample_data()
    
    if success:
        print("\n✅ Sample data setup complete!")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Visit: http://localhost:8000/docs")
        print("3. Try queries like:")
        print("   - 'Who works at Google?'")
        print("   - 'Show me alumni from 2020'") 
        print("   - 'Find machine learning experts'")
        print("   - 'Who is in Bangalore?'")
    else:
        print("\n❌ Failed to set up sample data. Please check MongoDB connection.")