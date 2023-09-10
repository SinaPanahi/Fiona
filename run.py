from fiona import app, db

# Debug Mode: On during development
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    