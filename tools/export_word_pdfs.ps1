$ErrorActionPreference = "Stop"

$desktop = [Environment]::GetFolderPath('Desktop')
$tempDir = Join-Path $desktop 'AI_Attendance_PDF_Temp'

New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Export-HtmlToPdf {
    param(
        [string]$BaseName,
        [string]$Html
    )

    $htmlPath = Join-Path $tempDir ($BaseName + '.html')
    $pdfPath = Join-Path $desktop ($BaseName + '.pdf')

    Set-Content -LiteralPath $htmlPath -Value $Html -Encoding UTF8

    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    try {
        $doc = $word.Documents.Open($htmlPath, $false, $true)
        $doc.ExportAsFixedFormat($pdfPath, 17)
        $doc.Close($false)
    }
    finally {
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    }
}

$style = @"
<style>
body { font-family: 'Times New Roman', serif; color: #000; background: #fff; margin: 40px; }
.exp { margin: 0 0 10px 0; font-size: 15pt; font-weight: 700; }
.sub { margin: 0 0 24px 0; font-size: 12pt; font-weight: 700; line-height: 1.25; }
.title { margin: 0 0 24px 0; text-align: center; font-family: Arial, sans-serif; font-size: 18pt; font-weight: 700; }
.caption { margin-top: 24px; text-align: center; font-size: 13pt; font-weight: 700; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; }
th, td { border: 1px solid #666; padding: 6px 7px; vertical-align: middle; font-size: 10.2pt; line-height: 1.2; }
th { background: #f2f2f2; text-align: center; font-family: Arial, sans-serif; font-size: 10pt; font-weight: 700; }
.center { text-align: center; }
.icon { width: 7%; text-align: center; font-family: Arial, sans-serif; font-weight: 700; }
.diagram-wrap { text-align: center; }
svg { max-width: 100%; height: auto; }
</style>
"@

$docs = @(
    @{
        Name = '01_Test_Case_Chart'
        Html = @"
<!doctype html><html><head><meta charset='utf-8'><title>01 Test Case Chart</title>$style</head><body>
<p class='exp'>Experiment No. 7</p>
<p class='sub'>Prepare the sample test cases for the identified project.</p>
<div class='title'>TEST CASE CHART</div>
<table>
<thead><tr><th class='icon'></th><th style='width:12%'>Test Case ID</th><th style='width:22%'>Test Scenario</th><th style='width:23%'>Input</th><th style='width:26%'>Expected Output</th><th style='width:10%'>Result</th></tr></thead>
<tbody>
<tr><td class='icon'>O</td><td class='center'>TC01</td><td>Valid Student Enrollment</td><td>Student details with a clear face image</td><td>Student record is registered successfully</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>X</td><td class='center'>TC02</td><td>Empty Student Form</td><td>No data entered</td><td>Error message is displayed</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>!</td><td class='center'>TC03</td><td>Invalid Face Image</td><td>Blurred image or image without a face</td><td>Face validation error is shown</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>C</td><td class='center'>TC04</td><td>Attendance Marking</td><td>Classroom image with registered students</td><td>Attendance is marked successfully</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>?</td><td class='center'>TC05</td><td>Unknown Face Detection</td><td>Classroom image with an unregistered face</td><td>Unknown face is shown for review</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>E</td><td class='center'>TC06</td><td>Edit Student Record</td><td>Updated student details</td><td>Student record is updated successfully</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>D</td><td class='center'>TC07</td><td>Delete Student Record</td><td>Delete an existing student</td><td>Student record is deleted successfully</td><td class='center'><strong>Pass</strong></td></tr>
<tr><td class='icon'>R</td><td class='center'>TC08</td><td>Attendance Report View</td><td>Saved attendance data</td><td>Attendance summary is displayed correctly</td><td class='center'><strong>Pass</strong></td></tr>
</tbody></table>
<div class='caption'>Test cases for AI Attendance Management System.</div>
</body></html>
"@
    },
    @{
        Name = '02_Cost_Estimation'
        Html = @"
<!doctype html><html><head><meta charset='utf-8'><title>02 Cost Estimation</title>$style</head><body>
<p class='exp'>Experiment No. 9</p>
<p class='sub'>Prepare the estimation of cost for identified projects, also identify and write the sample test cases.</p>
<div class='title'>COST ESTIMATION</div>
<table>
<thead><tr><th class='icon'></th><th style='width:32%'>Component</th><th style='width:41%'>Description</th><th style='width:20%'>Estimated Cost (INR)</th></tr></thead>
<tbody>
<tr><td class='icon'>T</td><td><strong>Development Tools</strong></td><td>VS Code, Python, GitHub (Free)</td><td class='center'><strong>₹ 0</strong></td></tr>
<tr><td class='icon'>F</td><td><strong>Frontend</strong></td><td>HTML, CSS, and local user interface development</td><td class='center'><strong>₹ 0</strong></td></tr>
<tr><td class='icon'>B</td><td><strong>Backend</strong></td><td>Python server-side development</td><td class='center'><strong>₹ 0</strong></td></tr>
<tr><td class='icon'>A</td><td><strong>Face Recognition Libraries</strong></td><td>OpenCV, NumPy, and free local models</td><td class='center'><strong>₹ 0</strong></td></tr>
<tr><td class='icon'>D</td><td><strong>Database</strong></td><td>SQLite</td><td class='center'><strong>₹ 0</strong></td></tr>
<tr><td class='icon'>H</td><td><strong>Hosting</strong></td><td>Local system / self-hosted setup</td><td class='center'><strong>₹ 0</strong></td></tr>
<tr><td class='icon'>I</td><td><strong>Internet &amp; Miscellaneous</strong></td><td>Testing, downloads, printing support</td><td class='center'><strong>₹ 500</strong></td></tr>
<tr><td colspan='3' class='center'><strong>Total Estimated Cost</strong></td><td class='center'><strong>₹ 500 (Approx.)</strong></td></tr>
</tbody></table>
<div class='caption'>Cost for AI Attendance Management System.</div>
</body></html>
"@
    }
)

foreach ($doc in $docs) {
    Export-HtmlToPdf -BaseName $doc.Name -Html $doc.Html
}

Get-ChildItem -LiteralPath $desktop -Filter '0*_*.pdf' | Select-Object Name, Length, FullName
