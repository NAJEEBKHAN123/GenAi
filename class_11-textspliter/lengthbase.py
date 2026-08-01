from langchain_text_splitters import CharacterTextSplitter


text = """
🎓 **Project Completed — School Management System**

I’m happy to share that I’ve successfully completed my **School Management System** project. 🚀

The goal of this project was to build a centralized system that can help schools manage their daily operations more efficiently.

Some of the key areas I worked on include:

• Student management
• Teacher management
• Attendance management
• Classes and courses
• Student records
• Marks and academic information
• Administrative management
• User authentication and role-based access

Building this project gave me valuable experience in developing a **real-world full-stack application**, from designing the interface to implementing the backend, database, authentication, and overall system logic.

This project also helped me better understand how different parts of a software system work together to solve an actual problem.

💻 **Technologies:** React, Node.js, Express.js, MongoDB, and other tools used throughout the development process.

I’m excited to keep improving the system and continue building more practical and meaningful software projects.

**One project completed. More to build. 🚀**

#SchoolManagementSystem #FullStackDevelopment #WebDevelopment #React #NodeJS #MongoDB #SoftwareDevelopment

"""


splitter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=0
)


result = splitter.split_text(text)
print(result)