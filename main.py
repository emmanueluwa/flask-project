from website import create_app

app = create_app()

#to run flask app, only if we run __name.. should we execute line
if __name__ == '__main__':
    #everytime we change code, web server automaically runs. should be off during production
    app.run(debug=True)
  