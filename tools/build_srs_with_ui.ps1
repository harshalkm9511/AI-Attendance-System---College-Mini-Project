$out = 'C:\Users\Lenovo\OneDrive\Desktop\SRS G5 Professional With UI New.rtf'
$rtf = @'
{\rtf1\ansi\deff0
{\fonttbl{\f0 Times New Roman;}{\f1 Bahnschrift;}}
\margl1440\margr1440\margt1440\margb1440
\qc\b\f1\fs30 Experiment No-3\par\sa80
\qc\b\f1\fs26 Prepare the Software Requirements Specification (SRS) document, covering functional and non-functional requirements, system functionality, user interactions, and limitations.\par\sa180
\qc\b\f0\fs36 Software Requirements Specification (SRS)\par\sa180
\qc\b\f1\fs26 For\par\sa60
\qc\b\f0\fs32 Intelligent Attendance System Using Deep Learning and Computer Vision\par\sa180
\qc\b\f1\fs26 Prepared by\par\sa80
\qc\f0\fs26 1. Harshal Mahajan, A33\par\sa30
\qc\f0\fs26 2. Hrishikesh Sawarikar, A39\par\sa30
\qc\f0\fs26 3. Kartik Gunjal, A43\par\sa30
\qc\f0\fs26 4. Karan Sign, A42\par\sa140
\qc\b\f1\fs26 Institution: G H Raisoni College of Engineering and Management, Pune\par\sa0
\page
\ql\b\f0\fs30 1. Introduction\par\sa120
\ql\b\f0\fs26 1.1 Purpose\par\sa120
\ql\f0\fs24 This Software Requirements Specification defines the functional and non-functional requirements of the Intelligent Attendance System Using Deep Learning and Computer Vision. It serves as a formal reference for implementation, testing, academic evaluation, and future enhancement of the project.\par\sa120
\ql\b\f0\fs26 1.2 Scope\par\sa120
\ql\f0\fs24 The system automates classroom attendance using deep learning and computer vision techniques. It enables teachers to sign in, enroll students, upload reference images, create class sessions, upload classroom images, review recognition results, finalize attendance, export reports, and monitor attendance analytics.\par\sa120
\ql\b\f0\fs26 1.3 Definitions, Acronyms, and Abbreviations\par\sa120
\ql\f0\fs24 AI: Artificial Intelligence. DL: Deep Learning. CV: Computer Vision. UI: User Interface. API: Application Programming Interface. CSV: Comma-Separated Values. SRS: Software Requirements Specification.\par\sa120
\ql\b\f0\fs30 2. Overall Description\par\sa120
\ql\b\f0\fs26 2.1 Product Features\par\sa120
\ql\f0\fs24 The product features include teacher login, dashboard monitoring, student enrollment, student record maintenance, classroom image-based attendance marking, manual review, class history tracking, CSV export, and student attendance analysis.\par\sa120
\ql\b\f0\fs30 3. External Interface Requirements\par\sa120
\ql\b\f0\fs26 3.1 User Interface Requirements\par\sa120
\ql\f0\fs24 The interface provides distinct pages for login, dashboard, student records, class session creation, recognition review, class history, export, and analytics. The design is teacher-friendly and organized through sidebar navigation.\par\sa120
\ql\b\f0\fs30 4. Functional Requirements\par\sa120
\ql\f0\fs24 FR1: The system shall allow teacher login using username and password credentials.\par\sa120
\ql\f0\fs24 FR2: The system shall allow student enrollment using name, roll number, department, division, and one to three face images.\par\sa120
\ql\f0\fs24 FR3: The system shall allow search, filtering, edit, and deletion of student records.\par\sa120
\ql\f0\fs24 FR4: The system shall allow class session creation using department, division, time range, and classroom image input.\par\sa120
\ql\f0\fs24 FR5: The system shall detect faces, compare them with enrolled student data, and produce recognition results with confidence scores.\par\sa120
\ql\f0\fs24 FR6: The system shall support manual roster review before final attendance save.\par\sa120
\ql\f0\fs24 FR7: The system shall maintain session history and support CSV export.\par\sa120
\ql\f0\fs24 FR8: The system shall display analytics such as attendance percentage, recent sessions, and students needing attention.\par\sa120
\ql\b\f0\fs30 5. Non-Functional Requirements\par\sa120
\ql\f0\fs24 The system should be usable, reliable, accurate, and maintainable for routine classroom deployment using free and open-source technologies.\par\sa120
\ql\b\f0\fs30 6. UI Feature Screens\par\sa120
\ql\f0\fs24 The following screenshots are included to represent implemented project features.\par\sa120
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 095936.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 1. Login page showing username and password based teacher authentication.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100000.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 2. Dashboard showing registered students, average attendance, total classes held, and summary panels.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100028.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 3. Student Records page showing enrollment form and searchable student records directory.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100102.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 4. Class session creation page used to upload classroom image and define session timing.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100119.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 5. Class History page showing saved sessions, filters, session detail, and export option.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100240.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 6. CSV export output containing student attendance results and score information.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100605.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 7. Recognition result panel showing detected faces, recognized count, unknown count, and confidence scores.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100624.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 8. Roster review screen used for manual attendance confirmation and final save.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100744.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 9. Students needing attention panel highlighting low-attendance students.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100834.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 10. Recent class sessions panel showing date, division, attendance ratio, and session performance.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100912.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 11. Student directory analytics showing student-wise attendance status categories.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 100935.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 12. Enrollment module showing student details form and reference image upload section.\par\sa160
{\pard\qc{\field{\*\fldinst INCLUDEPICTURE "C:\\Users\\Lenovo\\OneDrive\\Pictures\\Screenshots\\Screenshot 2026-04-13 101039.png" \\d}{\fldrslt [Image]}}\par\sa120}
\qc\i\f0\fs22 Figure 13. Student management table showing edit and delete controls for stored student records.\par\sa160
}
'@
Set-Content -LiteralPath $out -Value $rtf -Encoding ASCII
Get-Item -LiteralPath $out | Format-List FullName,Length,LastWriteTime
