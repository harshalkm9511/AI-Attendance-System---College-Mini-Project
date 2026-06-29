$reportPath = 'C:\Users\Lenovo\OneDrive\Desktop\AI_Attendance_Project_Report.rtf'

function New-Paragraph {
    param(
        [string]$Text,
        [string]$Style = 'body',
        [int]$SpaceAfter = 120
    )

    $styles = @{
        coverTop = '\qc\b\f1\fs30 '
        coverMid = '\qc\b\f1\fs26 '
        coverTitle = '\qc\b\f0\fs38 '
        coverSub = '\qc\b\f0\fs32 '
        coverName = '\qc\f0\fs26 '
        certHead = '\qc\b\f0\fs34 '
        h1 = '\ql\b\f0\fs30 '
        h2 = '\ql\b\f0\fs26 '
        body = '\ql\f0\fs24 '
        centered = '\qc\f0\fs24 '
        caption = '\qc\i\f0\fs22 '
    }

    $escaped = $Text.Replace('\', '\\').Replace('{', '\{').Replace('}', '\}')
    return $styles[$Style] + $escaped + "\par\sa$SpaceAfter"
}

function New-IncludePicture {
    param([string]$Path)

    $escapedPath = $Path.Replace('\', '\\')
    return "{\pard\qc{\field{\*\fldinst INCLUDEPICTURE `"$escapedPath`" \\d}{\fldrslt [Image]}}\par\sa120}"
}

$diagramDir = 'C:\Users\Lenovo\OneDrive\Desktop\AI_Attendance_Images'
$screensDir = 'C:\Users\Lenovo\OneDrive\Pictures\Screenshots'

$content = @()
$content += '{\rtf1\ansi\deff0'
$content += '{\fonttbl{\f0 Times New Roman;}{\f1 Bahnschrift;}}'
$content += '\margl1440\margr1440\margt1440\margb1440'

# Cover page
$content += New-Paragraph 'A Mini Project Report' 'coverTop' 40
$content += New-Paragraph 'on' 'coverMid' 40
$content += New-Paragraph 'INTELLIGENT ATTENDANCE SYSTEM USING DEEP LEARNING AND COMPUTER VISION' 'coverTitle' 120
$content += New-Paragraph 'by' 'coverMid' 50
$content += New-Paragraph 'Harshal Mahajan (A-33)' 'coverName' 20
$content += New-Paragraph 'Hrishikesh Sawarikar (A-39)' 'coverName' 20
$content += New-Paragraph 'Karan Sign (A-42)' 'coverName' 20
$content += New-Paragraph 'Kartik Gunjal (A-43)' 'coverName' 100
$content += New-Paragraph 'Under the guidance of' 'coverMid' 40
$content += New-Paragraph 'Dr. Swati Barik' 'coverName' 100
$content += New-Paragraph 'Department of Artificial Intelligence Machine Learning' 'coverMid' 30
$content += New-Paragraph 'G H Raisoni Collage of Engineering & Management' 'coverMid' 20
$content += New-Paragraph 'Pune' 'coverMid' 20
$content += New-Paragraph '(An Empowered Autonomous Institute, Affiliated to SPPU, Pune)' 'coverName' 40
$content += New-Paragraph 'Jan-April 2026' 'coverName' 0
$content += '\page'

# Certificate
$content += New-Paragraph 'Department of Artificial Intelligence Machine Learning' 'coverMid' 30
$content += New-Paragraph 'G H Raisoni Collage of Engineering & Management, Pune' 'coverMid' 40
$content += New-Paragraph 'CERTIFICATE' 'certHead' 120
$content += New-Paragraph 'This is to certify that Harshal Mahajan (A-33), Hrishikesh Sawarikar (A-39), Karan Sign (A-42), and Kartik Gunjal (A-43) of Semester 4 have successfully completed their mini project work on "Intelligent Attendance System Using Deep Learning and Computer Vision" at G H Raisoni Collage of Engineering & Management, Pune, in partial fulfillment of the academic requirements. The work has been carried out under the Department of Artificial Intelligence Machine Learning during the academic year 2025-2026, Semester IV.' 'body' 140
$content += New-Paragraph 'Dr. Swati Barik                                             Head of the Department' 'centered' 0
$content += '\page'

# Acknowledgement
$content += New-Paragraph 'Acknowledgement' 'certHead' 100
$content += New-Paragraph 'We express our sincere gratitude to our guide, Dr. Swati Barik, for her valuable guidance, encouragement, and continuous support throughout the development of this project. Her suggestions helped us shape the project in a more practical and academically meaningful way.' 'body' 100
$content += New-Paragraph 'We are thankful to the Head of the Department and all faculty members of the Department of Artificial Intelligence Machine Learning, G H Raisoni Collage of Engineering & Management, Pune, for providing the academic environment and support required for successful completion of this work.' 'body' 100
$content += New-Paragraph 'We also thank our friends and family members for their motivation, patience, and support during the planning, implementation, testing, and documentation of this project.' 'body' 100
$content += New-Paragraph 'Harshal Mahajan (A-33)' 'body' 0
$content += New-Paragraph 'Hrishikesh Sawarikar (A-39)' 'body' 0
$content += New-Paragraph 'Karan Sign (A-42)' 'body' 0
$content += New-Paragraph 'Kartik Gunjal (A-43)' 'body' 0
$content += '\page'

# Contents
$content += New-Paragraph 'Contents' 'certHead' 80
$content += New-Paragraph 'Abstract' 'body' 20
$content += New-Paragraph 'Chapter 1  Introduction' 'body' 10
$content += New-Paragraph 'Chapter 2  System Architecture & Methodology' 'body' 10
$content += New-Paragraph 'Chapter 3  Software Requirement Specification (SRS)' 'body' 10
$content += New-Paragraph 'Chapter 4  UML Diagrams' 'body' 10
$content += New-Paragraph 'Chapter 5  Project Plan & Cost Estimation' 'body' 10
$content += New-Paragraph 'Chapter 6  Result & Discussion' 'body' 10
$content += New-Paragraph 'This report follows the reference template structure. Page numbering, final formatting, and table of contents can be updated inside Microsoft Word if required before final printing.' 'body' 0
$content += '\page'

# Abstract
$content += New-Paragraph 'Abstract' 'certHead' 100
$content += New-Paragraph 'Traditional attendance systems used in educational institutions are repetitive, time-consuming, and vulnerable to proxy attendance. Manual roll calls reduce effective classroom time and increase the chance of human error in record maintenance. To address these issues, this mini project proposes an Intelligent Attendance System using Deep Learning and Computer Vision.' 'body' 100
$content += New-Paragraph 'The proposed system provides a modern web interface for teacher login, student enrollment, attendance processing, roster review, attendance history, and analytics. Students are enrolled with one or more reference face images. During attendance marking, the teacher creates a class session and uploads a classroom image. The system detects faces, compares them against enrolled students using local face embeddings, and generates a recognition summary with confidence scores.' 'body' 100
$content += New-Paragraph 'After automatic recognition, the teacher can review the attendance roster, correct uncertain cases manually, and save the final attendance record. The system also stores previous class sessions, exports attendance data in CSV format, and displays analytics such as average attendance, recent class performance, and low-attendance alerts.' 'body' 100
$content += New-Paragraph 'The project is developed using free and open-source technologies including React, FastAPI, SQLite, and OpenCV-based recognition models. The result is a practical, low-cost, and locally deployable attendance solution suitable for academic environments.' 'body' 0
$content += '\page'

# Chapter 1
$content += New-Paragraph 'Chapter 1  Introduction' 'h1' 120
$content += New-Paragraph '1.1 Overview & Motivation' 'h2' 100
$content += New-Paragraph 'Attendance management is one of the most common and repetitive tasks in educational institutions. Traditional paper-based and roll-call methods consume lecture time, create administrative overhead, and allow proxy attendance. As the number of students and classes increases, maintaining accurate records manually becomes more difficult.' 'body' 100
$content += New-Paragraph 'Advances in deep learning and computer vision make it possible to identify students automatically using facial features. This project was motivated by the need to create a practical attendance platform that reduces manual effort, improves data accuracy, and gives teachers better visibility into attendance trends.' 'body' 100
$content += New-Paragraph 'The proposed system combines student registration, classroom image processing, recognition review, report export, and dashboard analytics in one integrated solution. The project demonstrates how AI can be applied to solve a real academic management problem in a simple and cost-effective way.' 'body' 100
$content += New-Paragraph '1.2 Problem Statement' 'h2' 100
$content += New-Paragraph 'Existing attendance systems are often inefficient, error-prone, and weak in identity verification. Manual methods take time, create inconsistent records, and fail to prevent proxy attendance. Even when digital systems are used, they often still depend heavily on manual data entry and do not provide automatic recognition, image-based evidence, or useful analytics. Therefore, there is a need for a smarter attendance system that can identify students accurately, reduce manual workload, and maintain reliable records.' 'body' 100
$content += New-Paragraph '1.3 Project Scope & Limitations' 'h2' 100
$content += New-Paragraph 'Scope:' 'body' 20
$content += New-Paragraph '- Teacher login and secure access to attendance features.' 'body' 10
$content += New-Paragraph '- Student enrollment with face-image registration.' 'body' 10
$content += New-Paragraph '- Classroom image-based attendance marking.' 'body' 10
$content += New-Paragraph '- Manual review of recognition results before final save.' 'body' 10
$content += New-Paragraph '- Storage of session history and CSV export of attendance records.' 'body' 10
$content += New-Paragraph '- Dashboard analytics including attendance percentage and low-attendance alerts.' 'body' 60
$content += New-Paragraph 'Limitations:' 'body' 20
$content += New-Paragraph '- Recognition accuracy depends on image quality, lighting, and visibility of faces.' 'body' 10
$content += New-Paragraph '- Similar-looking students may require manual review.' 'body' 10
$content += New-Paragraph '- The current deployment is designed mainly for local or departmental use.' 'body' 10
$content += New-Paragraph '- Performance may reduce on low-end systems or with poor-quality classroom images.' 'body' 100
$content += New-Paragraph '1.4 Hardware & Software Requirement' 'h2' 100
$content += New-Paragraph 'Hardware Requirements:' 'body' 20
$content += New-Paragraph '- Computer or Laptop' 'body' 10
$content += New-Paragraph '- Minimum 4 GB RAM' 'body' 10
$content += New-Paragraph '- Local storage for student and classroom images' 'body' 10
$content += New-Paragraph '- Camera or image source for capturing student/classroom photos' 'body' 60
$content += New-Paragraph 'Software Requirements:' 'body' 20
$content += New-Paragraph '- Windows operating system' 'body' 10
$content += New-Paragraph '- Python and FastAPI for the backend' 'body' 10
$content += New-Paragraph '- React and Vite for the frontend' 'body' 10
$content += New-Paragraph '- SQLite for local database storage' 'body' 10
$content += New-Paragraph '- OpenCV YuNet and SFace models for recognition' 'body' 0
$content += '\page'

# Chapter 2
$content += New-Paragraph 'CHAPTER 2: SYSTEM ARCHITECTURE & METHODOLOGY' 'h1' 120
$content += New-Paragraph '2.1 System Overview' 'h2' 100
$content += New-Paragraph 'The Intelligent Attendance System is a web-based application that allows teachers to manage attendance using deep learning and computer vision. The workflow begins with teacher login, followed by student enrollment with reference images. For attendance, the teacher creates a class session, uploads a classroom image, and reviews the generated recognition results before saving final attendance.' 'body' 100
$content += New-Paragraph 'The system uses a split architecture where the frontend handles user interaction, the backend processes attendance logic, the database stores structured records, and the recognition engine extracts and compares face features. This makes the system modular, easier to manage, and suitable for future enhancement.' 'body' 100
$content += New-Paragraph '2.2 System Architecture' 'h2' 100
$content += New-Paragraph 'Main Components:' 'body' 20
$content += New-Paragraph '- Frontend interface for login, dashboard, enrollment, review, and history.' 'body' 10
$content += New-Paragraph '- Backend API for authentication, student records, session creation, and exports.' 'body' 10
$content += New-Paragraph '- Recognition engine for face detection, alignment, and matching.' 'body' 10
$content += New-Paragraph '- SQLite database for teachers, students, classes, and attendance logs.' 'body' 10
$content += New-Paragraph '- Local storage for classroom images and student face samples.' 'body' 60

if (Test-Path "$diagramDir\05_Deployment_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\05_Deployment_Diagram.png"
    $content += New-Paragraph 'Figure 2.1 Deployment / system architecture diagram for the AI Attendance project.' 'caption' 160
}

$content += New-Paragraph '2.3 Algorithms & Methodology Used' 'h2' 100
$content += New-Paragraph 'The system uses a local embedding-based face-recognition pipeline instead of simple image correlation. YuNet is used for face detection, while SFace is used to generate numerical face embeddings. The embedding of each detected face is compared with registered student embeddings using cosine similarity. If the score crosses the threshold, the student is recognized; otherwise, the system marks the face as unknown.' 'body' 100
$content += New-Paragraph 'Step-by-Step Working:' 'body' 20
$content += New-Paragraph '1. Teacher creates class session and uploads classroom image.' 'body' 10
$content += New-Paragraph '2. System detects faces present in the classroom image.' 'body' 10
$content += New-Paragraph '3. Face features are extracted using the recognition model.' 'body' 10
$content += New-Paragraph '4. Extracted features are compared with enrolled student encodings.' 'body' 10
$content += New-Paragraph '5. Recognition results are shown with score values.' 'body' 10
$content += New-Paragraph '6. Teacher reviews roster and saves final attendance.' 'body' 60

if (Test-Path "$diagramDir\08_Activity_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\08_Activity_Diagram.png"
    $content += New-Paragraph 'Figure 2.2 Activity diagram representing the attendance-processing methodology.' 'caption' 0
}
$content += '\page'

# Chapter 3
$content += New-Paragraph 'CHAPTER 3: SOFTWARE REQUIREMENT SPECIFICATION (SRS)' 'h1' 120
$content += New-Paragraph '3.1 Functional Requirements' 'h2' 100
$content += New-Paragraph 'The system should perform the following functions:' 'body' 20
$content += New-Paragraph '- Allow teacher login using username and password.' 'body' 10
$content += New-Paragraph '- Enroll students with name, roll number, department, division, and face images.' 'body' 10
$content += New-Paragraph '- Display, search, edit, and delete student records.' 'body' 10
$content += New-Paragraph '- Create class sessions with department, division, date, and time range.' 'body' 10
$content += New-Paragraph '- Process classroom image for face detection and recognition.' 'body' 10
$content += New-Paragraph '- Show confidence scores and manual review interface.' 'body' 10
$content += New-Paragraph '- Save attendance history and export data as CSV.' 'body' 10
$content += New-Paragraph '- Display student attendance analytics and alerts.' 'body' 100
$content += New-Paragraph '3.2 Non-Functional Requirements' 'h2' 100
$content += New-Paragraph 'The system should provide acceptable recognition accuracy, fast local response time, simple user interaction, reliable record storage, and modular code for future maintenance. It should use free and open-source tools only and should continue to work in a local environment without depending on paid services.' 'body' 100
$content += New-Paragraph '3.3 Performance Requirements' 'h2' 100
$content += New-Paragraph 'The system should process classroom images within a practical time for daily academic usage. Dashboard loading, student directory retrieval, and class history access should remain responsive under normal local deployment. Exporting attendance data should also complete quickly for typical class sizes.' 'body' 100
$content += New-Paragraph '3.4 Design Constraints' 'h2' 100
$content += New-Paragraph 'The system is limited by image quality, classroom lighting, face orientation, and local hardware performance. Since the project is designed to remain free, it depends on open-source models and local storage rather than paid cloud services.' 'body' 100
$content += New-Paragraph '3.5 External Interface Requirements' 'h2' 100
$content += New-Paragraph 'The user interface includes login page, dashboard, student records page, class session page, recognition review panel, and history/export page. The software interface connects React frontend to FastAPI backend using HTTP. The backend connects with SQLite and local image storage.' 'body' 0
$content += '\page'

# Chapter 4 UML
$content += New-Paragraph 'CHAPTER 4: UML DIAGRAMS' 'h1' 120
$content += New-Paragraph 'This chapter represents the structure and behavior of the Intelligent Attendance System using UML diagrams.' 'body' 100
$content += New-Paragraph '4.1 Use Case Diagram' 'h2' 80
if (Test-Path "$diagramDir\11_Use_Case_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\11_Use_Case_Diagram.png"
    $content += New-Paragraph 'Figure 4.1 Use case diagram for the AI Attendance project.' 'caption' 120
}
$content += New-Paragraph '4.2 Class Diagram' 'h2' 80
if (Test-Path "$diagramDir\10_Class_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\10_Class_Diagram.png"
    $content += New-Paragraph 'Figure 4.2 Class diagram for the AI Attendance project.' 'caption' 120
}
$content += New-Paragraph '4.3 Sequence Diagram' 'h2' 80
if (Test-Path "$diagramDir\09_Sequence_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\09_Sequence_Diagram.png"
    $content += New-Paragraph 'Figure 4.3 Sequence diagram for the AI Attendance project.' 'caption' 120
}
$content += New-Paragraph '4.4 Activity Diagram' 'h2' 80
if (Test-Path "$diagramDir\08_Activity_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\08_Activity_Diagram.png"
    $content += New-Paragraph 'Figure 4.4 Activity diagram for the AI Attendance project.' 'caption' 120
}
$content += New-Paragraph '4.5 State Diagram' 'h2' 80
if (Test-Path "$diagramDir\07_State_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\07_State_Diagram.png"
    $content += New-Paragraph 'Figure 4.5 State diagram for the AI Attendance project.' 'caption' 120
}
$content += New-Paragraph '4.6 Component Diagram' 'h2' 80
if (Test-Path "$diagramDir\06_Component_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\06_Component_Diagram.png"
    $content += New-Paragraph 'Figure 4.6 Component diagram for the AI Attendance project.' 'caption' 120
}
$content += New-Paragraph '4.7 Deployment Diagram' 'h2' 80
if (Test-Path "$diagramDir\05_Deployment_Diagram.png") {
    $content += New-IncludePicture "$diagramDir\05_Deployment_Diagram.png"
    $content += New-Paragraph 'Figure 4.7 Deployment diagram for the AI Attendance project.' 'caption' 0
}
$content += '\page'

# Chapter 5
$content += New-Paragraph 'CHAPTER 5: PROJECT PLAN & COST ESTIMATION' 'h1' 120
$content += New-Paragraph '5.1 Project Plan' 'h2' 100
$content += New-Paragraph 'The project plan defines the sequence of activities required to complete the Intelligent Attendance System systematically. The work begins with requirement analysis and system design, followed by UI implementation, backend development, recognition integration, testing, and documentation.' 'body' 100
$content += New-Paragraph 'Development phases include requirement analysis, system design, student management module, attendance module, analytics/dashboard creation, testing, debugging, and final documentation.' 'body' 100
if (Test-Path "$diagramDir\04_Project_Plan.png") {
    $content += New-IncludePicture "$diagramDir\04_Project_Plan.png"
    $content += New-Paragraph 'Figure 5.1 Project plan for the AI Attendance project.' 'caption' 120
}
if (Test-Path "$diagramDir\03_Gantt_Chart.png") {
    $content += New-IncludePicture "$diagramDir\03_Gantt_Chart.png"
    $content += New-Paragraph 'Figure 5.2 Gantt chart showing the eight-week development schedule.' 'caption' 100
}
$content += New-Paragraph 'The Gantt chart represents the project schedule using a task versus week structure and helps in understanding the planned order of development and delivery.' 'body' 100
$content += New-Paragraph '5.2 Cost Estimation' 'h2' 100
$content += New-Paragraph 'The cost estimation is based on approximate development effort and resource usage. Since the project intentionally uses free and open-source technologies, the total software cost remains low.' 'body' 100
if (Test-Path "$diagramDir\02_Cost_Estimation.png") {
    $content += New-IncludePicture "$diagramDir\02_Cost_Estimation.png"
    $content += New-Paragraph 'Figure 5.3 Cost estimation chart for the AI Attendance project.' 'caption' 0
}
$content += '\page'

# Chapter 6
$content += New-Paragraph 'CHAPTER 6: RESULT & DISCUSSION' 'h1' 120
$content += New-Paragraph '6.1 Results' 'h2' 100
$content += New-Paragraph 'The developed system successfully demonstrates the complete attendance workflow from teacher login to final attendance export. The dashboard displays registered student count, average attendance, total classes held, recent sessions, and low-attendance alerts. Student registration accepts multiple face samples, and the attendance page creates class sessions using classroom images.' 'body' 100
$content += New-Paragraph 'Recognition results show detected face counts, recognized students, unknown faces, and confidence scores. The roster review page allows manual corrections before attendance is saved. Historical class sessions can be revisited, and attendance can be exported in CSV format for reporting.' 'body' 100

$uiFigures = @(
    @{Path="$screensDir\Screenshot 2026-04-13 100000.png"; Caption='Figure 6.1 Dashboard view showing attendance summary and recent sessions.'},
    @{Path="$screensDir\Screenshot 2026-04-13 100028.png"; Caption='Figure 6.2 Student Records page with enrollment form and directory.'},
    @{Path="$screensDir\Screenshot 2026-04-13 100102.png"; Caption='Figure 6.3 Attendance session creation screen.'},
    @{Path="$screensDir\Screenshot 2026-04-13 100605.png"; Caption='Figure 6.4 Recognition results panel showing detected and recognized faces.'},
    @{Path="$screensDir\Screenshot 2026-04-13 100624.png"; Caption='Figure 6.5 Roster review screen for final attendance confirmation.'},
    @{Path="$screensDir\Screenshot 2026-04-13 100119.png"; Caption='Figure 6.6 Class history and session detail page.'}
)

foreach ($figure in $uiFigures) {
    if (Test-Path $figure.Path) {
        $content += New-IncludePicture $figure.Path
        $content += New-Paragraph $figure.Caption 'caption' 120
    }
}

$content += New-Paragraph '6.2 Discussion' 'h2' 100
$content += New-Paragraph 'The project shows that a free and locally deployable AI attendance platform can be built with practical features and an easy-to-use interface. Compared with manual attendance systems, the project reduces repetitive work, improves record consistency, and supports teacher review for uncertain recognition cases.' 'body' 100
$content += New-Paragraph 'The main strengths of the system are its modern interface, local processing pipeline, attendance history, CSV export, and analytics dashboard. However, the quality of recognition still depends on good student enrollment images and suitable classroom conditions. Therefore, the system balances automatic recognition with manual review to improve reliability in real use.' 'body' 100
$content += New-Paragraph 'Overall, the results confirm that the Intelligent Attendance System is a useful academic mini-project that demonstrates the practical use of deep learning and computer vision in attendance management.' 'body' 0

$content += '}'

$content -join "`r`n" | Set-Content -LiteralPath $reportPath -Encoding ASCII
Get-Item -LiteralPath $reportPath | Format-List FullName,Length,LastWriteTime
