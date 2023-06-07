from flask import Flask, render_template

app = Flask(__name__)

hat='''<style>.center {margin: auto;width: 50%;padding: 10px;text-align:center;}</style><div class="center"><button onclick="window.location.href='register'">Регистрация</button>&nbsp;&nbsp;&nbsp;<button onclick="window.location.href='top'">ТОП</button>&nbsp;&nbsp;<button><a href="https://docs.google.com/spreadsheets/d/17bsx0wYd9wtbvp8splCud6oiYWkyCLudZJbsXD_sN4g/edit#gid=1160036369">ОЛИМПИАДЫ</a></button></div>''' #'''<button onclick="window.location.href='getreward'">Получить награду</button>&nbsp;&nbsp;&nbsp;
@app.route("/register", methods=['POST', 'GET'])
def register():
    global olimpiadas
    olimps=str([f"""<opti
    on value='{i}: побед-{olimpiadas[i][0]},приз-{olimpiadas[i][1]},участник-{olimpiadas[i][2]}'>""" for i in olimpiadas]).replace(', ','').replace(',',', ').replace('"','')[1:-1]
    return render_template('register.html',olimpiadas=olimps,hat=hat)

@app.route("/reg_next",methods=['POST'])
def reg_next():
    global hat,olmps
    global olimpiadas
    #olimpiadas={"Всерос информатика":[125,100,10],"Всерос математика":[125,100,10],"Мош":[50,25,5]}
    if request.method == 'POST':
        places={'Победитель':0,'Призёр':1,'Участник':2}
        f = request.form.get('familiya')
        n = request.form.get('name')
        otch = request.form.get('otchestvo')
        c = request.form.get('class')
        o = request.form.get('olimps')
        p = request.form.get('place')

        fio=f.capitalize()+" "+n.capitalize()+''+otch.capitalize()
        fio=''.join([i for i in fio if i in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛ МНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'])
        print(fio)
        print(c)
        print(o,type(o))
        print(p)
        if fio.lower() not in students:
            return f'<script>alert("Вас не существует");window.location.href = "/register";</script>'
        if c not in [str(i) for i in range(5,12)]:
            return f'<script>alert("Неверный класс");window.location.href = "/register";</script>'
        try:
            score=olimpiadas[o[:o.find(':')]][places[p]]
        except:
            return f'<script>alert("Выберите олимпиаду, а не впишите свою");window.location.href = "/register";</script>'
        if fio not in [i[0] for i in get_all_users()]:
            add_new_user(fio,c)
            update_score(fio,score)
            olmps[fio] = olmps.get(fio,[])+[o[:o.find(":")]+" "+p]
        else:
            olmps[fio] = olmps.get(fio,[])+[o[:o.find(":")]+" "+p]
            update_score(fio,get_user(fio)[1]+int(score))
        print(olmps)
        return f'<script>alert("Спасибо за ваш ответ вам начислено {score} баллов");window.location.href = "/";</script>'

@app.route("/top")
def top():
    global hat
    top=''
    x={i[0]:i[1] for i in get_all_users()}
    for ID in range(len(x)):
        i=[_ for _ in reversed(x)][ID]
        top+=f"""<p><b>{ID+1}.</b> {i}: {x[i]}</p>"""
    return render_template('top.html',top=top,hat=hat)

@app.route("/")
def main_page():
    return render_template('Index.html')

def getrewards():
    return render_template("getreward.html",rewards=str(["<p>"+ f"'{i}: {rewards[i]} баллов'" +"</p>" for i in rewards]).replace(', ','').replace(',',', ').replace('"','').replace("'",'')[1:-1])

def getreward():
    global rewards
    scripts=''
    if request.method=='POST':
        f = request.form.get('familiya')
        n = request.form.get('name')
        otch = request.form.get('otchestvo')
        reward=request.form.get('reward')
        fio=f+" "+n+' '+otch
        fio=''.join([i for i in fio if i in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛ МНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'])
        reward=reward[:reward.find(':')]
        if reward in rewards and fio in [i[0] for i in get_all_users()] and get_user(fio)[1]>=rewards[reward]:
            update_score(fio,get_user(fio)[1]-rewards[reward])
            scripts=f'Вы получили {reward}'
            tgbot.send(fio,reward)
        else:
            script='Что-то пошло не так'
            print('something wrong',reward in rewards, fio in [i[0] for i in get_all_users()], get_user(fio)[1]>=rewards[reward])
    return render_template('getreward.html',rewards=str(["<option value="+ f"'{i}: {rewards[i]} баллов'" +">" for i in rewards]).replace(', ','').replace(',',', ').replace('"','')[1:-1],scripts=scripts)

@app.route("/4aa190549e28c0d7a2c7ce57f1f78ac568512c36")
def aelus():
    global olmps
    return str([f"<p>{i}: {str(olmps[i])[1:-1]}</p>" for i in olmps if i in [i[0] for i in get_all_users()]])[1:-1]

if __name__ == "__main__":
    app.run()