from django.shortcuts import render
import psycopg2
# Create your views here.

def Leaderboard(request):
    if request.method=='POST':
        connection = psycopg2.connect(host="localhost", database="S5_T1", user="postgres", password="admin")
        cursor = connection.cursor()
        gname = request.POST['gamename']
        query = f"select game_id from game where game_name='{gname}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        query = f"select * from show_player_leaderboard({int(rows[0][0])}) join person on id=player"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows[0])
        return render(request,'leaderboard.html',{'item':rows,'name':gname})
    else:
        return render(request,'form1.html')

def Profile(request):
    return render(request,'profile.html')

def Gamepage(request):
    return render(request,'game.html')

def indexpage(request):
        return render(request,'home.html')

def login(request):
    if request.method=='POST':
        connection = psycopg2.connect(host="localhost", database="S5_T1", user="postgres", password="admin")

        cursor = connection.cursor()
        cursor.execute('SELECT  version()')
        
        db_version = cursor.fetchone()

        user_name = request.POST['exampleInputUsername']
        password = request.POST['exampleInputPassword1']

        query = f"select id from person where username='{user_name}' and password='{password}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows)==0:
            error_message = "Please Enter correct Username and password."
            return render(request,'login.html',{'iserror':1,'msg':error_message})
        else:
            print(rows[0][0])
            query = f"select * from get_player_profile({rows[0][0]})"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return render(request,'profile.html',{'iserror':0,'player':rows})
    else:
        error_message ="No"
        return render(request,'login.html',{'iserror':0,'msg':error_message})



def signup(request):
    if request.method=='POST':
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        cno = request.POST['CNO']
        age = request.POST['age']
        email = request.POST['email']
        uname = request.POST['uname']
        password = request.POST['password']
        height = request.POST['height']
        weight = request.POST['weight']
        tid = request.POST['tid']

        user_type = 'player'

        connection = psycopg2.connect(host="localhost", database="S5_T1", user="postgres", password="admin")

        cursor = connection.cursor()
        cursor.execute('SELECT  version()')
        
        db_version = cursor.fetchone()
        query = f"select max(id) from person"
        cursor.execute(query)
        max_id = cursor.fetchall()
        id = int(max_id[0][0])+1

        query = f"insert into person values({id},'{fname}','{mname}','{lname}',{age},'{cno}','{email}','{user_type}','{uname}','{password}')"
        cursor.execute(query)
        connection.commit()
        
        if(len(tid)==0):
            query = f"insert into player(player_id,height,weight) values({id},{height},{weight})"
        else:  
            query = f"insert into player values({id},{height},{weight},{tid})"
        
        cursor.execute(query)
        connection.commit()

        query = f"select * from person where id={id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return render(request,'home.html',{'Authenticate':rows})
    else:
        return render(request,'Signup.html')


