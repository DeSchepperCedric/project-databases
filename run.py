from app import app
from app.common.database import init_db

init_db()
app.run(debug=True)
