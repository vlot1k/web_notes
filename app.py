from datetime import datetime
import locale

# Импорт необходимых модулей из библиотек Flask и Flask-WTF
from flask import Flask, redirect, render_template, request
from flask_wtf import FlaskForm

# Импорт классов полей из модуля wtforms
from wtforms import StringField, SubmitField, TextAreaField

# Импорт валидаторов из модуля wtforms.validators
from wtforms.validators import InputRequired

# Импорт модуля SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Установка URI для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'

# Создаем объект базы данных
db = SQLAlchemy(app)


# Класс Заметок для базы данных
class Note(db.Model):
    # Указываем имя таблицы
    __tablename__ = 'notes'
    # Заводим поля
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text_note = db.Column(db.String(80))
    date_create = db.Column(db.String(80))

    # Инициализатор для создания объектов класса
    def __init__(self, title, text_note, date_create):
        self.title = title
        self.text_note = text_note
        self.date_create = date_create


# Определение класса формы создания заметки
class NewNoteForm(FlaskForm):
    # Заводим поля
    title = StringField('Заголовок:', validators=[InputRequired()])
    text_note = TextAreaField('Текст:', validators=[InputRequired()],
                              render_kw={'rows': 3, 'cols': 27})
    date_create = StringField()
    # Поле кнопки отправки формы
    submit = SubmitField('Создать')


# Обработчик маршрута для главной страницы
@app.route('/')
def index():
    db.create_all()
    return render_template('main.html')


# Обработчик маршрута для страницы заметок с таблицей
@app.route('/notes')
def notes():
    # SELECT запрос на получение всей таблицы (список записей)
    people = Note.query.all()
    # Вывод полученных заметок в консоль
    for note in people:
        print(note)
    # Возвращаем html c таблицей
    return render_template('notes.html', notes=people)


locale.setlocale(locale.LC_ALL, 'ru_RU')  # Для отображения даты и времени МСК


# Обработчик маршрута для страницы создания заметок
@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
    # Создаем экземпляр формы для создания
    form = NewNoteForm()
    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        now = datetime.now()  # Получаем текущее время
        date_create = now.strftime("%d %B %Y, %H:%M")
        # Если форма прошла валидацию, получаем данные из полей формы
        title, text_note = form.title.data, form.text_note.data
        # Выводим данные формы в консоль для отладки
        print(title, text_note, date_create)
        # Создаем новый объект
        new_note = Note(title=title, text_note=text_note,
                        date_create=date_create)
        db.session.add(new_note)  # Добавляем в базу данных
        db.session.commit()  # Фиксация изменений в базе данных
        return redirect('/notes')
    # Если форма не была отправлена или не прошла валидацию,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных данных
    return render_template('new_note_form.html', form=form)


# Обработчик маршрута для открытия заметки
@app.route('/notes/open/<int:id>')
def open_note(id):
    note = Note.query.get(id)
    return render_template('open_note.html', note=note)


# Обработчик маршрута для изменения заметки
@app.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get(id)
    if request.method == "POST":
        note.title = request.form['title']
        note.text_note = request.form['text_note']
        # Создаем новый объект
        db.session.commit()  # Фиксация изменений в базе данных
        return redirect('/notes')
    # Если форма не была отправлена,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных данных
    return render_template('edit_note.html', note=note)


# Обработчик маршрута для изменения открытой заметки
@app.route('/notes/open/<int:id>/edit', methods=['GET', 'POST'])
def edit_open_note(id):
    note = Note.query.get(id)
    if request.method == "POST":
        note.title = request.form['title']
        note.text_note = request.form['text_note']
        # Создаем новый объект
        db.session.commit()  # Фиксация изменений в базе данных
        return redirect('/notes')
    # Если форма не была отправлена,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных данных
    return render_template('edit_note.html', note=note)


# Обработчик маршрута для удаления заметки
@app.route('/notes/delete/<int:id>')
def delete_note(id):
    note_del = Note.query.get_or_404(id)
    db.session.delete(note_del)
    db.session.commit()
    return redirect('/notes')


# Обработчик маршрута для удаления открытой заметки
@app.route('/notes/open/<int:id>/delete')
def delete_open_note(id):
    note_del = Note.query.get_or_404(id)
    db.session.delete(note_del)
    db.session.commit()
    return redirect('/notes')


# Обработчик маршрута для страницы с контактами
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF WTForms
    app.run(debug=True)  # Запускаем приложение в режиме отладки
