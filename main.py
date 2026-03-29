from flet import *
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                stdname TEXT,
                stdemail TEXT,
                stdphone TEXT,
                stdaddress TEXT,
                math INTEGER,
                arabic INTEGER,
                kurdish INTEGER,
                science INTEGER,
                english INTEGER,
                chemistry INTEGER)''')
conn.commit()

def main(page: Page):
    page.title = "student list"
    page.window.height = 740
    page.window.width = 390
    page.window.top = 60
    page.window.left = 950
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO
    
    tabel_name = 'students'
    query = f"SELECT COUNT(*) FROM {tabel_name}"
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]

    total_students_text = Text(f"{row_count}", size=15, text_align=TextAlign.CENTER, color=Colors.BLUE, weight=FontWeight.BOLD)

    def refresh_row_count():
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM students")
        cnt = c.fetchone()[0]
        total_students_text.value = str(cnt)
        page.update()
    
############### Add Data to database###################
    
################# Show Data ########################

    view_list = Column(spacing=10)
    editing_id = None

    def edit_student(e, student_id):
        nonlocal editing_id
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE id=?", (student_id,))
        row = c.fetchone()
        if row:
            _, name, email, phone, address, math, arabic, kurdish, science, english, chemistry = row
            tname.value = name
            temail.value = email
            tphone.value = phone
            taddress.value = address
            mathmatic.value = str(math)
            marabic.value = str(arabic)
            mkurdish.value = str(kurdish)
            mscience.value = str(science)
            menglish.value = str(english)
            chemstry.value = str(chemistry)
            editing_id = student_id
            addbutton.text = "Update Student"
            page.go("/Home")
            page.update()

    def delete_student(e, student_id):
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        refresh_row_count()
        show()

    def show(e=None):
        view_list.controls.clear()
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        users = c.fetchall()

        if users:
            keys = ['id','stdname','stdemail','stdphone','stdaddress','math','arabic','kurdish','science','english','chemistry']
            result =[ dict(zip(keys, values)) for values in users]

            for x in result:
                m =x["math"]
                a =x["arabic"]
                k =x["kurdish"]
                s =x["science"]
                eng =x["english"]
                ch =x["chemistry"]
                res = (m + a + k + s + eng + ch) / 6
                if res >= 90:
                    grade = "A"
                    avg = res
                elif res >= 80:
                    grade = "B"
                    avg = res
                elif res >= 70:
                    grade = "C"
                    avg = res
                elif res >= 60:
                    grade = "D"
                    avg = res
                else:
                    grade = "F"
                    avg = res

                view_list.controls.append(
                    Card(
                
                        content=Container(
                            content=Column([
                                ListTile(
                                    leading=Icon(Icons.PERSON, color=Colors.BLUE),
                                    title=Text(f'Name: {x["stdname"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                ),
                                ListTile(
                                    leading=Icon(Icons.EMAIL, color=Colors.BLUE),
                                    title=Text(f'Email: {x["stdemail"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                ),
                                ListTile(
                                    leading=Icon(Icons.PHONE, color=Colors.BLUE),
                                    title=Text(f'Phone: {x["stdphone"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                ),
                                ListTile(
                                    leading=Icon(Icons.HOME, color=Colors.BLUE),
                                    title=Text(f'Address: {x["stdaddress"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                ),
                                Row([
                                Text(f'Math: {x["math"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                Text(f'Arabic: {x["arabic"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                Text(f'Kurdish: {x["kurdish"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                ],alignment=MainAxisAlignment.SPACE_BETWEEN),
                                Row([
                                Text(f'Science: {x["science"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                Text(f'English: {x["english"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                Text(f'Chemistry: {x["chemistry"]}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                ],alignment=MainAxisAlignment.SPACE_BETWEEN),
                                Text(f'Average: {res}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                Text(f'Grade: {grade}', size=15, color=Colors.BLUE, weight=FontWeight.BOLD),
                                Row([
                                    ElevatedButton("Edit", on_click=lambda e, student_id=x["id"]: edit_student(e, student_id), bgcolor=Colors.ORANGE, width=100, height=30, color=Colors.WHITE),
                                    ElevatedButton("Delete", on_click=lambda e, student_id=x["id"]: delete_student(e, student_id), bgcolor=Colors.RED, width=100, height=30, color=Colors.WHITE),
                                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                            ],
                            margin=10,
                            
                            ),
                        ),
                        width=350,
                        bgcolor=Colors.GREY_300,
                        margin=10,
                        
                        ),
                )
            page.update()
        else:
            view_list.controls.append(Text("No students available", size=16, color=Colors.RED, weight=FontWeight.BOLD))
            page.update()
####################################################

#######  feild ############
    tname = TextField(label="Student Name",hint_text="Enter student name", height=35 , icon=Icons.PERSON)
    temail = TextField(label="Student Email", hint_text="Enter student email", height=35, icon=Icons.EMAIL)
    tphone = TextField(label="Student Phone", hint_text="Enter student phone", height=35, icon=Icons.PHONE)
    taddress = TextField(label="Student Address", hint_text="Enter student address", height=35, icon=Icons.HOME)
    #######  Student Marks ############
    marktext = Text("Student Marks", size=20, text_align=TextAlign.CENTER, color=Colors.RED, weight=FontWeight.BOLD)
    mathmatic = TextField(label="Maths", width=110, height=35 )
    marabic = TextField(label="Arabic", width=110, height=35)
    mkurdish = TextField(label="kurdish", width=110, height=35)
    mscience = TextField(label="Science", width=110, height=35 )
    menglish = TextField(label="English", width=110, height=35)
    chemstry = TextField(label="Chemistry", width=110, height=35)
    
    ###########################

    def add(e):
        nonlocal editing_id
        stdname = tname.value
        stdemail = temail.value
        stdphone = tphone.value
        stdaddress = taddress.value
        math = int(mathmatic.value or 0)
        arabic = int(marabic.value or 0)
        kurdish = int(mkurdish.value or 0)
        science = int(mscience.value or 0)
        english = int(menglish.value or 0)
        chemistry = int(chemstry.value or 0)

        if editing_id is None:
            cursor.execute('''INSERT INTO students (stdname, stdemail, stdphone, stdaddress, math, arabic, kurdish, science, english, chemistry)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (stdname, stdemail, stdphone, stdaddress, math, arabic, kurdish, science, english, chemistry))
        else:
            cursor.execute('''UPDATE students SET stdname=?, stdemail=?, stdphone=?, stdaddress=?, math=?, arabic=?, kurdish=?, science=?, english=?, chemistry=? WHERE id=?''',
                            (stdname, stdemail, stdphone, stdaddress, math, arabic, kurdish, science, english, chemistry, editing_id))
            editing_id = None
            addbutton.text = "Add Student"

        conn.commit()
        refresh_row_count()
        tname.value = ""
        temail.value = ""
        tphone.value = ""
        taddress.value = ""
        mathmatic.value = ""
        marabic.value = ""
        mkurdish.value = ""
        mscience.value = ""
        menglish.value = ""
        chemstry.value = ""
        page.update()
        show()
    ######################################################

    ############## Buttons ############
    addbutton = ElevatedButton("Add Student", on_click=add, bgcolor=Colors.GREEN, width=150, height=40, color=Colors.WHITE )
    showbutton = ElevatedButton("Show Student", on_click=lambda _: page.go("/view"), bgcolor=Colors.GREEN, width=150, height=40, color=Colors.WHITE)
    ###################################

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                route="/Home",
                controls=[

                    AppBar(
                        title=Text("Student Adding system",size=20, color=Colors.WHITE, weight=FontWeight.BOLD),
                        center_title=True,
                        color=Colors.BLUE,
                        bgcolor=Colors.RED,
                        
                    ),
                    Row([
                        Image(src="student.png", width=150, height=150),
                    ],alignment=MainAxisAlignment.CENTER),
                    Row([
                        Text("Student Adding system", size=20, color=Colors.BLUE, weight=FontWeight.BOLD),
                    ],alignment=MainAxisAlignment.CENTER),
                    Row([
                        Text("Total Students :", size=15, text_align=TextAlign.CENTER, color=Colors.RED, weight=FontWeight.BOLD),
                        total_students_text,
                    ],alignment=MainAxisAlignment.CENTER),
                    Column([
                        tname,
                        temail,
                        tphone,
                        taddress,
                    ],alignment=MainAxisAlignment.CENTER),
                    Row([
                        marktext,
                    ],alignment=MainAxisAlignment.CENTER),
                    Row([
                        mathmatic,
                        marabic,
                        mkurdish,
                    ], alignment=MainAxisAlignment.CENTER),
                    Row([
                        mscience,
                        menglish,
                        chemstry,
                    ], alignment=MainAxisAlignment.CENTER),
                    Row([
                        addbutton,
                        showbutton,
                    ],alignment=MainAxisAlignment.CENTER)
                ],    
            ) 
        )
        if page.route == "/view":
            page.views.append(
                View(
                    route="/view",
                    scroll=ScrollMode.AUTO,
                    controls=[
                        AppBar(
                            title=Text("Student List"),
                            center_title=True,
                            color=Colors.BLUE,
                            bgcolor=Colors.GREY_300,
                        ),
                        Text("Student List", width=370, size=30, text_align=TextAlign.CENTER, color=Colors.RED, weight=FontWeight.BOLD),
                        view_list,
                        Row([
                            ElevatedButton("Home", on_click=lambda e: page.go("/Home"), bgcolor=Colors.BLUE, color=Colors.WHITE),
                        ], alignment=MainAxisAlignment.CENTER),
                    ],
                )
            )
            show()
            

            
    page.update()

    def page_back(view):
        page.views.pop()
        page_back = page.views[-1]
        page.go(page_back.route)

    page.on_route_change = route_change
    # Initialize with the root route
    page.on_view_pop = page_back
    page.go("/Home")

app(target=main)
